from sql_graph.sql_state import SqlState
from sqlalchemy import text
from sql.db_schema import engine



def execute_delete_node(state: SqlState):
    print("Enter in execute_delete_node")

    

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