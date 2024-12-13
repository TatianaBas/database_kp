import streamlit as st
from functions.admin_conn import get_employees, update_employee_status
from settings import DB_CONFIG


def admin_all_employees_page():
    st.title("Управление сотрудниками")

    employees = get_employees()

    if employees:
        for employee in employees:
            employee_id, first_name, last_name, phone, email, role, description, address, verify = employee
            st.subheader(f"{first_name} {last_name} (ID: {employee_id})")
            st.write(f"Роль: {role}")
            st.write(f"Телефон: {phone}")
            st.write(f"Email: {email}")
            st.write(f"Адрес: {address}")
            st.write(f"Описание: {description}")

            current_status = "Верифицирован" if verify == 1 else "Не верифицирован"
            st.write(f"Текущий статус: {current_status}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Принять ({employee_id})", key=f"accept_{employee_id}"):
                    update_employee_status(employee_id, 1)
            with col2:
                if st.button(f"Отклонить ({employee_id})", key=f"reject_{employee_id}"):
                    update_employee_status(employee_id, 0)


            st.write("---")
    else:
        st.info("Список сотрудников пуст.")

