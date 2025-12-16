import argparse
import io
import json
from pathlib import Path
from collections import defaultdict


def load_jsonl(path: Path):
    rows = []
    with io.open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def load_val_index(path: Path):
    idx = {}
    if not path.exists():
        return idx
    for r in load_jsonl(path):
        idx[r.get("id")] = r
    return idx


def to_md(summary):
    lines = []
    lines.append("# Errores Prioritarios — Evaluación de Recuperación")
    lines.append("")
    lines.append(f"- Total preguntas: {summary['totals']['n']}")
    lines.append(f"- Fallos (P@1=0): {summary['totals']['fails']} ({summary['totals']['fail_rate']:.1%})")
    lines.append("")
    lines.append("## Categorías más problemáticas")
    lines.append("- Ordenadas por mayor tasa de fallo (luego por número de preguntas)")
    for cat in summary["ordered_cats"]:
        met = summary["by_cat"][cat]
        lines.append(f"\n### {cat}")
        lines.append(f"- n={met['n']} | fallos={met['fails']} ({met['fail_rate']:.1%}) | P@1={met['p1']:.3f} | MRR={met['mrr']:.3f}")
        examples = met.get("examples", [])
        if examples:
            lines.append("- Ejemplos (hasta 5):")
            for ex in examples[:5]:
                lines.append(f"  - {ex['id']} — lbl={ex['label']} | top1: pág {ex['top1_page']} score={ex['top1_score']:.4f}")
                if ex.get("expected_pages"):
                    lines.append(f"    · esperadas: {ex['expected_pages']}")
                if ex.get("expected_keywords"):
                    lines.append(f"    · keywords: {', '.join(ex['expected_keywords'][:6])}{'…' if len(ex['expected_keywords'])>6 else ''}")
                lines.append(f"    · snippet: {ex['snippet']}")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--details", default="results/eval_details.jsonl")
    ap.add_argument("--validation", default="validation/validation_set.jsonl")
    ap.add_argument("--out", default="results/eval_top_errors.md")
    ap.add_argument("--max_snippet", type=int, default=220)
    args = ap.parse_args()

    details_path = Path(args.details)
    val_path = Path(args.validation)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows = load_jsonl(details_path)
    val_idx = load_val_index(val_path)

    by_cat = defaultdict(list)
    for r in rows:
        cat = r.get("category", "") or "(sin_categoria)"
        by_cat[cat].append(r)

    def metrics(arr):
        n = len(arr)
        fails = sum(1 for x in arr if float(x.get("precision1", 0.0)) <= 0.0)
        p1 = sum(float(x.get("precision1", 0.0)) for x in arr) / n if n else 0.0
        mrr = sum(float(x.get("mrr_contrib", 0.0)) for x in arr) / n if n else 0.0
        return {"n": n, "fails": fails, "fail_rate": (fails / n if n else 0.0), "p1": p1, "mrr": mrr}

    meta = {}
    for cat, arr in by_cat.items():
        m = metrics(arr)
        # ejemplos: solo fallos
        examples = []
        for x in arr:
            if float(x.get("precision1", 0.0)) > 0.0:
                continue
            topk = x.get("topk", []) or []
            top1 = topk[0] if topk else {}
            ttxt = str(top1.get("text", "")).replace("\n", " ").strip()
            if args.max_snippet and len(ttxt) > args.max_snippet:
                ttxt = ttxt[: args.max_snippet - 1] + "…"
            vx = val_idx.get(x.get("id"), {})
            examples.append({
                "id": x.get("id"),
                "label": x.get("label"),
                "top1_page": top1.get("page"),
                "top1_score": float(top1.get("distance", 0.0)) if top1 else 0.0,
                "snippet": ttxt,
                "expected_pages": vx.get("expected_pages", []),
                "expected_keywords": vx.get("expected_keywords", []),
            })
        m["examples"] = examples
        meta[cat] = m

    totals = metrics(rows)
    ordered = sorted(meta.keys(), key=lambda c: (meta[c]["fail_rate"], meta[c]["n"]), reverse=True)
    summary = {"totals": totals, "by_cat": meta, "ordered_cats": ordered}

    md = to_md(summary)
    with io.open(out_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
