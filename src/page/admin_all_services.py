import streamlit as st
import psycopg2
from settings import DB_CONFIG
from functions.admin_conn import get_services, add_service, edit_service, delete_service
from streamlit_extras.switch_page_button import switch_page


def admin_all_services_page():
    st.title("Управление услугами")

    services = get_services()

    # Отображение таблицы услуг
    cols = ["ID", "Название", "Описание", "Цена"]
    data = [[service[0], service[1], service[2], service[3]] for service in services]
    if data:
        st.table(data)
    else:
        st.info("Список услуг пуст.")

    # Добавление новой услуги
    st.subheader("Добавить услугу")
    with st.form("add_service_form"):
        service_name = st.text_input("Название услуги", key="service_name")
        description = st.text_area("Описание", key="description")
        price = st.number_input("Цена", value=0.0, min_value=0.0, step=0.01, format="%.2f", key="price")
        submitted = st.form_submit_button("Добавить")

        if submitted:
            if not service_name or price <=0:
                st.error("Пожалуйста, заполните все поля корректно.")
            else:
                add_service(service_name, description, price)
                switch_page("main")


    # Редактирование и удаление услуг
    st.subheader("Редактировать/Удалить услугу")
    if services:
        selected_service_id = st.selectbox("Выберите услугу для редактирования/удаления", [service[0] for service in services], key="selected_service")

        selected_service = next((service for service in services if service[0] == selected_service_id), None)
        if selected_service:
            with st.form("edit_service_form"):
                service_name = st.text_input("Название услуги", value=selected_service[1], key="edit_service_name")
                description = st.text_area("Описание", value=selected_service[2], key="edit_description")
                #Convert Decimal to float for number_input to work correctly.
                price = st.number_input("Цена", value=float(selected_service[3]), min_value=0.0, step=0.01, format="%.2f", key="edit_price")
                edit_submitted = st.form_submit_button("Сохранить изменения") #Added submit button
                if edit_submitted:
                    if not service_name or price <=0:
                        st.error("Пожалуйста, заполните все поля корректно.")
                    else:
                        edit_service(service_name, description, price, selected_service_id)
                        switch_page("main")

            if st.button("Удалить услугу"):
                delete_service(selected_service_id)
                switch_page("main") #Обновляем страницу после удаления
