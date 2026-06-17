from ddgs import DDGS

search = DDGS()

def fetch_macro_news() ->str:
    """
    Fetches the latest macroeconomic news headlines impacting gold and inflation
    """
    query = "US Federal Reserve interest rates inflation global economy gold impact latest news"


    try:
        results = search.news(query=query, max_results=5) 
        # Perform a search query using the DuckDuckGo Search API to fetch the latest macroeconomic news. We specify a maximum of 5 results to keep the output concise.

        return results 

    except Exception as e:
        return f"Error fetching news: {str(e)}" 
        # If there is an error during the search process (e.g., network issues, API errors, etc.), we catch the exception and return an error message indicating that there was an issue fetching the news. This way, we can handle errors gracefully without crashing the application.