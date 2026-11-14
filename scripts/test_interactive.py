"""Interactive query tool to test retrieval across strategies A, B, and C."""
import argparse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Dynamic root finding
current_dir = Path(__file__).resolve().parent
candidate = current_dir
while candidate != candidate.parent:
    if (candidate / "STUDENT.md").exists() or (candidate / "BENCHMARK.md").exists():
        root_dir = candidate
        break
    candidate = candidate.parent
else:
    root_dir = current_dir.parent

sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / "starter"))
sys.path.insert(0, str(root_dir / "src"))

env_paths = [root_dir / "starter" / ".env", root_dir / ".env"]
for ep in env_paths:
    if ep.exists():
        load_dotenv(ep)
        break

from starter.src.embeddings import GeminiEmbedder
from starter.src.store import PgVectorStore


def test_query(strategy: str = "c", query: str = "", section: str | None = None, top_k: int = 3):
    db_url = os.getenv("DATABASE_URL", "postgresql://day6:day6_local_only@127.0.0.1:55433/day6_lab")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[Error] GEMINI_API_KEY is not set in environment or starter/.env")
        return

    embedder = GeminiEmbedder(api_key=api_key, model_name="models/gemini-embedding-2", dimensions=768)
    store = PgVectorStore(database_url=db_url, dimensions=768)

    strat_key = f"strategy_{strategy.lower()}"
    print(f"\n=======================================================")
    print(f"🔍 Truy vấn: '{query}'")
    print(f"⚙️  Chiến lược: {strat_key.upper()}")
    if section:
        print(f"🎯 Metadata Filter (section): '{section}'")
    print(f"=======================================================")

    q_vec = embedder.embed_query(query)
    filters = {"section": section} if section else None
    hits = store.search(strat_key, q_vec, top_k=top_k, filters=filters)

    if not hits:
        print("❌ Không tìm thấy kết quả phù hợp.")
        return

    for idx, hit in enumerate(hits, 1):
        score = hit.get("score", 0.0)
        page = hit.get("page")
        chunk_id = hit.get("chunk_id")
        sec = hit.get("metadata", {}).get("section", "N/A")
        text = hit.get("text", "").strip()

        print(f"\n--- [Top {idx}] --- (Score: {score:.4f} | Trang: {page} | Section: {sec})")
        print(f"ID: {chunk_id}")
        print(f"Nội dung:\n{text[:400]}..." if len(text) > 400 else f"Nội dung:\n{text}")


def main():
    parser = argparse.ArgumentParser(description="Test retrieval on Day 06 Vector Store")
    parser.add_argument("--strategy", "-s", choices=["a", "b", "c"], default="c", help="Strategy to query: a, b, or c")
    parser.add_argument("--query", "-q", type=str, default="", help="Query question string")
    parser.add_argument("--section", "-sec", type=str, default=None, help="Optional section filter for Strategy C")
    parser.add_argument("--top-k", "-k", type=int, default=3, help="Number of hits to retrieve (default: 3)")
    args = parser.parse_args()

    if args.query:
        test_query(strategy=args.strategy, query=args.query, section=args.section, top_k=args.top_k)
    else:
        # Interactive mode
        print("=== Chế độ Test Truy Vấn Tương Tác (Day 06) ===")
        print("Gõ 'exit' hoặc 'quit' để thoát.\n")
        strat = input("Chọn chiến lược (A/B/C) [Mặc định: C]: ").strip().lower() or "c"
        sec = input("Nhập section filter nếu có (ví dụ: admissions, tuition_scholarships) [Bỏ trống nếu không lọc]: ").strip() or None

        while True:
            try:
                user_q = input("\nNhập câu hỏi cần test: ").strip()
                if user_q.lower() in ("exit", "quit", "q"):
                    break
                if not user_q:
                    continue
                test_query(strategy=strat, query=user_q, section=sec, top_k=args.top_k)
            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    main()
