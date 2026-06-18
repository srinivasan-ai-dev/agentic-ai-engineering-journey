from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq

def analyze_news_sentiment(raw_news: list) -> dict:
    """
    Parses raw news dictionary payloads and calculates an aggregated 
    macroeconomic sentiment score for gold.
    """
    # Initialize the high-speed reasoning model
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.0)
    
    if not raw_news:
        return {"score": 0.0, "rationale": "Neutral sentiment due to no recent macroeconomic news signals found."}
        
    # Format the input payload for the context window
    formatted_context = ""
    for idx, item in enumerate(raw_news):
        formatted_context += f"[{idx+1}] Title: {item.get('title')}\nBody: {item.get('body')}\n\n"
        # This loop iterates through the list of raw news items, extracting the title and body of each news article. 
        # It formats them into a structured string that will be used as input for the sentiment analysis model. 
        # Each news item is prefixed with its index for clarity, and the formatted string is built up incrementally to create a comprehensive context for the model to analyze.
    

    # Define the professional analytical prompt
    # The prompt is designed to instruct the model to analyze the provided news context 
    # And assess its impact on gold prices based on specific macroeconomic principles. 
    #ChatPromptTemplate is used to create a structured prompt that includes system instructions and user input.
    # It specifies that the model must return a JSON object with a sentiment score and rationale, ensuring that the output is structured and machine-readable.
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         """
         You are an expert quantitative macroeconomic analyst specializing in commodities.
        Analyze the provided real-world news reports and assess their mathematical impact on Gold prices.
        
        Consider these foundational principles:
        - High/Rising Inflation = Bullish for Gold (Inflation hedge).
        - Impending Interest Rate Hikes = Bearish for Gold (Increases opportunity cost of holding non-yielding assets).
        - Geopolitical Instability/War = Bullish for Gold (Safe-haven asset).
        
        You MUST respond strictly with a valid JSON object matching this structure:
        {{
            "score": <float between -1.0 and 1.0>,
            "rationale": "<one concise sentence combining the dominant drivers>"
        }}
        Do not add any text before or after the JSON payload.
        """),
        ("user", "Latest News Signals:\n{news_context}")
    ])
    
    # Chain assembly via LCEL.
    chain = prompt | llm | JsonOutputParser()
    # Prompt → AI Model → JSON Parser
    # LCEL (LangChain Execution Language) allows for the creation of a processing chain where the prompt is first processed by the language model, and then the output is parsed into a structured JSON format. 
    # This ensures that the final output is both accurate and machine-readable, facilitating further analysis or integration into other systems.

    
    try:
        sentiment_output = chain.invoke({"news_context": formatted_context})
        return sentiment_output
    except Exception as e:
        return {"score": 0.0, "rationale": f"Sentiment calculation failed: {str(e)}"}