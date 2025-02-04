Given the reference note:
{reference}

Analyze the following target note:
{target_content}

Based on the reference, generate a YAML header with:
- `tags`: A list of relevant keywords.
- `category`: A high-level classification.
- `aliases`: Alternative titles.
- `phase`: The phase of the machine learning workflow.
- `topic`: The specific topic of the note.
- `filename`: The final name of the script.

Output the response strictly as YAML in the following format:

```
---
tags: 
  - {tag1}
  - {tag2}
  - {tag3}
aliases:
category: {category}
phase: {phase}
topic: {topic}
filename: {filename}
---
```
