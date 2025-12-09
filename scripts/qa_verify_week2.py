import os
import re
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_DIR = ROOT / "data" / "text_by_page"
CHUNKS_FILE = ROOT / "data" / "chunks" / "chunks.jsonl"
OUT_JSON = ROOT / "docs" / "qa_results_week2.json"
OUT_MD = ROOT / "docs" / "qa_summary_week2.md"


def read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8", errors="replace") as f:
        return f.read()


def analyze_text_by_page(expected_pages: int | None = None) -> dict:
    files = sorted(TEXT_DIR.glob("page_*.txt"))
    name_re = re.compile(r"^page_(\d{3})\.txt$")

    page_nums: list[int] = []
    bad_names: list[str] = []
    empty_files: list[str] = []
    bom_files: list[str] = []
    replacement_char_files: list[str] = []

    header_candidates: Counter = Counter()
    footer_candidates: Counter = Counter()
    hyphen_breaks = 0
    hyphen_positions = 0
    double_spaces = 0
    triple_spaces = 0

    lengths: list[int] = []

    for fp in files:
        m = name_re.match(fp.name)
        if not m:
            bad_names.append(fp.name)
            continue

        page_num = int(m.group(1))
        page_nums.append(page_num)

        text = read_text(fp)
        lengths.append(len(text))
        if not text.strip():
            empty_files.append(fp.name)

        # BOM detection
        if text.startswith("\ufeff"):
            bom_files.append(fp.name)

        # replacement character detection
        if "�" in text:
            replacement_char_files.append(fp.name)

        # header/footer candidates: first and last non-empty line
        lines = [ln.strip() for ln in text.splitlines()]
        non_empty = [ln for ln in lines if ln]
        if non_empty:
            header_candidates[non_empty[0]] += 1
            footer_candidates[non_empty[-1]] += 1

        # hyphenation heuristic
        for i, ln in enumerate(lines[:-1]):
            if ln.rstrip().endswith("-"):
                hyphen_positions += 1
                nxt = lines[i + 1].lstrip()
                if nxt and nxt[:1].islower():
                    hyphen_breaks += 1

        double_spaces += text.count("  ")
        triple_spaces += text.count("   ")

    page_nums_sorted = sorted(page_nums)
    missing: list[int] = []
    extra: list[int] = []
    if expected_pages:
        expected_set = set(range(1, expected_pages + 1))
        observed = set(page_nums_sorted)
        missing = sorted(expected_set - observed)
        extra = sorted(observed - expected_set)

    total_pages = len(page_nums_sorted)
    header_common = header_candidates.most_common(5)
    footer_common = footer_candidates.most_common(5)

    hyphen_break_rate = (hyphen_breaks / hyphen_positions) if hyphen_positions else 0.0

    lengths_summary = {}
    if lengths:
        try:
            q = statistics.quantiles(lengths, n=4)
            lengths_summary = {
                "min": min(lengths),
                "p25": int(q[0]),
                "median": int(statistics.median(lengths)),
                "p75": int(q[2]),
                "max": max(lengths),
                "mean": float(statistics.fmean(lengths)),
            }
        except Exception:
            lengths_summary = {
                "min": min(lengths),
                "median": int(statistics.median(lengths)),
                "max": max(lengths),
                "mean": float(statistics.fmean(lengths)),
            }

    return {
        "total_pages_found": total_pages,
        "pages_listed": page_nums_sorted[:10] + (["..."] if total_pages > 10 else []) + page_nums_sorted[-5:],
        "bad_names": bad_names,
        "empty_files": empty_files,
        "bom_files": bom_files,
        "replacement_char_files": replacement_char_files,
        "missing_pages": missing,
        "extra_pages": extra,
        "header_candidates_top": header_common,
        "footer_candidates_top": footer_common,
        "hyphen_positions": hyphen_positions,
        "hyphen_breaks": hyphen_breaks,
        "hyphen_break_rate": hyphen_break_rate,
        "double_spaces": double_spaces,
        "triple_spaces": triple_spaces,
        "lengths_summary": lengths_summary,
    }


def jaccard_bigrams(a: str, b: str) -> float:
    def bigrams(s: str):
        s = re.sub(r"\s+", " ", s.strip().lower())
        return {s[i : i + 2] for i in range(max(0, len(s) - 1))}

    A, B = bigrams(a), bigrams(b)
    if not A and not B:
        return 1.0
    if not A or not B:
        return 0.0
    inter = len(A & B)
    union = len(A | B)
    return inter / union if union else 0.0


def analyze_chunks() -> dict:
    if not CHUNKS_FILE.exists():
        return {"error": f"Chunks file not found: {CHUNKS_FILE}"}

    ids = set()
    dup_ids = []
    bad_lines = []
    missing_fields = []
    empty_text = []
    text_lengths = []
    text_hash_counts = Counter()

    by_source = defaultdict(list)

    with CHUNKS_FILE.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception as e:
                bad_lines.append({"line": i, "error": str(e)})
                continue

            cid = obj.get("chunk_id")
            txt = obj.get("text")
            meta = obj.get("metadata", {}) or {}

            if cid in ids:
                dup_ids.append({"line": i, "chunk_id": cid})
            else:
                ids.add(cid)

            required_meta = ["source", "page_number"]
            missing = [k for k in required_meta if k not in meta]
            if (cid is None) or (txt is None) or missing:
                missing_fields.append({"line": i, "chunk_id": cid, "missing": missing})

            if not txt or not str(txt).strip():
                empty_text.append({"line": i, "chunk_id": cid})
            else:
                tnorm = re.sub(r"\s+", " ", str(txt).strip())
                text_lengths.append(len(tnorm))
                text_hash_counts[hash(tnorm)] += 1

            src = meta.get("source")
            if src is not None:
                by_source[src].append(obj)

    # approximate overlap via Jaccard bigrams between consecutive chunks in same source
    overlaps = []
    for src, arr in by_source.items():
        # sort by chunk_id suffix if present
        def keyfn(o):
            cid = o.get("chunk_id", "")
            m = re.search(r"-(\d+)$", cid)
            return (int(m.group(1)) if m else 0)

        arr_sorted = sorted(arr, key=keyfn)
        for a, b in zip(arr_sorted, arr_sorted[1:]):
            s = jaccard_bigrams(a.get("text", ""), b.get("text", ""))
            overlaps.append(s)

    text_len_summary = {}
    if text_lengths:
        try:
            text_len_summary = {
                "min": min(text_lengths),
                "p25": int(statistics.quantiles(text_lengths, n=4)[0]),
                "median": int(statistics.median(text_lengths)),
                "p75": int(statistics.quantiles(text_lengths, n=4)[2]),
                "max": max(text_lengths),
                "mean": float(statistics.fmean(text_lengths)),
            }
        except Exception:
            text_len_summary = {
                "min": min(text_lengths),
                "median": int(statistics.median(text_lengths)),
                "max": max(text_lengths),
                "mean": float(statistics.fmean(text_lengths)),
            }

    dup_texts = sum(c for c in text_hash_counts.values() if c > 1)
    approx_overlap_summary = {}
    if overlaps:
        approx_overlap_summary = {
            "count_pairs": len(overlaps),
            "mean": float(statistics.fmean(overlaps)),
            "median": float(statistics.median(overlaps)),
            "p75": float(statistics.quantiles(overlaps, n=4)[2]),
            "p90": float(statistics.quantiles(overlaps, n=10)[8]),
            "max": float(max(overlaps)),
        }

    return {
        "total_lines": len(ids) + len(dup_ids),
        "unique_ids": len(ids),
        "dup_ids": dup_ids[:50],  # cap
        "bad_lines": bad_lines[:50],
        "missing_fields": missing_fields[:50],
        "empty_text": empty_text[:50],
        "text_len_summary": text_len_summary,
        "duplicate_text_occurrences": dup_texts,
        "approx_overlap_summary": approx_overlap_summary,
    }


def to_markdown(results: dict) -> str:
    tbp = results.get("text_by_page", {})
    ch = results.get("chunks", {})

    md = []
    md.append("# QA Summary — Semana 2")
    md.append("")
    md.append("## Extracción (text_by_page)")
    md.append(f"- Páginas encontradas: {tbp.get('total_pages_found')}" )
    if tbp.get("missing_pages"):
        md.append(f"- Páginas faltantes: {len(tbp['missing_pages'])} -> {tbp['missing_pages'][:20]}{' ...' if len(tbp['missing_pages'])>20 else ''}")
    if tbp.get("extra_pages"):
        md.append(f"- Páginas extra: {len(tbp['extra_pages'])} -> {tbp['extra_pages'][:20]}{' ...' if len(tbp['extra_pages'])>20 else ''}")
    md.append(f"- Archivos vacíos: {len(tbp.get('empty_files', []))}")
    md.append(f"- Archivos con BOM: {len(tbp.get('bom_files', []))}")
    md.append(f"- Archivos con caracteres de reemplazo: {len(tbp.get('replacement_char_files', []))}")
    lens = tbp.get("lengths_summary", {})
    if lens:
        md.append(f"- Longitud por página (chars) — min/med/max: {lens.get('min')}/{lens.get('median')}/{lens.get('max')} (mean≈{lens.get('mean', 0):.1f})")
    md.append(f"- Hyphen breaks (aprox): {tbp.get('hyphen_breaks',0)}/{tbp.get('hyphen_positions',0)} => rate≈{tbp.get('hyphen_break_rate',0):.2f}")
    md.append(f"- Doble espacios: {tbp.get('double_spaces',0)} | Triples: {tbp.get('triple_spaces',0)}")
    if tbp.get("header_candidates_top"):
        md.append("- Headers frecuentes (Top 3):")
        for s, c in tbp["header_candidates_top"][:3]:
            md.append(f"  - '{s}'  —  {c} páginas")
    if tbp.get("footer_candidates_top"):
        md.append("- Footers frecuentes (Top 3):")
        for s, c in tbp["footer_candidates_top"][:3]:
            md.append(f"  - '{s}'  —  {c} páginas")

    md.append("")
    md.append("## Chunking (chunks.jsonl)")
    md.append(f"- Líneas totales: {ch.get('total_lines')}")
    md.append(f"- IDs únicos: {ch.get('unique_ids')}")
    md.append(f"- IDs duplicados (muestra): {len(ch.get('dup_ids', []))}")
    md.append(f"- Líneas inválidas (parse JSON): {len(ch.get('bad_lines', []))}")
    md.append(f"- Campos faltantes (muestra): {len(ch.get('missing_fields', []))}")
    md.append(f"- Chunks con texto vacío (muestra): {len(ch.get('empty_text', []))}")
    tls = ch.get("text_len_summary", {})
    if tls:
        md.append(f"- Longitud de texto — min/med/max: {tls.get('min')}/{tls.get('median')}/{tls.get('max')} (mean≈{tls.get('mean', 0):.1f})")
    aos = ch.get("approx_overlap_summary", {})
    if aos:
        md.append(f"- Overlap aprox. (Jaccard bigrams) — median/p90/max: {aos.get('median',0):.2f}/{aos.get('p90',0):.2f}/{aos.get('max',0):.2f}")
    md.append(f"- Duplicados por texto (normalizado) detectados: {ch.get('duplicate_text_occurrences',0)}")

    return "\n".join(md)


def main():
    # Usa 212 páginas como referencia provista por el usuario
    tbp = analyze_text_by_page(expected_pages=212)
    ch = analyze_chunks()
    results = {"text_by_page": tbp, "chunks": ch}

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    md = to_markdown(results)
    with OUT_MD.open("w", encoding="utf-8") as f:
        f.write(md + "\n")

    print(f"Wrote: {OUT_JSON}")
    print(f"Wrote: {OUT_MD}")


if __name__ == "__main__":
    main()
