from .base_model import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


class GPT4OMiniModel(BaseModel):
    def __init__(self):
        super().__init__(name="gpt-4o-mini")
        self.model_instance = ChatOpenAI(
            model="gpt-4o-mini", temperature=0.1, verbose=True
        )

    def process(self, request: str) -> str:
        messages = [
            HumanMessage(request),
        ]
        response = self.model_instance.invoke(messages)
        return response
