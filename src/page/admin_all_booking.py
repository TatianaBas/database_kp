import streamlit as st
from functions.admin_conn import get_all_booking

def admin_all_booking_page():
    st.title("Все пользователи")

    booking = get_all_booking()

    st.table(booking)