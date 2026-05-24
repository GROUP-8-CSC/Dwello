"""
controllers/auth_controller.py
Dwello – Authentication Controller

Called by: ui/auth_screen.py
Calls to:  database layer (db/auth_queries.py or similar)

Replace the stub logic below with real DB calls.
"""


def login_controller(email: str, password: str) -> dict:
    """
    Verify user credentials against the database.

    Parameters
    ----------
    email    : str  – user-supplied email
    password : str  – user-supplied plain-text password

    Returns
    -------
    dict with keys:
        success  : bool
        user     : dict | None   – e.g. {"id": 1, "name": "Josemaria", "email": "..."}
        message  : str           – error description on failure
    """
    # ── TODO: replace with real DB call ───────────────────────────────────────
    # from db.auth_queries import verify_login
    # return verify_login(email, password)

    if not email or not password:
        return {"success": False, "message": "Email and password are required."}

    # Stub: accept any non-empty credentials
    return {
        "success": True,
        "user": {"id": 1, "name": "Josemaria", "email": email},
        "message": "",
    }


def signup_controller(name: str, email: str, password: str) -> dict:
    """
    Register a new user in the database.

    Parameters
    ----------
    name     : str
    email    : str
    password : str  – plain text (hash before storing)

    Returns
    -------
    dict with keys:
        success  : bool
        user     : dict | None
        message  : str
    """
    # ── TODO: replace with real DB call ───────────────────────────────────────
    # from db.auth_queries import create_user
    # return create_user(name, email, password)

    if not name or not email or not password:
        return {"success": False, "message": "All fields are required."}

    if len(password) < 6:
        return {"success": False, "message": "Password must be at least 6 characters."}

    # Stub: always succeeds
    return {
        "success": True,
        "user": {"id": 1, "name": name, "email": email},
        "message": "",
    }
