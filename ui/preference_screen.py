import tkinter as tk
from tkinter import font as tkfont, messagebox
from PIL import Image, ImageTk
import os, pathlib, sys

# ── Asset paths ────────────────────────────────────────────────────────────────
_HERE   = pathlib.Path(__file__).parent
_ASSETS = _HERE.parent / "assets" / "images"

LOGO_PATH           = str(_ASSETS / "dwello_logo.png")
EXPLORE_PATH        = str(_ASSETS / "compass.png")
HOME_PATH           = str(_ASSETS / "house.png")
CART_PATH           = str(_ASSETS / "shopping-cart.png")
MAINLAND_ILLUS_PATH = str(_ASSETS / "image_1.png")
ISLAND_ILLUS_PATH   = str(_ASSETS / "image_2.png")

# ── Colours ────────────────────────────────────────────────────────────────────
SIDEBAR_BG     = "#1B3A2D"
SIDEBAR_ACTIVE = "#2D5A40"
SIDEBAR_TEXT   = "#FFFFFF"
SIDEBAR_MUTED  = "#8FB8A0"
MAIN_BG        = "#FFFFFF"
ACCENT_GREEN   = "#2E7D52"
LIGHT_GREEN    = "#E8F5EE"
BORDER_GREEN   = "#2E7D52"
CARD_BORDER    = "#D0E8D8"
INACTIVE_CARD  = "#F5F5F5"
INACTIVE_TEXT  = "#AAAAAA"
INACTIVE_ICON  = "#CCCCCC"
HEADING        = "#1A1A1A"
SUBTEXT        = "#666666"
BUDGET_BG      = "#F0F0F0"
BTN_BG         = "#1A1A2E"
BTN_TEXT_C     = "#FFFFFF"
NAIRA_GREEN    = "#2E7D52"
ACCENT_BLUE    = "#1565C0"
LIGHT_BLUE     = "#E3F0FB"
BORDER_BLUE    = "#1565C0"

ICON_SIZE = (26, 26)
LOGO_SIZE = (80, 80)


# ── Image helpers ──────────────────────────────────────────────────────────────
def _load_image(path, size):
    img = Image.open(path).convert("RGBA").resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

def _load_icon_white(path, size):
    img = Image.open(path).convert("RGBA").resize(size, Image.LANCZOS)
    _, _, _, a = img.split()
    white = Image.new("RGBA", img.size, (255, 255, 255, 255))
    white.putalpha(a)
    return ImageTk.PhotoImage(white)

def _load_icon_dark(path, size):
    img = Image.open(path).convert("RGBA").resize(size, Image.LANCZOS)
    _, _, _, a = img.split()
    colored = Image.new("RGBA", img.size, (46, 125, 82, 255))
    colored.putalpha(a)
    return ImageTk.PhotoImage(colored)


# ══════════════════════════════════════════════════════════════════════════════
class PreferenceScreen(tk.Toplevel):
    """
    Region + Budget preference window.

    Public functions (per UI breakdown):
        select_region(region)     – stores "mainland" or "island" and refreshes cards
        validate_budget()         – calls utils/validators.py :: validate_budget()
        handle_search()           – collects input → calls property_controller → opens marketplace
        open_marketplace(props)   – launches marketplace_screen.py
    """

    def __init__(self, master=None, user=None):
        super().__init__(master)
        self.title("Dwello – Choose Your Preferences")
        self.geometry("900x600")
        self.resizable(False, False)
        self.configure(bg=SIDEBAR_BG)

        self.user            = user
        self.selected_region = "mainland"   # default
        self.active_page     = "Explore"
        self._sidebar_rows   = {}

        self._init_fonts()
        self._load_images()
        self._build_layout()

    # ── Fonts ─────────────────────────────────────────────────────────────────
    def _init_fonts(self):
        F = tkfont.Font
        self.f_title     = F(family="Helvetica", size=20, weight="bold")
        self.f_sub       = F(family="Helvetica", size=10)
        self.f_section   = F(family="Helvetica", size=13, weight="bold")
        self.f_body      = F(family="Helvetica", size=9)
        self.f_sidebar   = F(family="Helvetica", size=11)
        self.f_sidebar_b = F(family="Helvetica", size=11, weight="bold")
        self.f_btn       = F(family="Helvetica", size=12, weight="bold")
        self.f_logout    = F(family="Helvetica", size=11, weight="bold")
        self.f_input     = F(family="Helvetica", size=10)

    # ── Images ────────────────────────────────────────────────────────────────
    def _load_images(self):
        def safe(fn, *args):
            try:
                return fn(*args)
            except Exception:
                return None

        self.img_logo      = safe(_load_image,      LOGO_PATH,           LOGO_SIZE)
        self.img_home_w    = safe(_load_icon_white,  HOME_PATH,           ICON_SIZE)
        self.img_explore_w = safe(_load_icon_white,  EXPLORE_PATH,        ICON_SIZE)
        self.img_cart_w    = safe(_load_icon_white,  CART_PATH,           ICON_SIZE)
        self.img_explore_g = safe(_load_icon_dark,   EXPLORE_PATH,        ICON_SIZE)
        self.img_mainland  = safe(_load_image,       MAINLAND_ILLUS_PATH, (90, 80))
        self.img_island    = safe(_load_image,       ISLAND_ILLUS_PATH,   (90, 80))

    # ── Layout ────────────────────────────────────────────────────────────────
    def _build_layout(self):
        sidebar = tk.Frame(self, bg=SIDEBAR_BG, width=160)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        self._build_sidebar(sidebar)

        main = tk.Frame(self, bg=MAIN_BG)
        main.pack(side="left", fill="both", expand=True)
        self._build_main(main)

    # ── Sidebar ───────────────────────────────────────────────────────────────
    def _build_sidebar(self, parent):
        logo_frame = tk.Frame(parent, bg=SIDEBAR_BG, pady=20)
        logo_frame.pack(fill="x")
        if self.img_logo:
            tk.Label(logo_frame, image=self.img_logo, bg=SIDEBAR_BG).pack()
        tk.Label(logo_frame, text="DWELLO", fg=SIDEBAR_TEXT, bg=SIDEBAR_BG,
                 font=tkfont.Font(family="Helvetica", size=14, weight="bold")).pack(pady=(4, 0))

        tk.Frame(parent, bg="#2D5A40", height=1).pack(fill="x", padx=16, pady=4)

        nav_items = [
            ("Dashboard", self.img_home_w),
            ("Explore",   self.img_explore_g),
            ("Cart",      self.img_cart_w),
        ]
        for label, icon in nav_items:
            active = (label == self.active_page)
            row = self._sidebar_item(parent, icon, label, active=active)
            self._sidebar_rows[label] = row

        tk.Frame(parent, bg=SIDEBAR_BG).pack(fill="both", expand=True)
        self._sidebar_logout(parent)

    def _sidebar_item(self, parent, icon, label, active=False):
        bg  = SIDEBAR_ACTIVE if active else SIDEBAR_BG
        fg  = SIDEBAR_TEXT   if active else SIDEBAR_MUTED
        row = tk.Frame(parent, bg=bg, cursor="hand2")
        row.pack(fill="x", pady=1)
        inner = tk.Frame(row, bg=bg, padx=16, pady=10)
        inner.pack(fill="x")
        if icon:
            icon_lbl = tk.Label(inner, image=icon, bg=bg)
            icon_lbl.pack(side="left")
        text_lbl = tk.Label(inner, text=label, fg=fg, bg=bg,
                            font=self.f_sidebar_b if active else self.f_sidebar)
        text_lbl.pack(side="left", padx=10)

        row._inner    = inner
        row._text_lbl = text_lbl
        row._label    = label

        for w in (row, inner, text_lbl):
            w.bind("<Button-1>", lambda e, l=label: self._on_nav_click(l))
        return row

    def _on_nav_click(self, label):
        for lbl, row in self._sidebar_rows.items():
            is_active = (lbl == label)
            bg = SIDEBAR_ACTIVE if is_active else SIDEBAR_BG
            fg = SIDEBAR_TEXT   if is_active else SIDEBAR_MUTED
            row.configure(bg=bg)
            row._inner.configure(bg=bg)
            row._text_lbl.configure(bg=bg, fg=fg)

    def _sidebar_logout(self, parent):
        frame = tk.Frame(parent, bg=SIDEBAR_BG, pady=22)
        frame.pack(fill="x")
        c = tk.Canvas(frame, bg=SIDEBAR_BG, highlightthickness=0, height=44, width=150)
        c.pack(padx=20)
        c.create_rectangle(2, 2, 148, 42, outline=SIDEBAR_TEXT, width=1.5, fill=SIDEBAR_BG)
        c.create_text(20, 22, text="←", fill=SIDEBAR_TEXT,
                      font=tkfont.Font(family="Helvetica", size=13, weight="bold"))
        c.create_text(82, 22, text="Log Out", fill=SIDEBAR_TEXT, font=self.f_logout)
        c.bind("<Button-1>", lambda e: self.destroy())

    # ── Main content ──────────────────────────────────────────────────────────
    def _build_main(self, parent):
        # Heading
        tk.Label(parent, text="Let's find the perfect property for you",
                 font=self.f_title, fg=HEADING, bg=MAIN_BG).pack(anchor="w", padx=24, pady=(24, 2))
        tk.Label(parent, text="Choose your preferred region and budget to get started",
                 font=self.f_sub, fg=SUBTEXT, bg=MAIN_BG).pack(anchor="w", padx=24)

        # Region section
        tk.Label(parent, text="Choose Your Preferred Region",
                 font=self.f_section, fg=HEADING, bg=MAIN_BG).pack(anchor="w", padx=24, pady=(18, 8))

        cards_row = tk.Frame(parent, bg=MAIN_BG)
        cards_row.pack(fill="x", padx=24)
        self.mainland_card_frame = self._build_mainland_card(cards_row)
        self.island_card_frame   = self._build_island_card(cards_row)

        # Budget section
        tk.Label(parent, text="Set Your Budget Range",
                 font=self.f_section, fg=HEADING, bg=MAIN_BG).pack(anchor="w", padx=24, pady=(20, 8))

        budget_row = tk.Frame(parent, bg=MAIN_BG)
        budget_row.pack(anchor="w", padx=24)
        self._build_budget_inputs(budget_row)

        # Explore button
        btn = tk.Button(parent, text="Explore Properties  →",
                        bg=BTN_BG, fg=BTN_TEXT_C, font=self.f_btn,
                        relief="flat", bd=0, cursor="hand2",
                        activebackground="#2C3E6A", activeforeground=BTN_TEXT_C,
                        command=self.handle_search)
        btn.pack(anchor="e", padx=24, pady=(20, 0), ipadx=16, ipady=10)

    # ── Region cards ──────────────────────────────────────────────────────────
    def _build_mainland_card(self, parent):
        card = tk.Frame(parent, bg=LIGHT_GREEN, bd=0,
                        highlightbackground=BORDER_GREEN, highlightthickness=2,
                        cursor="hand2")
        card.pack(side="left", fill="both", expand=True, ipadx=12, ipady=12, padx=(0, 8))

        top = tk.Frame(card, bg=LIGHT_GREEN)
        top.pack(fill="x", padx=12, pady=(12, 4))
        tk.Label(top, text="Lagos Mainland",
                 font=tkfont.Font(family="Helvetica", size=13, weight="bold"),
                 fg=ACCENT_GREEN, bg=LIGHT_GREEN).pack(side="left")

        chk = tk.Canvas(top, width=22, height=22, bg=LIGHT_GREEN, highlightthickness=0)
        chk.pack(side="right")
        chk.create_oval(1, 1, 21, 21, fill=ACCENT_GREEN, outline=ACCENT_GREEN)
        chk.create_text(11, 11, text="✓", fill="white",
                        font=tkfont.Font(family="Helvetica", size=11, weight="bold"))

        body = tk.Frame(card, bg=LIGHT_GREEN)
        body.pack(fill="x", padx=12, pady=4)
        if self.img_mainland:
            tk.Label(body, image=self.img_mainland, bg=LIGHT_GREEN, bd=0).pack(side="left", padx=(0, 12))

        bullets = tk.Frame(body, bg=LIGHT_GREEN)
        bullets.pack(side="left", anchor="n", pady=4)
        for item in ["Lower cost of living", "Central transport access",
                     "Easy interstate access", "Vibrant urban lifestyle"]:
            row = tk.Frame(bullets, bg=LIGHT_GREEN)
            row.pack(anchor="w", pady=1)
            c = tk.Canvas(row, width=16, height=16, bg=LIGHT_GREEN, highlightthickness=0)
            c.pack(side="left")
            c.create_oval(1, 1, 15, 15, fill=ACCENT_GREEN, outline=ACCENT_GREEN)
            c.create_text(8, 8, text="✓", fill="white",
                          font=tkfont.Font(family="Helvetica", size=8, weight="bold"))
            tk.Label(row, text=item, fg=ACCENT_GREEN, bg=LIGHT_GREEN,
                     font=self.f_body).pack(side="left", padx=4)

        self._bind_card(card, "mainland")
        return card

    def _build_island_card(self, parent):
        card = tk.Frame(parent, bg=INACTIVE_CARD, bd=0,
                        highlightbackground=CARD_BORDER, highlightthickness=1,
                        cursor="hand2")
        card.pack(side="left", fill="both", expand=True, ipadx=12, ipady=12)

        top = tk.Frame(card, bg=INACTIVE_CARD)
        top.pack(fill="x", padx=12, pady=(12, 4))
        tk.Label(top, text="Lagos Island",
                 font=tkfont.Font(family="Helvetica", size=13, weight="bold"),
                 fg=INACTIVE_TEXT, bg=INACTIVE_CARD).pack(side="left")

        body = tk.Frame(card, bg=INACTIVE_CARD)
        body.pack(fill="x", padx=12, pady=4)
        if self.img_island:
            tk.Label(body, image=self.img_island, bg=INACTIVE_CARD, bd=0).pack(side="left", padx=(0, 12))

        bullets = tk.Frame(body, bg=INACTIVE_CARD)
        bullets.pack(side="left", anchor="n", pady=4)
        for item in ["Proximity to business districts", "Upscale neighborhoods",
                     "Premium amenities", "Coastal lifestyle"]:
            row = tk.Frame(bullets, bg=INACTIVE_CARD)
            row.pack(anchor="w", pady=1)
            c = tk.Canvas(row, width=16, height=16, bg=INACTIVE_CARD, highlightthickness=0)
            c.pack(side="left")
            c.create_oval(1, 1, 15, 15, fill=INACTIVE_ICON, outline=INACTIVE_ICON)
            tk.Label(row, text=item, fg=INACTIVE_TEXT, bg=INACTIVE_CARD,
                     font=self.f_body).pack(side="left", padx=4)

        self._bind_card(card, "island")
        return card

    def _bind_card(self, widget, region):
        widget.bind("<Button-1>", lambda e: self.select_region(region))
        for child in widget.winfo_children():
            self._bind_card(child, region)

    # ══════════════════════════════════════════════════════════════════════════
    # PUBLIC: select_region
    # ══════════════════════════════════════════════════════════════════════════
    def select_region(self, region: str):
        """Store chosen region and visually highlight the selected card."""
        self.selected_region = region
        self._refresh_mainland_card()
        self._refresh_island_card()

    def _refresh_mainland_card(self):
        active    = (self.selected_region == "mainland")
        bg        = LIGHT_GREEN   if active else INACTIVE_CARD
        fg_title  = ACCENT_GREEN  if active else INACTIVE_TEXT
        icon_fill = ACCENT_GREEN  if active else INACTIVE_ICON
        border    = BORDER_GREEN  if active else CARD_BORDER
        self.mainland_card_frame.configure(
            bg=bg, highlightbackground=border,
            highlightthickness=2 if active else 1)
        self._recolour_card(self.mainland_card_frame, bg, fg_title, icon_fill,
                            title_text="Lagos Mainland", show_tick=active)

    def _refresh_island_card(self):
        active    = (self.selected_region == "island")
        bg        = LIGHT_BLUE   if active else INACTIVE_CARD
        fg_title  = ACCENT_BLUE  if active else INACTIVE_TEXT
        icon_fill = ACCENT_BLUE  if active else INACTIVE_ICON
        border    = BORDER_BLUE  if active else CARD_BORDER
        self.island_card_frame.configure(
            bg=bg, highlightbackground=border,
            highlightthickness=2 if active else 1)
        self._recolour_card(self.island_card_frame, bg, fg_title, icon_fill,
                            title_text="Lagos Island", show_tick=active)

    def _recolour_card(self, card, bg, fg_title, icon_fill, title_text, show_tick):
        for w in self._iter_all(card):
            try:
                w.configure(bg=bg)
            except tk.TclError:
                pass
            if isinstance(w, tk.Label):
                if w.cget("text") == title_text:
                    w.configure(fg=fg_title)
                elif w.cget("fg") in (ACCENT_GREEN, ACCENT_BLUE,
                                      INACTIVE_TEXT, "#2E7D52", "#1565C0"):
                    w.configure(fg=fg_title if w.cget("text") != title_text else fg_title)
            elif isinstance(w, tk.Canvas):
                w.configure(bg=bg)
                w.delete("all")
                size = w.winfo_width()
                if size >= 20:
                    w.create_oval(1, 1, 21, 21, fill=icon_fill, outline=icon_fill)
                    if show_tick:
                        w.create_text(11, 11, text="✓", fill="white",
                                      font=tkfont.Font(family="Helvetica", size=11, weight="bold"))
                else:
                    w.create_oval(1, 1, 15, 15, fill=icon_fill, outline=icon_fill)
                    if show_tick:
                        w.create_text(8, 8, text="✓", fill="white",
                                      font=tkfont.Font(family="Helvetica", size=8, weight="bold"))

    def _iter_all(self, widget):
        yield widget
        for child in widget.winfo_children():
            yield from self._iter_all(child)

    # ── Budget inputs ─────────────────────────────────────────────────────────
    def _build_budget_inputs(self, parent):
        self._min_budget_entry = self._budget_field(parent, "Min (e.g. 2,000,000)")
        tk.Label(parent, text=" – ", bg=MAIN_BG, fg=HEADING,
                 font=self.f_input).pack(side="left")
        self._max_budget_entry = self._budget_field(parent, "Max (e.g. 5,000,000)")

    def _budget_field(self, parent, placeholder):
        vcmd = (self.register(self._only_digits), "%P")
        frame = tk.Frame(parent, bg=BUDGET_BG, bd=0)
        frame.pack(side="left")

        # Naira symbol
        naira = tk.Canvas(frame, width=22, height=28, bg=BUDGET_BG, highlightthickness=0)
        naira.pack(side="left")
        naira.create_text(11, 14, text="₦", fill=NAIRA_GREEN,
                          font=tkfont.Font(family="Helvetica", size=13, weight="bold"))

        entry = tk.Entry(frame, font=self.f_input, fg="#AAAAAA", bg=BUDGET_BG,
                         relief="flat", bd=4, width=18, insertbackground=HEADING,
                         validate="key", validatecommand=vcmd)
        entry.insert(0, placeholder)
        entry.pack(ipady=6, ipadx=6)

        def on_in(e):
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.config(fg=HEADING)
        def on_out(e):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg="#AAAAAA")

        entry.bind("<FocusIn>",  on_in)
        entry.bind("<FocusOut>", on_out)
        return entry

    @staticmethod
    def _only_digits(value):
        return all(c.isdigit() or c == "," for c in value) or value == ""

    # ══════════════════════════════════════════════════════════════════════════
    # PUBLIC: validate_budget
    # ══════════════════════════════════════════════════════════════════════════
    def validate_budget(self) -> bool:
        """
        Delegates to utils/validators.py => validate_budget().
        Returns True if valid, shows error and returns False otherwise.
        """
        from utils.validators import validate_budget

        min_val = self._min_budget_entry.get().replace(",", "")
        max_val = self._max_budget_entry.get().replace(",", "")
        is_valid  = validate_budget(min_val, max_val)

        if not is_valid:
            messagebox.showerror("Invalid Budget", "Please enter a valid budget range. Ensure Min and Max are positive numbers, and Min is not greater than Max.")
            return False
        return True

    # ══════════════════════════════════════════════════════════════════════════
    # PUBLIC: handle_search
    # ══════════════════════════════════════════════════════════════════════════
    def handle_search(self):
        """
        Validate inputs → call search_properties_controller() → open marketplace.
        Wires to: controllers/property_controller.py :: search_properties_controller()
        """
        if not self.validate_budget():
            return

        from controllers.property_controller import search_properties_controller

        min_b = self._min_budget_entry.get().replace(",", "")
        max_b = self._max_budget_entry.get().replace(",", "")

        result = search_properties_controller(
            region=self.selected_region,
            min_budget=int(min_b) if min_b.isdigit() else 0,
            max_budget=int(max_b) if max_b.isdigit() else 999_999_999,
        )

        if result["success"]:
            self.open_marketplace(properties=result.get("properties", []))
        else:
            messagebox.showerror("Search Failed", result.get("message", "No properties found"))

    # ══════════════════════════════════════════════════════════════════════════
    # PUBLIC: open_marketplace
    # ══════════════════════════════════════════════════════════════════════════
    def open_marketplace(self, properties=None):
        """
        Hide preference screen and launch marketplace.
        Wires to: ui/marketplace_screen.py :: MarketplaceScreen
        """
        from ui.marketplace_screen import MarketplaceScreen
        self.withdraw()
        market = MarketplaceScreen(
            master=self,
            user=self.user,
            region=self.selected_region,
            properties=properties or [],
        )
        market.protocol("WM_DELETE_WINDOW", self.destroy)


# ── Stand-alone entry ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
    root = tk.Tk()
    root.withdraw()
    app = PreferenceScreen(master=root)
    app.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()
