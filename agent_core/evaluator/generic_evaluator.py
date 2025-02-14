# evaluator/generic_evaluator.py

import re
from typing import Optional
from .base_evaluator import BaseEvaluator
from .entities.evaluator_result import EvaluatorResult


class GenericEvaluator(BaseEvaluator):
    DEFAULT_PROMPT = """
You are an expert evaluator of AI-generated outputs. Evaluate the provided subtask output based on the following criteria:

1. **Accuracy** (Score 1-5): The output fulfills the requirements of the subtask accurately.
2. **Completeness** (Score 1-5): The output addresses all aspects of the subtask.
3. **Relevance** (Score 1-5): The content is directly relevant to the subtask without extraneous information.
4. **Coherence and Clarity** (Score 1-5): The output is logically structured, clear, and easy to understand.
5. **Consistency** (Score 1-5): The output is consistent with previous subtasks and doesn't contradict itself.
6. **Following Instructions** (Score 1-5): The output adheres to any specific instructions or formats specified.
7. **Error Analysis** (Score 1-5): The output is free from factual, grammatical, and logical errors.
8. **Ethical Compliance** (Score 1-5): The content complies with ethical guidelines and policies.

For each criterion, provide:

- **Score (1-5)**
- **Justification:** A brief explanation for your score.

At the end:

- Calculate the **Total Score**.
- Provide a final recommendation:

- **Accept Output** if the total score is above 35 and no criterion scored below 3.
- **Rerun Subtask** if the total score is 35 or below, or if any criterion scored below 3.

- If recommending a rerun, provide suggestions on how to improve the output.

---

**Context**
{context}

**Subtask Description:**
{request}

**Subtask Output:**
{response}

**Evaluation:**
"""

    def __init__(self, model_name: Optional[str] = None, log_level: Optional[str] = None,
                 evaluation_threshold: Optional[float] = 0.9):
        super().__init__(model_name, log_level, evaluation_threshold)

    def evaluate(self, request, response, context_manager) -> EvaluatorResult:
        """
        Mandatory method from BaseEvaluator. Must return (decision, score, details).
        """
        prompt_text = self.prompt.format(request=request, response=response, context=context_manager.context_to_str())
        evaluation_response = self._model.process(prompt_text)
        decision, total_score, scores = self.parse_scored_evaluation_response(
            evaluation_response
        )
        details = {"score_breakdown": scores, "raw_evaluation": evaluation_response}
        return EvaluatorResult(decision, total_score, details)

    def default_prompt(self):
        return self.DEFAULT_PROMPT

    def parse_scored_evaluation_response(self, evaluation_response):
        """
        Attempts to parse numeric scores from the text and compute a total_score.
        We also check if any single score < 3 triggers a rerun decision.
        """
        scores = []
        total_score = 0

        lines = evaluation_response.strip().split("\n")
        for line in lines:
            # Several regex attempts to capture "Score: <digit>"
            match_1 = re.match(
                r"\d+\.\s\*\*([A-Za-z\s]+)\*\*\s\(Score\s1-5\):\s*Score:\s*(\d)", line
            )
            match_2 = re.match(r"\d+\.\s\*\*([A-Za-z\s]+) \(Score (\d+)\)", line)
            match_3 = re.match(
                r"\d+\.\s+\*\*([A-Za-z\s]+)\s*\(Score:? (\d+)\)\*\*", line
            )
            match_4 = re.match(r"\d+\.\s+\*\*([A-Za-z\s]+)\*\* \(Score (\d+)\):", line)
            match_5 = re.match(r"\*\*([A-Za-z\s]+)\s*\(Score\s1-5\):\s*(\d+)\*\*", line)
            match_6 = re.match(
                r"\d+\.\s+\*\*([A-Za-z\s]+)\s*\(Score\s1-5\):\*\*\s*(\d+)", line
            )
            match_7 = re.match(
                r"\d+\.\s+\*\*([A-Za-z\s]+)\s*\(Score\s1-5\):\s*(\d+)\*\*", line
            )
            match_8 = re.match(
                r"\d+\.\s+\*\*([A-Za-z\s]+)\s*\(Score\s1-5\)\*\*:\s*(\d+)", line
            )
            match_9 = re.match(r"\d+\.\s+\*\*([A-Za-z\s]+)\s*\((\d+)/5\):\*\*", line)
            match_10 = re.match(r"\d+\.\s+\*\*([A-Za-z\s]+)\s*\((\d+)\):\*\*", line)
            match_11 = re.match(
                r"\d+\.\s+\*\*([A-Za-z\s]+)\s*\(Score:\s*(\d+)\):\*\*", line
            )
            match = (
                match_1
                or match_2
                or match_3
                or match_4
                or match_5
                or match_6
                or match_7
                or match_8
                or match_9
                or match_10
                or match_11
            )

            if match:
                criterion = match.group(1).strip()
                score = int(match.group(2))
                scores.append((criterion, score))
                total_score += score

        # Check if any criterion scored below 3
        any_low_scores = any(score < 3 for _, score in scores)

        # Final decision logic
        if float(total_score) / 40.0 > self.evaluation_threshold and not any_low_scores:
            decision = "Accept Output"
        else:
            decision = "Rerun Subtask"

        return decision, total_score, scores