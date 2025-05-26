from langchain_core.messages import AIMessage, SystemMessage, ToolMessage
from src.schemas.chat_state import ChatState
from src.utils.config import get_llm
from src.prompt.prompts import WEB_SEARCH_SYSTEM_PROMPT, IF_WEB_SEARCH_NEED_SYSTEM_PROMPT
from src.components.search_tool import tavily_search


def chatbot(state: ChatState) -> ChatState:
    llm = get_llm()
    messages = state.messages
    search_tools = [tavily_search]

    # ToolMessage가 있는지 확인 (검색이 완료된 상태인지 판단)
    has_tool_message = any(
        isinstance(msg, ToolMessage)
        for msg in messages
    )

    if has_tool_message:
        # 검색 결과가 있는 경우: 최종 응답 생성
        messages_with_system = [
            SystemMessage(content=WEB_SEARCH_SYSTEM_PROMPT),
            *messages,
        ]

        response = llm.invoke(messages_with_system)

        return ChatState(
            messages=messages + [response],
            next=None,
            needs_search=False,
            search_query=state.search_query,
            search_results=state.search_results,
            current_step="completed",
        )

    else:
        # 첫 번째 호출: 검색 필요성 판단
        llm_with_tools = llm.bind_tools(search_tools)
        system_prompt = IF_WEB_SEARCH_NEED_SYSTEM_PROMPT

        messages_with_system = [
            SystemMessage(content=system_prompt),
            *messages,
        ]

        # LLM 호출하여 검색 필요성 판단
        response = llm_with_tools.invoke(messages_with_system)

        # AIMessage이고 tool_calls가 있는지 확인
        if (
            isinstance(response, AIMessage)
            and hasattr(response, 'tool_calls')
            and response.tool_calls
        ):
            # 검색이 필요한 경우
            tool_call = response.tool_calls[0]
            search_query = tool_call["args"]["query"]

            return ChatState(
                messages=messages + [response],
                next="search",
                needs_search=True,
                search_query=search_query,
                search_results=None,
                current_step="search_needed"
            )
        else:
            # 검색이 불필요한 경우: 바로 응답
            return ChatState(
                messages=messages + [response],
                next=None,
                needs_search=False,
                search_query=None,
                search_results=None,
                current_step="completed"
            )
