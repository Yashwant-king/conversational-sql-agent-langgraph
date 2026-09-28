from langgraph.graph import StateGraph,END,START
from sql_graph.sql_state import graph
from langgraph.types import interrupt,Command
from sql_graph.sql_nodes import attemp_fix_select,refill_attemps,attemp_query_node,schema_node,query_node,validate_sql_node,first_routing
from sql_graph.sql_nodes import approve_routing,not_sql
from sql_graph.select_part import execute_select_node,decode_to_natural_language,select_routing,fix_select
from sql_graph.common import cyclic_attempts_fix_node,explain_final_answer,fix_common_node,common_routing,explain_sql,common_approve_node,continue_human_decision
from sql_graph.insert import execute_insert_node
from sql_graph.update import execute_update_node
from sql_graph.delete import execute_delete_node
from langgraph.checkpoint.memory import InMemorySaver
############################### NODES


checkpoint = InMemorySaver()
    
from uuid import uuid4
       

graph.add_node("schema_node",schema_node)
graph.add_node("query_node",query_node)
graph.add_node("validate_sql_node",validate_sql_node)
graph.add_node("execute_select_node",execute_select_node)
graph.add_node("decode_to_natural_language",decode_to_natural_language)
graph.add_node("fix_select",fix_select)
graph.add_node("attemp_query_node",attemp_query_node)
graph.add_node("refill_attempts",refill_attemps)
graph.add_node("attemp_fix_select",attemp_fix_select)
graph.add_node("explain_sql",explain_sql)
# graph.add_node("common_approve_node",common_approve_node)
graph.add_node("fix_common_node",fix_common_node)
graph.add_node("explain_final_answer",explain_final_answer)
graph.add_node("execute_insert_node",execute_insert_node)
graph.add_node("execute_update_node",execute_update_node)
graph.add_node("execute_delete_node",execute_delete_node)
graph.add_node("not_sql",not_sql)
graph.add_node("approve_routing",approve_routing)



###################################  Edges
    
graph.add_edge(START,"schema_node")
graph.add_edge("schema_node","approve_routing")
graph.add_edge("not_sql",END)
graph.add_edge("query_node","validate_sql_node")
# graph.add_conditional_edges("validate_sql_node",operation_verify)
graph.add_conditional_edges("validate_sql_node",first_routing)
graph.add_edge("attemp_query_node","query_node")
graph.add_edge("refill_attempts","execute_select_node")
graph.add_conditional_edges("execute_select_node",select_routing)
graph.add_edge("fix_select","attemp_fix_select")
graph.add_edge("attemp_fix_select","execute_select_node")

graph.add_edge("decode_to_natural_language",END)
#---------------------------------------------------------------
graph.add_conditional_edges("explain_sql",common_approve_node)
# graph.add_conditional_edges("common_approve_node",continue_human_decision)
graph.add_conditional_edges("execute_insert_node",common_routing)
graph.add_conditional_edges("execute_update_node",common_routing)
graph.add_conditional_edges("execute_delete_node",common_routing)
graph.add_conditional_edges("fix_common_node",cyclic_attempts_fix_node)
graph.add_edge("explain_final_answer",END)









app=graph.compile(checkpointer=checkpoint)

config = {
            "configurable": {
                "thread_id": str(uuid4()),
            }
        }



# user_question = input("Enter your question: ")

# result = app.invoke({
#     "user_question": user_question,
#     "operation_not_find":"",
#     "operation":"",
#     "sql": "",
#     "error": "",
#     "attempts":2,
#     "approval": "",
#     "answer": ""
# }, config=config)  # type: ignore[arg-type]

# #-------------------------------------------- interrupt----------------
# state = app.get_state(config)



# for task in state.tasks:
#     for interrupt in task.interrupts:
#         print("Interrupt:", interrupt.value)

# command_input = input("Enter command : ")
# app.invoke(Command(resume=command_input), config=config)  # type: ignore[arg-type]


# #---------------------------------------------------------------------------------

# print(f"result[\"sql\"] = {result['sql']}")
# print(f"result[\"operation\"] = {result['operation']}")
# print(f"result[\"answer\"] = {result['answer']}")






