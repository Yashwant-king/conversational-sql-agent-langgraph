from typing import TypedDict
from langgraph.graph import StateGraph

class SqlState(TypedDict):
    user_question: str
    schema: str
    sql: str
    result: dict
    approval: str
    answer: str
    error: str
    operation:str
    operation_not_find:str
    attempts:int
    explanation:str
    human_decision:str
    rowcount:int


graph=StateGraph(SqlState)





    