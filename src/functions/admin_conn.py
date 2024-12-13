from pandas import DataFrame
import psycopg2
import psycopg2.extras
from settings import DB_CONFIG
import psycopg2 # или другой драйвер вашей базы данных
import pandas as pd
import streamlit as st


def get_all_users() -> DataFrame:
    query = f"SELECT username,user_type FROM users"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return DataFrame(cursor.fetchall(), columns=['login', 'role'])
        

def get_all_employees():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Employees")
        rows = cur.fetchall()
        

        columns = [desc[0] for desc in cur.description]
        employees_df = pd.DataFrame(rows, columns=columns)

        cur.close()
        conn.close()
        return employees_df
    except psycopg2.Error as e:
        print(f"Ошибка при получении данных: {e}")
        return None

def update_employee_verify(employee_id, verify):
    try:
        conn = psycopg2.connect(**DB_CONFIG) # Замените на ваши данные
        cur = conn.cursor()
        cur.execute("UPDATE Employees SET verify = %s WHERE employee_id = %s", (verify, employee_id))
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        raise Exception(f"Ошибка при обновлении статуса: {e}")
    
def get_all_booking() -> DataFrame:
    query = """SELECT s.service_name, a.name, b.check_in_date, b.check_out_date,
                e.first_name, e.last_name, o.first_name, o.last_name, b.status
            FROM bookings b
            JOIN services s ON b.service_id = s.service_id
            JOIN animals a ON b.animal_id = a.animal_id
            JOIN employees e ON b.employee_id = e.employee_id
            JOIN owners o ON a.owner_id = o.owner_id
            ORDER BY b.check_in_date;"""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return DataFrame(cursor.fetchall(), columns=['service', 'name', 'check_in_date', 
                                                         'check_out_date', 'employee_first_name', 'employee_last_name', 
                                                         'owner_first_name', 'owner_last_name', 'status'])

def get_food():
    """Получает информацию о кормах из базы данных."""
    try:
        conn = psycopg2.connect(**DB_CONFIG) 
        cur = conn.cursor()
        cur.execute("SELECT food_id, food_name, description, price FROM food")
        food = cur.fetchall()
        cur.close()
        conn.close()
        return food
    except (Exception, psycopg2.Error) as error:
        st.error(f"Ошибка при получении информации о кормах: {error}")
        return []

def add_food(food_name, description, price):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("INSERT INTO food (food_name, description, price) VALUES (%s, %s, %s)", (food_name, description, price))
        conn.commit()
        cur.close()
        conn.close()
        st.success("Корм добавлен!") #Обновляем страницу после добавления
    except (Exception, psycopg2.Error) as error:
        st.error(f"Ошибка при добавлении корма: {error}")

def edit_food(food_name, description, price, selected_food_id):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("UPDATE food SET food_name = %s, description = %s, price = %s WHERE food_id = %s", (food_name, description, price, selected_food_id))
        conn.commit()
        cur.close()
        conn.close()
        st.success("Изменения сохранены!")
    except (Exception, psycopg2.Error) as error:
        st.error(f"Ошибка при сохранении изменений: {error}")


def delete_food(selected_food_id):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("DELETE FROM food WHERE food_id = %s", (selected_food_id,))
        conn.commit()
        cur.close()
        conn.close()
        st.success("Корм удален!")
    except (Exception, psycopg2.Error) as error:
        st.error(f"Ошибка при удалении корма: {error}")

def get_employees():
    """Получает информацию о сотрудниках из базы данных."""
    try:
        conn = psycopg2.connect(**DB_CONFIG) 
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                employee_id, first_name, last_name, phone, email, role, description, address, verify
            FROM employees
        """)
        employees = cur.fetchall()
        cur.close()
        conn.close()
        return employees
    except (Exception, psycopg2.Error) as error:
        st.error(f"Ошибка при получении информации о сотрудниках: {error}")
        return []

def update_employee_status(employee_id, status):
    """Обновляет статус бронирования."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("UPDATE employees SET verify = %s WHERE employee_id = %s", (status, employee_id))
        conn.commit()
        cur.close()
        conn.close()
        st.success(f"Статус сотрудника изменен.")
    except (Exception, psycopg2.Error) as error:
        st.error(f"Ошибка при обновлении статуса сотрудника: {error}")

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
    
def add_service(service_name, description, price):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("INSERT INTO services (service_name, description, price) VALUES (%s, %s, %s)", (service_name, description, price))
        conn.commit()
        cur.close()
        conn.close()
        st.success("Услуга добавлена!") #Обновляем страницу после добавления
    except (Exception, psycopg2.Error) as error:
        st.error(f"Ошибка при добавлении услуги: {error}")

def delete_service(selected_service_id):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("DELETE FROM services WHERE service_id = %s", (selected_service_id,))
        conn.commit()
        cur.close()
        conn.close()
        st.success("Услуга удалена!")
    except (Exception, psycopg2.Error) as error:
        st.error(f"Ошибка при удалении услуги: {error}")

def edit_service(service_name, description, price, selected_service_id):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("UPDATE services SET service_name = %s, description = %s, price = %s WHERE service_id = %s", (service_name, description, price, selected_service_id))
        conn.commit()
        cur.close()
        conn.close()
        st.success("Изменения сохранены!")
    except (Exception, psycopg2.Error) as error:
        st.error(f"Ошибка при сохранении изменений: {error}")