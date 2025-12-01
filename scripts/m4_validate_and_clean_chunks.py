#!/usr/bin/env python3
# scripts/validate_and_clean_chunks.py
import json, argparse, re, unicodedata
import hashlib

CONTROL_RE = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F]')
MULTISPACE_RE = re.compile(r'\s+')

def clean_text(text):
    if text is None:
        return ""
    text = unicodedata.normalize('NFC', text)
    text = text.lstrip('\ufeff')
    text = CONTROL_RE.sub('', text)
    text = text.replace('\r\n','\n').replace('\r','\n')
    text = text.replace('\u00A0', ' ')
    text = MULTISPACE_RE.sub(' ', text)
    return text.strip()

def deterministic_id_from_row(row, filename=None):
    if 'id' in row and row['id']:
        return row['id']
    src = row.get('source') or filename or "unknown"
    payload = f"{src}:{row.get('page','')}-{row.get('start','')}-{row.get('end','')}"
    return hashlib.sha1(payload.encode('utf-8')).hexdigest()[:16]

def validate_and_clean(inpath, outpath, min_len=20, max_len=10000):
    seen_ids = set()
    errors = []
    total = 0
    written = 0
    with open(inpath,'r',encoding='utf-8') as inf, open(outpath,'w',encoding='utf-8') as outf:
        for line_no, line in enumerate(inf, start=1):
            line = line.strip()
            if not line:
                continue
            total += 1
            try:
                row = json.loads(line)
            except Exception as e:
                errors.append(f"LINE {line_no}: JSON parse error: {e}")
                continue
            # required fields
            missing = [k for k in ('page','start','end','text') if k not in row]
            if missing:
                errors.append(f"LINE {line_no}: missing fields {missing}")
                continue
            try:
                row['page'] = int(row['page'])
                row['start'] = int(row['start'])
                row['end'] = int(row['end'])
            except:
                errors.append(f"LINE {line_no}: page/start/end must be integers")
                continue
            if not (0 <= row['start'] < row['end'] or (row['start']==0 and row['end']>=0)):
                errors.append(f"LINE {line_no}: invalid start/end")
                continue
            # id
            row_id = row.get('id') or deterministic_id_from_row(row,inpath)
            if row_id in seen_ids:
                errors.append(f"LINE {line_no}: duplicate id {row_id}")
                continue
            row['id'] = row_id
            seen_ids.add(row_id)
            # clean text
            cleaned = clean_text(row.get('text',''))
            row['text'] = cleaned
            L = len(cleaned)
            if L < min_len:
                errors.append(f"LINE {line_no}: text too short ({L}) id={row_id}")
                continue
            # write
            outf.write(json.dumps(row, ensure_ascii=False) + "\n")
            written += 1
    return {'total':total,'written':written,'errors':errors}

if __name__ == "__main__":
    import sys
    ap = argparse.ArgumentParser()
    ap.add_argument('infile')
    ap.add_argument('--out','-o',default=None)
    args = ap.parse_args()
    out = args.out or args.infile + ".cleaned.jsonl"
    report = validate_and_clean(args.infile, out)
    print(f"Processed {report['total']} lines, written {report['written']}. Errors: {len(report['errors'])}")
    for e in report['errors'][:200]:
        print(e)
