from database.db_properties import (
    save_to_cart,
    fetch_user_cart,
    remove_from_cart
)

from utils import session_manager


def add_to_cart_controller(property_id):

    user = session_manager.current_user

    if user is None:
        return "No active user"

    result = save_to_cart(
        user["user_id"],
        property_id
    )

    return result


def load_cart_controller():

    user = session_manager.current_user

    if user is None:
        return []

    cart_items = fetch_user_cart(
        user["user_id"]
    )

    return cart_items


def remove_from_cart_controller(property_id):

    user = session_manager.current_user

    if user is None:
        return False

    result = remove_from_cart(
        user["user_id"],
        property_id
    )

    return result