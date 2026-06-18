---
name: quality-quiz
description: |
  Provides a list of questions and answers about Software Quality Processes, Software Development Processes, Agile Testing, Agile Methodology, Manual testing, Automation Testing, and related topics. Use this skill whenever a user asks for a quiz, test questions, or practice items on software quality or development processes—whether they request a specific number of questions, a particular difficulty level, or a format (multiple‑choice, true/false, or short answer). Even if the request is vague (e.g., "test my knowledge of testing"), default to a concise 5‑question quiz covering the requested domain. Also trigger when users mention studying for ISTQB, preparing for QA interviews, or reviewing software testing concepts—this skill is the go-to for any software quality or testing knowledge check, not just explicit "quiz" requests.

metadata:
  version: "1.2"
  last_updated: "2026-06-18"
---

## Overview
This skill generates practice quizzes for learning and assessing knowledge of software quality and development concepts. It supports:
- **Topic** — `Agile Testing`, `Manual Testing`, `Automation Testing`, `Software Quality`, `Software Development Processes`
- **Count** — 1–20 questions (default: 5)
- **Difficulty** — `easy`, `medium`, `hard` (default: `medium`)
- **Format** — `multiple_choice`, `true_false`, `short_answer`, `json`, `text` (default: `multiple_choice`)
- **Explanations** — include answer explanations (default: yes)

## Default output path
When saving quiz output to a file (e.g., text export, JSON export), use the following default directory:
```
/home/hiennhan/Desktop/agent-skills-tutorial/claude-test/.claude/skills/quality-quiz/output/
```

## Usage
When the skill is invoked, follow these steps:

1. **Parse the request** — extract `topic`, `count`, `difficulty`, `format`, and whether `explanations` are wanted.
   - If no topic is specified but the user mentions a related concept (e.g., "test automation"), infer the closest matching topic.
   - If no count is given, default to **5**.
   - If no difficulty is given, default to **mixed** (pull from all levels).
   - If the user is vague (e.g., "quiz me on testing"), pick a topic and give them a 5-question multiple-choice quiz.

2. **Select questions** — questions live in the `questions/` directory as YAML files. Each question has `topic`, `difficulty`, `format`, `question`, `options`, `answer`, and `explanation` fields. Filter by the requested criteria, then randomly sample the requested number.

3. **Render output** — use the requested output format:
   - **Markdown** (default): numbered questions with emoji counters, options lettered A-D, answer and explanation on separate lines.
   - **JSON**: structured JSON with topic and questions array.
   - **Plain text**: use `scripts/to_text.py` for full bank export, or format inline for single quizzes.

4. **Save to file** — when the user wants a file, save it to the default output path with a descriptive filename (e.g., `quiz_agile_testing_2026-06-18.txt`).

### Output example (markdown)
```
### Quality-Quiz: Agile Testing (5 questions)

1️⃣ *What is the primary goal of agile testing?*
   - A) Find bugs early
   - B) Validate requirements
   - C) Ensure continuous feedback
   - D) All of the above
   **Answer:** D) All of the above
   **Explanation:** Agile testing aims for early defect detection and continuous feedback throughout development.
```

## Scripts
The skill ships with helper scripts under `scripts/`:

| Script | Purpose | Usage |
|--------|---------|-------|
| `render.py` | Renders quizzes from YAML bank to markdown/JSON (stdin JSON payload) | `echo '{"topic":"Agile Testing","count":5}' \| python render.py` |
| `to_text.py` | Exports full question bank to plain text | `python to_text.py <questions_folder> <output_file>` |
| `to_excel.py` | Exports full question bank to Excel (.xlsx) | `python to_excel.py <questions_folder> <output_folder>` |

Use these scripts directly when the user wants to export the entire question bank rather than generating a custom quiz.

## Question Bank
Topics and their files:

| Topic | File | Questions |
|-------|------|-----------|
| Agile Testing | `questions/agile_testing.yml` | 4 |
| Manual Testing | `questions/manual_testing.yml` | 3 |
| Automation Testing | `questions/automation_testing.yml` | 3 |
| Software Quality | `questions/software_quality.yml` | 5 |
| Software Development Processes | `questions/software_development_processes.yml` | 5 |

### Question format
```yaml
- id: 1
  topic: Agile Testing
  difficulty: easy
  format: multiple_choice
  question: "What is the primary goal of agile testing?"
  options: ["Find bugs early", "Validate requirements", "Ensure continuous feedback", "All of the above"]
  answer: "All of the above"
  explanation: "Agile testing aims for early defect detection and continuous feedback throughout development."
```

## Implementation notes
- When generating quizzes from the YAML bank, use `scripts/render.py` for consistent formatting.
- For JSON output, always include the `topic`, `difficulty`, and `questions` array in the root object.
- For plain-text file exports, default to the output path defined above.
- If the requested topic has fewer questions than requested, use all available questions and note it to the user.

## Evals
Test prompts are in `evals/evals.json`. Run them to verify skill behavior after changes.
