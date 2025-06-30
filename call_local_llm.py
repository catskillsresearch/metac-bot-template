import requests, time

def _call_local_llm(prompt, model):
    """Sends a prompt to locally hosted LLM and return response."""
    api_url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,

        # https://www.perplexity.ai/search/is-there-a-correlation-between-zzHkfGvOTwuYiep_W.x4yw
        # Higher is better 
        "temperature": 0.7, 
        
        "stream": False  # Get complete response at once
    }
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        return f"Error contacting Ollama API: {str(e)}"

def call_local_llm(prompt, model):
    print('START model', model)
    start_time = time.time()
    answer = _call_local_llm(prompt, model)
    end_time = time.time()
    dt = end_time - start_time
    print('model', model, 'minutes', dt/60)
    return answer

if __name__=="__main__":
    from ollama_models import ollama_models
    models = ollama_models()
    for model in models:
        print("MODEL", model)
        result = call_local_llm("What will be the impact of BRICS expansion on USD dominance?")
        print(result)
        print("============================")
