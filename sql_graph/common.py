from sql_graph.sql_state import SqlState
from llm import llm_gpt
from sql.db_schema import get_schema,execute_sql
from langgraph.graph import START,END
from pydantic import BaseModel,Field
# from sql_graph.pydantic_classes import Verify_user_query
from  langgraph.types import Command,interrupt
from sql_graph.insert import execute_insert_node


from sqlalchemy import text
from sql.db_schema import engine




def common_approve_node(state:SqlState):
    print("Enter In Common approve node")
    human_decision=interrupt(
        
        f"""
            "explanation":{state["explanation"]},
            "sql":{state["sql"]},
            "your_decision":"approve or reject"
         """
        
    )
    if human_decision.strip().lower()=="approve":
        print(f"Human decision is {human_decision}")
        if state["operation"]=="UPDATE":
            return "execute_update_node"
        elif state["operation"]=="DELETE":
            return "execute_delete_node"
        elif state["operation"]=="INSERT":
            return "execute_insert_node"

    else:
        print(f"Human decision is {human_decision}")
        return END



def explain_sql(state:SqlState):
    print("Enter in explain_sql node")


    sql = state["sql"]
    prompt = f"""
You are an expert SQL Server query explainer.
Explain the risk and impact of the following SQL query.
Explain what this SQL query does and what it is intended to achieve.

user_question: {state["user_question"]}
------------------------------------------------

SQL query:
{sql}

-------------------------------------------------
"""
    response = llm_gpt.invoke(prompt)
    return {
        "explanation": response.content
    }


def continue_human_decision(state:SqlState):
    print("Enter in continue_human_decision node")
    if state["operation"]=="UPDATE" and state["human_decision"]=="approve":
        return "execute_update_node"
    elif state["operation"]=="DELETE" and state["human_decision"]=="approve":
        return "execute_delete_node"
    elif state["operation"]=="INSERT" and state["human_decision"]=="approve":
        return "execute_insert_node"
    else:
        print("Error in continue_human_decision: Unsupported SQL operation or decision.")
        return END



def common_routing(state:SqlState):
    print("Enter in common_routing node")
    if state["error"] or len(state["error"].strip())>0:
        return "fix_common_node"
   
    else:
        return "explain_final_answer"




def fix_common_node(state:SqlState):
    print("Enter in fix_common_node")
   
    question = state["user_question"]
    schema = state["schema"]
    sql = state["sql"]
    error = state["error"]

    prompt = f"""
You are an expert SQL Server developer.

User question:
{question}

Database schema:
{schema}

Previous SQL:
{sql}

SQL Server error:
{error}

Fix the SQL query.

Rules:
- Use only tables and columns from the schema.
- Return ONLY the corrected SQL query.
- Do not use markdown code fences.
- Generate SQL Server compatible SQL.
"""

    response = llm_gpt.invoke(prompt)
    

    return {
        "sql": response.content.strip(),
        "error": "",
        "attempts":state["attempts"]-1
    }




def explain_final_answer(state:SqlState):
    print("Enter in explain_final_answer node")
    question = state["user_question"]
    result = state["result"]

    prompt = f"""
You are a helpful database assistant.

User question:
{question}

Database result:
{result}

Answer the user's question using only the database result.

Rules:
- Be concise.
- Do not invent information.
- If the result is empty, clearly say that no matching records were found.
"""

    response = llm_gpt.invoke(prompt)

    return {
        "answer": response.content
    }


def cyclic_attempts_fix_node(state:SqlState):
    print("Enter in cyclic_attempts_fix_node")
    if state["attempts"]<0:
        print("Error in cyclic_attempts_fix_node: Maximum attempts reached. Cannot fix the SQL query.Your 2 attempts are over")
        raise ValueError("Maximum attempts reached. Cannot fix the SQL query.Your 2 attempts are over")
    elif state["operation"]=="INSERT":
        return "execute_insert_node"
    elif state["operation"]=="UPDATE":
        return "execute_update_node"
    elif state["operation"]=="DELETE":
        return "execute_delete_node"
    else:
        print("Error in cyclic_attempts_fix_node: Unsupported SQL operation. Cannot fix the SQL query.")
        raise ValueError("Unsupported SQL operation. Cannot fix the SQL query.")
        