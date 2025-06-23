import requests

def call_local_llm(prompt, model = "llama3:8b"):
    """Sends a prompt to locally hosted LLM and return response."""
    api_url = "http://localhost:11434/api/generate"
    if 'qwen' in model:
        prompt = '/think ' + prompt
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False  # Get complete response at once
    }
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        return f"Error contacting Ollama API: {str(e)}"

if __name__=="__main__":
    from ollama_models import ollama_models
    models = ollama_models()
    for model in models:
        print("MODEL", model)
        result = call_local_llm("What will be the impact of BRICS expansion on USD dominance?")
        print(result)
        print("============================")
