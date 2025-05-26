from langchain_community.tools.tavily_search import TavilySearchResults
from typing import List, TypedDict
from langchain_core.tools import tool


class SearchResult(TypedDict):
    title: str
    url: str
    content: str
    score: int


tavily_search_results = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=True,
)


@tool
def tavily_search(query: str) -> List[SearchResult]:
    """
    **Tavily Search Tool**
    - This is a Tavily Search tool which uses the LangChain-Tavily integration to perform comprehensive web searches.
    - The tool processes search queries and returns structured results containing relevant web content.
    """

    formatted_results: List[SearchResult] = []
    results = tavily_search_results.invoke({"query": query})

    for result in results:
        formatted_results.append(
            SearchResult(
                title=result.get("title"),
                url=result.get("url"),
                content=result.get("content"),
                score=result.get("score"),
            )
        )

    return (
        formatted_results
        if formatted_results else [
            SearchResult(
                title="",
                url="",
                content="No search results found.",
                score=0
            )
        ]
    )
