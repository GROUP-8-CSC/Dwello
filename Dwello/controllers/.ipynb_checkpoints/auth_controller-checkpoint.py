from database.db_auth import (
    register_user,
    verify_login,
    create_session,
    logout_user
)

from utils import session_manager


def signup_controller(full_name, email, password):

    if not full_name or not email or not password:
        return "All fields are required"

    result = register_user(
        full_name,
        email,
        password
    )

    return result


def login_controller(email, password):

    if not email or not password:
        return None

    user = verify_login(email, password)

    if user:

        session_manager.current_user = user

        create_session(user["user_id"])

        return user

    return None


def logout_controller():

    user = session_manager.current_user

    if user:

        logout_user(user["user_id"])

        session_manager.current_user = None
    
    