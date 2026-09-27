from graph.state import TicketClassification
from dotenv import load_dotenv
load_dotenv()
import os
from langchain_groq import ChatGroq

llm_gpt=ChatGroq(
    model="openai/gpt-oss-20b"
    )





llm_qwen=ChatGroq(
    model="qwen/qwen3.8-27b"
)




