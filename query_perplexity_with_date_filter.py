import requests, re
from datetime import datetime

def query_perplexity_with_date_filter(api_key: str, prompt: str, search_before_date: str) -> str:
    """
    Query Perplexity API with a search_before_date_filter using direct HTTP request.

    Args:
        api_key (str): Your Perplexity API key.
        prompt (str): User prompt.
        search_before_date (str): Date string in 'YYYY-MM-DD' format.

    Returns:
        str: The assistant's reply.
    """
    # Convert YYYY-MM-DD to MM/DD/YYYY
    date_obj = datetime.strptime(search_before_date, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%m/%d/%Y")
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "sonar-pro",  # search-enabled model
        "messages": [
            {"role": "system", "content": f"Answer using only information available before {formatted_date}."},
            {"role": "user", "content": prompt}
        ],
        "search_before_date_filter": formatted_date
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    s = data["choices"][0]["message"]["content"]
    return re.sub(r'\[\d+\]', '', s)  # Remove citation marks

if __name__=="__main__":
    import load_secrets
    load_secrets.load_secrets()
    (prompt, search_before_date) = ['What day is it?', '2025-06-04']
    import os
    api_key = os.getenv('PERPLEXITY_API_KEY')
    query_perplexity_with_date_filter(api_key, prompt, search_before_date)
