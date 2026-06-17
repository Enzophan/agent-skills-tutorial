# Output Formats

The quiz can be rendered in three formats:

## Markdown (default)
```
### Quality-Quiz: <Topic> (<count> questions)

1️⃣ *<question text>*
   - A) <option A>
   - B) <option B>
   - C) <option C>
   - D) <option D>
   **Answer:** <correct answer>
   **Explanation:** <explanation (if requested)>

2️⃣ *<true/false question>*
   **Answer:** True/False
   **Explanation:** <explanation>
```

## JSON (if format: json requested)
```json
{
  "topic": "<topic>",
  "difficulty": "<easy|medium|hard>",
  "questions": [
    {
      "id": 1,
      "question": "<question text>",
      "format": "multiple_choice|true_false|short_answer",
      "options": ["A", "B", "C", "D"],
      "answer": "<correct answer>",
      "explanation": "<explanation>"
    }
  ]
}
```

## Plain text (via scripts/to_text.py)
Exports the full question bank to a plain-text file. Each question is numbered with its question text, options (if applicable), answer, and explanation.

Examples in `examples/Quiz.xlsx` show the Excel export format (via scripts/to_excel.py).
