import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI
from tavily import TavilyClient
from supabase import create_client

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


class Message(BaseModel):
    role: str
    content: str


class ChatPayload(BaseModel):
    session_id: str
    messages: list[Message]
    enable_web_search: bool = True


def search_web(query: str) -> str:
    try:
        results = tavily.search(
            query=query,
            search_depth="basic",
            max_results=5
        )

        text = "معلومات من الإنترنت:\n"

        for result
