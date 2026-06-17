"""
predict.py
==========
Live inference for the agentic gold prediction pipeline.

This file is called by your agentic orchestrator AFTER:
  1. Market API fetches today's prices
  2. Search API fetches latest news
  3. Groq sentiment node returns a score

Usage:
  from predict import predict_direction

  result = predict_direction(
      today_prices={"gold": 2340.5, "oil": 82.3, "dxy": 104.2, "yield_10y": 4.31},
      groq_sentiment=0.6,
      price_history=price_history_df   # optional but recommended
  )
  # Returns: {"direction": "UP", "confidence": 0.73, "xgb_raw_prob": 0.73}
"""

import joblib
import numpy as np
import pandas as pd

MODEL_PATH    = "gold_direction_model.pkl"
SCALER_PATH   = "scaler.pkl"
FEATURES_PATH = "feature_columns.pkl"


def predict_direction(
    today_prices: dict,
    groq_sentiment: float,
    price_history: pd.DataFrame = None,
) -> dict:
    """
    Predict next-day gold direction.

    Args:
        today_prices (dict): Must contain:
            - gold       : current gold price (USD/oz)
            - oil        : current WTI oil price
            - dxy        : US Dollar Index
            - yield_10y  : 10-Year Treasury Yield

        groq_sentiment (float): Sentiment from Groq node, range [-1, +1]
            Positive = bullish macro news, Negative = bearish macro news

        price_history (pd.DataFrame, optional):
            DataFrame with columns [gold, oil, dxy, yield_10y]
            indexed by date. If provided, computes accurate lag/vol features.
            Minimum 30 rows recommended (for MA/vol calculations).

    Returns:
        dict:
            direction    : "UP" or "DOWN"
            confidence   : float [0.5, 1.0] — model's certainty
            xgb_raw_prob : raw probability of UP from XGBoost
    """
    model        = joblib.load(MODEL_PATH)
    scaler       = joblib.load(SCALER_PATH)
    feature_cols = joblib.load(FEATURES_PATH)

    if price_history is not None and len(price_history) >= 30:
        row = _compute_features_from_history(today_prices, groq_sentiment, price_history)
    else:
        row = _compute_features_minimal(today_prices, groq_sentiment)

    X = pd.DataFrame([row]).reindex(columns=feature_cols, fill_value=0.0).values
    X_scaled = scaler.transform(X)

    prob_up   = float(model.predict_proba(X_scaled)[0][1])
    direction = "UP" if prob_up >= 0.5 else "DOWN"

    return {
        "direction"   : direction,
        "confidence"  : round(prob_up, 4),
        "xgb_raw_prob": round(prob_up, 4),
    }


def _compute_features_from_history(today_prices, groq_sentiment, history):
    """Full feature computation using rolling price history."""
    # Append today to history for computation
    today_row = pd.DataFrame([today_prices], index=[pd.Timestamp.today().normalize()])
    df = pd.concat([history[["gold", "oil", "dxy", "yield_10y"]], today_row])
    df = df.ffill()

    row = {}

    # Returns
    for col in ["gold", "oil", "dxy", "yield_10y"]:
        row[f"{col}_ret1"] = np.log(df[col].iloc[-1] / df[col].iloc[-2] + 1e-9)
        row[f"{col}_ret3"] = np.log(df[col].iloc[-1] / df[col].iloc[-4] + 1e-9)
        row[f"{col}_ret5"] = np.log(df[col].iloc[-1] / df[col].iloc[-6] + 1e-9)

    # Lags
    for lag in [1, 3, 5, 7, 14]:
        row[f"gold_lag_{lag}"] = df["gold"].iloc[-lag-1] / df["gold"].iloc[-1] - 1

    # Volatility
    ret1 = df["gold"].pct_change()
    row["gold_vol_7d"]  = ret1.iloc[-7:].std()
    row["gold_vol_21d"] = ret1.iloc[-21:].std()
    row["oil_vol_7d"]   = df["oil"].pct_change().iloc[-7:].std()

    # RSI
    delta = df["gold"].diff()
    gain  = delta.clip(lower=0).rolling(14).mean().iloc[-1]
    loss  = (-delta.clip(upper=0)).rolling(14).mean().iloc[-1]
    row["gold_rsi14"] = 100 - (100 / (1 + gain / (loss + 1e-9)))

    # MACD
    ema12 = df["gold"].ewm(span=12).mean()
    ema26 = df["gold"].ewm(span=26).mean()
    macd  = ema12 - ema26
    row["gold_macd_signal"] = (macd - macd.ewm(span=9).mean()).iloc[-1]

    # Bollinger
    sma20 = df["gold"].rolling(20).mean().iloc[-1]
    std20 = df["gold"].rolling(20).std().iloc[-1]
    row["gold_bb_position"] = (today_prices["gold"] - sma20) / (2 * std20 + 1e-9)

    # Cross-asset
    row["gold_oil_ratio"]    = today_prices["gold"] / (today_prices["oil"] + 1e-9)
    row["gold_dxy_interact"] = row["gold_ret1"] * row["dxy_ret1"]
    row["oil_yield_spread"]  = row["oil_ret1"] - row["yield_10y_ret1"]

    # Trend
    ma50  = df["gold"].rolling(50).mean().iloc[-1]
    ma200 = df["gold"].rolling(200).mean().iloc[-1] if len(df) >= 200 else ma50
    ma20  = df["gold"].rolling(20).mean().iloc[-1]
    row["gold_above_ma50"]  = int(today_prices["gold"] > ma50)
    row["gold_above_ma200"] = int(today_prices["gold"] > ma200)
    row["gold_ma_cross"]    = int(ma20 > ma50)

    # Calendar
    today = pd.Timestamp.today()
    row["day_of_week"] = today.dayofweek
    row["month"]       = today.month

    # Sentiment
    row["sentiment"]          = groq_sentiment
    row["sentiment_ma3"]      = groq_sentiment   # single point fallback
    row["sentiment_ma7"]      = groq_sentiment
    row["sentiment_momentum"] = groq_sentiment
    row["sentiment_vol"]      = 0.0

    return row


def _compute_features_minimal(today_prices, groq_sentiment):
    """Minimal feature row when no history is available. Less accurate."""
    row = {
        "gold_ret1"        : today_prices.get("gold_return", 0.0),
        "oil_ret1"         : today_prices.get("oil_return", 0.0),
        "dxy_ret1"         : today_prices.get("dxy_return", 0.0),
        "yield_10y_ret1"   : today_prices.get("yield_return", 0.0),
        "gold_oil_ratio"   : today_prices["gold"] / (today_prices["oil"] + 1e-9),
        "sentiment"        : groq_sentiment,
        "sentiment_momentum": groq_sentiment,
        "sentiment_ma3"    : groq_sentiment,
        "sentiment_ma7"    : groq_sentiment,
        "day_of_week"      : pd.Timestamp.today().dayofweek,
        "month"            : pd.Timestamp.today().month,
    }
    return row


if __name__ == "__main__":
    # Quick smoke test (won't be accurate without trained model)
    sample = {
        "gold": 2340.5, "oil": 82.3, "dxy": 104.2, "yield_10y": 4.31,
        "gold_return": 0.003, "oil_return": -0.01
    }
    result = predict_direction(sample, groq_sentiment=0.45)
    print(result)