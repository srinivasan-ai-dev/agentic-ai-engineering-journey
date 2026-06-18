from duckduckgo_search import DDGS

search = DDGS()

def fetch_macro_news() -> list:
    """
    Fetches the latest macroeconomic news headlines impacting gold and inflation.
    Returns a list of dicts with keys: date, title, body, url, image, source.
    """
    query = "US Federal Reserve interest rates inflation global economy gold impact latest news"


    try:
        results = search.news(query, max_results=5) 
        # Perform a search query using the DuckDuckGo Search API to fetch the latest macroeconomic news. We specify a maximum of 5 results to keep the output concise.

        return results 

    except Exception as e:
        print(f"   [WARNING] Error fetching news: {str(e)}")
        return []
        # If there is an error during the search process (e.g., network issues, API errors, etc.), we catch the exception and return an empty list. This way, we can handle errors gracefully without crashing the application.
