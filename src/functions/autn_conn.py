import psycopg2
import psycopg2.extras
from settings import DB_CONFIG
from service.hash import hash_password, check_password
from psycopg2 import extras

# Регистрация нового пользователя на странице "Регистрация"
def reg_new_user(login, password, user_type):
    query = """
            INSERT INTO users (username, password_hash, user_type)
            VALUES (%s, %s, %s);
        """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (login, password, user_type))


# Проверка существует ли пользователь с таким логином на странице "Регистрация"
def check_new_user_login(login):
    query = f"SELECT username,password_hash FROM users WHERE username = '{login}';"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchall()
            if (len(row) == 0):
                return 1
            else:
                return 0
            

def check_auth_user(login, password):
    """Проверяет аутентификационные данные пользователя."""
    query = "SELECT password_hash FROM users WHERE username = %s;"  # Use parameterized query
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute(query, (login,)) # Pass login as parameter
                result = cur.fetchone()
                if result:
                    hashed_password = result['password_hash']
                    if check_password(hashed_password, password):
                        return 0  # Success
                    else:
                        return 1  # Incorrect password
                else:
                    return 2  # User not found
    except psycopg2.Error as e:
        print(f"Database error: {e}")  # Log database errors for debugging
        return 3 # Database error
    except Exception as e:
        print(f"An unexpected error occurred: {e}") # Log other errors for debugging
        return 4 # Unexpected error
            
            
def return_user_data(login, password) -> list:
    query = f"""SELECT user_id, username, password_hash, user_type 
                FROM users 
                WHERE username = '{login}';"""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
