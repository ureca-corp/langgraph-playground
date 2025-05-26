# LangGraph 스마트 챗봇 with Tavily Search

이 프로젝트는 LangGraph를 사용하여 **웹 검색 기능이 통합된 스마트 챗봇**을 구현한 예제입니다. 
챗봇이 질문을 분석하여 최신 정보가 필요하다고 판단하면 자동으로 Tavily Search를 사용해 웹에서 정보를 검색하고, 그 결과를 바탕으로 답변을 생성합니다.

## 🚀 주요 기능

### ✨ 스마트 검색 판단
- **자동 검색 판단**: LLM이 질문을 분석하여 웹 검색이 필요한지 자동으로 결정
- **조건부 라우팅**: 검색이 필요한 경우에만 검색 노드로 분기
- **실시간 정보**: 최신 뉴스, 날씨, 주식, 환율 등 실시간 정보 제공

### 🔍 검색이 실행되는 경우
1. 최신 뉴스나 실시간 정보가 필요한 경우
2. 특정 회사, 인물, 사건에 대한 구체적인 정보가 필요한 경우  
3. 날씨, 주식, 환율 등 변동하는 정보가 필요한 경우
4. 사용자가 명시적으로 "검색해줘", "찾아봐줘" 등을 요청한 경우

### 💬 일반 대화
검색이 필요하지 않은 일반적인 질문이나 대화는 바로 답변을 생성합니다.

## 🏗️ 개선된 그래프 구조

```
START -> ChatBot -> (조건부 분기)
                 -> 검색 필요시: Search -> ChatBot -> END
                 -> 검색 불필요시: END
```

### 그래프 플로우 설명
1. **START**: 사용자 입력으로 시작
2. **ChatBot**: 질문 분석 및 검색 필요성 판단
3. **조건부 분기**:
   - 검색 필요 → Search 노드로 이동
   - 검색 불필요 → 바로 답변 생성 후 종료
4. **Search**: Tavily API로 웹 검색 실행
5. **ChatBot (재방문)**: 검색 결과를 활용하여 최종 답변 생성
6. **END**: 대화 완료

## 📦 설치 방법

### 1. 의존성 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

다음 환경 변수들을 설정해야 합니다:

```bash
# 필수: OpenAI API 키 (챗봇용)
export OPENAI_API_KEY=your-openai-api-key-here

# 필수: Tavily API 키 (웹 검색용)
export TAVILY_API_KEY=your-tavily-api-key-here

# 선택: LangSmith 추적 (디버깅용)
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_PROJECT=langgraph-chatbot-with-search
export LANGCHAIN_API_KEY=your-langsmith-api-key-here
```

#### API 키 발급 방법
- **OpenAI API**: [OpenAI Platform](https://platform.openai.com/api-keys)에서 발급
- **Tavily API**: [Tavily](https://tavily.com/)에서 무료 계정 생성 후 발급

## 🎯 실행 방법

```bash
python main.py
```

실행 후 터미널에서 다음과 같은 대화를 시도해보세요:

### 📝 예시 대화

**검색이 필요한 질문들:**
- "오늘 삼성전자 주가 어떻게 됐어?"
- "최근 AI 관련 뉴스 찾아줘"
- "서울 날씨 알려줘"
- "비트코인 현재 가격 검색해줘"

**일반 대화:**
- "안녕하세요!"
- "파이썬에서 리스트와 튜플의 차이점은?"
- "좋은 하루 보내세요"

## 🔧 코드 구조

### 📁 프로젝트 구조
```
src/
├── components/
│   ├── chat_node.py      # 개선된 챗봇 노드 (도구 호출 지원)
│   ├── search_node.py    # 검색 실행 노드
│   └── search_tool.py    # Tavily Search 도구
├── graphs/
│   └── chat_graph.py     # 조건부 라우팅 그래프
├── schemas/
│   └── chat_state.py     # 확장된 상태 스키마
└── utils/
    └── config.py         # LLM 설정
```

### 🔍 주요 컴포넌트

#### 1. **ChatState** (확장된 상태 스키마)
- `messages`: 대화 히스토리
- `needs_search`: 검색 필요 여부
- `search_query`: 검색 쿼리
- `search_results`: 검색 결과
- `current_step`: 현재 처리 단계

#### 2. **chatbot()** (스마트 챗봇 노드)
- 도구 바인딩으로 검색 도구 사용 가능
- 질문 분석하여 검색 필요성 자동 판단
- 검색 결과 활용한 답변 생성

#### 3. **search_executor()** (검색 노드)
- Tavily API로 웹 검색 실행
- 검색 결과 처리 및 상태 업데이트

#### 4. **tavily_search()** (검색 도구)
- Tavily API 통합
- 고급 검색 옵션 지원
- 오류 처리 포함

## 🎨 개선 사항

### 기존 문제점
- 단순한 선형 구조로 외부 정보 검색 불가능
- 실시간 정보에 대한 질문에 답변 불가
- 도구 호출 기능 없음

### 개선된 기능
- **조건부 라우팅**: 검색 필요 시에만 검색 노드 실행
- **스마트 판단**: LLM이 자동으로 검색 필요성 판단
- **검색 결과 활용**: 웹 검색 결과를 바탕으로 정확한 답변 생성
- **오류 처리**: 검색 실패 시 적절한 오류 메시지 제공
- **성능 최적화**: 불필요한 검색 방지로 응답 속도 향상

## 🚦 사용 팁

1. **검색 기능 활용**: "검색해줘", "찾아줘" 등의 키워드로 명시적 검색 요청
2. **실시간 정보**: 날씨, 주가, 뉴스 등 실시간 정보 질문 시 자동 검색
3. **대화 종료**: 'exit' 입력으로 대화 종료
4. **디버깅**: LangSmith 추적 활성화로 그래프 실행 과정 모니터링

이제 더 똑똑하고 실용적인 챗봇을 경험해보세요! 🤖✨
