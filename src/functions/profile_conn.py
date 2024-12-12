import psycopg2
import psycopg2.extras
from settings import DB_CONFIG
import streamlit as st
import datetime

def update_user_login(user_id,user_name):
    query = f"UPDATE users SET username = '{user_name}' WHERE user_id = {user_id};"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)

def get_owner_data(user_id):
    """Получает данные владельца из базы данных по user_id."""
    try:
        conn = psycopg2.connect(**DB_CONFIG) # Замените на ваши данные
        cur = conn.cursor()
        cur.execute("SELECT owner_id, first_name, last_name, phone, email, address FROM owners WHERE user_id = %s", (user_id,))
        owner_data = cur.fetchone()
        cur.close()
        conn.close()
        return owner_data
    except (Exception, psycopg2.Error) as error:
        st.error(f"Ошибка при получении данных владельца: {error}")
        return None
    


def update_owner_data(user_id, first_name, last_name, phone, email, address):
    """Обновляет данные владельца в базе данных."""
    try:
        conn = psycopg2.connect(**DB_CONFIG) # Замените на ваши данные
        cur = conn.cursor()
        cur.execute("""
            UPDATE owners
            SET first_name = %s, last_name = %s, phone = %s, email = %s, address = %s
            WHERE user_id = %s
        """, (first_name, last_name, phone, email, address, user_id))
        conn.commit()
        cur.close()
        conn.close()
        st.success("Данные успешно обновлены!")
    except (Exception, psycopg2.Error) as error:
        st.error(f"Ошибка при обновлении данных владельца: {error}")

def add_owner_data(user_id, first_name, last_name, phone, email, address):
    """Добавляет данные владельца в базу данных."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO owners (user_id, first_name, last_name, phone, email, address)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_id, first_name, last_name, phone, email, address))
        conn.commit()
        cur.close()
        conn.close()
        st.success("Данные успешно добавлены!")

    except (Exception, psycopg2.Error) as error:
        st.error(f"Ошибка при добавлении данных владельца: {error}")

def get_active_bookings(owner_id):
    """Получает активные бронирования с информацией о сотруднике и статусом."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        today = datetime.date.today()
        cur.execute("""
            SELECT 
                b.booking_id, s.service_name, a.name, b.check_in_date, b.check_out_date,
                e.first_name, e.last_name, e.address, e.email, e.phone, b.status
            FROM bookings b
            JOIN services s ON b.service_id = s.service_id
            JOIN animals a ON b.animal_id = a.animal_id
            JOIN employees e ON b.employee_id = e.employee_id
            WHERE a.owner_id = %s AND (b.status = 'Confirmed' OR b.status = 'Waiting' OR b.status = 'Cancelled') AND b.check_out_date >= %s
            ORDER BY b.check_in_date;
        """, (owner_id, today))
        bookings = cur.fetchall()
        cur.close()
        conn.close()
        return bookings
    except (Exception, psycopg2.Error) as error:
        st.error(f"Ошибка при получении активных броней: {error}")
        return []

# def get_active_booking(user_id,today):
#     query = f"""
#             select 
#                 h.name,h.country_loc,h.city_loc,h.location,
#                 rt.type_name, b.check_in_date,b.check_out_date,r.price
#             from booking b 
#             join room r 
#                 on r.room_id = b.room_id 
#             join hotel h 
#                 on h.hotel_id = r.hotel_id 
#             join room_types rt 
#                 on rt.room_type = r.room_type
#             where 1=1
#                 and b.user_id = {user_id}
#                 and check_in_date <= '{today}'
#                 and check_out_date >= '{today}'
#             """
#     with psycopg2.connect(**DB_CONFIG) as conn:
#         with conn.cursor() as cursor:
#             cursor.execute(query)
#             return cursor.fetchall()