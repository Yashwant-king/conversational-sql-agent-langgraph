from sql_graph.sql_state import SqlState
from llm import llm_gpt
from sql.db_schema import get_schema,execute_sql
from langgraph.graph import START,END
from pydantic import BaseModel,Field
from sql_graph.pydantic_classes import Verify_user_query


#---------------------------------------------------------------------

def schema_node(state:SqlState):
    print("Enter in schema_node")
    result_schema=get_schema()
    if not result_schema or len(result_schema.strip())==0:
        raise ValueError("schema not found in schema_node")
    return {"schema":result_schema}

#-----------------------------------------------------------------------

def approve_routing(state:SqlState):
    print("Enter in approve_routing node")
    approve_model=llm_gpt.with_structured_output(Verify_user_query)
    user_query=state["user_question"]
    approve_result=approve_model.invoke(f"Find that given user question is related to SQL or not user_question={user_query}. Give answer in bool")
    try:
       if approve_result.approve:
           return "query_node"
       else:
           print("Your question is not related to SQL. Please ask a valid SQL-related question.")
           print(f"bool value of approve_result.approve={approve_result.approve}")
           print(f"approve_result={approve_result}")
           return END
    except Exception as e:
        print(f"Error in approve_routing node error={e}")
        raise ValueError()






#---------------------------------------------------------------------

def query_node(state:SqlState):
    print("Enter in query_node")

    question = state["user_question"]
    schema = state["schema"]

    prompt = f"""
You are an expert SQL Server query generator.

Your task is to convert the user's natural-language question
into a SQL Server SQL query.

Database schema:
{schema}

User question:
{question}

Rules:
- Use only tables and columns present in the schema.
- Generate SQL Server compatible SQL.
- Return ONLY the SQL query.
- Do not use markdown code fences.
"""

    response = llm_gpt.invoke(prompt)

    try:
        sql = response.content
    except Exception as e:
        print(f"{e} error in query_node")
        raise ValueError("Error in query_node")    

    return {
        "sql": sql
    }


#-----------------------------------------------------------------------

def validate_sql_node(state:SqlState):
    print("Enter in validate_sql_node")

    sql = state["sql"].strip()

    sql_clean = sql.replace("```sql", "").replace("```", "").strip()

    operation = sql_clean.split()[0].upper()
    if not operation:
        return {
            "operation_not_find":"True"
        }
    allowed_operations = {
        "SELECT",
        "INSERT",
        "UPDATE",
        "DELETE"
    }

    if operation not in allowed_operations:
        return {
            "operation_not_find":"True"
        }
       

    return {
        "sql": sql_clean,
        "operation": operation,
        "error": ""
    }


#---------------------------------------------------------------------------
def first_routing(state:SqlState):
    print("Enter in first_routing node")

    if state["operation_not_find"]=="True":
        return "attemp_query_node"
                

    elif state["operation"]=="SELECT":
        return "refill_attempts" 

    elif state["operation"]=="DELETE":
        return "explain_sql"
    elif state["operation"]=="UPDATE":
        return "explain_sql"
    elif state["operation"]=="INSERT":
        return "explain_sql"
    else:
        raise ValueError(f"state['operation'] is not valid . error in first_routing node. state['operation']={state['operation']}")
        




def attemp_query_node(state:SqlState):
    if state["attempts"]<=0:
        raise ValueError("Maximum attempts reached. Cannot fix the SQL query.")
    
    return {
        "attempts":state["attempts"]-1
    }

    
        
def refill_attemps(state:SqlState):
    return {
        "attempts":2
    }




def attemp_fix_select(state:SqlState):
    if state["attempts"]<=0:
        raise ValueError("Maximum attempts reached. Cannot fix the SQL query.")
    
    return {
        "attempts":state["attempts"]-1
    }






