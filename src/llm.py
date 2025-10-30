import requests
from .config import OLLAMA_HOST, OLLAMA_MODEL, OLLAMA_TIMEOUT

def ollama_generate(prompt: str, model: str = OLLAMA_MODEL, timeout: int = OLLAMA_TIMEOUT) -> str:
    """
    Calls Ollama local REST API /api/generate.
    Works even if streaming is not supported.
    """
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": False}
    try:
        resp = requests.post(url, json=payload, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "")
    except Exception as e:
        return f"ERROR contacting Ollama: {e}"
