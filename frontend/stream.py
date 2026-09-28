import streamlit as st 
from typing import cast
from sql_graph.sql_main import app,config
from langgraph.types import Command,interrupt

from sql_graph.sql_state import SqlState
st.title("SQL Graph Application")


with st.chat_message("user"):
    user_question = st.text_input("Enter your SQL-related question: ")
    if user_question:
          graph_result = app.invoke(cast(SqlState, {
                          "user_question": user_question,
                           "operation_not_find":"",
                          "operation":"",
                          "sql": "",
                          "error": "",
                         "attempts":2,
                         "approval": "",
                         "answer": ""
                     }), config=config)
         

if user_question:
    with st.chat_message("assistant"):
         

            state = app.get_state(config)



            for task in state.tasks:
               for interrupt in task.interrupts:
                    st.write("Interrupt:", interrupt.value)
            if graph_result["operation"]:
                command_input = st.text_input("Enter command : ")
                if command_input:
                   app.invoke(Command(resume=command_input), config=config)
                   st.write(f"result[\"sql\"] = {graph_result['sql']}")
                   st.write(f"result[\"operation\"] = {graph_result['operation']}")
                   st.write(f"result[\"answer\"] = {graph_result['answer']}")
                   st.write(f"result[\"error\"] = {graph_result['error']}")
                   st.write(f"result[\"\result\"] = {graph_result['result']}")    
            else:
                 st.write(f"result[\"answer\"] = {graph_result['answer']}")       
else:
     st.chat_message("assistant").write("Your question is not related to SQL. Please ask a valid SQL-related question.")




