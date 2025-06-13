import requests

def query_duckduckgo(query):
    url = "http://localhost:3000/search"
    payload = {"query": query}

    try:
        res = requests.post(url, json=payload)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return f"Failed to query server: {e}"

if __name__ == "__main__":
    print(query_duckduckgo("Top open source LLMs in 2024"))
