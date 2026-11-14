"""Pipeline entry point for Day 06 Data Ingestion Engineering benchmark."""
import csv
import json
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# Ensure starter modules and root modules can be imported
current_dir = Path(__file__).resolve().parent
if (current_dir.parent / "data").exists() or (current_dir.parent / "starter").exists():
    repo_root = current_dir.parent
else:
    repo_root = current_dir.parent.parent

sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(repo_root / "starter"))
sys.path.insert(0, str(current_dir.parent))

from starter.src.ingestion import load_pdf
from starter.src.chunking import fixed_size, by_paragraph
from starter.src.embeddings import GeminiEmbedder
from starter.src.store import PgVectorStore
from starter.src.evaluation import evaluate_query, summarize


def find_file(relative_path: str) -> Path:
    candidates = [
        repo_root / relative_path,
        repo_root / "starter" / relative_path,
        current_dir.parent / relative_path,
    ]
    for c in candidates:
        if c.exists():
            return c
    raise FileNotFoundError(f"Cannot find {relative_path} in any of {candidates}")


def main() -> None:
    # 0. Load environment
    env_paths = [repo_root / "starter" / ".env", repo_root / ".env"]
    for ep in env_paths:
        if ep.exists():
            load_dotenv(ep)
            break

    db_url = os.getenv("DATABASE_URL", "postgresql://day6:day6_local_only@127.0.0.1:55433/day6_lab")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment or .env")

    print("=== Step 1: Ingestion & Validation ===")
    pdf_path = find_file("data/vinuni_academic_handbook_2025_2026.pdf")
    pages = load_pdf(pdf_path, document_id="vinuni-handbook-2025", source="data/vinuni_academic_handbook_2025_2026.pdf")
    total_content_pages = len(pages)
    total_chars = sum(len(p.text) for p in pages)
    print(f"Loaded {total_content_pages} content pages from {pdf_path.name}")
    print(f"Total normalized characters: {total_chars:,}")
    if total_content_pages < 30:
        raise AssertionError(f"Expected at least 30 content pages, got {total_content_pages}")

    print("\n=== Step 2: Chunking Strategies ===")
    # Strategy A: Fixed-size 500 characters, 50 overlap
    chunks_a = fixed_size(pages, size=500, overlap=50)
    # Strategy B & C: Paragraph-aware, max 1000 characters
    chunks_b = by_paragraph(pages, max_size=1000)
    chunks_c = chunks_b  # Strategy C uses identical chunking as B

    print(f"Strategy A (Fixed 500/50): {len(chunks_a)} chunks, avg len: {sum(len(c.text) for c in chunks_a)/len(chunks_a):.1f} chars")
    print(f"Strategy B/C (Paragraph max 1000): {len(chunks_b)} chunks, avg len: {sum(len(c.text) for c in chunks_b)/len(chunks_b):.1f} chars")

    print("\n=== Step 3: Embeddings & Vector Store ===")
    embedder = GeminiEmbedder(api_key=api_key, model_name="models/gemini-embedding-001", dimensions=768)
    store = PgVectorStore(database_url=db_url, dimensions=768)
    store.create_schema()

    # Ingest Strategy A
    start_t_a = time.time()
    print("Embedding Strategy A chunks...")
    texts_a = [c.text for c in chunks_a]
    vectors_a = embedder.embed_documents(texts_a)
    store.upsert("strategy_a", chunks_a, vectors_a)
    time_a = time.time() - start_t_a
    print(f"Strategy A stored in {time_a:.2f}s ({len(chunks_a)} chunks)")

    # Ingest Strategy B & C
    start_t_b = time.time()
    print("Embedding Strategy B/C chunks...")
    texts_b = [c.text for c in chunks_b]
    vectors_b = embedder.embed_documents(texts_b)
    store.upsert("strategy_b", chunks_b, vectors_b)
    store.upsert("strategy_c", chunks_c, vectors_b)
    time_b = time.time() - start_t_b
    print(f"Strategy B & C stored in {time_b:.2f}s ({len(chunks_b)} chunks)")

    print("\n=== Step 4: Dev & Test Benchmark Queries ===")
    questions_path = find_file("benchmark/questions.json")
    with open(questions_path, "r", encoding="utf-8") as f:
        questions = json.load(f)

    dev_count = sum(1 for q in questions if q.get("split") == "dev")
    test_count = sum(1 for q in questions if q.get("split") == "test")
    filter_count = sum(1 for q in questions if q.get("filter"))
    print(f"Loaded {len(questions)} questions ({dev_count} dev, {test_count} test, {filter_count} with filter)")

    # Pre-embed all questions once to maintain consistent evaluation
    print("Embedding query questions...")
    query_vectors = {}
    for q in questions:
        query_vectors[q["id"]] = embedder.embed_query(q["question"])
        time.sleep(0.1)

    # Execute Strategy A (no filter)
    print("\nRunning queries for Strategy A...")
    traces_a = []
    for q in questions:
        hits = store.search("strategy_a", query_vectors[q["id"]], top_k=3, filters=None)
        trace = evaluate_query(q, hits)
        traces_a.append(trace)

    # Execute Strategy B (no filter)
    print("Running queries for Strategy B...")
    traces_b = []
    for q in questions:
        hits = store.search("strategy_b", query_vectors[q["id"]], top_k=3, filters=None)
        trace = evaluate_query(q, hits)
        traces_b.append(trace)

    # Execute Strategy C (with metadata filter when provided)
    print("Running queries for Strategy C...")
    traces_c = []
    for q in questions:
        f_spec = q.get("filter")
        hits = store.search("strategy_c", query_vectors[q["id"]], top_k=3, filters=f_spec)
        trace = evaluate_query(q, hits)
        traces_c.append(trace)

    # Step 5: Summarize & Export
    summary_a = summarize(traces_a)
    summary_b = summarize(traces_b)
    summary_c = summarize(traces_c)

    results_dir = repo_root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    starter_results_dir = repo_root / "starter" / "results"
    starter_results_dir.mkdir(parents=True, exist_ok=True)

    with open(results_dir / "traces_strategy_a.json", "w", encoding="utf-8") as f:
        json.dump(traces_a, f, ensure_ascii=False, indent=2)
    with open(results_dir / "traces_strategy_b.json", "w", encoding="utf-8") as f:
        json.dump(traces_b, f, ensure_ascii=False, indent=2)
    with open(results_dir / "traces_strategy_c.json", "w", encoding="utf-8") as f:
        json.dump(traces_c, f, ensure_ascii=False, indent=2)

    all_summary = {
        "strategy_a": {
            "chunk_count": len(chunks_a),
            "ingest_time_seconds": round(time_a, 2),
            "metrics": summary_a
        },
        "strategy_b": {
            "chunk_count": len(chunks_b),
            "ingest_time_seconds": round(time_b, 2),
            "metrics": summary_b
        },
        "strategy_c": {
            "chunk_count": len(chunks_c),
            "ingest_time_seconds": round(time_b, 2),
            "metrics": summary_c
        }
    }

    with open(results_dir / "summary_metrics.json", "w", encoding="utf-8") as f:
        json.dump(all_summary, f, ensure_ascii=False, indent=2)

    # Mirror to starter/results
    for fname in ["traces_strategy_a.json", "traces_strategy_b.json", "traces_strategy_c.json", "summary_metrics.json"]:
        content = (results_dir / fname).read_text(encoding="utf-8")
        (starter_results_dir / fname).write_text(content, encoding="utf-8")

    # Step 6: Update experiment_log.csv
    exp_log_path = repo_root / "artifacts" / "experiment_log.csv"
    with open(exp_log_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "strategy", "chunking", "chunk_size", "overlap", "metadata", "filter",
            "vectorizer", "hypothesis", "dev_hit1", "dev_hit3", "test_hit1", "test_hit3", "notes"
        ])
        writer.writerow([
            "A", "fixed_size", "500", "50", "doc,page,section", "none",
            "gemini-embedding-001(768d)", "Fixed chunks may split sentences/paragraphs, lowering evidence recall",
            summary_a["dev"]["hit_1_ratio"], summary_a["dev"]["hit_3_ratio"],
            summary_a["test"]["hit_1_ratio"], summary_a["test"]["hit_3_ratio"],
            f"{len(chunks_a)} chunks, {time_a:.1f}s ingest"
        ])
        writer.writerow([
            "B", "by_paragraph", "1000", "0", "doc,page,section", "none",
            "gemini-embedding-001(768d)", "Paragraph chunking preserves semantic integrity, improving Hit@1 and Hit@3",
            summary_b["dev"]["hit_1_ratio"], summary_b["dev"]["hit_3_ratio"],
            summary_b["test"]["hit_1_ratio"], summary_b["test"]["hit_3_ratio"],
            f"{len(chunks_b)} chunks, {time_b:.1f}s ingest"
        ])
        writer.writerow([
            "C", "by_paragraph", "1000", "0", "doc,page,section", "metadata_filter(section)",
            "gemini-embedding-001(768d)", "Adding metadata filtering eliminates cross-section distractor noise for filtered queries",
            summary_c["dev"]["hit_1_ratio"], summary_c["dev"]["hit_3_ratio"],
            summary_c["test"]["hit_1_ratio"], summary_c["test"]["hit_3_ratio"],
            f"{len(chunks_c)} chunks, {time_b:.1f}s ingest, filter queries 100% compliant"
        ])

    print("\n=== Benchmark Results Summary ===")
    print(f"{'Strategy':<10} | {'Split':<6} | {'Hit@1':<12} | {'Evidence Hit@3':<16} | {'Chunks':<7}")
    print("-" * 62)
    for name, s in [("A", summary_a), ("B", summary_b), ("C", summary_c)]:
        count = len(chunks_a) if name == "A" else len(chunks_b)
        print(f"Strategy {name:<2} | dev    | {s['dev']['hit_1_ratio']:<12} | {s['dev']['hit_3_ratio']:<16} | {count}")
        print(f"Strategy {name:<2} | test   | {s['test']['hit_1_ratio']:<12} | {s['test']['hit_3_ratio']:<16} | {count}")
        print(f"Strategy {name:<2} | OVERALL| {s['overall']['hit_1_ratio']:<12} | {s['overall']['hit_3_ratio']:<16} | {count}")
        print("-" * 62)

    print(f"\nExecution finished successfully! Results saved to {results_dir}")


if __name__ == "__main__":
    main()
