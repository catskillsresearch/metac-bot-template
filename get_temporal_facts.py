import requests, json, os
from datetime import datetime

def get_temporal_facts(question: str, cutoff_date: str, api_key: str):
    """
    Retrieves all known facts about a question as of a specific date
    using Perplexity's most advanced model with date filtering.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "sonar-pro",  # Valid Pro model with web search
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a research assistant. List ALL relevant facts, events, and context "
                    "known as of the cutoff date. Include citations for each fact. NEVER provide "
                    "predictions or conclusions - only report verifiable information."
                )
            },
            {
                "role": "user",
                "content": f"{question} [Cutoff: {cutoff_date}]"
            }
        ],
        "search_before_date_filter": datetime.strptime(cutoff_date, "%Y-%m-%d").strftime("%m/%d/%Y"),
        "max_tokens": 4000,
        "temperature": 0.4,
        "search_focus": "internet"
    }

    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error {response.status_code}: {response.text}"
            
    except Exception as e:
        return f"API request failed: {str(e)}"

if __name__=="__main__":
    from load_secrets import load_secrets
    load_secrets()
    
    import os
    API_KEY = os.getenv('PERPLEXITY_API_KEY')
    QUESTION = "Will Pierre Poilievre become Prime Minister of Canada before 2026?"
    CUTOFF_DATE = "2025-03-02" #  YYYY-MM-DD format
    
    facts = get_temporal_facts(QUESTION, CUTOFF_DATE, API_KEY)
    print(facts)