import requests
import streamlit as st

st.title("Basic Todo App")

data = requests.get("http://localhost:8000/todos").json()


st.table(data)





