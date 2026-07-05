import yaml, json, random, sys, pathlib, datetime

def load_questions(topic_path):
    questions = []
    for file in pathlib.Path(topic_path).glob('*.yml'):
        data = yaml.safe_load(file.read_text())
        if data:
            questions.extend(data)
    return questions

def filter_questions(qs, difficulty=None, fmt=None, topic=None):
    if topic:
        topic_key = topic.lower().replace(' ', '_').replace('&', 'and')
        qs = [q for q in qs if q.get('topic', '').lower().replace(' ', '_').replace('&', 'and') == topic_key]
    if difficulty:
        qs = [q for q in qs if q.get('difficulty') == difficulty]
    if fmt:
        qs = [q for q in qs if q.get('format') == fmt]
    return qs

def render_text(selected, include_explanations=True, title="Quality Quiz", topic=None):
    lines = []
    lines.append(f"{title}: {topic or 'Mixed Topics'} ({len(selected)} questions)")
    lines.append(f"Generated: {datetime.date.today().isoformat()}")
    lines.append("")
    for i, q in enumerate(selected, 1):
        fmt = q.get('format', 'single_choice')
        lines.append(f"{i}. {q['question']} ({fmt})")
        if fmt in ('single_choice', 'multi_select'):
            opts = q.get('options', [])
            for idx, opt in enumerate(opts, 1):
                lines.append(f"   {chr(64+idx)}) {opt}")
        # Answer line
        ans = q.get('answer', '')
        if isinstance(ans, list):
            ans_str = ', '.join(ans)
        else:
            ans_str = str(ans)
        lines.append(f"   Answer: {ans_str}")
        if include_explanations and q.get('explanation'):
            lines.append(f"   Explanation: {q['explanation']}")
        lines.append("")
    return "\n".join(lines)

def render_markdown(selected, include_explanations=True, topic=None):
    lines = []
    lines.append(f"### Quality-Quiz: {topic or 'Mixed Topics'} ({len(selected)} questions)")
    lines.append("")
    for i, q in enumerate(selected, 1):
        fmt = q.get('format', 'single_choice')
        lines.append(f"{i}️⃣ *{q['question']}*")
        if fmt in ('single_choice', 'multi_select'):
            for idx, opt in enumerate(q.get('options', []), 1):
                lines.append(f"   - {chr(64+idx)}) {opt}")
        ans = q.get('answer', '')
        if isinstance(ans, list):
            ans_str = ', '.join(ans)
        else:
            ans_str = str(ans)
        lines.append(f"**Answer:** {ans_str}")
        if include_explanations:
            lines.append(f"**Explanation:** {q.get('explanation','')}")
        lines.append("")
    return "\n".join(lines)

def render_json(selected, topic=None):
    return json.dumps({"topic": topic or "Mixed", "count": len(selected), "questions": selected}, indent=2)

def save_to_file(content, output_path):
    out = pathlib.Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding='utf-8')
    return out

def main():
    # Expected payload from skill execution (passed via stdin JSON)
    payload = json.load(sys.stdin)
    topic = payload.get('topic')
    count = int(payload.get('count', 5))
    difficulty = payload.get('difficulty')
    fmt = payload.get('format')
    explanations = payload.get('explanations', True)
    base = pathlib.Path(__file__).parent.parent / 'questions'
    qs = load_questions(base)
    filtered = filter_questions(qs, difficulty, fmt, topic)

    # If no format specified, distribute across the three required formats as evenly as possible
    if not fmt and not payload.get('balanced') is False:
        # Group by format
        by_format = {'single_choice': [], 'multi_select': [], 'true_false': [], 'short_answer': []}
        for q in filtered:
            by_format.setdefault(q.get('format', 'single_choice'), []).append(q)
        for v in by_format.values():
            random.shuffle(v)
        # Distribute as evenly as possible across the three required formats
        per_format = max(1, count // 3)
        remainder = count - per_format * 3
        selected = []
        for f in ('single_choice', 'multi_select', 'true_false'):
            selected.extend(by_format.get(f, [])[:per_format])
        # Fill remainder from the format with the most remaining questions
        for f in ('single_choice', 'multi_select', 'true_false'):
            if remainder <= 0:
                break
            already = sum(1 for q in selected if q.get('format') == f)
            remaining = by_format.get(f, [])[already:already + remainder]
            selected.extend(remaining)
            remainder -= len(remaining)
        # If still short, append any leftovers
        if len(selected) < count:
            used_ids = {id(q) for q in selected}
            for q in filtered:
                if id(q) not in used_ids:
                    selected.append(q)
                    if len(selected) >= count:
                        break
        random.shuffle(selected)
        selected = selected[:count]
    else:
        random.shuffle(filtered)
        selected = filtered[:min(count, len(filtered))]

    output_format = payload.get('output_format', 'text')
    save_file = payload.get('save_file', True)
    output_path = payload.get('output_path')

    title = payload.get('title', 'QUALITY QUIZ')
    if output_format == 'json':
        rendered = render_json(selected, topic)
    elif output_format == 'markdown':
        rendered = render_markdown(selected, explanations, topic)
    else:
        rendered = render_text(selected, explanations, title, topic)

    if save_file:
        if not output_path:
            out_dir = pathlib.Path(__file__).parent.parent / 'output'
            out_dir.mkdir(parents=True, exist_ok=True)
            topic_slug = (topic or 'mixed').lower().replace(' ', '_').replace('&', 'and')
            date_str = datetime.date.today().isoformat()
            output_path = out_dir / f"quiz_{topic_slug}_{date_str}.txt"
        saved = save_to_file(rendered, output_path)
        print(f"✅ Saved to: {saved}")
        print()
    print(rendered)

if __name__ == '__main__':
    main()
