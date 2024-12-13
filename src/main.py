import streamlit as st
from page.register import registration
from page.auth import authentification
from page.profile import profile_page
from page.booking import booking_page
from page.employees import employees_page
from page.booking_employee import booking_employee_page
from page.admin_all_users import admin_all_users_page
from page.admin_all_employees import admin_all_employees_page
from page.admin_all_services import admin_all_services_page
from page.admin_all_booking import admin_all_booking_page
from page.admin_all_food import admin_all_food_page
from streamlit_extras.switch_page_button import switch_page


def main():
    if 'page' not in st.session_state:
       st.session_state.page = "registration"
    if st.session_state.page == "registration":
        registration()
    elif st.session_state.page == "login":
        authentification()
    elif st.session_state.page == "initial":
        if (st.session_state.user_info[0][3] == 'user'):
            st.title(f"Добро пожаловать, {st.session_state.user_info[0][1]}!")

            st.sidebar.title("Навигация")
            page = st.sidebar.radio(
                "Перейти к странице",
                ["Информация", "Бронирование", "Профиль"],
            )
            if st.sidebar.button("Выход"):
                st.session_state.user_info = []
                st.session_state.page = "registration"
                switch_page("main")
            if page == "Информация":
                employees_page()
            elif page == "Бронирование":
                booking_page()
            elif page == "Профиль":
                profile_page()
        
        elif (st.session_state.user_info[0][3] == 'employee'):
            st.title(f"Добро пожаловать, {st.session_state.user_info[0][1]}!")

            st.sidebar.title("Навигация")
            page = st.sidebar.radio(
                "Перейти к странице",
                ["Мои заказы", "Профиль"],
            )

            if st.sidebar.button("Выход"):
                st.session_state.user_info = []
                st.session_state.page = "registration"
                switch_page("main")

            if page == "Мои заказы":
                booking_employee_page()
            elif page == "Профиль":
                profile_page()
        
        else:
            st.title(f"Добро пожаловать, {st.session_state.user_info[0][1]}!")

            st.sidebar.title("Навигация")
            page = st.sidebar.radio(
                "Перейти к странице",
                ["Все пользователи", "Все работники", "Все услуги", "Все брони", "Все корма"],
            )

            if st.sidebar.button("Выход"):
                st.session_state.user_info = []
                st.session_state.page = "registration"
                switch_page("main")

            if page == "Все пользователи":
                admin_all_users_page()
            elif page == "Все работники":
                admin_all_employees_page()
            elif page == "Все услуги":
                admin_all_services_page()
            elif page == "Все брони":
                admin_all_booking_page()
            elif page == "Все корма":
                admin_all_food_page()

if __name__ == "__main__":
    main()


