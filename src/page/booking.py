
import streamlit as st
import datetime
import psycopg2
from functions.profile_conn import get_owner_data
from functions.booking_conn import get_employees, get_food, get_services, add_animal, add_booking
from settings import DB_CONFIG




def booking_page():
    st.title("Бронирование")


    user_id = st.session_state.user_info[0][0]
    owner_data = get_owner_data(user_id)

    # Проверка наличия данных о владельце
    if not owner_data or not all(owner_data[1:]): # Проверяем наличие всех данных кроме owner_id
        st.error("Пожалуйста, заполните информацию о себе в разделе 'Профиль' прежде чем делать бронирование.")
        return  # Прерываем выполнение функции
 
    owner_id = get_owner_data(user_id)[0] # получить ID владельца 

    # Данные о животном
    animal_type = st.text_input("Тип животного")
    breed = st.text_input("Порода")
    name = st.text_input("Кличка")
    birth_date = st.date_input("Дата рождения")
    special_needs = st.text_area("Особые потребности")

    # Выбор услуг, сотрудника и корма
    services = get_services()
    selected_service = st.selectbox("Услуга", [service[1] for service in services], format_func=lambda x: x if services else "Услуги отсутствуют")

    employees = get_employees()
    selected_employee = st.selectbox("Сотрудник", [employee[1] for employee in employees], format_func=lambda x: x if employees else "Сотрудники отсутствуют")

    food = get_food()
    selected_food = st.selectbox("Корм", [f[1] for f in food], format_func=lambda x: x if food else "Корм отсутствует")


    # Даты заезда и выезда
    check_in_date = st.date_input("Дата заезда")
    check_out_date = st.date_input("Дата выезда")

    if check_in_date and check_out_date:
        if check_in_date > check_out_date:
            st.error("Дата заезда должна быть раньше даты выезда.")

    if check_in_date and check_out_date and check_in_date < check_out_date:
        days = (check_out_date - check_in_date).days+1
    else:
        days = 1

    # Расчет цены
    service_price = next((s[2] for s in services if s[1] == selected_service), 0)
    food_price = next((f[2] for f in food if f[1] == selected_food), 0)
    price = service_price * days + (food_price / 30) * days
    st.write(f"Цена: {price:.2f}")

    # Кнопка бронирования
    if st.button("Забронировать", key = "book_button"):
        if not all([animal_type, breed, name]):
            st.error("Пожалуйста, заполните все поля, касающиеся животного.")
        elif check_in_date > check_out_date:
            st.error("Ошибка в полях даты заезда и выезда.")
        else:
            animal_id = add_animal(owner_id, animal_type, breed, name, birth_date, special_needs)
            service_id = next((s[0] for s in services if s[1] == selected_service), None)
            employee_id = next((e[0] for e in employees if e[1] == selected_employee), None)
            food_id = next((f[0] for f in food if f[1] == selected_food), None)

            if animal_id and service_id and employee_id and food_id:
                add_booking(animal_id, service_id, check_in_date, check_out_date, employee_id, food_id)
            else:
                st.error("Ошибка при создании бронирования. Проверьте все поля.")
