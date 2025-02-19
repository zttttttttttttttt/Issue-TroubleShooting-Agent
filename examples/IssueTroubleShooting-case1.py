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
import IssueTroubleShootingSummary


@tool("metric")
def get_metric(
        metric_name: Annotated[str, "metric  name"],
        start_time: Annotated[int, "start time"],
        end_time: Annotated[int, "end time"],
) -> List:
    """Get metric data from prometheus by component name"""
    return [
        {"metric_name": "CPU Usage",
         "desc": "the cpu usage of the component, unit is %", "data": [[123456789, 95], [123456789, 95]]},

        {"metric_name": "Memory Usage",
         "desc": "the memory usage of the database, unit is %", "data": [[123456789, 80], [123456789, 81]]}
    ]


@tool("log")
def get_log(
        component_name: Annotated[str, "component name"],
        start_time: Annotated[int, "start time"],
        end_time: Annotated[int, "end time"],
) -> dict:
    """Get log from kibana by component name"""
    return {"trace_id": "123456-123456-123456", "component": "client maintain system","log": "sql execute time longer than 30s"}


@tool("trace")
def get_trace(trace_id: Annotated[str, "trace id"]) -> List:
    """Get trace data from jaeger by trace id"""
    return [
        {
            "traceId": "123456-123456-123456",
            "process": "sql execute failed, select * from ClientInfo.table where client_name like '%z%'",
        }
    ]


def main():
    agent = Agent(model_name="gemini-1.5-flash-002")
    agent.tools = [get_metric, get_log, get_trace]

    agent.knowledge = """\
    You are expert at issue trouble shooting. 
    You understand user query with knowledge to determine issue context, 
    then give out detailed trouble shooting plans and execute plans with tools,
    finally you provide summary report including issue descript, root cause cause and solution advise
    """

    agent.background = """\
    The client maintain system provides functions for traders to view clients' information and their intentions of finical products.
    In client's profile page, traders can view the latest info of clients based on resultful apis.
    Billion Client info are stored in Database where client id are indexed but client name is not indexed. 
    """

    agent.planner = GraphPlanner()

    task = "I cannot open client's profile page in client maintain system from 3:00 AM, I cannot see the latest info of clients. Pls give me the root cause"
    agent.execute(task)

    # add summary_prompt
    agent.summary_prompt = IssueTroubleShootingSummary.ISSUE_TROUBLESHOOT_PROMPT

    execution_history = agent.execution_history
    print(f"Execution History: {execution_history}")
    print("\n")
    print(f"Response: {agent.execution_responses}")
    execution_result = agent.get_execution_result_summary()
    print("\n")
    print(f"Execution Summary: {execution_result}")


if __name__ == "__main__":
    main()
