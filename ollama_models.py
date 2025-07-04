import requests

OLLAMA_URL = "http://localhost:11434"  # Default Ollama server URL

def ollama_models():
    response = requests.get(f"{OLLAMA_URL}/api/tags")
    response.raise_for_status()
    models = response.json().get("models", [])
    return list(sorted([model['name'] for model in models]))

if __name__ == "__main__":
    models = ollama_models()
    print(', '.join(models))

