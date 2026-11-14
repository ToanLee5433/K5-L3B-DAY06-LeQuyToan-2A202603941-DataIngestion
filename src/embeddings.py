"""Gemini Embeddings adapter with local disk caching and adaptive rate-limit handling."""
import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Protocol


class Embedder(Protocol):
    model_name: str
    dimensions: int

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Return one vector per input text, in the same order."""
        ...

    def embed_query(self, question: str) -> list[float]:
        """Return a query vector compatible with the stored document vectors."""
        ...


class GeminiEmbedder:
    """Production Gemini Embeddings adapter using models/gemini-embedding-2 (Gemini Embedding 2, 768 dimensions)."""

    def __init__(
        self,
        api_key: str | None = None,
        model_name: str = "models/gemini-embedding-2",
        dimensions: int = 768,
        cache_path: str | Path | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required for GeminiEmbedder")
        self.model_name = model_name
        self.dimensions = dimensions

        if cache_path:
            self.cache_path = Path(cache_path)
        else:
            self.cache_path = Path(__file__).resolve().parent.parent / "data" / "embeddings_cache.json"

        self._cache: dict[str, list[float]] = {}
        self._load_cache()

    def _load_cache(self) -> None:
        if self.cache_path.exists():
            try:
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    self._cache = json.load(f)
            except Exception:
                self._cache = {}

    def _save_cache(self) -> None:
        try:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_path, "w", encoding="utf-8") as f:
                json.dump(self._cache, f)
        except Exception as e:
            print(f"Warning: could not save embeddings cache: {e}")

    def _hash_text(self, text: str) -> str:
        return hashlib.sha256(f"{self.model_name}:{self.dimensions}:{text}".encode("utf-8")).hexdigest()

    def _post_json(self, url: str, payload: dict, max_retries: int = 5) -> dict:
        for attempt in range(max_retries):
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    return json.load(resp)
            except urllib.error.HTTPError as exc:
                err_body = exc.read().decode("utf-8", errors="replace")
                if exc.code == 429 and attempt < max_retries - 1:
                    sleep_time = 15 * (attempt + 1)
                    print(f"\n[Embedder] Rate limited (429). Sleeping {sleep_time}s before retry ({attempt+1}/{max_retries})...")
                    time.sleep(sleep_time)
                    continue
                elif exc.code in (500, 502, 503, 504) and attempt < max_retries - 1:
                    time.sleep(5)
                    continue
                raise RuntimeError(f"Embedding API error HTTP {exc.code}: {err_body}") from exc
            except urllib.error.URLError as exc:
                if attempt < max_retries - 1:
                    time.sleep(3)
                    continue
                raise RuntimeError(f"Network error connecting to embedding API: {exc.reason}") from exc
        raise RuntimeError("Embedding API retries exhausted")

    def embed_documents(self, texts: list[str], batch_size: int = 10) -> list[list[float]]:
        """Batch-embed list of texts using batchEmbedContents endpoint with caching."""
        if not texts:
            return []

        results: list[list[float] | None] = [None] * len(texts)
        missing_indices: list[int] = []

        # Check cache first
        for idx, text in enumerate(texts):
            h = self._hash_text(text)
            if h in self._cache:
                results[idx] = self._cache[h]
            else:
                missing_indices.append(idx)

        if not missing_indices:
            return [vec for vec in results if vec is not None]

        print(f"[Embedder] Cached: {len(texts) - len(missing_indices)}/{len(texts)}, Fetching: {len(missing_indices)} texts...")
        url = f"https://generativelanguage.googleapis.com/v1beta/{self.model_name}:batchEmbedContents?key={self.api_key}"

        for i in range(0, len(missing_indices), batch_size):
            batch_idxs = missing_indices[i:i + batch_size]
            batch_texts = [texts[idx] for idx in batch_idxs]
            requests = [
                {
                    "model": self.model_name,
                    "content": {"parts": [{"text": t}]},
                    "output_dimensionality": self.dimensions,
                }
                for t in batch_texts
            ]
            data = self._post_json(url, {"requests": requests})
            embeddings = data.get("embeddings", [])
            for batch_pos, item in enumerate(embeddings):
                target_idx = batch_idxs[batch_pos]
                vec = item.get("values", [])
                results[target_idx] = vec
                self._cache[self._hash_text(texts[target_idx])] = vec

            self._save_cache()
            if i + batch_size < len(missing_indices):
                time.sleep(1.0)  # Safe spacing to respect TPM/RPM limits

        return [vec for vec in results if vec is not None]

    def embed_query(self, question: str) -> list[float]:
        """Embed a single query text with caching."""
        h = self._hash_text(question)
        if h in self._cache:
            return self._cache[h]

        url = f"https://generativelanguage.googleapis.com/v1beta/{self.model_name}:embedContent?key={self.api_key}"
        payload = {
            "content": {"parts": [{"text": question}]},
            "output_dimensionality": self.dimensions,
        }
        data = self._post_json(url, payload)
        vec = data.get("embedding", {}).get("values", [])
        self._cache[h] = vec
        self._save_cache()
        return vec


# Alias for backward compatibility
MyEmbedder = GeminiEmbedder
