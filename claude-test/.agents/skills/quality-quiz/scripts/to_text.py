#!/usr/bin/env python3
"""Export the question bank to a plain‑text file.

Usage:
    python to_text.py <questions_folder> <output_file>

The script reads all ``*.yml`` files in ``<questions_folder>`` and writes a
human‑readable representation of each question to ``<output_file>``.
"""

import pathlib, yaml, sys

def format_question(q, idx):
    lines = []
    lines.append(f"{idx}. {q.get('question', '').strip()}")
    fmt = q.get('format')
    if fmt == 'multiple_choice':
        opts = q.get('options', [])
        if isinstance(opts, str):
            opts = [o.strip() for o in opts.split('|') if o.strip()]
        for i, opt in enumerate(opts, 1):
            lines.append(f"   {i}) {opt}")
    elif fmt == 'true_false':
        lines.append("   (True/False)")
    # Answer line
    answer_val = q.get('answer', '')
    if isinstance(answer_val, bool):
        answer_str = str(answer_val)
    else:
        answer_str = str(answer_val).strip()
    lines.append(f"Answer: {answer_str}")
    # Optional explanation
    if q.get('explanation'):
        lines.append(f"Explanation: {q['explanation'].strip()}")
    lines.append("")
    return "\n".join(lines)

def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: to_text.py <questions_folder> <output_file>")
    src = pathlib.Path(sys.argv[1])
    out_path = pathlib.Path(sys.argv[2])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    idx = 1
    with out_path.open('w', encoding='utf-8') as out_f:
        for yaml_file in sorted(src.glob('*.yml')):
            rows = yaml.safe_load(yaml_file.read_text()) or []
            for q in rows:
                out_f.write(format_question(q, idx))
                out_f.write('\n')
                idx += 1
    print(f"✅ Text file written to {out_path}")

if __name__ == "__main__":
    main()
