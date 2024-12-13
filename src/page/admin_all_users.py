import streamlit as st
from functions.admin_conn import get_all_users

def admin_all_users_page():
    st.title("Все пользователи")

    users = get_all_users()

    st.table(users)