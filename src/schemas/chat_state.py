from typing import Optional, List, Dict, Any
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class ChatState(BaseModel):
    # 메시지는 add_messages reducer를 사용하여 자동 병합
    messages: Annotated[List[BaseMessage], add_messages] = Field(
        default_factory=list,
        description="대화 메시지 목록"
    )

    # 다음 노드 지정
    next: Optional[str] = Field(
        default=None,
        description="다음 노드 지정"
    )

    # 도구 호출이 필요한지 여부
    needs_search: Optional[bool] = Field(
        default=None,
        description="도구 호출이 필요한지 여부"
    )

    # 검색 쿼리
    search_query: Optional[str] = Field(
        default=None,
        description="검색 쿼리"
    )

    # 검색 결과
    search_results: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="검색 결과"
    )

    # 현재 처리 단계
    current_step: Optional[str] = Field(
        default=None,
        description="현재 처리 단계"
    )

    class Config:
        """Pydantic 설정"""
        arbitrary_types_allowed = True  # BaseMessage 등 사용자 정의 타입 허용
