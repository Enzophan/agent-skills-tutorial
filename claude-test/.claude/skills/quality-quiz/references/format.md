# Output Formats

The quiz supports three required formats and several output renderings.

## The three required quiz formats

1. **single_choice** — one correct option from a list of 3–5 options.
   ```
   What is the primary goal of agile testing? (single_choice)
   A) Find bugs early
   B) Validate requirements
   C) Ensure continuous feedback
   D) All of the above
   Answer: All of the above
   ```

2. **multi_select** — two or more correct options from a list of 4–6 options ("Select all that apply").
   ```
   Which of the following are characteristics of agile testing? (multi_select)
   A) Iterative
   B) Heavy documentation
   C) Continuous feedback
   D) Late testing
   E) Cross-functional teams
   Answer: A, C, E
   ```

3. **true_false** — a statement the test-taker marks True or False.
   ```
   In agile, test automation should be introduced only at the end of the sprint. (true_false)
   Answer: False
   ```

A fourth format, `short_answer`, is also supported for backward compatibility.

## Rendered outputs

### Plain text (default artifact)
Saved to `.claude/skills/quality-quiz/output/quiz_<topic>_<date>.txt`. Always save this file when generating a quiz. Also display the quiz inline in the conversation.

### Markdown
```
### Quality-Quiz: <Topic> (<count> questions)

1️⃣ *<question text>* (single_choice)
   - A) <option A>
   - B) <option B>
   ...
   **Answer:** <correct answer>
   **Explanation:** <explanation (if requested)>
```

### JSON
```json
{
  "topic": "<topic>",
  "count": 5,
  "questions": [
    {
      "id": 1,
      "question": "<question text>",
      "format": "single_choice|multi_select|true_false|short_answer",
      "options": ["A", "B", "C", "D"],
      "answer": "<correct answer>",
      "explanation": "<explanation>"
    }
  ]
}
```

Examples in `examples/Quiz.xlsx` show the Excel export format (via scripts/to_excel.py).
