



from langgraph.graph import StateGraph
from tools import log_interaction, sentiment_tool, suggest_tool
from typing import TypedDict

# ✅ Correct State
class State(TypedDict):
    input: str
    log: str
    sentiment: str
    suggestion: str


# ✅ Nodes (OUTSIDE function)
def log_node(state: State):
    return {
        "log": log_interaction(state["input"])
    }


def sentiment_node(state: State):
    return {
        "sentiment": sentiment_tool(state["input"])
    }


def suggest_node(state: State):
    return {
        "suggestion": suggest_tool(state["input"])
    }


# ✅ Graph Builder
builder = StateGraph(State)

builder.add_node("log", log_node)
builder.add_node("sentiment", sentiment_node)
builder.add_node("suggest", suggest_node)

builder.set_entry_point("log")

builder.add_edge("log", "sentiment")
builder.add_edge("sentiment", "suggest")

builder.set_finish_point("suggest")

graph = builder.compile()


# ✅ Run function
def run_agent(input_text):
    return graph.invoke({
        "input": input_text
    })