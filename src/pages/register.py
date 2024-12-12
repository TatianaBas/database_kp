from service.hash import check_password, hash_password
import psycopg2
import streamlit as st
from settings import DB_CONFIG
from functions.autn_conn import reg_new_user, check_new_user_login, return_user_data



# Streamlit приложение
def registration():
    st.title("Регистрация")

    username = st.text_input("Имя пользователя")
    password = st.text_input("Пароль", type="password")
    confirm_password = st.text_input("Подтверждение пароля", type="password")
#    submit_button = st.form_submit_button("Зарегистрироваться")

    #Обработка формы регистрации
    if st.button("Зарегистрироваться"):
        if username and password and confirm_password:
            if password != confirm_password:
                st.error("Пароли не совпадают.")
            else:
                if check_new_user_login(username):
                    st.success("Вы успешно зарегистрированы!")

                    # Добавляю нового пользователя в БД
                    reg_new_user(username, hash_password(password))
                    user_data = return_user_data(username, hash_password(password))
                    user_data[0] = list(user_data[0])
                    st.session_state.user_info = user_data

                    st.session_state.page = "login"
                else:
                    st.error("Пользователь с таким логином уже существует")
        else:
            st.error("Пожалуйста, заполните все поля.")

    if st.button("Уже есть аккаунт? Войти"):
        st.session_state.page = "login"


