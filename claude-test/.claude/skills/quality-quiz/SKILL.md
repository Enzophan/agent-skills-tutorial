---
name: quality-quiz
description: |
  Provides a list of questions and answers about Software Quality Processes, Software Development Processes, Agile Testing, Agile Methodology, Agile QA, Manual Testing, Automation Testing, Security Testing, Performance Testing, API Testing, DevOps & CI/CD, Emerging Technologies, and related topics. Use this skill whenever a user asks for a quiz, test questions, or practice items on software quality or development processes—whether they request a specific number of questions, a particular difficulty level, or a format (single‑choice, multi‑select, or true/false). Even if the request is vague (e.g., "test my knowledge of testing"), default to a concise 5‑question quiz covering the requested domain. Also trigger when users mention studying for ISTQB, preparing for QA interviews, or reviewing software testing concepts—this skill is the go-to for any software quality or testing knowledge check, not just explicit "quiz" requests.

metadata:
  version: "2.0"
  last_updated: "2026-07-04"
---

## Overview
This skill generates practice quizzes for learning and assessing knowledge of software quality, testing, and development concepts. It supports:
- **Topic** — `Agile Testing`, `Agile QA`, `Manual Testing`, `Automation Testing`, `Security Testing`, `Performance Testing`, `API Testing`, `DevOps & CI/CD`, `Software Quality`, `Software Development Processes`, `Emerging Technologies` (default: all topics, mixed)
- **Count** — 1–20 questions (default: 5)
- **Difficulty** — `easy`, `medium`, `hard` (default: `medium`, mixed across levels when not specified)
- **Format** — three required formats: `single_choice` (one correct option), `multi_select` (multiple correct options), `true_false` (default: mixed across all three)
- **Explanations** — include answer explanations (default: yes)

## Three required quiz format types
Every quiz must include questions in these three formats (mixed by default):

1. **single_choice** — one correct option from a list of 3–5 options (also called "multiple‑choice" with a single answer).
   ```yaml
   format: single_choice
   question: "Which tool is commonly used for UI automation?"
   options: ["Selenium", "Docker", "Git", "Jenkins"]
   answer: "Selenium"
   ```
2. **multi_select** — two or more correct options from a list of 4–6 options (also called "multiple options" / "multiple answer").
   ```yaml
   format: multi_select
   question: "Which of the following are characteristics of agile testing? (Select all that apply)"
   options: ["Iterative", "Heavy documentation", "Continuous feedback", "Late testing", "Cross‑functional teams"]
   answer: ["Iterative", "Continuous feedback", "Cross‑functional teams"]
   ```
3. **true_false** — a statement that the test‑taker marks True or False.
   ```yaml
   format: true_false
   question: "Automated tests require no maintenance once written."
   answer: false
   ```

When the user requests a specific format, honor that request. When the user does not specify a format, distribute questions across all three formats as evenly as possible (e.g., a 5‑question quiz → ~2 single_choice, ~2 multi_select, ~1 true_false).

## Default output behavior
**Always save the generated quiz to a text file** at the default output path:
```
/home/hiennhan/Desktop/agent-skills-tutorial/claude-test/.claude/skills/quality-quiz/output/
```
Use a descriptive filename like `quiz_<topic>_<YYYY-MM-DD>.txt`. After saving, also show the quiz inline in the conversation for the user to read immediately. This applies whether the user explicitly asks for a file or not — the text file is the default artifact.

## Default output path
```
/home/hiennhan/Desktop/agent-skills-tutorial/claude-test/.claude/skills/quality-quiz/output/
```

## Usage
When the skill is invoked, follow these steps:

1. **Parse the request** — extract `topic`, `count`, `difficulty`, `format`, and whether `explanations` are wanted.
   - If no topic is specified but the user mentions a related concept (e.g., "test automation"), infer the closest matching topic from the supported list.
   - If no count is given, default to **5**.
   - If no difficulty is given, default to **mixed** (pull from all levels).
   - If the user is vague (e.g., "quiz me on testing"), pick a topic and give them a 5‑question quiz mixing the three required formats.

2. **Select questions** — questions live in the `questions/` directory as YAML files, one file per topic. Each question has `topic`, `difficulty`, `format`, `question`, `options` (for single/multi), `answer`, and `explanation` fields. Filter by the requested criteria, then randomly sample the requested number, ensuring balanced coverage of the three required formats when no specific format is requested.

3. **Render output** — produce the quiz using one of these formats:
   - **Plain text** (default and primary artifact): numbered questions, options lettered A‑D (or A‑F for multi_select), answer and explanation on separate lines. Save to a `.txt` file in the default output directory.
   - **Markdown**: numbered questions with emoji counters, options lettered A‑F, answer and explanation on separate lines.
   - **JSON**: structured JSON with topic, format, and questions array.

4. **Save to file** — always save the generated quiz as a `.txt` file in the default output directory. Use a descriptive filename (e.g., `quiz_agile_qa_2026-07-04.txt`). Also display the quiz inline in the response.

### Output example (plain text — default)
```
QUALITY QUIZ: Agile Testing (5 questions)
Generated: 2026-07-04

1. What is the primary goal of agile testing? (single_choice)
   A) Find bugs early
   B) Validate requirements
   C) Ensure continuous feedback
   D) All of the above
   Answer: All of the above
   Explanation: Agile testing aims for early defect detection and continuous feedback throughout development.

2. Which of the following are characteristics of agile testing? (multi_select)
   A) Iterative
   B) Heavy documentation
   C) Continuous feedback
   D) Late testing
   E) Cross‑functional teams
   Answer: A, C, E
   Explanation: Agile testing emphasizes iterative cycles, continuous feedback, and cross‑functional collaboration — not heavy documentation or late testing.

3. In agile, test automation should be introduced only at the end of the sprint. (true_false)
   Answer: False
   Explanation: Automation is built incrementally throughout the sprint.
```

## Scripts
The skill ships with helper scripts under `scripts/`:

| Script | Purpose | Usage |
|--------|---------|-------|
| `render.py` | Renders quizzes from YAML bank to markdown/JSON/text (stdin JSON payload) | `echo '{"topic":"Agile Testing","count":5}' \| python render.py` |
| `to_text.py` | Exports full question bank to plain text | `python to_text.py <questions_folder> <output_file>` |
| `to_excel.py` | Exports full question bank to Excel (.xlsx) | `python to_excel.py <questions_folder> <output_folder>` |

Use these scripts directly when the user wants to export the entire question bank rather than generating a custom quiz.

## Question Bank
Topics and their files:

| Topic | File | Questions |
|-------|------|-----------|
| Agile Testing | `questions/agile_testing.yml` | 4 |
| Agile QA | `questions/agile_qa.yml` | 5 |
| Manual Testing | `questions/manual_testing.yml` | 3 |
| Automation Testing | `questions/automation_testing.yml` | 3 |
| Security Testing | `questions/security_testing.yml` | 5 |
| Performance Testing | `questions/performance_testing.yml` | 5 |
| API Testing | `questions/api_testing.yml` | 5 |
| DevOps & CI/CD | `questions/devops_cicd.yml` | 5 |
| Software Quality | `questions/software_quality.yml` | 5 |
| Software Development Processes | `questions/software_development_processes.yml` | 5 |
| Emerging Technologies | `questions/emerging_technologies.yml` | 5 |

### Question format
```yaml
- id: 1
  topic: Agile Testing
  difficulty: easy
  format: single_choice
  question: "What is the primary goal of agile testing?"
  options: ["Find bugs early", "Validate requirements", "Ensure continuous feedback", "All of the above"]
  answer: "All of the above"
  explanation: "Agile testing aims for early defect detection and continuous feedback throughout development."

- id: 2
  topic: Agile QA
  difficulty: medium
  format: multi_select
  question: "Which of the following are common responsibilities of a QA in an agile team? (Select all that apply)"
  options: ["Writing test cases", "Defining acceptance criteria", "Sprint planning", "Production deployment only", "Defect triage"]
  answer: ["Writing test cases", "Defining acceptance criteria", "Sprint planning", "Defect triage"]
  explanation: "Agile QAs are embedded in the team and contribute to test design, acceptance criteria, planning, and triage — not just deployment."

- id: 3
  topic: Security Testing
  difficulty: easy
  format: true_false
  question: "SQL injection is an example of a security vulnerability."
  answer: true
  explanation: "SQL injection allows attackers to manipulate database queries through unsanitized input."
```

## Implementation notes
- Every question bank file should include questions in all three required formats (single_choice, multi_select, true_false) so mixed‑format quizzes always have something to draw from.
- When generating quizzes from the YAML bank, use `scripts/render.py` for consistent formatting, or render inline when answering in conversation.
- The default output is a plain `.txt` file in `output/`. Save the file AND display the quiz inline.
- For JSON output, always include the `topic`, `difficulty`, and `questions` array in the root object.
- For plain-text file exports, default to the output path defined above.
- If the requested topic has fewer questions than requested, use all available questions and note it to the user.
- If the user requests a specific format (e.g., "all true/false"), filter strictly to that format.
- If the user doesn't request a specific format, distribute across the three required formats as evenly as possible.

## Evals
Test prompts are in `evals/evals.json`. Run them to verify skill behavior after changes.
