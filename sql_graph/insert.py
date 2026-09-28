from sql_graph.sql_state import SqlState
from llm import llm_gpt
from sql.db_schema import get_schema,execute_sql
from langgraph.graph import START,END
from pydantic import BaseModel,Field
from sql_graph.pydantic_classes import Verify_user_query







from sql_graph.sql_state import SqlState
from sqlalchemy import text
from sql.db_schema import engine


def execute_insert_node(state: SqlState):
    print("Enter in execute_insert_node")

    sql = state["sql"]

    try:
        with engine.begin() as conn:
            result = conn.execute(text(sql))

            return {
                "result": {
                    "rowcount": result.rowcount
                },
                "error": ""
            }

    except Exception as e:
        return {
            "result": {},
            "error": str(e)
        }






    



     







