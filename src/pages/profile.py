import streamlit as st
from functions.profile_conn import update_user_login, get_owner_data, update_owner_data, add_owner_data, get_active_bookings

def profile_page():
    st.title("Ваш профиль:")

    user_id = st.session_state.user_info[0][0]
    owner_data = get_owner_data(user_id)
    st.markdown(f"***Логин***: {st.session_state.user_info[0][1]}")

    if "update_login_button" not in st.session_state:
        st.session_state["update_login_button"] = False

    if st.button("Редактировать логин"):
        st.session_state["update_login_button"] = not st.session_state["update_login_button"]

    if st.session_state["update_login_button"]:
        new_login = st.text_input("Новый логин")
        # new_email = st.text_input("Новый email")
        # new_phone = st.text_input("Новый телефон")
        if st.button("Обновить"):
            if new_login:
                # if valid_login(new_login):
                update_user_login(st.session_state.user_info[0][0],new_login)
                st.success("Логин обновлен")
                st.session_state.user_info[0][1] = new_login
                st.session_state["update_login_button"] = not st.session_state["update_login_button"]
                # else:
                #     st.error("Некорректный логин")

    st.subheader("Информация о вас:")

    if owner_data:  # Если данные владельца уже существуют
        first_name = st.text_input("Имя", value=owner_data[1])
        last_name = st.text_input("Фамилия", value=owner_data[2])
        phone = st.text_input("Телефон", value=owner_data[3])
        email = st.text_input("Email", value=owner_data[4])
        address = st.text_area("Адрес", value=owner_data[5])
        if st.button("Обновить данные"):
            update_owner_data(user_id, first_name, last_name, phone, email, address)
    else:  # Если данные владельца еще не добавлены
        first_name = st.text_input("Имя")
        last_name = st.text_input("Фамилия")
        phone = st.text_input("Телефон")
        email = st.text_input("Email")
        address = st.text_area("Адрес")
        if st.button("Сохранить"):
            if first_name and last_name and phone and email and address:
                add_owner_data(user_id, first_name, last_name, phone, email, address)
            else:
                st.warning("Пожалуйста, заполните все поля.")

    st.subheader("Ваши активные брони:")
    if owner_data:
        active_bookings = get_active_bookings(owner_data[0])
        if active_bookings:
            for booking in active_bookings:
                st.write(f"Номер брони: {booking[0]}")
                st.write(f"Услуга: {booking[1]}")
                st.write(f"Животное: {booking[2]}")
                st.write(f"Дата заезда: {booking[3]}")
                st.write(f"Дата выезда: {booking[4]}")
                st.write(f"Сотрудник: {booking[5]} {booking[6]}")
                st.write(f"Адрес сотрудника: {booking[7]}")
                st.write(f"Email сотрудника: {booking[8]}")
                st.write(f"Телефон сотрудника: {booking[9]}")
                if booking[10] == 'Waiting':
                    st.write(f"Статус: Ожидание ответа сотрудника")
                elif booking[10] == 'Confirmed':
                    st.write (f"Статус: Принято")
                elif booking[10] == 'Cancelled':
                    st.write (f"Статус: Бронь была отменена сотрудником. Дождитесь ответа сотрудника или свяжитесь с администратором.")# Добавлено отображение статуса
                st.write("---")
        else:
            st.info("У вас нет активных броней.")
    else:
        st.info("У вас нет активных броней.")
    







    # if(st.session_state.user_info[0][5] == 1 or st.session_state.user_info[0][5] == '1'):
    #     st.markdown(f"***Статус***: Путешественник\n")

    #     st.markdown("***Ваши активные брони***: ")
    #     active_booking = get_active_booking(st.session_state.user_info[0][0],datetime.date.today())
    #     if (len(active_booking) == 0):
    #         st.write("У вас нет активных броней.")
    #     else:
    #         st.write(f"{active_booking[0][0]}, {active_booking[0][1]}, {active_booking[0][2]},{active_booking[0][3]}")
    #         st.write(f"От {active_booking[0][5]} до {active_booking[0][6]}\n")

    #     st.markdown("***Ваши отзывы***: ")
    #     active_reviews = get_reviews(st.session_state.user_info[0][0])
    #     if(len(active_reviews) == 0):
    #         st.write("У вас еще нет отзывов.")
    #     else:
    #         for i in range(len(active_reviews)):
    #             st.write(f"{active_reviews[i][0]}, {active_reviews[i][1]}, {active_reviews[i][2]} - {active_reviews[i][3]}, {active_reviews[i][4]}")

    # elif(st.session_state.user_info[0][5] == 2 or st.session_state.user_info[0][5] == '2'):
    #     st.markdown(f"***Статус***: Владелец")