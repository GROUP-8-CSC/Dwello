import tkinter as tk
from tkinter import font as tkfont
import os, pathlib

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# Change lines 11 to 31 to use this robust directory pathing:

_HERE = pathlib.Path(__file__).parent
# Go up a level from 'ui' folder to root, then hit assets/images
_ASSETS_DIR = _HERE.parent / "assets" / "images"

def _p(name):
    return str(_ASSETS_DIR / name)

LOGO_FILE    = _p("dwello_logo.png")
ICON_HOME    = _p("house.png")         # Fixed typo from "house.ong"
ICON_EXPLORE = _p("compass.png")
ICON_CART    = _p("shopping-cart.png")

CARD_IMGS = [
    _p("6.jpeg"),   
    _p("5.jpeg"),   
    _p("4.jpeg"),   
    _p("3.jpeg"),      
    _p("2.jpeg"),   
    _p("1.jpeg"),   
]

CARD_DATA = [
    ("2 Bedroom Apartment",  "Yaba, Lagos Mainland",           "₦4,000,000.00"),
    ("Luxury House",         "Victoria Island, Lagos Mainland","₦4,500,000.00"),
    ("Standard Duplex",      "Yaba, Lagos Mainland",           "₦3,800,000.00"),
    ("6 Bedroom House",      "Banana Island, Lagos Mainland",  "₦5,000,000.00"),
    ("Mini Flat",            "Surulere, Lagos Mainland",       "₦2,500,000.00"),
    ("Penthouse Suite",      "Lekki, Lagos Mainland",          "₦4,900,000.00"),
]

# ── Palette ───────────────────────────────────────────────────────────────────
SB_BG        = "#1B3A2D"   # sidebar dark green
SB_ACTIVE    = "#2E6B45"   # active nav row
SB_TEXT      = "#FFFFFF"
SB_MUTED     = "#8FBB9E"
MAIN_BG      = "#FFFFFF"
PANEL_BG     = "#F0F0F0"   # right panel & search bar bg
ACCENT       = "#2E7D52"   # buttons, price badge bg
ACCENT_DARK  = "#1F5C3A"   # button hover
PRICE_BG     = "#D6EFE0"   # light-green price badge
PRICE_TEXT   = "#1F6B3E"
HEADING      = "#111111"
SUBTEXT      = "#666666"
CARD_BG      = "#FFFFFF"
CARD_BORDER  = "#E0E0E0"
BTN_TEXT     = "#FFFFFF"
BTN_OUTLINE  = "#2E7D52"   # outline colour for "Added to Cart" border button
BTN_ADDED_FG = "#2E7D52"   # text colour for "Added to Cart"
SUMM_BG      = "#FFFFFF"
SUMM_BORDER  = "#DDDDDD"
ICON_SZ      = 26          # 26.35 → 26px
LOGO_SZ      = 80          # sidebar display size
PROP_W       = 217
PROP_H       = 216         # ≈215.64

# ── Image helpers ─────────────────────────────────────────────────────────────
_img_cache = {}

def _load(path, size, tint=None):
    key = (path, size, tint)
    if key in _img_cache:
        return _img_cache[key]
    if not HAS_PIL or not os.path.exists(path):
        _img_cache[key] = None
        return None
    try:
        img = Image.open(path).convert("RGBA").resize(size, Image.LANCZOS)
        if tint:
            r, g, b, a = img.split()
            colored = Image.new("RGBA", img.size, tint + (255,))
            colored.putalpha(a)
            img = colored
        tk_img = ImageTk.PhotoImage(img)
        _img_cache[key] = tk_img
        return tk_img
    except Exception:
        _img_cache[key] = None
        return None


def logo_img():
    return _load(LOGO_FILE, (LOGO_SZ, LOGO_SZ))

def icon_white(path):
    return _load(path, (ICON_SZ, ICON_SZ), tint=(255, 255, 255))

def icon_dark(path):
    return _load(path, (ICON_SZ, ICON_SZ), tint=(46, 125, 82))

def prop_img(path):
    return _load(path, (PROP_W, PROP_H))


# ══════════════════════════════════════════════════════════════════════════════
class DwelloSearch(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dwello – Search Results")
        self.geometry("1200x760")
        self.minsize(1100, 680)
        self.configure(bg=SB_BG)

        self._fonts()
        self._preload_images()
        self._build()

    # ── Fonts ─────────────────────────────────────────────────────────────────
    def _fonts(self):
        self.fnt = {
            "logo"    : tkfont.Font(family="Helvetica", size=15, weight="bold"),
            "nav"     : tkfont.Font(family="Helvetica", size=11),
            "nav_b"   : tkfont.Font(family="Helvetica", size=11, weight="bold"),
            "logout"  : tkfont.Font(family="Helvetica", size=11, weight="bold"),
            "heading" : tkfont.Font(family="Helvetica", size=14, weight="bold"),
            "title"   : tkfont.Font(family="Helvetica", size=11, weight="bold"),
            "sub"     : tkfont.Font(family="Helvetica", size=9),
            "price"   : tkfont.Font(family="Helvetica", size=9, weight="bold"),
            "btn"     : tkfont.Font(family="Helvetica", size=10, weight="bold"),
            "summ_h"  : tkfont.Font(family="Helvetica", size=13, weight="bold"),
            "summ_lbl": tkfont.Font(family="Helvetica", size=10, weight="bold"),
            "summ_val": tkfont.Font(family="Helvetica", size=10),
            "search"  : tkfont.Font(family="Helvetica", size=11),
        }

    # ── Pre-load ──────────────────────────────────────────────────────────────
    def _preload_images(self):
        self.img_logo        = logo_img()
        self.img_home_w      = icon_white(ICON_HOME)
        self.img_home_g      = icon_dark(ICON_HOME)
        self.img_explore_w   = icon_white(ICON_EXPLORE)
        self.img_cart_w      = icon_white(ICON_CART)
        self.img_props       = [prop_img(p) for p in CARD_IMGS] # ◄◄ Uses CARD_IMGS
        
    # ── Top-level layout ──────────────────────────────────────────────────────
    def _build(self):
        # Sidebar (fixed 210px)
        self.sidebar = tk.Frame(self, bg=SB_BG, width=210)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        self._build_sidebar()

        # Centre content (fills remaining space — no right panel)
        self.centre = tk.Frame(self, bg=MAIN_BG)
        self.centre.pack(side="left", fill="both", expand=True)
        self._build_centre()

    # ── Sidebar ───────────────────────────────────────────────────────────────
    def _build_sidebar(self):
        sb = self.sidebar

        # Back arrow (top-right of sidebar)
        top_bar = tk.Frame(sb, bg=SB_BG)
        top_bar.pack(fill="x", padx=10, pady=(10, 0))
        tk.Label(top_bar, text="←", fg=SB_TEXT, bg=SB_BG,
                 font=tkfont.Font(family="Helvetica", size=14, weight="bold"),
                 cursor="hand2").pack(side="right")

        # Logo
        logo_frame = tk.Frame(sb, bg=SB_BG, pady=6)
        logo_frame.pack(fill="x")
        if self.img_logo:
            tk.Label(logo_frame, image=self.img_logo, bg=SB_BG).pack()
        tk.Label(logo_frame, text="DWELLO", fg=SB_TEXT, bg=SB_BG,
                 font=self.fnt["logo"]).pack(pady=(4, 0))

        # Divider
        tk.Frame(sb, bg="#2D5A40", height=1).pack(fill="x", padx=18, pady=6)

        # Nav items  (Dashboard = active)
        self._nav_item(sb, self.img_home_g,    "Dashboard", active=True)
        self._nav_item(sb, self.img_explore_w, "Explore",   active=False)
        self._nav_item(sb, self.img_cart_w,    "Cart",      active=False)

        tk.Frame(sb, bg=SB_BG).pack(fill="both", expand=True)

        # Log Out
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

    # ── Centre (scrollable) ───────────────────────────────────────────────────
    def _build_centre(self):
        c = self.centre

        # Search bar row
        search_row = tk.Frame(c, bg=MAIN_BG, pady=18)
        search_row.pack(fill="x", padx=30)

        # Search box with magnifier
        sb_frame = tk.Frame(search_row, bg=PANEL_BG, bd=1,
                            highlightbackground="#CCCCCC", highlightthickness=1)
        sb_frame.pack(side="left")
        tk.Label(sb_frame, text="🔍", bg=PANEL_BG, font=self.fnt["search"],
                 fg="#888888").pack(side="left", padx=(10, 4), pady=8)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(sb_frame, textvariable=self.search_var,
                                font=self.fnt["search"], fg="#888888",
                                bg=PANEL_BG, relief="flat", bd=0, width=32)
        search_entry.insert(0, "Search Cart")
        search_entry.pack(side="left", ipady=8, padx=(0, 12))
        self._placeholder(search_entry, "Search Cart")

        # Small filter box (right of search)
        filter_box = tk.Frame(search_row, bg=PANEL_BG, bd=1,
                              highlightbackground="#CCCCCC", highlightthickness=1,
                              width=90, height=42)
        filter_box.pack(side="left", padx=(10, 0))
        filter_box.pack_propagate(False)

        # ── Scrollable card area ──────────────────────────────────────────────
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
            lambda e: canvas_scroll.configure(
                scrollregion=canvas_scroll.bbox("all")))
        canvas_scroll.bind("<Configure>",
            lambda e: canvas_scroll.itemconfig(
                self._card_window, width=e.width))
        canvas_scroll.bind_all("<MouseWheel>",
            lambda e: canvas_scroll.yview_scroll(-1*(e.delta//120), "units"))

        self._build_cards()

    def _placeholder(self, entry, text):
        def on_in(e):
            if entry.get() == text:
                entry.delete(0, "end")
                entry.config(fg=HEADING)
        def on_out(e):
            if entry.get() == "":
                entry.insert(0, text)
                entry.config(fg="#888888")
        entry.bind("<FocusIn>", on_in)
        entry.bind("<FocusOut>", on_out)

    def _build_cards(self):
        f = self.card_frame
        # 3 cards per row
        for idx, (title, loc, price) in enumerate(CARD_DATA):
            col = idx % 3
            row = idx // 3
            self._property_card(f, idx, title, loc, price, row, col)

    def _property_card(self, parent, idx, title, loc, price, grid_row, grid_col):
        card = tk.Frame(parent, bg=CARD_BG, bd=1,
                        highlightbackground=CARD_BORDER, highlightthickness=1,
                        cursor="hand2")
        card.grid(row=grid_row, column=grid_col, padx=8, pady=8, sticky="nsew")
        parent.grid_columnconfigure(grid_col, weight=1)

        # Property image
        img = self.img_props[idx] if idx < len(self.img_props) else None
        if img:
            lbl = tk.Label(card, image=img, bg=CARD_BG)
            lbl.image = img # ◄◄ CRITICAL: Keeps a reference so garbage collection doesn't delete it!
        else:
            lbl = tk.Label(card, bg="#CCCCCC", width=PROP_W, height=PROP_H,
                           text="No image", fg="#888888")
        lbl.pack()

        # Content area
        content = tk.Frame(card, bg=CARD_BG, padx=12, pady=10)
        content.pack(fill="x")

        tk.Label(content, text=title, font=self.fnt["title"],
                 fg=HEADING, bg=CARD_BG, anchor="w").pack(fill="x")
        tk.Label(content, text=loc, font=self.fnt["sub"],
                 fg=SUBTEXT, bg=CARD_BG, anchor="w").pack(fill="x", pady=(2, 6))

        # Price badge
        price_badge = tk.Frame(content, bg=PRICE_BG, padx=6, pady=3)
        price_badge.pack(anchor="w")
        tk.Label(price_badge, text=price, font=self.fnt["price"],
                 fg=PRICE_TEXT, bg=PRICE_BG).pack()

        # Added to Cart button — white background, green border & text
        btn = tk.Canvas(content, bg=CARD_BG, highlightthickness=0,
                        height=38, width=PROP_W - 24)
        btn.pack(pady=(10, 2))
        btn.create_rectangle(0, 0, PROP_W - 24, 38,
                             fill=CARD_BG, outline=BTN_OUTLINE, width=1.5)
        btn.create_text((PROP_W - 24) // 2, 19,
                        text="Added to Cart", fill=BTN_ADDED_FG,
                        font=self.fnt["btn"])
        btn.bind("<Enter>",
                 lambda e, b=btn: b.itemconfig(1, fill="#E8F5EE"))
        btn.bind("<Leave>",
                 lambda e, b=btn: b.itemconfig(1, fill=CARD_BG))



# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = DwelloSearch()
    app.mainloop()