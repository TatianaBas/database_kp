import streamlit as st
import psycopg2
from settings import DB_CONFIG
from functions.employees_conn import get_employees, get_food, get_services


def employees_page():
    st.title("Наши сотрудники и услуги")

    employees = get_employees()
    food_items = get_food()
    services = get_services()

    st.subheader("Наши сотрудники")
    if employees:
        for employee in employees:
            st.subheader(f"{employee[1]} {employee[2]} ({employee[5]})")  # ФИО и роль
            st.write(f"Телефон: {employee[3]}")
            st.write(f"Email: {employee[4]}")
            st.write(f"Описание: {employee[6]}")
            st.write(f"Адрес: {employee[7]}")
            st.write("---") # Разделитель между сотрудниками
    else:
        st.info("Информация о сотрудниках отсутствует.")


    st.subheader("Наши корма")
    if food_items:
        for food in food_items:
            st.write(f"**{food[1]}**")  # Название корма
            st.write(f"Описание: {food[2]}")
            st.write("---")
    else:
        st.info("Информация о кормах отсутствует.")

    st.subheader("Наши услуги")
    if services:
        for service in services:
            st.write(f"**{service[1]}**")  # Название услуги
            st.write(f"Описание: {service[2]}")
            st.write(f"Цена: {service [3] :.2f} р. в сутки")
            st.write("---")
    else:
        st.info("Информация об услугах отсутствует.")