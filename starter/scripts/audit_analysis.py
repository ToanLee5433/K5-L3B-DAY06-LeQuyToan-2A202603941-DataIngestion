"""Script to perform manual audit calculations for Day 06 Benchmark."""
import json
from pathlib import Path

def main():
    root = Path(__file__).resolve().parent.parent
    with open(root / "results" / "traces_strategy_a.json", encoding="utf-8") as f:
        ta = json.load(f)
    with open(root / "results" / "traces_strategy_b.json", encoding="utf-8") as f:
        tb = json.load(f)
    with open(root / "results" / "traces_strategy_c.json", encoding="utf-8") as f:
        tc = json.load(f)

    # 1. Inspect test questions
    for s_name, traces in [("Strategy A", ta), ("Strategy B", tb), ("Strategy C", tc)]:
        print(f"\n==================== {s_name} (Test Set) ====================")
        test_traces = [t for t in traces if t["split"] == "test"]
        for t in test_traces:
            qid = t["question_id"]
            q_text = t["question"]
            gold_p = t["gold_page"]
            h1 = t["hit_at_1"]
            h3 = t["evidence_hit_at_3"]
            rank = t["hit_rank"]
            print(f"[{qid}] Page {gold_p} | Hit@1: {h1} | Evidence Hit@3: {h3} | Rank: {rank}")
            print(f"  Q: {q_text}")
            for i, hit in enumerate(t["hits"][:3], 1):
                p = hit.get("page")
                sec = hit.get("metadata", {}).get("section")
                score = round(hit.get("score", 0), 4)
                preview = hit.get("text", "")[:120].replace("\n", " ")
                print(f"    Hit {i}: Page {p} [{sec}] score={score} -> {preview}...")

if __name__ == "__main__":
    main()
