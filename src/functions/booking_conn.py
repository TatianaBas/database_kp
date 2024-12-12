
import streamlit as st
import datetime
import psycopg2
from functions.profile_conn import get_owner_data
from settings import DB_CONFIG

def get_services():
    """Получает список услуг из базы данных."""
    try:
        conn = psycopg2.connect(**DB_CONFIG) #Замените на ваши данные
        cur = conn.cursor()
        cur.execute("SELECT service_id, service_name, price FROM services")
        services = cur.fetchall()
        cur.close()
        conn.close()
        return services
    except (Exception, psycopg2.Error) as error:
        st.error(f"Ошибка при получении списка услуг: {error}")
        return []


def get_employees():
    """Получает список сотрудников из базы данных."""
    try:
        conn = psycopg2.connect(**DB_CONFIG) #Замените на ваши данные
        cur = conn.cursor()
        cur.execute("SELECT employee_id, first_name || ' ' || last_name FROM employees") # выводим ФИО
        employees = cur.fetchall()
        cur.close()
        conn.close()
        return employees
    except (Exception, psycopg2.Error) as error:
        st.error(f"Ошибка при получении списка сотрудников: {error}")
        return []

def get_food():
    """Получает список кормов из базы данных."""
    try:
        conn = psycopg2.connect(**DB_CONFIG) #Замените на ваши данные
        cur = conn.cursor()
        cur.execute("SELECT food_id, food_name, price FROM food")
        food = cur.fetchall()
        cur.close()
        conn.close()
        return food
    except (Exception, psycopg2.Error) as error:
        st.error(f"Ошибка при получении списка кормов: {error}")
        return []

def add_booking(animal_id, service_id, check_in_date, check_out_date, employee_id, food_id, price):
  """Добавляет бронирование в базу данных."""
  try:
      conn = psycopg2.connect(**DB_CONFIG) #Замените на ваши данные
      cur = conn.cursor()
      cur.execute("""
          INSERT INTO bookings (animal_id, service_id, check_in_date, check_out_date, status, employee_id, food_id, price)
          VALUES (%s, %s, %s, %s, 'Waiting', %s, %s, %s)
      """, (animal_id, service_id, check_in_date, check_out_date, employee_id, food_id, price))
      conn.commit()
      cur.close()
      conn.close()
      st.success("Бронирование успешно создано!")
  except (Exception, psycopg2.Error) as error:
      st.error(f"Ошибка при создании бронирования: {error}")


def add_animal(owner_id, animal_type, breed, name, birth_date, special_needs):
    """Добавляет животное в базу данных."""
    try:
        conn = psycopg2.connect(**DB_CONFIG) #Замените на ваши данные
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO animals (owner_id, animal_type, breed, name, birth_date, special_needs)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING animal_id;
        """, (owner_id, animal_type, breed, name, birth_date, special_needs))
        animal_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return animal_id
    except (Exception, psycopg2.Error) as error:
        st.error(f"Ошибка при добавлении животного: {error}")
        return None