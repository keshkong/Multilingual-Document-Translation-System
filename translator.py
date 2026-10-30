"""LibreTranslate API integration and optional Moses tokenization helpers."""
import requests
try:
    from sacremoses import MosesTokenizer, MosesDetokenizer
except ImportError:
    MosesTokenizer = MosesDetokenizer = None

class TranslationError(Exception):
    pass

class LibreTranslateClient:
    def __init__(self, api_url, api_key="", timeout=60):
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def translate(self, text, source="en", target="es"):
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Text to translate cannot be empty.")
        data = {"q": text, "source": source, "target": target, "format": "text"}
        if self.api_key:
            data["api_key"] = self.api_key
        try:
            response = requests.post(self.api_url + "/translate", data=data,
                                     timeout=self.timeout)
            response.raise_for_status()
            result = response.json()
        except requests.RequestException as exc:
            raise TranslationError(f"Translation service request failed: {exc}") from exc
        except ValueError as exc:
            raise TranslationError("Translation service returned invalid JSON.") from exc
        if result.get("error"):
            raise TranslationError(str(result["error"]))
        translated = result.get("translatedText")
        if not isinstance(translated, str):
            raise TranslationError("API response did not contain translatedText.")
        return translated

def tokenize_text(text, language="en"):
    if MosesTokenizer is None:
        return text.split()
    return MosesTokenizer(lang=language).tokenize(text, return_str=False)

def detokenize_tokens(tokens, language="en"):
    if MosesDetokenizer is None:
        return " ".join(tokens)
    return MosesDetokenizer(lang=language).detokenize(tokens)
