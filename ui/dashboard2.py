import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import os
 
# ── Asset Paths ────────────────────────────────────────────────────────────────
BASE = r"C:\Users\LENOVO T14\Documents\Dwello\assets\images"
 
LOGO_PATH      = os.path.join(BASE, "dwello_logo.png")   # Dwello logo  (223×223)
USER_PATH      = os.path.join(BASE, "u.png")              # User avatar  (40×40)
ICON_STATS_PATH= os.path.join(BASE, "s.png")              # Stats / bar-chart icon (44×44)
ICON_CART_PATH = os.path.join(BASE, "g.png")              # Cart icon    (48×48)
 
# Property images  1-3 → Recent Visits    4-6 → My Cart
PROP_1 = os.path.join(BASE, "1.jpeg")
PROP_2 = os.path.join(BASE, "2.jpeg")
PROP_3 = os.path.join(BASE, "3.jpeg")
PROP_4 = os.path.join(BASE, "4.jpeg")
PROP_5 = os.path.join(BASE, "5.jpeg")
PROP_6 = os.path.join(BASE, "6.jpeg")
 
PROP_PATHS = [PROP_1, PROP_2, PROP_3, PROP_4, PROP_5, PROP_6]
 
# ── Dimensions ────────────────────────────────────────────────────────────────
LOGO_LOAD_SIZE   = (223, 223)   # original load size as specified
LOGO_DISPLAY_SIZE= (80, 83)     # scaled-down sidebar display size
THUMB_SIZE       = (48, 48)     # property thumbnails
ICON_STAT_SIZE   = (44, 44)     # stat-card icons
USER_SIZE        = (32, 32)     # top-bar user avatar
NAV_ICON_SIZE    = (24, 24)     # sidebar nav icons
 
# ── Colours ───────────────────────────────────────────────────────────────────
SIDEBAR_BG     = "#1B3A2D"
SIDEBAR_ACTIVE = "#2D5A40"
SIDEBAR_HOVER  = "#243F30"
SIDEBAR_TEXT   = "#FFFFFF"
SIDEBAR_MUTED  = "#8FB8A0"
MAIN_BG        = "#F4F6F8"
CARD_WHITE     = "#FFFFFF"
ACCENT_GREEN   = "#2E7D52"
DARK_NAVY      = "#1A1A2E"
HEADING        = "#1A1A1A"
SUBTEXT        = "#666666"
STAT_CART_BG   = "#1A2E4A"     # dark blue  – "Items in cart" card
STAT_BOOK_BG   = "#2E7D52"     # green      – "Total Bookings" card
TOP_BAR_TEXT   = "#FFFFFF"
DIVIDER        = "#E8E8E8"
PRICE_GREEN    = "#2E7D52"
LOC_GREY       = "#999999"
VIEW_ALL_GREEN = "#2E7D52"
 
 
# ── Image helpers ─────────────────────────────────────────────────────────────
def load_rgba(path: str, size: tuple) -> ImageTk.PhotoImage:
    """Open any image, convert to RGBA, resize and return a PhotoImage."""
    return ImageTk.PhotoImage(
        Image.open(path).convert("RGBA").resize(size, Image.LANCZOS)
    )
 
 
def load_rgb(path: str, size: tuple) -> ImageTk.PhotoImage:
    """Open any image, convert to RGB, resize and return a PhotoImage."""
    return ImageTk.PhotoImage(
        Image.open(path).convert("RGB").resize(size, Image.LANCZOS)
    )
 
 
def tint_icon(path: str, size: tuple, colour_hex: str) -> ImageTk.PhotoImage:
    """
    Load an icon, preserve its alpha channel, and flood-fill its RGB
    channels with *colour_hex*.  Returns a PhotoImage.
    """
    img = Image.open(path).convert("RGBA").resize(size, Image.LANCZOS)
    _, _, _, alpha = img.split()
    r = int(colour_hex[1:3], 16)
    g = int(colour_hex[3:5], 16)
    b = int(colour_hex[5:7], 16)
    tinted = Image.new("RGBA", size, (r, g, b, 255))
    tinted.putalpha(alpha)
    return ImageTk.PhotoImage(tinted)
 
 
# ── Main Application ──────────────────────────────────────────────────────────
class DwelloDashboard(tk.Tk):
 
    def __init__(self):
        super().__init__()
        self.title("Dwello – Dashboard")
        self.geometry("900x600")
        self.resizable(False, False)
        self.configure(bg=SIDEBAR_BG)
 
        self.active_page = "Dashboard"
        self._sidebar_rows: dict = {}
 
        self._init_fonts()
        self._init_images()
        self._build_layout()
 
    # ── Font initialisation ───────────────────────────────────────────────────
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
 
    # ── Image initialisation ──────────────────────────────────────────────────
    def _init_images(self):
        # Logo: load at spec size, display smaller
        logo_pil = Image.open(LOGO_PATH).convert("RGBA") \
                        .resize(LOGO_LOAD_SIZE, Image.LANCZOS) \
                        .resize(LOGO_DISPLAY_SIZE, Image.LANCZOS)
        self.img_logo = ImageTk.PhotoImage(logo_pil)
 
        # Top-bar user avatar
        self.img_user = load_rgba(USER_PATH, USER_SIZE)
 
        # Stat-card icons (white tint for dark backgrounds)
        self.img_stat_cart  = tint_icon(ICON_CART_PATH,  ICON_STAT_SIZE, "#FFFFFF")
        self.img_stat_stats = tint_icon(ICON_STATS_PATH, ICON_STAT_SIZE, "#FFFFFF")
 
        # Sidebar nav icons
        self.img_nav_dashboard = tint_icon(USER_PATH,       NAV_ICON_SIZE, "#FFFFFF")
        self.img_nav_explore_w = tint_icon(ICON_STATS_PATH, NAV_ICON_SIZE, "#FFFFFF")
        self.img_nav_explore_g = tint_icon(ICON_STATS_PATH, NAV_ICON_SIZE, ACCENT_GREEN)
        self.img_nav_cart_w    = tint_icon(ICON_CART_PATH,  NAV_ICON_SIZE, "#FFFFFF")
 
        # Property thumbnails  (keep references so GC doesn't collect them)
        self.prop_imgs = [load_rgb(path, THUMB_SIZE) for path in PROP_PATHS]
 
    # ── Top-level layout ──────────────────────────────────────────────────────
    def _build_layout(self):
        # Left sidebar (fixed width)
        sidebar = tk.Frame(self, bg=SIDEBAR_BG, width=160)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        self._build_sidebar(sidebar)
 
        # Right content area
        content = tk.Frame(self, bg=MAIN_BG)
        content.pack(side="left", fill="both", expand=True)
        self._build_topbar(content)
        self._build_main(content)
 
    # ── Sidebar ───────────────────────────────────────────────────────────────
    def _build_sidebar(self, parent):
        # ── Logo block ──────────────────────────────────────────────────
        logo_frame = tk.Frame(parent, bg=SIDEBAR_BG, pady=16)
        logo_frame.pack(fill="x")
        tk.Label(logo_frame, image=self.img_logo, bg=SIDEBAR_BG).pack()
        tk.Label(logo_frame,
                 text="DWELLO", fg=SIDEBAR_TEXT, bg=SIDEBAR_BG,
                 font=tkfont.Font(family="Helvetica", size=14, weight="bold")
                 ).pack(pady=(2, 0))
 
        # Divider
        tk.Frame(parent, bg="#2D5A40", height=1).pack(fill="x", padx=16, pady=4)
 
        # ── Navigation items ────────────────────────────────────────────
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
 
        # Spacer
        tk.Frame(parent, bg=SIDEBAR_BG).pack(fill="both", expand=True)
 
        # Log-out button
        self._build_logout_btn(parent)
 
    def _sidebar_item(self, parent, icon, label: str, active: bool) -> tk.Frame:
        bg   = SIDEBAR_ACTIVE if active else SIDEBAR_BG
        fg   = SIDEBAR_TEXT   if active else SIDEBAR_MUTED
        font = self.f_sidebar_b if active else self.f_sidebar
 
        row = tk.Frame(parent, bg=bg, cursor="hand2")
        row.pack(fill="x", pady=1)
 
        inner = tk.Frame(row, bg=bg, padx=16, pady=10)
        inner.pack(fill="x")
 
        icon_lbl = tk.Label(inner, image=icon, bg=bg)
        icon_lbl.pack(side="left")
 
        text_lbl = tk.Label(inner, text=label, fg=fg, bg=bg, font=font)
        text_lbl.pack(side="left", padx=10)
 
        # Attach references for later recolouring
        row.inner    = inner
        row.icon_lbl = icon_lbl
        row.text_lbl = text_lbl
 
        # Bind click on every child widget
        for widget in (row, inner, icon_lbl, text_lbl):
            widget.bind("<Button-1>", lambda _e, l=label: self._on_nav_click(l))
 
        return row
 
    def _on_nav_click(self, label: str):
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
        canvas.create_text(18, 21, text="\u2190", fill=SIDEBAR_TEXT,
                            font=tkfont.Font(family="Helvetica", size=13, weight="bold"))
        canvas.create_text(72, 21, text="Log Out",
                            fill=SIDEBAR_TEXT, font=self.f_logout)
        canvas.bind("<Button-1>", lambda _e: self.destroy())
 
    # ── Top bar ───────────────────────────────────────────────────────────────
    def _build_topbar(self, parent):
        bar = tk.Frame(parent, bg=MAIN_BG, height=56)
        bar.pack(fill="x")
        bar.pack_propagate(False)
 
        # Page title (top-left)
        tk.Label(bar, text="Dashboard Page",
                 fg=SUBTEXT, bg=MAIN_BG, font=self.f_body).place(x=20, y=14)
 
        # Welcome chip (top-right)
        chip = tk.Frame(bar, bg=DARK_NAVY, padx=12, pady=6)
        chip.place(relx=1.0, rely=0.5, anchor="e", x=-16)
        tk.Label(chip, text="Welcome, Josemaria",
                 fg=TOP_BAR_TEXT, bg=DARK_NAVY, font=self.f_topbar).pack(side="left")
        tk.Label(chip, image=self.img_user,
                 bg=DARK_NAVY).pack(side="left", padx=(8, 0))
 
    # ── Main dashboard content ────────────────────────────────────────────────
    def _build_main(self, parent):
        outer = tk.Frame(parent, bg=MAIN_BG)
        outer.pack(fill="both", expand=True, padx=16, pady=(0, 16))
 
        # White card container
        container = tk.Frame(outer, bg=CARD_WHITE,
                             highlightbackground=DIVIDER, highlightthickness=1)
        container.pack(fill="both", expand=True)
 
        # ── Stat cards row ───────────────────────────────────────────────
        stats_row = tk.Frame(container, bg=CARD_WHITE)
        stats_row.pack(fill="x", padx=24, pady=(20, 16))
 
        self._stat_card(stats_row,
                        icon=self.img_stat_cart,
                        number="6",
                        label="Number of Items in cart",
                        bg=STAT_CART_BG)
 
        tk.Frame(stats_row, bg=CARD_WHITE, width=20).pack(side="left")
 
        self._stat_card(stats_row,
                        icon=self.img_stat_stats,
                        number="20",
                        label="Total Number of Bookings",
                        bg=STAT_BOOK_BG)
 
        # ── Two-column property section ──────────────────────────────────
        cols = tk.Frame(container, bg=CARD_WHITE)
        cols.pack(fill="both", expand=True, padx=24, pady=(0, 16))
 
        # Left column – Recent Visits
        left_col = tk.Frame(cols, bg=CARD_WHITE)
        left_col.pack(side="left", fill="both", expand=True)
 
        self._section_header(left_col, "Recent Visits", view_all=False)
 
        recent_visits = [
            ("2 Bedroom Apartment",     "Ikeja, Lagos",           "\u20a6 4,000,000",   0),
            ("Luxury 5 Bedroom House",  "Victoria Island, Lagos", "\u20a6 250,000,000",  1),
            ("Modern Studio Apartment", "Lekki Phase 1, Lagos",   "\u20a6 7,000,000",   2),
        ]
        for name, loc, price, idx in recent_visits:
            self._property_row(left_col, self.prop_imgs[idx], name, loc, price)
 
        # Column spacer
        tk.Frame(cols, bg=CARD_WHITE, width=24).pack(side="left")
 
        # Right column – My Cart
        right_col = tk.Frame(cols, bg=CARD_WHITE)
        right_col.pack(side="left", fill="both", expand=True)
 
        self._section_header(right_col, "My Cart", view_all=True)
 
        cart_items = [
            ("Luxury 8 Bedroom House",   "Banana Island, Lagos", "\u20a6 750,000,000", 3),
            ("Opulence 6 Bedroom House", "Ikoyi, Lagos",         "\u20a6 450,000,000", 4),
            ("3 Bedroom Apartment",      "Victoria Island",      "\u20a6 27,000,000",  5),
        ]
        for name, loc, price, idx in cart_items:
            self._property_row(right_col, self.prop_imgs[idx], name, loc, price)
 
    # ── Stat card widget ──────────────────────────────────────────────────────
    def _stat_card(self, parent, icon, number: str, label: str, bg: str):
        card = tk.Frame(parent, bg=bg, width=270, height=150)
        card.pack(side="left")
        card.pack_propagate(False)
 
        top_row = tk.Frame(card, bg=bg)
        top_row.pack(anchor="w", padx=20, pady=(20, 6))
 
        tk.Label(top_row, image=icon, bg=bg).pack(side="left")
        tk.Label(top_row, text=number, fg=SIDEBAR_TEXT, bg=bg,
                 font=self.f_stat_num).pack(side="left", padx=(12, 0))
 
        tk.Label(card, text=label, fg=SIDEBAR_TEXT, bg=bg,
                 font=self.f_stat_lbl, wraplength=220,
                 justify="left").pack(anchor="w", padx=20)
 
    # ── Section header (title + optional "View all") ──────────────────────────
    def _section_header(self, parent, title: str, view_all: bool):
        row = tk.Frame(parent, bg=CARD_WHITE)
        row.pack(fill="x", pady=(4, 6))
 
        tk.Label(row, text=title, fg=HEADING, bg=CARD_WHITE,
                 font=self.f_section).pack(side="left")
 
        if view_all:
            tk.Label(row, text="View all", fg=VIEW_ALL_GREEN, bg=CARD_WHITE,
                     font=self.f_viewall, cursor="hand2").pack(side="right")
 
    # ── Property row widget ───────────────────────────────────────────────────
    def _property_row(self, parent, thumb: ImageTk.PhotoImage,
                      name: str, location: str, price: str):
        row = tk.Frame(parent, bg=CARD_WHITE,
                       highlightbackground=DIVIDER, highlightthickness=1,
                       cursor="hand2")
        row.pack(fill="x", pady=3, ipady=6)
 
        # Thumbnail image
        tk.Label(row, image=thumb, bg=CARD_WHITE).pack(side="left", padx=(8, 0))
 
        # Name + location block
        info = tk.Frame(row, bg=CARD_WHITE)
        info.pack(side="left", padx=10, fill="x", expand=True)
 
        tk.Label(info, text=name, fg=HEADING, bg=CARD_WHITE,
                 font=self.f_body_b, anchor="w").pack(fill="x")
 
        loc_row = tk.Frame(info, bg=CARD_WHITE)
        loc_row.pack(fill="x")
        tk.Label(loc_row, text="\u2299", fg=LOC_GREY,
                 bg=CARD_WHITE, font=self.f_small).pack(side="left")
        tk.Label(loc_row, text=location, fg=LOC_GREY,
                 bg=CARD_WHITE, font=self.f_small).pack(side="left")
 
        # Price (right-aligned)
        tk.Label(row, text=price, fg=PRICE_GREEN, bg=CARD_WHITE,
                 font=self.f_price).pack(side="right", padx=10)
 
 
# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = DwelloDashboard()
    app.mainloop()