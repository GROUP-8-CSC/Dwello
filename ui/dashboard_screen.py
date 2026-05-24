import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import os, pathlib, sys

# ── Asset paths ────────────────────────────────────────────────────────────────
_HERE   = pathlib.Path(__file__).parent
_ASSETS = _HERE.parent / "assets" / "images"

LOGO_PATH       = str(_ASSETS / "dwello_logo.png")
USER_PATH       = str(_ASSETS / "u.png")
ICON_STATS_PATH = str(_ASSETS / "s.png")
ICON_CART_PATH  = str(_ASSETS / "g.png")

PROP_PATHS = [str(_ASSETS / f"{i}.jpeg") for i in range(1, 7)]

# ── Dimensions ─────────────────────────────────────────────────────────────────
LOGO_LOAD_SIZE    = (223, 223)
LOGO_DISPLAY_SIZE = (80, 83)
THUMB_SIZE        = (48, 48)
ICON_STAT_SIZE    = (44, 44)
USER_SIZE         = (32, 32)
NAV_ICON_SIZE     = (24, 24)

# ── Colours ────────────────────────────────────────────────────────────────────
SIDEBAR_BG     = "#1B3A2D"
SIDEBAR_ACTIVE = "#2D5A40"
SIDEBAR_TEXT   = "#FFFFFF"
SIDEBAR_MUTED  = "#8FB8A0"
MAIN_BG        = "#F4F6F8"
CARD_WHITE     = "#FFFFFF"
ACCENT_GREEN   = "#2E7D52"
DARK_NAVY      = "#1A1A2E"
HEADING        = "#1A1A1A"
SUBTEXT        = "#666666"
STAT_CART_BG   = "#1A2E4A"
STAT_BOOK_BG   = "#2E7D52"
TOP_BAR_TEXT   = "#FFFFFF"
DIVIDER        = "#E8E8E8"
PRICE_GREEN    = "#2E7D52"
LOC_GREY       = "#999999"
VIEW_ALL_GREEN = "#2E7D52"


# ── Image helpers ──────────────────────────────────────────────────────────────
def _load_rgba(path, size):
    try:
        return ImageTk.PhotoImage(
            Image.open(path).convert("RGBA").resize(size, Image.LANCZOS))
    except Exception:
        return None

def _load_rgb(path, size):
    try:
        return ImageTk.PhotoImage(
            Image.open(path).convert("RGB").resize(size, Image.LANCZOS))
    except Exception:
        return None

def _tint_icon(path, size, colour_hex):
    try:
        img = Image.open(path).convert("RGBA").resize(size, Image.LANCZOS)
        _, _, _, alpha = img.split()
        r = int(colour_hex[1:3], 16)
        g = int(colour_hex[3:5], 16)
        b = int(colour_hex[5:7], 16)
        tinted = Image.new("RGBA", size, (r, g, b, 255))
        tinted.putalpha(alpha)
        return ImageTk.PhotoImage(tinted)
    except Exception:
        return None


# ══════════════════════════════════════════════════════════════════════════════
class DashboardScreen(tk.Toplevel):
    """
    Dashboard overview page.
    Navigated to from sidebar "Dashboard" link on other screens.
    """

    def __init__(self, master=None, user=None, **kw):
        super().__init__(master, **kw)
        self.title("Dwello – Dashboard")
        self.geometry("900x600")
        self.resizable(False, False)
        self.configure(bg=SIDEBAR_BG)

        self.user        = user
        self.active_page = "Dashboard"
        self._sidebar_rows: dict = {}

        self._init_fonts()
        self._init_images()
        self._build_layout()

    # ── Fonts ─────────────────────────────────────────────────────────────────
    def _init_fonts(self):
        F = tkfont.Font
        self.f_sidebar   = F(family="Helvetica", size=11)
        self.f_sidebar_b = F(family="Helvetica", size=11, weight="bold")
        self.f_logout    = F(family="Helvetica", size=11, weight="bold")
        self.f_topbar    = F(family="Helvetica", size=11, weight="bold")
        self.f_section   = F(family="Helvetica", size=12, weight="bold")
        self.f_body      = F(family="Helvetica", size=9)
        self.f_body_b    = F(family="Helvetica", size=9,  weight="bold")
        self.f_small     = F(family="Helvetica", size=8)
        self.f_stat_num  = F(family="Helvetica", size=28, weight="bold")
        self.f_stat_lbl  = F(family="Helvetica", size=11, weight="bold")
        self.f_price     = F(family="Helvetica", size=9,  weight="bold")
        self.f_viewall   = F(family="Helvetica", size=9,  weight="bold")

    # ── Images ────────────────────────────────────────────────────────────────
    def _init_images(self):
        try:
            logo_pil = Image.open(LOGO_PATH).convert("RGBA") \
                           .resize(LOGO_LOAD_SIZE, Image.LANCZOS) \
                           .resize(LOGO_DISPLAY_SIZE, Image.LANCZOS)
            self.img_logo = ImageTk.PhotoImage(logo_pil)
        except Exception:
            self.img_logo = None

        self.img_user           = _load_rgba(USER_PATH,       USER_SIZE)
        self.img_stat_cart      = _tint_icon(ICON_CART_PATH,  ICON_STAT_SIZE, "#FFFFFF")
        self.img_stat_stats     = _tint_icon(ICON_STATS_PATH, ICON_STAT_SIZE, "#FFFFFF")
        self.img_nav_dashboard  = _tint_icon(USER_PATH,       NAV_ICON_SIZE,  "#FFFFFF")
        self.img_nav_explore_g  = _tint_icon(ICON_STATS_PATH, NAV_ICON_SIZE,  ACCENT_GREEN)
        self.img_nav_explore_w  = _tint_icon(ICON_STATS_PATH, NAV_ICON_SIZE,  "#FFFFFF")
        self.img_nav_cart_w     = _tint_icon(ICON_CART_PATH,  NAV_ICON_SIZE,  "#FFFFFF")
        self.prop_imgs = [_load_rgb(p, THUMB_SIZE) for p in PROP_PATHS]

    # ── Layout ────────────────────────────────────────────────────────────────
    def _build_layout(self):
        sidebar = tk.Frame(self, bg=SIDEBAR_BG, width=160)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        self._build_sidebar(sidebar)

        content = tk.Frame(self, bg=MAIN_BG)
        content.pack(side="left", fill="both", expand=True)
        self._build_topbar(content)
        self._build_main(content)

    # ── Sidebar ───────────────────────────────────────────────────────────────
    def _build_sidebar(self, parent):
        logo_frame = tk.Frame(parent, bg=SIDEBAR_BG, pady=16)
        logo_frame.pack(fill="x")
        if self.img_logo:
            tk.Label(logo_frame, image=self.img_logo, bg=SIDEBAR_BG).pack()
        tk.Label(logo_frame, text="DWELLO", fg=SIDEBAR_TEXT, bg=SIDEBAR_BG,
                 font=tkfont.Font(family="Helvetica", size=14, weight="bold")).pack(pady=(2, 0))

        tk.Frame(parent, bg="#2D5A40", height=1).pack(fill="x", padx=16, pady=4)

        nav_items = [
            ("Dashboard", self.img_nav_dashboard, self.img_nav_dashboard),
            ("Explore",   self.img_nav_explore_g, self.img_nav_explore_w),
            ("Cart",      self.img_nav_cart_w,    self.img_nav_cart_w),
        ]
        for label, icon_on, icon_off in nav_items:
            active = (label == self.active_page)
            icon   = icon_on if active else icon_off
            row    = self._sidebar_item(parent, icon, label, active)
            self._sidebar_rows[label] = row

        tk.Frame(parent, bg=SIDEBAR_BG).pack(fill="both", expand=True)
        self._build_logout_btn(parent)

    def _sidebar_item(self, parent, icon, label, active):
        bg   = SIDEBAR_ACTIVE if active else SIDEBAR_BG
        fg   = SIDEBAR_TEXT   if active else SIDEBAR_MUTED
        font = self.f_sidebar_b if active else self.f_sidebar

        row = tk.Frame(parent, bg=bg, cursor="hand2")
        row.pack(fill="x", pady=1)
        inner = tk.Frame(row, bg=bg, padx=16, pady=10)
        inner.pack(fill="x")

        if icon:
            icon_lbl = tk.Label(inner, image=icon, bg=bg)
        else:
            icon_lbl = tk.Label(inner, text="•", bg=bg, fg=fg)
        icon_lbl.pack(side="left")

        text_lbl = tk.Label(inner, text=label, fg=fg, bg=bg, font=font)
        text_lbl.pack(side="left", padx=10)

        row.inner    = inner
        row.icon_lbl = icon_lbl
        row.text_lbl = text_lbl

        for w in (row, inner, icon_lbl, text_lbl):
            w.bind("<Button-1>", lambda _e, l=label: self._on_nav_click(l))

        return row

    def _on_nav_click(self, label):
        for lbl, row in self._sidebar_rows.items():
            active = (lbl == label)
            bg     = SIDEBAR_ACTIVE if active else SIDEBAR_BG
            fg     = SIDEBAR_TEXT   if active else SIDEBAR_MUTED
            font   = self.f_sidebar_b if active else self.f_sidebar
            row.configure(bg=bg)
            row.inner.configure(bg=bg)
            row.icon_lbl.configure(bg=bg)
            row.text_lbl.configure(bg=bg, fg=fg, font=font)
        self.active_page = label

    def _build_logout_btn(self, parent):
        frame = tk.Frame(parent, bg=SIDEBAR_BG, pady=20)
        frame.pack(fill="x")
        canvas = tk.Canvas(frame, bg=SIDEBAR_BG, highlightthickness=0,
                           height=42, width=128, cursor="hand2")
        canvas.pack(padx=16)
        canvas.create_rectangle(0, 0, 128, 42,
                                 outline=SIDEBAR_TEXT, width=1.5, fill=SIDEBAR_BG)
        canvas.create_text(18, 21, text="←", fill=SIDEBAR_TEXT,
                            font=tkfont.Font(family="Helvetica", size=13, weight="bold"))
        canvas.create_text(72, 21, text="Log Out", fill=SIDEBAR_TEXT, font=self.f_logout)
        canvas.bind("<Button-1>", lambda _e: self.destroy())

    # ── Top bar ───────────────────────────────────────────────────────────────
    def _build_topbar(self, parent):
        bar = tk.Frame(parent, bg=MAIN_BG, height=56)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        tk.Label(bar, text="Dashboard Page",
                 fg=SUBTEXT, bg=MAIN_BG, font=self.f_body).place(x=20, y=14)

        username = getattr(self.user, "name", None) or \
                   (self.user.get("name") if isinstance(self.user, dict) else "Guest")

        chip = tk.Frame(bar, bg=DARK_NAVY, padx=12, pady=6)
        chip.place(relx=1.0, rely=0.5, anchor="e", x=-16)
        tk.Label(chip, text=f"Welcome, {username}",
                 fg=TOP_BAR_TEXT, bg=DARK_NAVY, font=self.f_topbar).pack(side="left")
        if self.img_user:
            tk.Label(chip, image=self.img_user, bg=DARK_NAVY).pack(side="left", padx=(8, 0))

    # ── Main content ──────────────────────────────────────────────────────────
    def _build_main(self, parent):
        outer = tk.Frame(parent, bg=MAIN_BG)
        outer.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        container = tk.Frame(outer, bg=CARD_WHITE,
                             highlightbackground=DIVIDER, highlightthickness=1)
        container.pack(fill="both", expand=True)

        # Stat cards
        stats_row = tk.Frame(container, bg=CARD_WHITE)
        stats_row.pack(fill="x", padx=24, pady=(20, 16))

        self._stat_card(stats_row, icon=self.img_stat_cart,
                        number="6", label="Number of Items in cart",
                        bg=STAT_CART_BG)
        tk.Frame(stats_row, bg=CARD_WHITE, width=20).pack(side="left")
        self._stat_card(stats_row, icon=self.img_stat_stats,
                        number="20", label="Total Number of Bookings",
                        bg=STAT_BOOK_BG)

        # Two-column property section
        cols = tk.Frame(container, bg=CARD_WHITE)
        cols.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        # Recent Visits
        left_col = tk.Frame(cols, bg=CARD_WHITE)
        left_col.pack(side="left", fill="both", expand=True)
        self._section_header(left_col, "Recent Visits", view_all=False)

        recent_visits = [
            ("2 Bedroom Apartment",     "Ikeja, Lagos",           "₦4,000,000",   0),
            ("Luxury 5 Bedroom House",  "Victoria Island, Lagos", "₦250,000,000", 1),
            ("Modern Studio Apartment", "Lekki Phase 1, Lagos",   "₦7,000,000",   2),
        ]
        for name, loc, price, idx in recent_visits:
            self._property_row(left_col, self.prop_imgs[idx], name, loc, price)

        tk.Frame(cols, bg=CARD_WHITE, width=24).pack(side="left")

        # My Cart
        right_col = tk.Frame(cols, bg=CARD_WHITE)
        right_col.pack(side="left", fill="both", expand=True)
        self._section_header(right_col, "My Cart", view_all=True)

        cart_items = [
            ("Luxury 8 Bedroom House",   "Banana Island, Lagos", "₦750,000,000", 3),
            ("Opulence 6 Bedroom House", "Ikoyi, Lagos",         "₦450,000,000", 4),
            ("3 Bedroom Apartment",      "Victoria Island",      "₦27,000,000",  5),
        ]
        for name, loc, price, idx in cart_items:
            self._property_row(right_col, self.prop_imgs[idx], name, loc, price)

    # ── Stat card ─────────────────────────────────────────────────────────────
    def _stat_card(self, parent, icon, number, label, bg):
        card = tk.Frame(parent, bg=bg, width=270, height=150)
        card.pack(side="left")
        card.pack_propagate(False)

        top_row = tk.Frame(card, bg=bg)
        top_row.pack(anchor="w", padx=20, pady=(20, 6))
        if icon:
            tk.Label(top_row, image=icon, bg=bg).pack(side="left")
        tk.Label(top_row, text=number, fg=SIDEBAR_TEXT, bg=bg,
                 font=self.f_stat_num).pack(side="left", padx=(12, 0))
        tk.Label(card, text=label, fg=SIDEBAR_TEXT, bg=bg,
                 font=self.f_stat_lbl, wraplength=220, justify="left").pack(anchor="w", padx=20)

    # ── Section header ────────────────────────────────────────────────────────
    def _section_header(self, parent, title, view_all=False):
        row = tk.Frame(parent, bg=CARD_WHITE)
        row.pack(fill="x", pady=(4, 6))
        tk.Label(row, text=title, fg=HEADING, bg=CARD_WHITE,
                 font=self.f_section).pack(side="left")
        if view_all:
            tk.Label(row, text="View all", fg=VIEW_ALL_GREEN, bg=CARD_WHITE,
                     font=self.f_viewall, cursor="hand2").pack(side="right")

    # ── Property row ──────────────────────────────────────────────────────────
    def _property_row(self, parent, thumb, name, location, price):
        row = tk.Frame(parent, bg=CARD_WHITE,
                       highlightbackground=DIVIDER, highlightthickness=1,
                       cursor="hand2")
        row.pack(fill="x", pady=3, ipady=6)

        if thumb:
            tk.Label(row, image=thumb, bg=CARD_WHITE).pack(side="left", padx=(8, 0))

        info = tk.Frame(row, bg=CARD_WHITE)
        info.pack(side="left", padx=10, fill="x", expand=True)
        tk.Label(info, text=name, fg=HEADING, bg=CARD_WHITE,
                 font=self.f_body_b, anchor="w").pack(fill="x")

        loc_row = tk.Frame(info, bg=CARD_WHITE)
        loc_row.pack(fill="x")
        tk.Label(loc_row, text="⊙", fg=LOC_GREY, bg=CARD_WHITE,
                 font=self.f_small).pack(side="left")
        tk.Label(loc_row, text=location, fg=LOC_GREY, bg=CARD_WHITE,
                 font=self.f_small).pack(side="left")

        tk.Label(row, text=price, fg=PRICE_GREEN, bg=CARD_WHITE,
                 font=self.f_price).pack(side="right", padx=10)


# ── Stand-alone entry ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
    root = tk.Tk()
    root.withdraw()
    app = DashboardScreen(master=root, user={"name": "Josemaria"})
    app.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()
