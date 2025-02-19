import sys
import os

# Add the parent directory to sys.path to allow imports from the framework
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from agent_core.agents import Agent
from agent_core.planners import GenericPlanner
from agent_core.planners import GraphPlanner
from langchain_core.tools import tool
from typing import Annotated, List
import IssueTroubleShootingSummary


@tool("metric")
def get_metric(
        component_name: Annotated[str, "component name"],
        start_time: Annotated[int, "start time"],
        end_time: Annotated[int, "end time"],
) -> List:
    """Get metric data from prometheus by component name"""
    return [
        {"component": "Client maintain system", "name": "CPU Usage",
         "desc": "the cpu usage of the component, unit is %", "data": [[123456789, 90], [123456789, 89]]},
        {"component": "Client maintain system", "name": "Memory Usage",
         "desc": "the memory usage of the database, unit is %", "data": [[123456789, 60], [123456789, 61]]},
    ]


@tool("log")
def get_log(
        component_name: Annotated[str, "component name"],
        start_time: Annotated[int, "start time"],
        end_time: Annotated[int, "end time"],
) -> dict:
    """Get log from kibana by component name and event id"""
    return {
        "trace_id": "123456-123456-123456", "component": "IE", "log": "504 Gateway Timeout for view commodity details",
        "trace_id": "123457-123457-123457", "component": "IE", "log": "504 Gateway Timeout for view commodity details"
    }


@tool("trace")
def get_trace(trace_id: Annotated[str, "trace id"]) -> List:
    """Get trace data from jaeger by trace id"""
    return [
        {
            "traceId": "123456-123456-123456",
            "process": "select * from commodities where id = 999",
        },
        {
            "traceId": "123457-123457-123457",
            "process": "select * from commodities where id = 1000",
        }
    ]


@tool("increase pod")
def increase_pod(pod_num: Annotated[int, "pod amount"]) -> List:
    """The tool that could be used to implement resolution you recommended :Increase pods number in Kubernetes"""
    return [
        {
            "podReplicas": 2
        }
    ]


def main():
    agent = Agent(model_name="gemini-1.5-flash-002")
    agent.tools = [get_metric, get_log, get_trace]

    agent.knowledge = """\
    You are expert at issue trouble shooting. 
    You understand user query with knowledge to determine issue context, then give out detailed trouble shooting plans and execute plans with tools,
    then you provide summary report including issue descript, root cause cause and solution advise
    finally you could use tool to do action with best recommended solution
    """

    agent.background = """\
    FIN is a web application deployed on Kubernetes that serves as the backend for an e-commerce platform.
    The traffic to FIN may increase significantly during shopping festival.
    The current deployment has 1 pod.
    """

    agent.planner = GraphPlanner()

    task = "Many users report experiencing extremely slowness in FIN specially in Black Friday"
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
