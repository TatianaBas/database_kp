import streamlit as st
import psycopg2
from settings import DB_CONFIG

def get_employees():
    """Получает информацию о сотрудниках из базы данных."""
    try:
        conn = psycopg2.connect(**DB_CONFIG) 
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                employee_id, first_name, last_name, phone, email, role, description, address
            FROM employees
        """)
        employees = cur.fetchall()
        cur.close()
        conn.close()
        return employees
    except (Exception, psycopg2.Error) as error:
        st.error(f"Ошибка при получении информации о сотрудниках: {error}")
        return []
    
def get_food():
    """Получает информацию о кормах из базы данных."""
    try:
        conn = psycopg2.connect(**DB_CONFIG) 
        cur = conn.cursor()
        cur.execute("SELECT food_id, food_name, description, price FROM food")
        food_items = cur.fetchall()
        cur.close()
        conn.close()
        return food_items
    except (Exception, psycopg2.Error) as error:
        st.error(f"Ошибка при получении информации о кормах: {error}")
        return []

def get_services():
    """Получает информацию об услугах из базы данных."""
    try:
        conn = psycopg2.connect(**DB_CONFIG) 
        cur = conn.cursor()
        cur.execute("SELECT service_id, service_name, description, price FROM services")
        services = cur.fetchall()
        cur.close()
        conn.close()
        return services
    except (Exception, psycopg2.Error) as error:
        st.error(f"Ошибка при получении информации об услугах: {error}")
        return []