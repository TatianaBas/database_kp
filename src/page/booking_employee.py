import streamlit as st
from settings import DB_CONFIG
from functions.profile_conn import get_employee_data
from functions.booking_emp_conn import get_employee_verify_status, get_employee_waiting_bookings, update_booking_status


def booking_employee_page():
    st.title("Ваши брони")
    user_id = st.session_state.user_info[0][0]
    employee_data = get_employee_data(user_id)
    if employee_data:
        employee_id = employee_data[0]

        if not get_employee_verify_status(employee_id):
            st.error("Ваш аккаунт не верифицирован. Обратитесь к администратору.")
            return

        waiting_bookings = get_employee_waiting_bookings(employee_id)

        if waiting_bookings:
            for booking in waiting_bookings:
                st.subheader(f"Бронирование #{booking[0]}")
                st.write(f"Услуга: {booking[1]}")
                st.write(f"Тип животного: {booking[2]}")
                st.write(f"Порода: {booking[3]}")
                st.write(f"Кличка: {booking[4]}")
                st.write(f"Дата рождения: {booking[5]}")
                st.write(f"Особые потребности: {booking[6]}")
                st.write(f"Корм: {booking[7]}")
                st.write(f"Дата заезда: {booking[8]}")
                st.write(f"Дата выезда: {booking[9]}")
                st.write(f"Владелец: {booking[10]} {booking[11]}")
                st.write(f"Телефон: {booking[12]}")
                st.write(f"Email: {booking[13]}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Принять ({booking[0]})", key=f"accept_{booking[0]}"):
                        update_booking_status(booking[0], "Confirmed")
                with col2:
                    if st.button(f"Отклонить ({booking[0]})", key=f"reject_{booking[0]}"):
                        update_booking_status(booking[0], "Cancelled")
                st.write("---")
        else:
            st.info("У вас нет ожидающих броней.")
    else: 
        st.error("Ваш аккаунт не верифицирован. Заполните данные о себе и ожидайте ответа администратора.")
        return