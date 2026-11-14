"""Evaluate retrieved evidence and preserve per-query traces."""
from pathlib import Path
from typing import Any
import unicodedata


def _normalize_text(text: str) -> str:
    if not text:
        return ""
    text = unicodedata.normalize("NFC", text)
    return " ".join(text.split()).lower()


def is_evidence_hit(question: dict[str, Any], hit: dict[str, Any]) -> bool:
    """Check if a retrieved hit contains the gold evidence and matches page/source."""
    # Check source/document ID
    gold_source = question.get("gold_source_id", "").lower().strip()
    hit_source = Path(hit.get("source", "")).name.lower().strip()
    hit_doc_id = hit.get("document_id", "").lower().strip()

    source_matches = (
        gold_source == hit_source
        or gold_source == hit_doc_id
        or gold_source.replace("-", "_") == hit_doc_id.replace("-", "_")
        or ("vinuni" in gold_source and "vinuni" in (hit_doc_id + " " + hit_source))
    )
    if not source_matches:
        return False

    # Check page
    gold_page = question.get("gold_page")
    if isinstance(gold_page, (list, tuple, set)):
        if hit.get("page") not in gold_page:
            return False
    elif hit.get("page") != gold_page:
        return False

    # Check evidence quote containment
    gold_quote = _normalize_text(question.get("evidence_quote", ""))
    hit_text = _normalize_text(hit.get("text", ""))
    return gold_quote in hit_text


def evaluate_query(question: dict[str, Any], hits: list[dict[str, Any]]) -> dict[str, Any]:
    """Check source/page and enough gold evidence; keep hit@1 and hit@3 trace."""
    hit_at_1 = len(hits) > 0 and is_evidence_hit(question, hits[0])
    evidence_hit_at_3 = any(is_evidence_hit(question, h) for h in hits[:3])

    hit_rank = None
    for idx, h in enumerate(hits[:3], 1):
        if is_evidence_hit(question, h):
            hit_rank = idx
            break

    filter_spec = question.get("filter")
    filter_compliant = True
    if filter_spec:
        for hit in hits:
            hit_meta = hit.get("metadata", {})
            for fk, fv in filter_spec.items():
                if str(hit_meta.get(fk)) != str(fv):
                    filter_compliant = False
                    break

    return {
        "question_id": question.get("id"),
        "split": question.get("split", "dev"),
        "question": question.get("question", ""),
        "expected_answer": question.get("expected_answer", ""),
        "gold_source_id": question.get("gold_source_id", ""),
        "gold_page": question.get("gold_page"),
        "evidence_quote": question.get("evidence_quote", ""),
        "filter": filter_spec,
        "hits": hits,
        "hit_at_1": hit_at_1,
        "evidence_hit_at_3": evidence_hit_at_3,
        "hit_rank": hit_rank,
        "filter_compliant": filter_compliant if filter_spec else None
    }


def summarize(traces: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate Hit@1 and Evidence Hit@3 by strategy and dev/test split."""
    def calc_split(items: list[dict[str, Any]]) -> dict[str, Any]:
        total = len(items)
        if total == 0:
            return {
                "total": 0,
                "hit_1_count": 0,
                "hit_1_rate": 0.0,
                "hit_1_ratio": "0/0",
                "hit_3_count": 0,
                "hit_3_rate": 0.0,
                "hit_3_ratio": "0/0"
            }
        hit_1 = sum(1 for t in items if t.get("hit_at_1"))
        hit_3 = sum(1 for t in items if t.get("evidence_hit_at_3"))
        return {
            "total": total,
            "hit_1_count": hit_1,
            "hit_1_rate": round(hit_1 / total, 4),
            "hit_1_ratio": f"{hit_1}/{total}",
            "hit_3_count": hit_3,
            "hit_3_rate": round(hit_3 / total, 4),
            "hit_3_ratio": f"{hit_3}/{total}"
        }

    dev_traces = [t for t in traces if t.get("split") == "dev"]
    test_traces = [t for t in traces if t.get("split") == "test"]
    filter_traces = [t for t in traces if t.get("filter")]

    filter_compliant_count = sum(1 for t in filter_traces if t.get("filter_compliant"))
    filter_compliance_ratio = (
        f"{filter_compliant_count}/{len(filter_traces)}" if filter_traces else "N/A"
    )

    return {
        "overall": calc_split(traces),
        "dev": calc_split(dev_traces),
        "test": calc_split(test_traces),
        "filter_queries": {
            "total": len(filter_traces),
            "compliant_count": filter_compliant_count,
            "compliance_ratio": filter_compliance_ratio
        }
    }
