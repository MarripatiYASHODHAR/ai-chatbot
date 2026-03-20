import requests

def search_web(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        data = requests.get(url).json()
        return data.get("Abstract", "No result found")
    except:
        return "Error in web search"