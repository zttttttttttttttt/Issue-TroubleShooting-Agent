class EvaluatorResult:

    def __init__(self, decision: str, score: int | float, details):
        """
        decision: "Accept Output" or "Rerun Subtask"
        score: a numeric measure of quality
        details: optional extra data, e.g., breakdown of scores
        """
        self.decision = decision
        self.score = score
        self.details = details