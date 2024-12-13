import streamlit as st
from functions.admin_conn import get_food, add_food, edit_food, delete_food
from streamlit_extras.switch_page_button import switch_page


def admin_all_food_page():
    st.title("Управление кормами")

    foods = get_food()

    # Отображение таблицы корм
    cols = ["ID", "Название", "Описание", "Цена"]
    data = [[food[0], food[1], food[2], food[3]] for food in foods]
    if data:
        st.table(data)
    else:
        st.info("Список кормов пуст.")

    # Добавление новой корма
    st.subheader("Добавить корм")
    with st.form("add_food_form"):
        food_name = st.text_input("Название корма", key="food_name")
        description = st.text_area("Описание", key="description")
        price = st.number_input("Цена", value=0.0, min_value=0.0, step=0.01, format="%.2f", key="price")
        submitted = st.form_submit_button("Добавить")

        if submitted:
            if not food_name or price <=0:
                st.error("Пожалуйста, заполните все поля корректно.")
            else:
                add_food(food_name, description, price)
                switch_page("main")


    # Редактирование и удаление корма
    st.subheader("Редактировать/Удалить корм")
    if foods:
        selected_food_id = st.selectbox("Выберите корм для редактирования/удаления", [food[0] for food in foods], key="selected_food")

        selected_food = next((food for food in foods if food[0] == selected_food_id), None)
        if selected_food:
            with st.form("edit_food_form"):
                food_name = st.text_input("Название корма", value=selected_food[1], key="edit_food_name")
                description = st.text_area("Описание", value=selected_food[2], key="edit_description")
                #Convert Decimal to float for number_input to work correctly.
                price = st.number_input("Цена", value=float(selected_food[3]), min_value=0.0, step=0.01, format="%.2f", key="edit_price")
                edit_submitted = st.form_submit_button("Сохранить изменения") #Added submit button
                if edit_submitted:
                    if not food_name or price <=0:
                        st.error("Пожалуйста, заполните все поля корректно.")
                    else:
                        edit_food(food_name, description, price, selected_food_id)
                        switch_page("main")

            if st.button("Удалить корм"):
                delete_food(selected_food_id)
                switch_page("main")


