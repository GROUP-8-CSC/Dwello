from db_connection import connect_db

import bcrypt


def register_user(full_name, email, password):
    connection = connect_db()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:
        check_query = """
        SELECT 1
        FROM users
        WHERE email = %s
        """

        cursor.execute(check_query, (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return "Email already exists"

        hashed_password = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

        insert_query = """
        INSERT INTO users
        (full_name, email, password_hash)
        VALUES (%s, %s, %s)
        """

        cursor.execute(
            insert_query,
            (full_name, email, hashed_password)
        )

        connection.commit()
        return True
    finally:
        cursor.close()
        connection.close()


def verify_login(email, password):
    connection = connect_db()

    if connection is None:
        return None

    cursor = connection.cursor()

    try:
        query = """
        SELECT user_id, full_name, email, password_hash
        FROM users
        WHERE email = %s
        """

        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if not user:
            return None

        stored_password = user[3]

        if bcrypt.checkpw(password.encode(), stored_password.encode()):
            return {
                "user_id": user[0],
                "full_name": user[1],
                "email": user[2]
            }

        return None
    finally:
        cursor.close()
        connection.close()


def create_session(user_id):
    connection = connect_db()

    if connection is None:
        return None

    cursor = connection.cursor()

    try:
        query = """
        INSERT INTO sessions
        (user_id, is_active)
        VALUES (%s, TRUE)
        RETURNING session_id
        """

        cursor.execute(query, (user_id,))
        session_id = cursor.fetchone()[0]
        connection.commit()
        return session_id
    finally:
        cursor.close()
        connection.close()


def logout_user(session_id):
    connection = connect_db()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:
        query = """
        UPDATE sessions
        SET is_active = FALSE
        WHERE session_id = %s
        """

        cursor.execute(query, (session_id,))
        connection.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
        connection.close()