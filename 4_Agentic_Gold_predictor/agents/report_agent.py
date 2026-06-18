from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


def generate_final_report(state: dict) -> str:
    """
    Takes the full pipeline state and generates a professional
    gold market analysis report using Groq LLM.
    """
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3)

    # Build a structured context string from the pipeline state
    market = state.get("market_data", {})
    sentiment_score = state.get("sentiment_score", 0.0)
    sentiment_rationale = state.get("sentiment_rationale", "N/A")
    ml_prediction = state.get("ml_prediction", {})

    context = f"""
=== LIVE MARKET DATA ===
Gold Price:       ${market.get('gold_price', 'N/A')}   (Change: {market.get('gold_change', 'N/A')}%)
Oil Price:        ${market.get('oil_price', 'N/A')}    (Change: {market.get('oil_change', 'N/A')}%)
DXY Index:        {market.get('dxy_price', 'N/A')}     (Change: {market.get('dxy_change', 'N/A')}%)
10Y Treasury:     {market.get('yield_price', 'N/A')}%  (Change: {market.get('yield_change', 'N/A')}%)

=== SENTIMENT ANALYSIS ===
Score: {sentiment_score} (range: -1.0 bearish to +1.0 bullish)
Rationale: {sentiment_rationale}

=== ML MODEL PREDICTION ===
Direction: {ml_prediction.get('direction', 'N/A')}
Confidence: {ml_prediction.get('confidence', 'N/A')}
XGBoost Raw Probability (UP): {ml_prediction.get('xgb_raw_prob', 'N/A')}
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         """
         You are an elite commodities strategist writing a daily gold market intelligence brief.
         
         Using the provided live data, sentiment analysis, and machine learning prediction,
         produce a concise, professional report in Markdown format with these sections:
         
         1. **📊 Market Snapshot** — Summarize today's key price levels and moves.
         2. **📰 Sentiment Analysis** — Interpret the sentiment score and rationale.
         3. **🤖 ML Model Verdict** — Present the model's directional call and confidence.
         4. **⚖️ Combined Outlook** — Synthesize all three signals into ONE clear verdict
            (Bullish / Bearish / Neutral) with a brief justification.
         5. **⚠️ Risk Factors** — List 2-3 key risks that could invalidate the outlook.
         
         Keep the report under 300 words. Be direct and data-driven.
         Do NOT add disclaimers or generic financial advice.
         """),
        ("user", "{analysis_context}")
    ])

    chain = prompt | llm

    try:
        response = chain.invoke({"analysis_context": context})
        return response.content
    except Exception as e:
        return f"⚠️ Report generation failed: {str(e)}"
