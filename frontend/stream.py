import streamlit as st 
from typing import cast
from sql_graph.sql_main import app,config
from langgraph.types import Command,interrupt

from sql_graph.sql_state import SqlState
st.title("SQL Graph Application")


with st.chat_message("user"):
    user_question = st.text_input("Enter your SQL-related question: ")
   
if user_question:
    with st.chat_message("assistant"):
            result = app.invoke(cast(SqlState, {
                 "user_question": user_question,
                  "operation_not_find":"",
                 "operation":"",
                 "sql": "",
                 "error": "",
                "attempts":2,
                "approval": "",
                "answer": ""
            }), config=config)

            state = app.get_state(config)



            for task in state.tasks:
               for interrupt in task.interrupts:
                    st.write("Interrupt:", interrupt.value)

            command_input = st.text_input("Enter command : ")
            if command_input:
                app.invoke(Command(resume=command_input), config=config)
                st.write(f"result[\"sql\"] = {result['sql']}")
                st.write(f"result[\"operation\"] = {result['operation']}")
                st.write(f"result[\"answer\"] = {result['answer']}")    
            





