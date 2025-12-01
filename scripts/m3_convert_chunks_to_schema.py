#!/usr/bin/env python3
# scripts/convert_chunks_to_schema.py
import json, argparse, unicodedata, re, hashlib
from collections import Counter

HYPHEN_LINE_RE = re.compile(r'(\w)-\n(\w)', flags=re.UNICODE)
MULTISPACE_RE = re.compile(r'\s+')

def clean_text_basic(text):
    if text is None:
        return ""
    text = unicodedata.normalize('NFC', text)
    text = text.lstrip('\ufeff')
    text = HYPHEN_LINE_RE.sub(r'\1\2', text)
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # collapse newlines into spaces (since headers not repeated, safe)
    text = text.replace('\n', ' ')
    text = text.replace('\u00A0', ' ')
    text = MULTISPACE_RE.sub(' ', text)
    return text.strip()

def deterministic_id(chunk_id, source, page, start, end):
    if chunk_id:
        return chunk_id.strip()
    payload = f"{source}:{page}:{start}:{end}"
    return hashlib.sha1(payload.encode('utf-8')).hexdigest()[:16]

def convert(infile, outfile):
    recs = []
    with open(infile, 'r', encoding='utf-8') as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception as e:
                print(f"[PARSE ERROR] line {line_no}: {e}")
                continue
            recs.append(r)

    with open(outfile, 'w', encoding='utf-8') as outf:
        for r in recs:
            chunk_id = r.get('chunk_id') or r.get('id') or None
            meta = r.get('metadata') or {}
            source = meta.get('source') or r.get('source') or None
            page = meta.get('page_number') or meta.get('page') or None
            try:
                page = int(page) if page is not None else -1
            except:
                page = -1
            raw_text = r.get('text','') or ''
            cleaned = clean_text_basic(raw_text)
            start = 0
            end = len(cleaned)
            new_id = deterministic_id(chunk_id, source or "unknown", page, start, end)
            out_obj = {
                "id": new_id,
                "page": page,
                "start": start,
                "end": end,
                "text": cleaned,
                "source": source
            }
            # optional: if first line upper-case and short, add as title
            first_line = raw_text.splitlines()[0].strip() if raw_text.splitlines() else ""
            if first_line and len(first_line) < 120 and first_line.isupper():
                out_obj['title'] = first_line
            outf.write(json.dumps(out_obj, ensure_ascii=False) + "\n")
    print(f"Conversion escrita en {outfile}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('infile')
    ap.add_argument('--out', '-o', default=None)
    args = ap.parse_args()
    out = args.out or args.infile + ".converted.jsonl"
    convert(args.infile, out)
