import streamlit as st
import psycopg2
from settings import DB_CONFIG
from functions.profile_conn import get_employee_data

def get_employee_waiting_bookings(employee_id):
    """Получает бронирования в статусе 'Waiting' для данного сотрудника с полной информацией."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                b.booking_id, s.service_name, a.animal_type, a.breed, a.name, a.birth_date, a.special_needs,
                f.food_name, b.check_in_date, b.check_out_date, o.first_name, o.last_name, o.phone, o.email
            FROM bookings b
            JOIN services s ON b.service_id = s.service_id
            JOIN animals a ON b.animal_id = a.animal_id
            JOIN owners o ON a.owner_id = o.owner_id
            JOIN food f ON b.food_id = f.food_id
            WHERE b.employee_id = %s AND b.status = 'Waiting'
            ORDER BY b.check_in_date;
        """, (employee_id,))
        bookings = cur.fetchall()
        cur.close()
        conn.close()
        return bookings
    except (Exception, psycopg2.Error) as error:
        st.error(f"Ошибка при получении броней: {error}")
        return []

def update_booking_status(booking_id, status):
    """Обновляет статус бронирования."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("UPDATE bookings SET status = %s WHERE booking_id = %s", (status, booking_id))
        conn.commit()
        cur.close()
        conn.close()
        st.success(f"Статус бронирования изменен на '{status}'.")
    except (Exception, psycopg2.Error) as error:
        st.error(f"Ошибка при обновлении статуса бронирования: {error}")


def get_employee_verify_status(employee_id):
    """Проверяет статус верификации сотрудника."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT verify FROM employees WHERE employee_id = %s", (employee_id,))
        verify_status = cur.fetchone()[0]
        cur.close()
        conn.close()
        return verify_status == 1  # Возвращает True, если верифицирован, иначе False
    except (Exception, psycopg2.Error) as error:
        st.error(f"Ошибка при проверке статуса верификации: {error}")
        return False