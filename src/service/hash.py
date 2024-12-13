import streamlit as st
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def check_password(hashed_password, provided_password):
    """Проверяет совпадение bcrypt-хеша с введенным паролем."""
    try:
        return bcrypt.checkpw(provided_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except (TypeError, bcrypt.Error) as e:
        st.error(f"Ошибка проверки пароля: {e}")
        return False