"""
ui/cart_screen.py
Dwello – Cart Screen  (Saved / bookmarked properties)

Renamed from: cart.py
Shows all properties the user has added to their cart.
"Added to Cart" state is pre-set on all cards shown here.
"""

import tkinter as tk
from tkinter import font as tkfont, messagebox
from PIL import Image, ImageTk
import os, pathlib, sys

# ── Asset paths ────────────────────────────────────────────────────────────────
_HERE   = pathlib.Path(__file__).parent
_ASSETS = _HERE.parent / "assets" / "images"

def _p(name):
    return str(_ASSETS / name)

LOGO_FILE    = _p("dwello_logo.png")
ICON_HOME    = _p("house.png")
ICON_EXPLORE = _p("compass.png")
ICON_CART    = _p("shopping-cart.png")

FALLBACK_IMGS = [_p(f"{i}.jpeg") for i in range(1, 7)]

# ── Palette ────────────────────────────────────────────────────────────────────
SB_BG        = "#1B3A2D"
SB_ACTIVE    = "#2E6B45"
SB_TEXT      = "#FFFFFF"
SB_MUTED     = "#8FBB9E"
MAIN_BG      = "#FFFFFF"
PANEL_BG     = "#F0F0F0"
ACCENT       = "#2E7D52"
PRICE_BG     = "#D6EFE0"
PRICE_TEXT   = "#1F6B3E"
HEADING      = "#111111"
SUBTEXT      = "#666666"
CARD_BG      = "#FFFFFF"
CARD_BORDER  = "#E0E0E0"
BTN_OUTLINE  = "#2E7D52"
BTN_ADDED_FG = "#2E7D52"
SUMM_BG      = "#FFFFFF"
SUMM_BORDER  = "#DDDDDD"
ICON_SZ      = 26
LOGO_SZ      = 80
PROP_W       = 217
PROP_H       = 216

# ── Image cache ────────────────────────────────────────────────────────────────
_img_cache = {}

def _load(path, size, tint=None):
    key = (path, size, tint)
    if key in _img_cache:
        return _img_cache[key]
    if not os.path.exists(path):
        _img_cache[key] = None
        return None
    try:
        img = Image.open(path).convert("RGBA").resize(size, Image.LANCZOS)
        if tint:
            _, _, _, a = img.split()
            colored = Image.new("RGBA", img.size, tint + (255,))
            colored.putalpha(a)
            img = colored
        tk_img = ImageTk.PhotoImage(img)
        _img_cache[key] = tk_img
        return tk_img
    except Exception:
        _img_cache[key] = None
        return None

def _logo():            return _load(LOGO_FILE,    (LOGO_SZ, LOGO_SZ))
def _icon_white(path):  return _load(path, (ICON_SZ, ICON_SZ), tint=(255, 255, 255))
def _icon_dark(path):   return _load(path, (ICON_SZ, ICON_SZ), tint=(46, 125, 82))
def _prop_img(path):    return _load(path, (PROP_W, PROP_H))


# ══════════════════════════════════════════════════════════════════════════════
class CartScreen(tk.Toplevel):
    """
    Displays all properties saved by the current user.

    Public functions (per UI breakdown):
        load_cart()                     – fetch items via controller
        remove_cart_item(property_id)   – remove via controller + refresh UI
    """

    SAMPLE_DATA = [
        {"id": 1, "title": "2 Bedroom Apartment",  "location": "Yaba, Lagos Mainland",            "price": "₦4,000,000.00"},
        {"id": 2, "title": "Luxury House",          "location": "Victoria Island, Lagos Mainland", "price": "₦4,500,000.00"},
        {"id": 3, "title": "Standard Duplex",       "location": "Yaba, Lagos Mainland",            "price": "₦3,800,000.00"},
        {"id": 4, "title": "6 Bedroom House",       "location": "Banana Island, Lagos Mainland",   "price": "₦5,000,000.00"},
        {"id": 5, "title": "Mini Flat",             "location": "Surulere, Lagos Mainland",        "price": "₦2,500,000.00"},
        {"id": 6, "title": "Penthouse Suite",       "location": "Lekki, Lagos Mainland",           "price": "₦4,900,000.00"},
    ]

    def __init__(self, master=None, user=None, **kw):
        super().__init__(master, **kw)
        self.title("Dwello – My Cart")
        self.geometry("1200x760")
        self.minsize(1100, 680)
        self.configure(bg=SB_BG)

        self.user = user
        self._cart_items = []

        self._init_fonts()
        self._preload_images()
        self._build_layout()
        self.load_cart()

    # ── Fonts ─────────────────────────────────────────────────────────────────
    def _init_fonts(self):
        F = tkfont.Font
        self.fnt = {
            "logo"   : F(family="Helvetica", size=15, weight="bold"),
            "nav"    : F(family="Helvetica", size=11),
            "nav_b"  : F(family="Helvetica", size=11, weight="bold"),
            "logout" : F(family="Helvetica", size=11, weight="bold"),
            "heading": F(family="Helvetica", size=14, weight="bold"),
            "title"  : F(family="Helvetica", size=11, weight="bold"),
            "sub"    : F(family="Helvetica", size=9),
            "price"  : F(family="Helvetica", size=9,  weight="bold"),
            "btn"    : F(family="Helvetica", size=10, weight="bold"),
            "search" : F(family="Helvetica", size=11),
        }

    # ── Images ────────────────────────────────────────────────────────────────
    def _preload_images(self):
        self.img_logo      = _logo()
        self.img_home_w    = _icon_white(ICON_HOME)
        self.img_home_g    = _icon_dark(ICON_HOME)
        self.img_explore_w = _icon_white(ICON_EXPLORE)
        self.img_cart_w    = _icon_white(ICON_CART)
        self.fallback_imgs = [_prop_img(p) for p in FALLBACK_IMGS]

    # ── Layout ────────────────────────────────────────────────────────────────
    def _build_layout(self):
        self.sidebar = tk.Frame(self, bg=SB_BG, width=210)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        self._build_sidebar()

        self.centre = tk.Frame(self, bg=MAIN_BG)
        self.centre.pack(side="left", fill="both", expand=True)
        self._build_centre()

    # ── Sidebar ───────────────────────────────────────────────────────────────
    def _build_sidebar(self):
        sb = self.sidebar

        top_bar = tk.Frame(sb, bg=SB_BG)
        top_bar.pack(fill="x", padx=10, pady=(10, 0))
        tk.Label(top_bar, text="←", fg=SB_TEXT, bg=SB_BG,
                 font=tkfont.Font(family="Helvetica", size=14, weight="bold"),
                 cursor="hand2").pack(side="right")

        logo_frame = tk.Frame(sb, bg=SB_BG, pady=6)
        logo_frame.pack(fill="x")
        if self.img_logo:
            tk.Label(logo_frame, image=self.img_logo, bg=SB_BG).pack()
        tk.Label(logo_frame, text="DWELLO", fg=SB_TEXT, bg=SB_BG,
                 font=self.fnt["logo"]).pack(pady=(4, 0))

        tk.Frame(sb, bg="#2D5A40", height=1).pack(fill="x", padx=18, pady=6)

        self._nav_item(sb, self.img_home_g,    "Dashboard", active=False)
        self._nav_item(sb, self.img_explore_w, "Explore",   active=False)
        self._nav_item(sb, self.img_cart_w,    "Cart",      active=True)

        tk.Frame(sb, bg=SB_BG).pack(fill="both", expand=True)
        self._logout_btn(sb)

    def _nav_item(self, parent, icon, label, active=False):
        bg  = SB_ACTIVE if active else SB_BG
        fg  = SB_TEXT   if active else SB_MUTED
        fnt = self.fnt["nav_b"] if active else self.fnt["nav"]
        row = tk.Frame(parent, bg=bg, cursor="hand2")
        row.pack(fill="x", pady=1)
        inner = tk.Frame(row, bg=bg, padx=18, pady=10)
        inner.pack(fill="x")
        if icon:
            tk.Label(inner, image=icon, bg=bg).pack(side="left")
        tk.Label(inner, text=label, fg=fg, bg=bg, font=fnt).pack(side="left", padx=10)

    def _logout_btn(self, parent):
        frame = tk.Frame(parent, bg=SB_BG, pady=22)
        frame.pack(fill="x")
        c = tk.Canvas(frame, bg=SB_BG, highlightthickness=0, height=44, width=150)
        c.pack(padx=20)
        c.create_rectangle(2, 2, 148, 42, outline=SB_TEXT, width=1.5, fill=SB_BG)
        c.create_text(20, 22, text="←", fill=SB_TEXT,
                      font=tkfont.Font(family="Helvetica", size=13, weight="bold"))
        c.create_text(82, 22, text="Log Out", fill=SB_TEXT, font=self.fnt["logout"])
        c.bind("<Button-1>", lambda e: self.destroy())

    # ── Centre ────────────────────────────────────────────────────────────────
    def _build_centre(self):
        c = self.centre

        # Header
        hdr = tk.Frame(c, bg=MAIN_BG, pady=18)
        hdr.pack(fill="x", padx=30)
        tk.Label(hdr, text="My Cart", font=self.fnt["heading"],
                 fg=HEADING, bg=MAIN_BG).pack(side="left")

        # Search bar
        sb_frame = tk.Frame(hdr, bg=PANEL_BG, bd=1,
                            highlightbackground="#CCCCCC", highlightthickness=1)
        sb_frame.pack(side="left", padx=(20, 0))
        tk.Label(sb_frame, text="🔍", bg=PANEL_BG,
                 font=self.fnt["search"], fg="#888888").pack(side="left", padx=(10, 4), pady=8)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(sb_frame, textvariable=self.search_var,
                                font=self.fnt["search"], fg="#888888",
                                bg=PANEL_BG, relief="flat", bd=0, width=28)
        search_entry.insert(0, "Search Cart")
        search_entry.pack(side="left", ipady=8, padx=(0, 12))
        self._placeholder(search_entry, "Search Cart")

        # Scrollable cards
        scroll_wrap = tk.Frame(c, bg=MAIN_BG)
        scroll_wrap.pack(fill="both", expand=True, padx=30, pady=(0, 10))

        canvas_scroll = tk.Canvas(scroll_wrap, bg=MAIN_BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(scroll_wrap, orient="vertical",
                                 command=canvas_scroll.yview)
        canvas_scroll.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas_scroll.pack(side="left", fill="both", expand=True)

        self.card_frame = tk.Frame(canvas_scroll, bg=MAIN_BG)
        self._card_window = canvas_scroll.create_window(
            (0, 0), window=self.card_frame, anchor="nw")

        self.card_frame.bind("<Configure>",
            lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all")))
        canvas_scroll.bind("<Configure>",
            lambda e: canvas_scroll.itemconfig(self._card_window, width=e.width))
        canvas_scroll.bind_all("<MouseWheel>",
            lambda e: canvas_scroll.yview_scroll(-1*(e.delta//120), "units"))

        self._canvas_scroll = canvas_scroll

    # ══════════════════════════════════════════════════════════════════════════
    # PUBLIC: load_cart
    # ══════════════════════════════════════════════════════════════════════════
    def load_cart(self):
        """
        Fetch cart items from DB and render cards.
        Wires to: controllers/cart_controller.py :: load_cart_controller()
        """
        from controllers.cart_controller import load_cart_controller

        result = load_cart_controller(user=self.user)

        if result["success"]:
            self._cart_items = result.get("items", [])
        else:
            # Fall back to sample data so UI still renders
            self._cart_items = self.SAMPLE_DATA

        self._render_cards()

    def _render_cards(self):
        for w in self.card_frame.winfo_children():
            w.destroy()

        for idx, prop in enumerate(self._cart_items):
            col = idx % 3
            row = idx // 3
            self._cart_card(self.card_frame, prop, row, col, idx)

    def _cart_card(self, parent, prop, grid_row, grid_col, fallback_idx):
        prop_id  = prop.get("id")
        title    = prop.get("title", "Property")
        location = prop.get("location", "Lagos")
        price    = prop.get("price", "₦0")
        img_path = prop.get("image_path")

        card = tk.Frame(parent, bg=CARD_BG, bd=1,
                        highlightbackground=CARD_BORDER, highlightthickness=1,
                        cursor="hand2")
        card.grid(row=grid_row, column=grid_col, padx=8, pady=8, sticky="nsew")
        parent.grid_columnconfigure(grid_col, weight=1)

        img = None
        if img_path and os.path.exists(img_path):
            img = _prop_img(img_path)
        elif fallback_idx < len(self.fallback_imgs):
            img = self.fallback_imgs[fallback_idx]

        if img:
            lbl = tk.Label(card, image=img, bg=CARD_BG)
            lbl.image = img
        else:
            lbl = tk.Label(card, bg="#CCCCCC", width=PROP_W, height=PROP_H,
                           text="No image", fg="#888888")
        lbl.pack()

        content = tk.Frame(card, bg=CARD_BG, padx=12, pady=10)
        content.pack(fill="x")
        tk.Label(content, text=title, font=self.fnt["title"],
                 fg=HEADING, bg=CARD_BG, anchor="w").pack(fill="x")
        tk.Label(content, text=location, font=self.fnt["sub"],
                 fg=SUBTEXT, bg=CARD_BG, anchor="w").pack(fill="x", pady=(2, 6))

        price_badge = tk.Frame(content, bg=PRICE_BG, padx=6, pady=3)
        price_badge.pack(anchor="w")
        tk.Label(price_badge, text=price, font=self.fnt["price"],
                 fg=PRICE_TEXT, bg=PRICE_BG).pack()

        # "Added to Cart" — outline style
        btn = tk.Canvas(content, bg=CARD_BG, highlightthickness=0,
                        height=38, width=PROP_W - 24)
        btn.pack(pady=(10, 2))
        btn.create_rectangle(0, 0, PROP_W - 24, 38,
                             fill=CARD_BG, outline=BTN_OUTLINE, width=1.5)
        btn.create_text((PROP_W - 24) // 2, 19,
                        text="Added to Cart", fill=BTN_ADDED_FG, font=self.fnt["btn"])
        btn.bind("<Button-1>", lambda e, pid=prop_id: self.remove_cart_item(pid))
        btn.bind("<Enter>", lambda e, b=btn: b.itemconfig(1, fill="#F5FFF8"))
        btn.bind("<Leave>", lambda e, b=btn: b.itemconfig(1, fill=CARD_BG))

    # ══════════════════════════════════════════════════════════════════════════
    # PUBLIC: remove_cart_item
    # ══════════════════════════════════════════════════════════════════════════
    def remove_cart_item(self, property_id):
        """
        Remove item from cart on button click.
        Wires to: controllers/cart_controller.py :: remove_from_cart_controller()
        """
        from controllers.cart_controller import remove_from_cart_controller

        result = remove_from_cart_controller(user=self.user, property_id=property_id)

        if result["success"]:
            self._cart_items = [p for p in self._cart_items if p.get("id") != property_id]
            self._render_cards()
        else:
            messagebox.showerror("Error", result.get("message", "Could not remove item"))

    # ── Placeholder helper ────────────────────────────────────────────────────
    def _placeholder(self, entry, text):
        def on_in(e):
            if entry.get() == text:
                entry.delete(0, "end")
                entry.config(fg=HEADING)
        def on_out(e):
            if entry.get() == "":
                entry.insert(0, text)
                entry.config(fg="#888888")
        entry.bind("<FocusIn>",  on_in)
        entry.bind("<FocusOut>", on_out)


# ── Stand-alone entry ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
    root = tk.Tk()
    root.withdraw()
    app = CartScreen(master=root)
    app.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()
