# scripts/analyze_chunk_escapes.py
import re, json, sys
from collections import Counter

IN = "data/chunks/chunks.cleaned.jsonl"

c = Counter()
p_escaped_quote = re.compile(r'\\"')     # secuencia backslash + quote en la línea RAW
p_literal_backslash_n = re.compile(r'\\n')  # secuencia literal \n en la línea RAW
p_smart = re.compile(r'[\u2018\u2019\u201C\u201D]')

with open(IN, 'r', encoding='utf-8') as f:
    for i, raw in enumerate(f, 1):
        if not raw.strip(): continue
        # 1) chequeo en la línea cruda (antes de json.loads)
        if p_escaped_quote.search(raw):
            c['raw_has_escaped_quote'] += 1
        if p_literal_backslash_n.search(raw):
            c['raw_has_backslash_n'] += 1
        # 2) después de parsear JSON, chequea si la cadena contiene contrabarra explícita
        try:
            obj = json.loads(raw)
            text = obj.get('text','') or ''
            if '\\"' in text or "\\'" in text:
                c['parsed_text_has_backslash_quote'] += 1
            if '\\n' in text:
                c['parsed_text_has_backslash_n'] += 1
            if p_smart.search(text):
                c['parsed_text_has_smart_quotes'] += 1
        except Exception as e:
            c['json_parse_errors'] += 1

        c['total_lines'] += 1

print("SUMMARY:", dict(c))
