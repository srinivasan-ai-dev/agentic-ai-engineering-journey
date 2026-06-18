"""
api.py
======
FastAPI backend that exposes the gold prediction pipeline as a REST API.
Run with: python api.py
"""

import sys
import os

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from tools.search_api import fetch_macro_news
from tools.market_api import fetch_live_metrics
from agents.sentiment_node import analyze_news_sentiment
from ml_engine.predict import predict_direction
from agents.report_agent import generate_final_report

app = FastAPI(title="Agentic Gold Predictor API", version="1.0.0")

# Allow CORS for local Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "Agentic Gold Predictor"}


@app.get("/api/analyze")
def run_analysis():
    """
    Runs the full gold prediction pipeline and returns structured JSON.
    """
    state = {
        "market_data": {},
        "raw_news": [],
        "sentiment_score": 0.0,
        "sentiment_rationale": "",
        "ml_prediction": {},
        "final_report": "",
    }

    # Step 1: Fetch live market metrics
    try:
        state["market_data"] = fetch_live_metrics()
    except Exception as e:
        state["market_data"] = {"error": str(e)}

    # Step 2: Fetch macroeconomic news
    try:
        state["raw_news"] = fetch_macro_news()
    except Exception as e:
        state["raw_news"] = []

    # Step 3: Sentiment analysis
    try:
        sentiment_result = analyze_news_sentiment(state["raw_news"])
        state["sentiment_score"] = sentiment_result.get("score", 0.0)
        state["sentiment_rationale"] = sentiment_result.get("rationale", "No rationale provided.")
    except Exception as e:
        state["sentiment_score"] = 0.0
        state["sentiment_rationale"] = f"Sentiment analysis failed: {str(e)}"

    # Step 4: ML Prediction
    try:
        market = state["market_data"]
        today_prices = {
            "gold":         market.get("gold_price", 0.0),
            "oil":          market.get("oil_price", 0.0),
            "dxy":          market.get("dxy_price", 0.0),
            "yield_10y":    market.get("yield_price", 0.0),
            "gold_return":  market.get("gold_change", 0.0) / 100,
            "oil_return":   market.get("oil_change", 0.0) / 100,
            "dxy_return":   market.get("dxy_change", 0.0) / 100,
            "yield_return": market.get("yield_change", 0.0) / 100,
        }
        state["ml_prediction"] = predict_direction(today_prices, state["sentiment_score"])
    except Exception as e:
        state["ml_prediction"] = {"direction": "N/A", "confidence": 0.0, "error": str(e)}

    # Step 5: Generate final report
    try:
        state["final_report"] = generate_final_report(state)
    except Exception as e:
        state["final_report"] = f"Report generation failed: {str(e)}"

    # Remove raw_news from response (too bulky for the frontend)
    state.pop("raw_news", None)

    return state


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
