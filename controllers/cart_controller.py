"""
controllers/cart_controller.py
Dwello – Cart Controller

Called by:
    ui/marketplace_screen.py  – handle_save_property(), load_cart(), remove_cart_item()
    ui/cart_screen.py         – load_cart(), remove_cart_item()
Calls to:
    database layer (db/cart_queries.py or similar)
"""

# In-memory cart store (replace with DB calls)
_in_memory_cart: dict[int, list] = {}   # user_id → [property_dict, ...]


def _get_user_id(user) -> int:
    if user is None:
        return 0
    if isinstance(user, dict):
        return user.get("id", 0)
    return getattr(user, "id", 0)


def add_to_cart_controller(user, property_id: int) -> dict:
    """
    Save a property to the user's cart.

    Parameters
    ----------
    user        : dict | object | None
    property_id : int

    Returns
    -------
    dict  { success: bool, message: str }
    """
    # ── TODO: replace with real DB call ───────────────────────────────────────
    # from db.cart_queries import save_to_cart
    # return save_to_cart(user_id, property_id)

    uid = _get_user_id(user)
    cart = _in_memory_cart.setdefault(uid, [])

    if any(p["id"] == property_id for p in cart):
        return {"success": False, "message": "Already in cart"}

    cart.append({"id": property_id})
    return {"success": True, "message": ""}


def load_cart_controller(user) -> dict:
    """
    Fetch all cart items for the user.

    Returns
    -------
    dict  { success: bool, items: list[dict], message: str }
    Each item dict has at minimum: id, title, location, price, image_path
    """
    # ── TODO: replace with real DB call ───────────────────────────────────────
    # from db.cart_queries import fetch_user_cart
    # return fetch_user_cart(user_id)

    uid   = _get_user_id(user)
    items = _in_memory_cart.get(uid, [])

    return {"success": True, "items": items, "message": ""}


def remove_from_cart_controller(user, property_id: int) -> dict:
    """
    Remove a property from the user's cart.

    Returns
    -------
    dict  { success: bool, message: str }
    """
    # ── TODO: replace with real DB call ───────────────────────────────────────
    # from db.cart_queries import delete_from_cart
    # return delete_from_cart(user_id, property_id)

    uid  = _get_user_id(user)
    cart = _in_memory_cart.get(uid, [])
    before = len(cart)
    _in_memory_cart[uid] = [p for p in cart if p["id"] != property_id]

    if len(_in_memory_cart[uid]) < before:
        return {"success": True, "message": ""}
    return {"success": False, "message": "Item not found in cart"}
