import argparse, json, io
import statistics
from pathlib import Path

def load_details(path):
    rows = []
    with io.open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows

def is_relevant(result_text: str, result_page: int, expected_pages, expected_keywords):
    if expected_pages:
        if result_page in set(expected_pages):
            return True
    if expected_keywords:
        txt = result_text.lower()
        hits = sum(1 for kw in expected_keywords if kw.lower() in txt)
        if hits >= max(3, int(0.6 * len(expected_keywords))):
            return True
    return False

def analyze(rows):
    # collect top-1 scores and labels
    top1 = []
    for r in rows:
        tk = r.get('topk', [])
        if not tk:
            continue
        first = tk[0]
        score = float(first.get('distance', 0.0))
        label = r.get('label', '')
        expected_pages = r.get('expected_pages', [])
        expected_keywords = r.get('expected_keywords', [])
        first_rel = is_relevant(first.get('text',''), int(first.get('page',-1)), expected_pages, expected_keywords)
        top1.append({
            'score': score,
            'label': label,
            'first_rel': first_rel
        })
    scores = [x['score'] for x in top1]
    pos_scores = [x['score'] for x in top1 if x['label'] == 'covered']
    neg_scores = [x['score'] for x in top1 if x['label'] == 'uncovered']
    return {
        'n': len(top1),
        'mean': statistics.fmean(scores) if scores else 0.0,
        'q10': float(sorted(scores)[int(0.1*len(scores))]) if scores else 0.0,
        'q25': float(sorted(scores)[int(0.25*len(scores))]) if scores else 0.0,
        'q50': float(sorted(scores)[int(0.5*len(scores))]) if scores else 0.0,
        'q75': float(sorted(scores)[int(0.75*len(scores))]) if scores else 0.0,
        'pos_mean': statistics.fmean(pos_scores) if pos_scores else 0.0,
        'neg_mean': statistics.fmean(neg_scores) if neg_scores else 0.0,
        'pos_n': len(pos_scores),
        'neg_n': len(neg_scores),
    }

def simulate_threshold_metrics(rows, threshold):
    # accuracy wrt label using threshold gate on top-1
    correct = 0
    for r in rows:
        tk = r.get('topk', [])
        if not tk:
            continue
        first = tk[0]
        score = float(first.get('distance', 0.0))
        label = r.get('label', '')
        expected_pages = r.get('expected_pages', [])
        expected_keywords = r.get('expected_keywords', [])
        first_rel = is_relevant(first.get('text',''), int(first.get('page',-1)), expected_pages, expected_keywords)
        # decision: answer if score>=threshold else no-answer
        answer = score >= threshold
        # correctness: if covered -> need first_rel and answer; if uncovered -> need no-answer
        if label == 'covered':
            if answer and first_rel:
                correct += 1
        else:
            if not answer:
                correct += 1
    return correct

def make_md(stats, trials):
    lines = []
    lines.append('# Threshold Analysis (Week 4)')
    lines.append('')
    lines.append(f"Samples: {stats['n']}")
    lines.append(f"Top-1 score mean: {stats['mean']:.3f} | pos_mean: {stats['pos_mean']:.3f} | neg_mean: {stats['neg_mean']:.3f}")
    lines.append(f"Quartiles: Q25={stats['q25']:.3f} Q50={stats['q50']:.3f} Q75={stats['q75']:.3f}")
    lines.append('')
    lines.append('## Accuracy vs Threshold (top-1 gate)')
    for thr, acc in trials:
        lines.append(f"- threshold={thr:.2f}: accuracy={acc}/{stats['n']} ({acc/stats['n']:.3f})")
    # recommend threshold near Q50 if neg_mean<<pos_mean
    rec = trials[max(range(len(trials)), key=lambda i: trials[i][1])][0]
    lines.append('')
    lines.append(f"**Recommended threshold**: {rec:.2f} (max accuracy in sweep)")
    return '\n'.join(lines)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--details', required=True)
    ap.add_argument('--out', default='results/week4_threshold.md')
    args = ap.parse_args()
    rows = load_details(args.details)
    stats = analyze(rows)
    # sweep thresholds 0.20..0.50 step 0.05
    trials = []
    for thr in [x/100.0 for x in range(20, 51, 5)]:
        acc = simulate_threshold_metrics(rows, thr)
        trials.append((thr, acc))
    md = make_md(stats, trials)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with io.open(out, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"Wrote: {out}")
