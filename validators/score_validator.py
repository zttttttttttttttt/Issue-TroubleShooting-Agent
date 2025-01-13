# validators/score_validator.py

import re


class ScoreValidator:

    def __init__(self, model):
        """
        Pass in the agent's model instance (i.e., agent.model)
        so we can call model.process(...) for validation prompts.
        """
        self.model = model

    def create_validator_prompt(self, request, response):
        prompt = f"""
        You are an expert validator of AI-generated outputs. Evaluate the provided subtask output based on the following criteria:

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

        **Subtask Description:**
        {request}

        **Subtask Output:**
        {response}

        **Evaluation:**
        """
        return prompt

    def parse_validation_response(self, validation_response):
        """
        Simple check to see if the model's textual response
        contains 'Accept Output' or 'Rerun Subtask'.
        """
        accept_keywords = ["Accept Output", "accept output"]
        rerun_keywords = ["Rerun Subtask", "rerun subtask"]

        if any(keyword in validation_response for keyword in accept_keywords):
            return "Accept Output"
        elif any(keyword in validation_response for keyword in rerun_keywords):
            return "Rerun Subtask"
        else:
            return "Undetermined"

    def parse_scored_validation_response(self, validation_response):
        """
        Attempts to parse numeric scores from the text and compute a total_score.
        We also check if any single score < 3 triggers a rerun decision.
        """
        scores = []
        total_score = 0

        lines = validation_response.strip().split("\n")
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
            match = match_1 or match_2 or match_3 or match_4

            if match:
                criterion = match.group(1).strip()
                score = int(match.group(2))
                scores.append((criterion, score))
                total_score += score

        # Check if any criterion scored below 3
        any_low_scores = any(score < 3 for _, score in scores)

        # Final decision logic
        if total_score > 35 and not any_low_scores:
            decision = "Accept Output"
        else:
            decision = "Rerun Subtask"

        return decision, total_score, scores

    def validate(self, request, response):
        """
        1) Build a validation prompt from subtask description & output.
        2) Call self.model.process(prompt).
        3) Return the raw textual response.
        """
        prompt = self.create_validator_prompt(request, response)
        validation_response = self.model.process(prompt)  # replaced LLMChat usage
        return validation_response


# Example usage as standalone script:
if __name__ == "__main__":
    from models.model_registry import ModelRegistry

    # For demonstration, get a mock model from your registry
    # (replace "gpt-4o-mini" with whatever is registered in your system)
    mock_model = ModelRegistry.get_model("gpt-4o-mini")

    subtask_description = "Translate the following text into French: 'Hello World.'"
    subtask_output = "Bonjour le monde."

    score_validator = ScoreValidator(mock_model)  # pass the agent's model
    validation_result = score_validator.validate(subtask_description, subtask_output)
    print("Raw Validation Response:\n", validation_result)

    # Parse out final decision and numeric scores
    decision, total_score, scores = score_validator.parse_scored_validation_response(
        validation_result
    )
    print("\nTotal Score:", total_score)
    print("Scores by Criterion:", scores)
    print("Final Decision:", decision)
