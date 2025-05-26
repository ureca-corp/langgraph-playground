from typing import Literal
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from src.schemas.chat_state import ChatState
from src.components.chat_node import chatbot
from src.components.search_node import search
from langgraph.graph import START, END
from langgraph.checkpoint.memory import MemorySaver


def should_search(state: ChatState) -> Literal["search", "__end__"]:
    if state.needs_search:
        return "search"
    else:
        return "__end__"


def create_chat_graph() -> CompiledStateGraph:
    workflow = StateGraph(ChatState)
    memory = MemorySaver()

    workflow.add_node("chatbot", chatbot)
    workflow.add_node("search", search)

    workflow.add_edge(START, "chatbot")

    workflow.add_conditional_edges(
        "chatbot",
        should_search,
        {
            "search": "search",
            "__end__": END
        }
    )

    workflow.add_edge("search", "chatbot")
    workflow.add_edge("chatbot", END)

    return workflow.compile(checkpointer=memory)
