import json
from typing import Optional, List
from utils.logger import get_logger
from .base_validator import BaseValidator
from config import Config


class CodingValidator(BaseValidator):
    DEFAULT_PROMPT = """\
You are an expert code reviewer with extensive experience in software engineering and multiple programming languages.
Your task is to evaluate the provided AI-generated code based on the following comprehensive criteria. Note: The provided code may be a complete implementation or just a code fragment. If a particular criterion is not applicable, please mark it as "N/A" and exclude it from the overall scoring.

1. **Requirements Coverage** (Score 1-5 or N/A): Evaluate to what extent the code addresses and fulfills the specified requirements. For a code fragment, consider whether it aligns with or partially implements the requirements.
2. **Correctness** (Score 1-5 or N/A): Assess whether the code implements correct logic and produces the expected outputs based on the provided requirements.
3. **Code Style and Conventions** (Score 1-5 or N/A): Determine if the code follows standard coding conventions and best practices.
4. **Readability and Documentation** (Score 1-5 or N/A): Evaluate how clear and well-documented the code is.
5. **Efficiency and Performance** (Score 1-5 or N/A): Assess whether the code is optimized for performance and resource usage.
6. **Maintainability and Scalability** (Score 1-5 or N/A): Evaluate if the code is structured in a way that makes it easy to maintain and extend, considering potential integration of the fragment.
7. **Security and Robustness** (Score 1-5 or N/A): Assess if the code incorporates proper error handling, security best practices, and robustness against edge cases.
8. **Testability** (Score 1-5 or N/A): Determine if the code is designed to be easily testable or includes testing provisions.

For each criterion, provide:

- **Score (1-5) or N/A**
- **Justification:** A brief explanation for your score or reason for marking it N/A.

At the end, return a JSON object with the following fields, ensuring it is a valid JSON string:

- `decision`: "Accept Code" or "Reject Code"
- `total_applicable_score`: The total score of applicable criteria.
- `average_score`: The average score of applicable criteria.
- `scores`: An array of objects with `criterion`, `score`, and `justification` for each criterion.
- `improvement_suggestions`: A string with improvement suggestions for each criterion that scored below 3.

Ensure the output is only the JSON string, with no additional characters, headers, or formatting.

**Request:**
{request}

**Response:**
{response}

**Evaluation (JSON Format):**
"""

    def __init__(
        self,
        model: Optional[str] = None,
        log_level: Optional[str] = None,
        validation_threshold: Optional[float] = 0.8,  # Average score threshold
    ):
        self.logger = get_logger("coding-validator", log_level)
        if not model:
            model = Config.DEFAULT_MODEL
        self.model = model
        self.validation_threshold = validation_threshold
        self._prompt = self.DEFAULT_PROMPT

    @property
    def prompt(self) -> str:
        """Get or set the evaluation prompt template."""
        return self._prompt

    @prompt.setter
    def prompt(self, value: str):
        self._prompt = value

    def parse_validation_response(self, validation_response: str) -> str:
        """
        Check if the model's response contains 'Accept Code' or 'Reject Code'.
        """
        accept_keywords = ["Accept Code", "accept code"]
        reject_keywords = ["Reject Code", "reject code"]

        if any(keyword in validation_response for keyword in accept_keywords):
            return "Accept Code"
        elif any(keyword in validation_response for keyword in reject_keywords):
            return "Reject Code"
        else:
            return "Undetermined"

    def parse_scored_validation_response(self, validation_response: str):
        """
        Parse the evaluation text to extract scores for each criterion, and calculate the total and average scores.
        For criteria marked as N/A, they are excluded from the score calculation.
        """
        try:
            cleaned_validation_response = validation_response.replace("```json", "").replace("```", "").strip()
            validation_data = json.loads(cleaned_validation_response)
        except json.JSONDecodeError:
            self.logger.error("Unable to parse the model's evaluation response.")
            return "Reject Code", 0, []

        scores = []
        total_score = 0
        applicable_criteria_count = 0

        for item in validation_data["scores"]:
            score_value = item["score"]
            if score_value != "N/A":
                scores.append((item["criterion"], score_value))
                total_score += score_value
                applicable_criteria_count += 1

        if applicable_criteria_count == 0:
            self.logger.warning("No valid criteria were parsed for evaluation.")
            return "Reject Code", 0, scores

        # Check if any criterion scored below 3
        any_low_scores = any(score < 3 for _, score in scores)
        average_score = total_score / applicable_criteria_count

        decision = "Accept Code" if average_score >= (5 * self.validation_threshold) and not any_low_scores else "Reject Code"

        return decision, total_score, scores

    def generate_improvement_suggestions(self, scores: List[tuple]) -> str:
        """
        Generate improvement suggestions based on the scores. For each applicable criterion with a score below 3,
        provide a specific suggestion.
        """
        suggestion_dict = {
            "Requirements Coverage": "Ensure the code fully addresses and implements the requirements.",
            "Correctness": "Review the logic and test the code to verify its correctness.",
            "Code Style and Conventions": "Follow standard coding practices and style guidelines.",
            "Readability and Documentation": "Improve code organization and add meaningful comments and documentation.",
            "Efficiency and Performance": "Optimize algorithms and resource usage for better performance.",
            "Maintainability and Scalability": "Refactor the code to enhance maintainability and facilitate future extensions.",
            "Security and Robustness": "Implement proper error handling and security measures to cover edge cases.",
            "Testability": "Design the code structure to facilitate unit testing and overall verification."
        }

        suggestions = []
        for criterion, score_value in scores:
            if score_value < 3:
                suggestion = suggestion_dict.get(
                    criterion,
                    f"Consider improving {criterion}."
                )
                suggestions.append(f"- {criterion}: {suggestion}")

        if not suggestions:
            suggestions.append(
                "Review the overall implementation to better meet the requirements and quality standards.")

        return "\n".join(suggestions)

    def validate(self, request: str, response: str):
        """
        Evaluate the provided request and generated code response.
        """
        prompt_text = self._prompt.format(request=request, response=response)

        try:
            validation_response = self.model.process(prompt_text)
        except Exception as e:
            self.logger.error("Error during model evaluation: %s", e)
            return (
                "Reject Code",
                0,
                {
                    "score_breakdown": [],
                    "raw_evaluation": "",
                    "improvement_suggestions": "Model evaluation failed. Please try again."
                }
            )

        decision, total_score, scores = self.parse_scored_validation_response(validation_response)

        details = {
            "score_breakdown": scores,
            "raw_evaluation": validation_response,
            "total_applicable_score": total_score
        }

        if decision == "Reject Code":
            improvement_suggestions = self.generate_improvement_suggestions(scores)
            details["improvement_suggestions"] = improvement_suggestions
        else:
            details["improvement_suggestions"] = ""

        return decision, total_score, details
