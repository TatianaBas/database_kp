import streamlit as st
import psycopg2
from psycopg2 import extras
from service.hash import hash_password
from functions.autn_conn import check_auth_user, return_user_data
from settings import DB_CONFIG

def authentification():

    st.title("Авторизация")

    entered_username = st.text_input("Имя пользователя")
    entered_password = st.text_input("Пароль", type="password")
    submit_button = st.button("Войти")

    if submit_button:

        if check_auth_user(entered_username, entered_password)==0:
            st.success("Вход выполнен успешно!")
            user_data = return_user_data(entered_username, hash_password(entered_password))
            user_data[0] = list(user_data[0])
            st.session_state.user_info = user_data
            st.session_state.page = "initial"
        elif check_auth_user(entered_username, entered_password)==1:
            st.error("Неверный пароль.")
        elif check_auth_user(entered_username, entered_password)==2:
            st.error("Пользователь не найден.")
        else:
            st.error("Ошибка")
    if st.button("Нет аккаунта? Зарегистрироваться"):
        st.session_state.page = "registration"

