from graph.state import TicketClassification
from dotenv import load_dotenv
load_dotenv()
import os
from langchain_groq import ChatGroq



# llm_gpt=ChatGroq(
#     model="openai/gpt-oss-20b"
#     )



def enter_your_api_key(api_key:str):
    try:
        return ChatGroq(
            model=api_key
        )
    except:
        raise ValueError("Please set your API key in the environment variable 'GROQ_API_KEY' or provide it as an argument to the ChatGroq constructor.")


llm_gpt=enter_your_api_key("openai/gpt-oss-20b")












