from sql_graph.sql_state import SqlState
from llm import llm_gpt
from sql.db_schema import get_schema,execute_sql
from langgraph.graph import START,END
from pydantic import BaseModel,Field
from sql_graph.pydantic_classes import Verify_user_query



from sqlalchemy import text
from sql.db_schema import engine


def execute_select_node(state:SqlState):
    print("Enter in execute_select_node")

    sql = state["sql"]

    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql))

            rows = [dict(row._mapping) for row in result]

        return {
            "result": {
                "rows": rows
            },
            "error": ""
        }

    except Exception as e:
        return {
            "result": {
                "rows": []
            },
            "error": str(e)
        }

def select_routing(state:SqlState):
    print("Enter in select_routing node")
    if state["error"]:
        return "fix_select"
    else:
        return "decode_to_natural_language"
    

def decode_to_natural_language(state:SqlState):
    print("Enter in decode_to_natural_language node")
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



def fix_select(state:SqlState):
    print("Enter in fix_select node")
    if state["attempts"] <= 0:
        raise ValueError("Maximum attempts reached. Cannot fix the SQL query.")
        
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




