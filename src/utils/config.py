from functools import lru_cache
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


@lru_cache(maxsize=10)
def get_llm(model_name: str = "gpt-4.1-nano") -> ChatOpenAI:
    return ChatOpenAI(model=model_name)
