# scripts/find_phrase.py
import json, argparse, re
ap = argparse.ArgumentParser()
ap.add_argument('--infile', default='data/chunks/chunks.cleaned.jsonl')
ap.add_argument('--phrase', required=True)
ap.add_argument('--context', type=int, default=120)
args = ap.parse_args()

phrase = args.phrase.lower()
with open(args.infile,'r',encoding='utf-8') as f:
    for i,line in enumerate(f,1):
        if not line.strip(): continue
        obj = json.loads(line)
        text = obj.get('text','').lower()
        if phrase in text:
            idx = text.index(phrase)
            start = max(0, idx-args.context)
            end = min(len(text), idx+len(phrase)+args.context)
            snippet = text[start:end].replace('\n',' ')
            print(f"LINE {i} id={obj.get('id')} page={obj.get('page')} | ...{snippet}...")
