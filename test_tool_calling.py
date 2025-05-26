"""
Tool Calling 메커니즘 테스트 스크립트

이 스크립트는 LLM이 어떻게 도구 호출 여부를 판단하는지 명확히 보여줍니다.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from src.components.search_tool import get_search_tools

load_dotenv()


def test_tool_calling_decision():
    """LLM의 도구 호출 판단 과정을 테스트"""

    # LLM 설정
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    search_tools = get_search_tools()
    llm_with_tools = llm.bind_tools(search_tools)

    # 시스템 프롬프트
    system_prompt = """
You are a helpful AI assistant.

Use the tavily_search tool in the following situations:
1. When real-time news or current information is needed
2. When specific information about companies, people, or events is required
3. When variable information like weather, stocks, or exchange rates is needed
4. When the user explicitly requests a search

For general questions, respond directly without using tools.
"""

    # 테스트 케이스들
    test_cases = [
        "안녕하세요!",                    # 일반 대화 → 도구 호출 안함
        "파이썬 리스트란 무엇인가요?",      # 일반 지식 → 도구 호출 안함
        "삼성전자 주가 알려줘",           # 실시간 정보 → 도구 호출
        "오늘 서울 날씨 어때?",           # 실시간 정보 → 도구 호출
        "최근 AI 뉴스 검색해줘",          # 명시적 검색 요청 → 도구 호출
    ]

    print("🔍 Tool Calling 판단 테스트\n" + "="*50)

    for i, question in enumerate(test_cases, 1):
        print(f"\n{i}. 질문: '{question}'")

        # LLM에 질문
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=question)
        ]

        response = llm_with_tools.invoke(messages)

        # 응답 분석 - AIMessage 타입 체크 추가
        if (
            isinstance(response, AIMessage)
            and hasattr(response, 'tool_calls')
            and response.tool_calls
        ):
            print(f"   📞 도구 호출: YES")
            print(f"   🔧 도구: {response.tool_calls[0]['name']}")
            print(f"   📝 검색어: {response.tool_calls[0]['args']['query']}")
            print(f"   🎯 판단: SEARCH 노드로 이동")
        else:
            print(f"   📞 도구 호출: NO")
            print(f"   💬 일반 응답: {response.content[:100]}...")
            print(f"   🎯 판단: 바로 응답 완료")


def show_actual_response_structure():
    """실제 LLM 응답 구조를 보여줌"""

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    search_tools = get_search_tools()
    llm_with_tools = llm.bind_tools(search_tools)

    print("\n" + "="*50)
    print("🏗️ 실제 LLM 응답 구조")
    print("="*50)

    # 검색이 필요한 질문
    messages = [
        SystemMessage(
            content="Use tavily_search tool when real-time information is needed."),
        HumanMessage(content="삼성전자 주가 알려줘")
    ]

    response = llm_with_tools.invoke(messages)

    print(f"\n📋 응답 타입: {type(response)}")
    print(f"📋 응답 클래스: {response.__class__.__name__}")
    print(f"📋 콘텐츠: '{response.content}'")

    # AIMessage 타입 체크 후 tool_calls 확인
    has_tool_calls = (
        isinstance(response, AIMessage)
        and hasattr(response, 'tool_calls')
        and response.tool_calls
    )
    print(f"📋 도구 호출 있음: {has_tool_calls}")

    if has_tool_calls and isinstance(response, AIMessage):
        print(f"\n🔧 Tool Calls 구조:")
        for i, tool_call in enumerate(response.tool_calls):
            print(f"   [{i}] ID: {tool_call['id']}")
            print(f"   [{i}] 이름: {tool_call['name']}")
            print(f"   [{i}] 인수: {tool_call['args']}")

    print(f"\n🎯 결론: 이 응답은 {'도구 호출' if has_tool_calls else '일반 텍스트'}입니다!")


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY 환경 변수가 필요합니다.")
        exit(1)

    test_tool_calling_decision()
    show_actual_response_structure()
