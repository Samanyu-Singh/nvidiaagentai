import json
import logging
import os
from typing import Annotated, Any, Sequence

from langchain_core.runnables import RunnableConfig
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic import BaseModel

from . import tools
from .prompts import research_prompt

_LOGGER = logging.getLogger(__name__)
_MAX_LLM_RETRIES = 3

# ──  initialise the LLM ──────────────────────────────────────────────
if not os.getenv("NVIDIA_API_KEY"):
    raise EnvironmentError("NVIDIA_API_KEY not set – cannot start ChatNVIDIA.")

llm = ChatNVIDIA(model="meta/llama-3.3-70b-instruct", temperature=0)
llm_with_tools = llm  #  ← no forced Tavily binding
# If you still want Tavily search, uncomment next line
# llm_with_tools = llm.bind_tools([tools.search_tavily])


class ResearcherState(BaseModel):
    topic: str  # raw ToS text or its summary
    number_of_queries: int = 5  # kept for compatibility
    messages: Annotated[Sequence[Any], add_messages] = []


# ──  tool-execution node  ───────────────────────────────────────────
async def tool_node(state: ResearcherState):
    outputs = []
    if not state.messages:
        return {"messages": outputs}

    last_message = state.messages[-1]
    tool_calls = []

    if isinstance(last_message, dict):
        tool_calls = last_message.get("tool_calls", [])
    else:
        tool_calls = getattr(last_message, "tool_calls", [])

    for call in tool_calls:
        tool = getattr(tools, call["name"])
        result = await tool.ainvoke(call["args"])
        outputs.append(
            {
                "role": "tool",
                "content": json.dumps(result),
                "name": call["name"],
                "tool_call_id": call["id"],
            }
        )
    return {"messages": outputs}


# ──  main model call  ───────────────────────────────────────────────
async def call_model(state: ResearcherState, config: RunnableConfig) -> dict[str, Any]:
    prompt = research_prompt.format(
        topic=state.topic, number_of_queries=state.number_of_queries
    )
    for attempt in range(_MAX_LLM_RETRIES):
        msgs = [{"role": "system", "content": prompt}] + list(state.messages)
        response = await llm_with_tools.ainvoke(msgs, config)
        if response:
            return {"messages": [response]}
    raise RuntimeError(f"LLM failed after {_MAX_LLM_RETRIES} tries.")


def has_tool_calls(state: ResearcherState) -> bool:
    if not state.messages:
        return False
    last_message = state.messages[-1]
    if isinstance(last_message, dict):
        return bool(last_message.get("tool_calls", []))
    return bool(getattr(last_message, "tool_calls", []))


# ──  build graph  ───────────────────────────────────────────────────
workflow = StateGraph(ResearcherState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", has_tool_calls, {True: "tools", False: END})
workflow.add_edge("tools", "agent")
graph = workflow.compile()
