# examples/example14.py

import sys
import os

# Add the parent directory to sys.path to allow imports from the framework
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from agent_core.agents import Agent
from agent_core.planners import GraphPlanner
from langchain_core.tools import tool
from typing import Annotated, List
from agent_core.utils.logger import get_logger

from openai import OpenAI

logger = get_logger("example13", "DEBUG")


@tool("financial_news")
def get_financial_news(query: Annotated[str, "keyword search query"],
                       output_cols:Annotated[List[str],"output column names"]) -> List[dict]:
    """Get Financial News. Columns: ['title', 'content', 'date']"""
    logger.info(f"financial_news.Query: {query}, Output Columns: {output_cols}")

    mock_news_corpus=[
        {"title": "Apple Inc. (AAPL) stock price", "content": "Apple Inc. (AAPL) stock price increased by 2% today", "date": "2022-01-01"},
        {"title": "Tesla Inc. (TSLA) stock price", "content": "Tesla Inc. (TSLA) stock price decreased by 1% today", "date": "2022-01-01"},
        {"title": "Amazon.com Inc. (AMZN) stock price", "content": "Amazon.com Inc. (AMZN) stock price increased by 3% today", "date": "2022-01-01"},
    ]

    results=[]
    for news in mock_news_corpus:
        if query.lower() in news["content"].lower():
            results.append(news)

    output=[{col:news.get(col) for col in output_cols} for news in results]

    return output

@tool("policy")
def get_policy_data(query: Annotated[str, "keyword search query"],
                   output_cols:Annotated[List[str],"output column names"]) -> List[dict]:
    """Get ALL Policy data. Columns: ['title', 'pdf_content', 'date']"""
    logger.info(f"policy.Query: {query}, Output Columns: {output_cols}")

    mock_policy_list=[
        {"title": "Security Policy", "pdf_content": "This is the content of policy 1", "date": "2022-01-01"},
        {"title": "Employee Policy", "pdf_content": "This is the content of policy not related to risk", "date": "2022-01-02"},
        {"title": "Risk Management Policy", "pdf_content": "This is the content of policy related to risk", "date": "2022-01-03"},
        {"title": "Not Risk Management Policy", "pdf_content": "The content is about governance", "date": "2022-01-04"}

    ]

    results=[]
    for news in mock_policy_list:
        if query.lower() in news["title"].lower():
            results.append(news)

    output=[{col:policy.get(col) for col in output_cols} for policy in results]

    return output


def main():
    agent = Agent()

    agent.tools = [get_financial_news, get_policy_data]
    agent.planner = GraphPlanner()
    # agent.enable_evaluators()

    # not working
    # task = "what is the stock price of apple"

    # not working if enable evaluators, as the tool will return with result not fully correct.
    # modify evaluation prompt?
    task = "list all policy name related to risk management" 

    response1 = agent.execute(task)
    print(response1)

    # for multi-turn what context should be removed? self._execution_history?
    follow_up_task="what is the create time of this policy"
    response2 = agent.execute(follow_up_task)
    print(response2)

    execution_history = agent.execution_history
    print(f"Execution History: {execution_history}")
    execution_result = agent.get_execution_result_summary()
    print(f"Execution Result: {execution_result}")


if __name__ == "__main__":
    main()
