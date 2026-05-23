from db_connection import connect_db


def fetch_properties(region, budget):

    connection = connect_db()

    if connection is None:
        return []

    cursor = connection.cursor()

    query = """
    SELECT *
    FROM properties
    WHERE region = %s
    AND price <= %s
    ORDER BY price ASC
    """

    cursor.execute(query, (region, budget))

    properties = cursor.fetchall()

    cursor.close()
    connection.close()

    return properties


def fetch_all_properties():

    connection = connect_db()

    if connection is None:
        return []

    cursor = connection.cursor()

    query = """
    SELECT *
    FROM properties
    ORDER BY created_at DESC
    """

    cursor.execute(query)

    properties = cursor.fetchall()

    cursor.close()
    connection.close()

    return properties


def save_to_cart(user_id, property_id):

    connection = connect_db()

    if connection is None:
        return False

    cursor = connection.cursor()

    check_query = """
    SELECT *
    FROM saved_properties
    WHERE user_id = %s
    AND property_id = %s
    """

    cursor.execute(check_query, (user_id, property_id))

    existing_item = cursor.fetchone()

    if existing_item:
        cursor.close()
        connection.close()
        return "Property already saved"

    insert_query = """
    INSERT INTO saved_properties
    (user_id, property_id)
    VALUES (%s, %s)
    """

    cursor.execute(insert_query, (user_id, property_id))

    connection.commit()

    cursor.close()
    connection.close()

    return True


def fetch_user_cart(user_id):

    connection = connect_db()

    if connection is None:
        return []

    cursor = connection.cursor()

    query = """
    SELECT
        properties.property_id,
        properties.title,
        properties.region,
        properties.neighborhood,
        properties.price,
        properties.description,
        properties.image_path
    FROM saved_properties
    JOIN properties
    ON saved_properties.property_id = properties.property_id
    WHERE saved_properties.user_id = %s
    """

    cursor.execute(query, (user_id,))

    cart_items = cursor.fetchall()

    cursor.close()
    connection.close()

    return cart_items


def remove_from_cart(user_id, property_id):

    connection = connect_db()

    if connection is None:
        return False

    cursor = connection.cursor()

    query = """
    DELETE FROM saved_properties
    WHERE user_id = %s
    AND property_id = %s
    """

    cursor.execute(query, (user_id, property_id))

    connection.commit()

    cursor.close()
    connection.close()

    return True


def search_by_neighborhood(neighborhood):

    connection = connect_db()

    if connection is None:
        return []

    cursor = connection.cursor()

    query = """
    SELECT *
    FROM properties
    WHERE neighborhood ILIKE %s
    """

    cursor.execute(query, (f"%{neighborhood}%",))

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results