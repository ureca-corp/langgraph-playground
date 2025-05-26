import json
from langchain_core.messages import ToolMessage, AIMessage
from src.schemas.chat_state import ChatState
from src.components.tools.search_tool import tavily_search


def search(state: ChatState) -> ChatState:
    search_query = state.search_query
    search_results = tavily_search.invoke({"query": search_query})
    messages = list(state.messages)
    last_message = messages[-1]

    if (
        isinstance(last_message, AIMessage)
        and hasattr(last_message, 'tool_calls')
        and last_message.tool_calls
    ):
        search_content = json.dumps(search_results, ensure_ascii=False)
        valid_results = len(
            list(
                filter(
                    lambda r: "error"
                    not in r, search_results
                )
            )
        )

        for tool_call in last_message.tool_calls:
            tool_message = ToolMessage(
                content=f"""
**Search Query:** {search_query}

**Search Results:**
```json\n{search_content}\n```

Found {valid_results} search results.
                """,
                tool_call_id=tool_call["id"]
            )
            messages.append(tool_message)

    return ChatState(
        messages=messages,
        next="chatbot",
        needs_search=False,
        search_query=search_query,
        search_results=search_results,
        current_step="search_completed"
    )
