import yfinance as yf

def fetch_macro_news() -> list:
    """
    Fetches the latest macroeconomic news headlines impacting gold and inflation.
    Returns a list of dicts with keys: date, title, body, url, image, source.
    """
    try:
        gold = yf.Ticker("GC=F")
        news_items = gold.news
        results = []
        
        for n in news_items[:5]:
            results.append({
                "title": n.get("content", {}).get("title", ""),
                "body": n.get("content", {}).get("summary", ""),
                "url": n.get("content", {}).get("clickThroughUrl", {}).get("url", ""),
            })
            
        return results 

    except Exception as e:
        print(f"   [WARNING] Error fetching news from Yahoo Finance: {str(e)}")
        return []
