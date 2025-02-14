# tests/evaluator/test_score_evaluator.py

import pytest
from agent_core.evaluator import GenericEvaluator
from agent_core.models import ModelRegistry


@pytest.fixture
def mock_model():
    return ModelRegistry.get_model("gpt-4o-mini")  # or a mock/fake model


@pytest.fixture
def score_evaluator(mock_model):
    return GenericEvaluator(mock_model)


def test_score_evaluator(score_evaluator):
    """Test basic score evaluation result structure."""
    evaluator_result = score_evaluator.evaluate("Say hi", "Hi there!")
    # We can't fully control LLM response, but we can check structure
    assert evaluator_result.decision in ("Accept Output", "Rerun Subtask")
    assert isinstance(evaluator_result.total_score, int) or isinstance(evaluator_result.total_score, float)
    assert "score_breakdown" in evaluator_result.details
    assert "raw_evaluation" in evaluator_result.details


def test_parse_scored_evaluation_response_1(score_evaluator):
    evaluation_response = """
1. **Accuracy (Score 1-5):** 4  
   **Justification:** The output accurately identifies the components of a flower (petals, stem, leaves) and assigns characters to each part. However, it could be more specific about the arrangement of the characters in relation to each other.

2. **Completeness (Score 1-5):** 3  
   **Justification:** While the output includes the necessary components of a flower, it lacks details on how the characters are arranged spatially to form the shape of a flower. More information on the positioning would enhance completeness.

3. **Relevance (Score 1-5):** 5  
   **Justification:** The content is directly relevant to the subtask of arranging characters to form a flower shape. There are no extraneous details.

4. **Coherence and Clarity (Score 1-5):** 4  
   **Justification:** The output is generally clear and logically structured, but the lack of spatial arrangement details makes it slightly less coherent in terms of visualizing the flower shape.

5. **Consistency (Score 1-5):** 5  
   **Justification:** The output is consistent with the requirements of the subtask and does not contradict any previous information.

6. **Following Instructions (Score 1-5):** 4  
   **Justification:** The output follows the instructions well but could improve by providing a more detailed arrangement that visually represents a flower.

7. **Error Analysis (Score 1-5):** 5  
   **Justification:** The output is free from grammatical, factual, and logical errors.

8. **Ethical Compliance (Score 1-5):** 5  
   **Justification:** The content complies with ethical guidelines and does not contain any inappropriate material.

**Total Score:** 35

**Final Recommendation:**  
**Rerun Subtask**  
**Suggestions for Improvement:**  
- Provide a more detailed description of how the characters are arranged spatially to visually represent a flower shape. For example, specify the positioning of the petals around the stem and how the leaves are placed in relation to the stem. This would enhance both completeness and clarity.
   """
    decision, total_score, scores = score_evaluator.parse_scored_evaluation_response(
        evaluation_response
    )
    assert decision in ("Accept Output", "Rerun Subtask")
    assert total_score == 35


def test_parse_scored_evaluation_response_2(score_evaluator):
    evaluation_response = """
1. **Accuracy** (Score 5): The output accurately identifies the components of a flower (petals, stem, leaves) and assigns them to specific computer characters.

2. **Completeness** (Score 5): The output addresses all aspects of the subtask by providing a character for each part of the flower.

3. **Relevance** (Score 5): The content is directly relevant to the subtask, focusing solely on the assignment of characters to flower parts without any extraneous information.

4. **Coherence and Clarity** (Score 5): The output is logically structured and clear, making it easy to understand which characters correspond to which parts of the flower.

5. **Consistency** (Score 5): The output does not contradict itself and maintains consistency in the format used for each flower part.

6. **Following Instructions** (Score 5): The output adheres to the instructions by clearly labeling each part of the flower with the corresponding computer character.

7. **Error Analysis** (Score 5): The output is free from factual, grammatical, and logical errors. The format is correct, and the information is presented accurately.

8. **Ethical Compliance** (Score 5): The content complies with ethical guidelines and policies, as it does not contain any inappropriate or harmful information.

**Total Score: 40**

**Final Recommendation: Accept Output** 

The output meets all criteria effectively, scoring above 35 with no individual criterion below 3.
    """
    decision, total_score, scores = score_evaluator.parse_scored_evaluation_response(
        evaluation_response
    )
    assert decision in ("Accept Output", "Rerun Subtask")
    assert total_score == 40
    assert len(scores) is 8


def test_parse_scored_evaluation_response_3(score_evaluator):
    evaluation_response = """
1. **Accuracy (Score 1-5):** 2  
   **Justification:** The output does not accurately represent a flower's arrangement. The use of "computer character A," "computer character B," and "computer character C" is vague and does not provide a clear depiction of the flower's features.

2. **Completeness (Score 1-5):** 2  
   **Justification:** The output lacks detail about the flower's appearance. While it mentions petals, stem, and leaves, it does not provide any information about their colors, sizes, or arrangement, which are essential for enhancing the flower's appearance.

3. **Relevance (Score 1-5):** 3  
   **Justification:** The output is somewhat relevant as it addresses the flower's arrangement. However, the use of generic terms detracts from its relevance to the specific task of enhancing appearance.

4. **Coherence and Clarity (Score 1-5):** 3  
   **Justification:** The structure of the output is clear, but the use of non-descriptive terms makes it difficult to understand how the flower's appearance is enhanced. More descriptive language would improve clarity.

5. **Consistency (Score 1-5):** 3  
   **Justification:** The output does not contradict previous subtasks, but it does not build on any established standards for flower arrangement, leading to a lack of consistency in quality.

6. **Following Instructions (Score 1-5):** 2  
   **Justification:** The output does not follow the instruction to enhance the flower's appearance effectively. It merely lists components without making any adjustments or improvements.

7. **Error Analysis (Score 1-5):** 3  
   **Justification:** There are no grammatical errors, but the factual representation of the flower is lacking. The use of "computer character" is not appropriate for this context.

8. **Ethical Compliance (Score 1-5):** 5  
   **Justification:** The content does not raise any ethical concerns and complies with guidelines.

**Total Score:** 20

**Final Recommendation:** Rerun Subtask  
**Suggestions for Improvement:**  
- Use descriptive terms for the petals, stem, and leaves, including colors and sizes, to provide a clearer picture of the flower's appearance.
- Consider the arrangement of the components to enhance visual appeal, such as varying the sizes of petals or adding details about their placement.
- Ensure that the output aligns more closely with the task of enhancing the flower's appearance rather than simply listing components.
    """
    decision, total_score, scores = score_evaluator.parse_scored_evaluation_response(
        evaluation_response
    )
    assert decision in ("Accept Output", "Rerun Subtask")
    assert total_score == 23
    assert len(scores) is 8


def test_parse_scored_evaluation_response_4(score_evaluator):
    evaluation_response = """
1. **Accuracy (Score 1-5): 2**
   - **Justification:** The output does not accurately represent a flower's arrangement. The use of "computer character A," "computer character B," and "computer character C" is vague and does not provide a clear depiction of a flower's physical attributes.

2. **Completeness (Score 1-5): 2**
   - **Justification:** The output lacks essential details that would enhance the flower's appearance, such as colors, sizes, or specific arrangements of petals, leaves, and stem. It does not fully address the subtask of enhancing the flower's appearance.

3. **Relevance (Score 1-5): 3**
   - **Justification:** While the output attempts to describe a flower's components, the use of generic terms like "computer character" detracts from its relevance. It does not provide meaningful information about the flower's arrangement.

4. **Coherence and Clarity (Score 1-5): 2**
   - **Justification:** The output is not coherent or clear. The terms used do not convey a clear image or understanding of the flower's arrangement, making it difficult to visualize.

5. **Consistency (Score 1-5): 3**
   - **Justification:** There is no contradiction within the output itself, but it does not align with typical expectations for a flower arrangement, which may lead to confusion about its consistency with prior subtasks.

6. **Following Instructions (Score 1-5): 2**
   - **Justification:** The output does not follow the instructions effectively. It fails to enhance the flower's appearance as requested, instead providing an unclear and unhelpful representation.

7. **Error Analysis (Score 1-5): 3**
   - **Justification:** There are no grammatical errors, but the logical structure is flawed due to the vague terminology used. The output does not convey factual information about flowers.

8. **Ethical Compliance (Score 1-5): 5**
   - **Justification:** The content does not raise any ethical concerns and complies with general guidelines.

**Total Score: 22**

**Final Recommendation: Rerun Subtask**
- **Suggestions for Improvement:**
  - Use specific and descriptive terms to represent the flower's components (e.g., "red petals," "green leaves").
  - Include details about the arrangement, such as the number of petals, their shape, and how they are positioned relative to the stem and leaves.
  - Provide a more vivid description that enhances the visual appeal of the flower.
    """
    decision, total_score, scores = score_evaluator.parse_scored_evaluation_response(
        evaluation_response
    )
    assert decision in ("Accept Output", "Rerun Subtask")
    assert total_score == 22
    assert len(scores) is 8


def test_parse_scored_evaluation_response_5(score_evaluator):
    evaluation_response = """
1. **Accuracy (Score 1-5): 3**
   - **Justification:** The output identifies characters for petals, stem, and leaves, but the choices are not accurate representations of typical flower anatomy. A rose is a flower, but a cactus is not a typical stem for a flower, and while ferns have leaves, they are not commonly associated with flowering plants.

2. **Completeness (Score 1-5): 4**
   - **Justification:** The output includes all three components (petals, stem, leaves) as required by the subtask. However, the choices could be more representative of a typical flower.

3. **Relevance (Score 1-5): 5**
   - **Justification:** The content is directly relevant to the subtask, as it provides specific characters for each part of the flower.

4. **Coherence and Clarity (Score 1-5): 5**
   - **Justification:** The output is clearly structured and easy to understand, with a straightforward format that lists the components.

5. **Consistency (Score 1-5): 4**
   - **Justification:** The output is consistent in its format and approach, but the choice of characters may not align with typical representations in previous subtasks or common knowledge.

6. **Following Instructions (Score 1-5): 5**
   - **Justification:** The output adheres to the instruction of selecting characters for the flower's parts without deviation from the task.

7. **Error Analysis (Score 1-5): 4**
   - **Justification:** There are no grammatical errors, but the factual accuracy regarding the appropriateness of the characters could be improved.

8. **Ethical Compliance (Score 1-5): 5**
   - **Justification:** The content complies with ethical guidelines and does not contain any inappropriate or harmful material.

**Total Score: 35**

**Final Recommendation: Rerun Subtask**
- **Suggestions for Improvement:**
  - Choose characters that are more representative of a flower's anatomy. For example, for petals, consider using "Daisy" or "Lily," for the stem, a "Sunflower" or "Tulip," and for leaves, perhaps "Maple" or "Oak" to better reflect typical flowering plants.
    """
    decision, total_score, scores = score_evaluator.parse_scored_evaluation_response(
        evaluation_response
    )
    assert decision in ("Accept Output", "Rerun Subtask")
    assert total_score == 35
    assert len(scores) is 8


def test_parse_scored_evaluation_response_6(score_evaluator):
    evaluation_response = """
1. **Accuracy (Score 1-5): 2**
   - **Justification:** The output inaccurately assigns characters to the flower's parts. For example, 'Lily' is a type of flower and not a character representing petals, and 'Sunflower' is also a flower, not a stem character. 

2. **Completeness (Score 1-5): 2**
   - **Justification:** The output includes all three components (petals, stem, leaves), but the selections do not fulfill the requirement of representing these parts accurately with appropriate characters.

3. **Relevance (Score 1-5): 3**
   - **Justification:** While the output mentions flower parts, the chosen characters do not align with the task's requirement to select characters that represent these parts. The relevance is somewhat diminished due to incorrect choices.

4. **Coherence and Clarity (Score 1-5): 4**
   - **Justification:** The output is structured clearly, listing the parts of the flower and their corresponding characters. However, the clarity is affected by the inaccuracy of the character choices.

5. **Consistency (Score 1-5): 3**
   - **Justification:** There is no contradiction within the output itself, but it does not align with the expected understanding of what characters should represent flower parts, which could lead to confusion.

6. **Following Instructions (Score 1-5): 2**
   - **Justification:** The output does not follow the instruction to select appropriate characters for the flower's petals, stem, and leaves, as the selections are not suitable.

7. **Error Analysis (Score 1-5): 3**
   - **Justification:** There are no grammatical errors, but the factual errors regarding the representation of flower parts detract from the overall quality of the output.

8. **Ethical Compliance (Score 1-5): 5**
   - **Justification:** The content does not raise any ethical concerns and complies with guidelines.

**Total Score: 22**

**Final Recommendation: Rerun Subtask**
- **Suggestions for Improvement:**
  - Select characters that are more representative of the flower's petals, stem, and leaves. For example, use characters that are commonly associated with these parts in botanical illustrations or educational contexts.
  - Ensure that the characters chosen are not themselves types of flowers, as this creates confusion regarding their representation.
    """
    decision, total_score, scores = score_evaluator.parse_scored_evaluation_response(
        evaluation_response
    )
    assert decision in ("Accept Output", "Rerun Subtask")
    assert total_score == 24
    assert len(scores) is 8


def test_parse_scored_evaluation_response_7(score_evaluator):
    evaluation_response = """
1. **Accuracy (Score 1-5):** 2  
   **Justification:** The output does not accurately fulfill the requirement of selecting an arrangement for the stem of the flower. The chosen characters (🌱🌾) do not represent a typical flower stem.

2. **Completeness (Score 1-5):** 2  
   **Justification:** The output fails to provide a complete representation of a flower stem. It only includes two characters without any additional context or elements that might be necessary for a full arrangement.

3. **Relevance (Score 1-5):** 3  
   **Justification:** While the characters are somewhat relevant to plant life, they do not specifically represent a flower stem, which is the focus of the subtask. 

4. **Coherence and Clarity (Score 1-5):** 3  
   **Justification:** The output is clear in its presentation of characters, but it lacks context or explanation, which could enhance understanding of how these characters relate to the flower stem.

5. **Consistency (Score 1-5):** 3  
   **Justification:** There is no contradiction within the output itself, but it does not align with typical representations of flower stems, which may have been established in previous subtasks.

6. **Following Instructions (Score 1-5):** 2  
   **Justification:** The output does not follow the instruction to select an appropriate arrangement for the stem of the flower, as the characters chosen do not represent a flower stem effectively.

7. **Error Analysis (Score 1-5):** 3  
   **Justification:** There are no grammatical errors, but the factual representation of a flower stem is incorrect, which impacts the overall quality of the output.

8. **Ethical Compliance (Score 1-5):** 5  
   **Justification:** The content is ethically compliant, as it does not contain any inappropriate or harmful material.

**Total Score:** 20

**Final Recommendation:** Rerun Subtask  
**Suggestions for Improvement:**  
- Choose characters that more accurately represent a flower stem, such as 🌹 (rose) or 🌻 (sunflower) for a clearer depiction.
- Provide additional context or a brief description to clarify how the chosen characters relate to the flower stem.
- Ensure that the output aligns with any established conventions from previous subtasks regarding flower representations.
    """
    decision, total_score, scores = score_evaluator.parse_scored_evaluation_response(
        evaluation_response
    )
    assert decision in ("Accept Output", "Rerun Subtask")
    assert total_score == 23
    assert len(scores) is 8


def test_parse_scored_evaluation_response_8(score_evaluator):
    evaluation_response = """
1. **Accuracy (Score 1-5)**: 5  
   **Justification:** The output accurately selects computer emoji characters to represent the body and torso of the dragon as specified in the subtask.

2. **Completeness (Score 1-5)**: 5  
   **Justification:** The output addresses both required components of the subtask: the body and the torso of the dragon.

3. **Relevance (Score 1-5)**: 5  
   **Justification:** The content is directly relevant to the subtask, focusing solely on the specified emoji characters without any extraneous information.

4. **Coherence and Clarity (Score 1-5)**: 5  
   **Justification:** The output is clearly structured, with a straightforward representation of the body and torso using emojis, making it easy to understand.

5. **Consistency (Score 1-5)**: 5  
   **Justification:** The output is consistent with the requirements of the subtask and does not contradict any previous information.

6. **Following Instructions (Score 1-5)**: 5  
   **Justification:** The output adheres to the instructions by providing the specific emoji characters as requested.

7. **Error Analysis (Score 1-5)**: 5  
   **Justification:** The output is free from factual, grammatical, and logical errors. The emoji representation is correct and appropriate.

8. **Ethical Compliance (Score 1-5)**: 5  
   **Justification:** The content complies with ethical guidelines, as it does not contain any inappropriate or harmful material.

**Total Score:** 40

**Final Recommendation:** Accept Output

The total score is above 35, and no criterion scored below 3. The output meets all the requirements effectively.
    """
    decision, total_score, scores = score_evaluator.parse_scored_evaluation_response(
        evaluation_response
    )
    assert decision in ("Accept Output", "Rerun Subtask")
    assert total_score == 40
    assert len(scores) is 8
