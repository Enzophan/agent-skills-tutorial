import yaml, json, random, sys, pathlib

def load_questions(topic_path):
    questions = []
    for file in pathlib.Path(topic_path).glob('*.yml'):
        data = yaml.safe_load(file.read_text())
        if data:
            questions.extend(data)
    return questions

def filter_questions(qs, difficulty=None, fmt=None):
    if difficulty:
        qs = [q for q in qs if q.get('difficulty') == difficulty]
    if fmt:
        qs = [q for q in qs if q.get('format') == fmt]
    return qs

def render_markdown(selected, include_explanations=True):
    lines = []
    for i, q in enumerate(selected, 1):
        lines.append(f"{i}️⃣ *{q['question']}*")
        if q['format'] == 'multiple_choice':
            for idx, opt in enumerate(q.get('options', []), 1):
                lines.append(f"   - {chr(64+idx)}) {opt}")
        lines.append(f"**Answer:** {q['answer']}")
        if include_explanations:
            lines.append(f"**Explanation:** {q.get('explanation','')}")
        lines.append("")
    return "\n".join(lines)

def render_json(selected):
    return json.dumps({"questions": selected}, indent=2)

def main():
    # Expected env vars from skill execution (passed via stdin JSON)
    payload = json.load(sys.stdin)
    topic = payload.get('topic')
    count = int(payload.get('count', 5))
    difficulty = payload.get('difficulty')
    fmt = payload.get('format')
    explanations = payload.get('explanations', True)
    base = pathlib.Path(__file__).parent.parent / 'questions'
    qs = load_questions(base)
    if topic:
        topic_key = topic.lower().replace(' ', '_')
        qs = [q for q in qs if q.get('topic', '').lower().replace(' ', '_') == topic_key]
    filtered = filter_questions(qs, difficulty, fmt)
    random.shuffle(filtered)
    selected = filtered[:min(count, len(filtered))]
    output_format = payload.get('output_format', 'markdown')
    if output_format == 'json':
        print(render_json(selected))
    else:
        print(render_markdown(selected, explanations))

if __name__ == '__main__':
    main()
