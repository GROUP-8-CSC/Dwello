import tkinter as tk
from tkinter import font as tkfont, messagebox
from PIL import Image, ImageTk
import os
 
# ── Paths ──────────────────────────────────────────────────────────────────────
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(_CURRENT_DIR, "..", "assets", "images"))
 
LOGO_PATH    = os.path.join(BASE, "dwello_logo.png")
EXPLORE_PATH = os.path.join(BASE, "compass.png")
HOME_PATH    = os.path.join(BASE, "house.png")
CART_PATH    = os.path.join(BASE, "shopping-cart.png")
 
MAINLAND_ILLUS_PATH = os.path.join(BASE, "image_1.png")   # bridge
ISLAND_ILLUS_PATH   = os.path.join(BASE, "image_2.png")   # palm/coastal
 
# ── Colours ───────────────────────────────────────────────────────────────────
SIDEBAR_BG    = "#1B3A2D"
SIDEBAR_ACTIVE= "#2D5A40"
SIDEBAR_TEXT  = "#FFFFFF"
SIDEBAR_MUTED = "#8FB8A0"
MAIN_BG       = "#FFFFFF"
ACCENT_GREEN  = "#2E7D52"
LIGHT_GREEN   = "#E8F5EE"
BORDER_GREEN  = "#2E7D52"
CARD_BORDER   = "#D0E8D8"
INACTIVE_CARD = "#F5F5F5"
INACTIVE_TEXT = "#AAAAAA"
INACTIVE_ICON = "#CCCCCC"
HEADING       = "#1A1A1A"
SUBTEXT       = "#666666"
BUDGET_BG     = "#F0F0F0"
BTN_BG        = "#1A1A2E"
BTN_TEXT      = "#FFFFFF"
NAIRA_GREEN   = "#2E7D52"
 
# ── Island card (blue theme when selected) ────────────────────────────────────
ACCENT_BLUE   = "#1565C0"
LIGHT_BLUE    = "#E3F0FB"
BORDER_BLUE   = "#1565C0"
 
ICON_SIZE = (26, 26)
LOGO_SIZE = (80, 80)
 
 
def load_image(path, size):
    img = Image.open(path).convert("RGBA").resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)
 
 
def load_icon_white(path, size):
    img = Image.open(path).convert("RGBA").resize(size, Image.LANCZOS)
    r, g, b, a = img.split()
    white = Image.new("RGBA", img.size, (255, 255, 255, 255))
    white.putalpha(a)
    return ImageTk.PhotoImage(white)
 
 
def load_icon_dark(path, size):
    img = Image.open(path).convert("RGBA").resize(size, Image.LANCZOS)
    r, g, b, a = img.split()
    colored = Image.new("RGBA", img.size, (46, 125, 82, 255))
    colored.putalpha(a)
    return ImageTk.PhotoImage(colored)
 
 
def set_bg_recursive(widget, color):
    """Recursively set background colour on a widget and all its children."""
    try:
        widget.configure(bg=color)
    except tk.TclError:
        pass
    for child in widget.winfo_children():
        set_bg_recursive(child, color)
 
 
# ── Main App ───────────────────────────────────────────────────────────────────
class DwelloApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dwello")
        self.geometry("900x600")
        self.resizable(False, False)
        self.configure(bg=SIDEBAR_BG)
 
        # Track selected region: "mainland" or "island"
        self.selected_region = "mainland"
 
        # Track active sidebar page
        self.active_page = "Explore"
 
        # ── Fonts ──────────────────────────────────────────────────────────────
        self.f_title      = tkfont.Font(family="Helvetica", size=20, weight="bold")
        self.f_sub        = tkfont.Font(family="Helvetica", size=10)
        self.f_section    = tkfont.Font(family="Helvetica", size=13, weight="bold")
        self.f_body       = tkfont.Font(family="Helvetica", size=9)
        self.f_sidebar    = tkfont.Font(family="Helvetica", size=11)
        self.f_sidebar_b  = tkfont.Font(family="Helvetica", size=11, weight="bold")
        self.f_btn        = tkfont.Font(family="Helvetica", size=12, weight="bold")
        self.f_logout     = tkfont.Font(family="Helvetica", size=11, weight="bold")
        self.f_input      = tkfont.Font(family="Helvetica", size=10)
 
        # ── Images ─────────────────────────────────────────────────────────────
        self.img_logo      = load_image(LOGO_PATH, LOGO_SIZE)
        self.img_home_w    = load_icon_white(HOME_PATH, ICON_SIZE)
        self.img_explore_w = load_icon_white(EXPLORE_PATH, ICON_SIZE)
        self.img_cart_w    = load_icon_white(CART_PATH, ICON_SIZE)
        self.img_explore_g = load_icon_dark(EXPLORE_PATH, ICON_SIZE)
        self.img_mainland  = load_image(MAINLAND_ILLUS_PATH, (90, 80))
        self.img_island    = load_image(ISLAND_ILLUS_PATH, (90, 80))
 
        # References updated on region toggle
        self.mainland_card_frame = None
        self.island_card_frame   = None
 
        # Sidebar nav row references for highlight toggling
        self._sidebar_rows = {}
 
        self._build_layout()
 
    # ── Layout ─────────────────────────────────────────────────────────────────
    def _build_layout(self):
        self.sidebar = tk.Frame(self, bg=SIDEBAR_BG, width=160)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        self._build_sidebar(self.sidebar)
 
        self.main_frame = tk.Frame(self, bg=MAIN_BG)
        self.main_frame.pack(side="left", fill="both", expand=True)
        self._build_main(self.main_frame)
 
    # ── Sidebar ────────────────────────────────────────────────────────────────
    def _build_sidebar(self, parent):
        logo_frame = tk.Frame(parent, bg=SIDEBAR_BG, pady=20)
        logo_frame.pack(fill="x")
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
        bg = SIDEBAR_ACTIVE if active else SIDEBAR_BG
        fg = SIDEBAR_TEXT if active else SIDEBAR_MUTED
 
        row = tk.Frame(parent, bg=bg, cursor="hand2")
        row.pack(fill="x", pady=1)
        inner = tk.Frame(row, bg=bg, padx=16, pady=10)
        inner.pack(fill="x")
 
        icon_lbl = tk.Label(inner, image=icon, bg=bg)
        icon_lbl.pack(side="left")
        text_lbl = tk.Label(inner, text=label, fg=fg, bg=bg,
                            font=self.f_sidebar_b if active else self.f_sidebar)
        text_lbl.pack(side="left", padx=10)
 
        # Store child widgets for re-colouring
        row._inner = inner
        row._icon_lbl = icon_lbl
        row._text_lbl = text_lbl
        row._label = label
 
        # Click binding on every part of the row
        for widget in (row, inner, icon_lbl, text_lbl):
            widget.bind("<Button-1>", lambda e, l=label: self._on_nav_click(l))
 
        return row
 
    def _on_nav_click(self, label):
        # Deactivate previous
        for lbl, row in self._sidebar_rows.items():
            is_active = (lbl == label)
            bg = SIDEBAR_ACTIVE if is_active else SIDEBAR_BG
            fg = SIDEBAR_TEXT if is_active else SIDEBAR_MUTED
            font = self.f_sidebar_b if is_active else self.f_sidebar
            row.configure(bg=bg)
            row._inner.configure(bg=bg)
            row._icon_lbl.configure(bg=bg)
            row._text_lbl.configure(bg=bg, fg=fg, font=font)
 
        self.active_page = label
        # Show a placeholder message for unimplemented pages
        if label != "Explore":
            messagebox.showinfo("Dwello", f"{label} page coming soon!")
 
    def _sidebar_logout(self, parent):
        frame = tk.Frame(parent, bg=SIDEBAR_BG, pady=20)
        frame.pack(fill="x")
        btn = tk.Frame(frame, bg=SIDEBAR_BG, bd=0)
        btn.pack(padx=16, fill="x")
 
        canvas = tk.Canvas(btn, bg=SIDEBAR_BG, highlightthickness=0,
                           height=42, width=128, cursor="hand2")
        canvas.pack()
        canvas.create_rectangle(0, 0, 128, 42,
                                 outline=SIDEBAR_TEXT, width=1.5, fill=SIDEBAR_BG)
        canvas.create_text(18, 21, text="←", fill=SIDEBAR_TEXT,
                            font=tkfont.Font(family="Helvetica", size=13, weight="bold"))
        canvas.create_text(72, 21, text="Log Out", fill=SIDEBAR_TEXT,
                            font=self.f_logout)
        canvas.bind("<Button-1>", lambda e: self.destroy())
 
    # ── Main Content ───────────────────────────────────────────────────────────
    def _build_main(self, parent):
        self.scroll_frame = tk.Frame(parent, bg=MAIN_BG)
        self.scroll_frame.pack(fill="both", expand=True, padx=40, pady=30)
 
        tk.Label(self.scroll_frame,
                 text="Let's find the perfect property for you",
                 font=self.f_title, fg=HEADING, bg=MAIN_BG).pack(anchor="center")
        tk.Label(self.scroll_frame,
                 text="Choose your preferred region and budget to get started",
                 font=self.f_sub, fg=SUBTEXT, bg=MAIN_BG).pack(anchor="center", pady=(4, 0))
 
        tk.Label(self.scroll_frame, text="Choose Your Preferred Region",
                 font=self.f_section, fg=HEADING, bg=MAIN_BG).pack(anchor="w", pady=(24, 10))
 
        cards_row = tk.Frame(self.scroll_frame, bg=MAIN_BG)
        cards_row.pack(fill="x")
 
        self.mainland_card_frame = self._build_mainland_card(cards_row)
        tk.Frame(cards_row, bg=MAIN_BG, width=16).pack(side="left")
        self.island_card_frame = self._build_island_card(cards_row)
 
        # ── Budget Section ──────────────────────────────────────────────────
        tk.Label(self.scroll_frame, text="Set Your Budget Range",
                 font=self.f_section, fg=HEADING, bg=MAIN_BG).pack(anchor="w", pady=(28, 12))
 
        budget_frame = tk.Frame(self.scroll_frame, bg=MAIN_BG)
        budget_frame.pack(anchor="w")
 
        self._budget_row(budget_frame, "eg. 2,000,000")
        tk.Label(budget_frame, text="—", fg=SUBTEXT, bg=MAIN_BG,
                 font=self.f_body).pack(anchor="w", padx=4, pady=2)
        self._budget_row(budget_frame, "eg. 5,000,000")
 
        # ── Explore Button ──────────────────────────────────────────────────
        btn_row = tk.Frame(self.scroll_frame, bg=MAIN_BG)
        btn_row.pack(fill="x", pady=(24, 0))
        tk.Frame(btn_row, bg=MAIN_BG).pack(side="left", expand=True)
 
        btn_canvas = tk.Canvas(btn_row, bg=MAIN_BG, highlightthickness=0,
                               height=50, width=210, cursor="hand2")
        btn_canvas.pack(side="right")
        btn_canvas.create_rectangle(0, 0, 210, 50, fill=BTN_BG,
                                    outline=BTN_BG, width=0, tags="btn_bg")
        btn_canvas.create_text(85, 25, text="Explore Properties",
                               fill=BTN_TEXT, font=self.f_btn,
                               anchor="center", tags="btn_text")
        btn_canvas.create_text(185, 25, text="→", fill=BTN_TEXT,
                               font=tkfont.Font(family="Helvetica", size=14, weight="bold"),
                               tags="btn_arrow")
 
        btn_canvas.bind("<Button-1>",       self._on_explore_click)
        btn_canvas.bind("<Enter>",          lambda e: btn_canvas.itemconfig("btn_bg", fill="#2E3060"))
        btn_canvas.bind("<Leave>",          lambda e: btn_canvas.itemconfig("btn_bg", fill=BTN_BG))
 
    # ── Region card toggling ────────────────────────────────────────────────────
    def _select_region(self, region):
        """Toggle the active/inactive state of both region cards."""
        self.selected_region = region
        self._refresh_mainland_card()
        self._refresh_island_card()
 
    def _refresh_mainland_card(self):
        active = (self.selected_region == "mainland")
        card = self.mainland_card_frame
        bg   = LIGHT_GREEN if active else INACTIVE_CARD
        fg   = ACCENT_GREEN if active else INACTIVE_TEXT
        icon_fill = ACCENT_GREEN if active else INACTIVE_ICON
 
        card.configure(bg=bg,
                       highlightbackground=BORDER_GREEN if active else CARD_BORDER,
                       highlightthickness=2 if active else 1)
 
        # Walk children and update colours + check visibility
        def update(w):
            try:
                w.configure(bg=bg)
            except tk.TclError:
                pass
            for c in w.winfo_children():
                update(c)
 
        update(card)
 
        # Update labels' fg
        for w in self._iter_all(card):
            if isinstance(w, tk.Label):
                if w.cget("text") == "Lagos Mainland":
                    w.configure(fg=fg)
                elif w.cget("fg") in (ACCENT_GREEN, INACTIVE_TEXT):
                    w.configure(fg=fg)
            elif isinstance(w, tk.Canvas):
                # checkmark circle or bullet
                try:
                    w.itemconfig("oval", fill=icon_fill, outline=icon_fill)
                except Exception:
                    pass
 
        # Redraw check/bullet canvases
        for w in self._iter_all(card):
            if isinstance(w, tk.Canvas):
                w.configure(bg=bg)
                w.delete("all")
                if w.winfo_width() <= 24:  # small bullet / checkmark canvas
                    size = w.winfo_width()
                    if size >= 20:
                        w.create_oval(1, 1, 21, 21, fill=icon_fill, outline=icon_fill)
                        if active:
                            w.create_text(11, 11, text="✓", fill="white",
                                          font=tkfont.Font(family="Helvetica", size=11, weight="bold"))
                    else:
                        w.create_oval(1, 1, 15, 15, fill=icon_fill, outline=icon_fill)
                        if active:
                            w.create_text(8, 8, text="✓", fill="white",
                                          font=tkfont.Font(family="Helvetica", size=8, weight="bold"))
 
    def _refresh_island_card(self):
        active = (self.selected_region == "island")
        card = self.island_card_frame
        bg        = LIGHT_BLUE    if active else INACTIVE_CARD
        fg        = ACCENT_BLUE   if active else INACTIVE_TEXT
        icon_fill = ACCENT_BLUE   if active else INACTIVE_ICON
 
        card.configure(bg=bg,
                       highlightbackground=BORDER_BLUE if active else CARD_BORDER,
                       highlightthickness=2 if active else 1)
 
        def update(w):
            try:
                w.configure(bg=bg)
            except tk.TclError:
                pass
            for c in w.winfo_children():
                update(c)
 
        update(card)
 
        for w in self._iter_all(card):
            if isinstance(w, tk.Label):
                if w.cget("text") == "Lagos Island":
                    w.configure(fg=fg)
                elif w.cget("fg") in (ACCENT_BLUE, INACTIVE_TEXT):
                    w.configure(fg=fg)
            elif isinstance(w, tk.Canvas):
                w.configure(bg=bg)
                w.delete("all")
                if w.winfo_width() <= 24:
                    w.create_oval(1, 1, 15, 15, fill=icon_fill, outline=icon_fill)
                    if active:
                        w.create_text(8, 8, text="✓", fill="white",
                                      font=tkfont.Font(family="Helvetica", size=8, weight="bold"))
 
    def _iter_all(self, widget):
        yield widget
        for child in widget.winfo_children():
            yield from self._iter_all(child)
 
    # ── Cards ──────────────────────────────────────────────────────────────────
    def _build_mainland_card(self, parent):
        card = tk.Frame(parent, bg=LIGHT_GREEN, bd=0,
                        highlightbackground=BORDER_GREEN, highlightthickness=2,
                        cursor="hand2")
        card.pack(side="left", fill="both", expand=True, ipadx=12, ipady=12)
 
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
 
        tk.Label(body, image=self.img_mainland, bg=LIGHT_GREEN,
                 bd=0).pack(side="left", padx=(0, 12))
 
        bullets = tk.Frame(body, bg=LIGHT_GREEN)
        bullets.pack(side="left", anchor="n", pady=4)
        for item in ["Lower cost of living", "Central transport access",
                     "Easy interstate access", "Vibrant urban lifestyle"]:
            row = tk.Frame(bullets, bg=LIGHT_GREEN)
            row.pack(anchor="w", pady=1)
            chk2 = tk.Canvas(row, width=16, height=16, bg=LIGHT_GREEN, highlightthickness=0)
            chk2.pack(side="left")
            chk2.create_oval(1, 1, 15, 15, fill=ACCENT_GREEN, outline=ACCENT_GREEN)
            chk2.create_text(8, 8, text="✓", fill="white",
                             font=tkfont.Font(family="Helvetica", size=8, weight="bold"))
            tk.Label(row, text=item, fg=ACCENT_GREEN, bg=LIGHT_GREEN,
                     font=self.f_body).pack(side="left", padx=4)
 
        # Bind click on entire card
        self._bind_card_click(card, "mainland")
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
 
        tk.Label(body, image=self.img_island, bg=INACTIVE_CARD,
                 bd=0).pack(side="left", padx=(0, 12))
 
        bullets = tk.Frame(body, bg=INACTIVE_CARD)
        bullets.pack(side="left", anchor="n", pady=4)
        for item in ["Proximity to business districts", "Upscale neighborhoods",
                     "Premium amenities", "Coastal lifestyle"]:
            row = tk.Frame(bullets, bg=INACTIVE_CARD)
            row.pack(anchor="w", pady=1)
            chk = tk.Canvas(row, width=16, height=16, bg=INACTIVE_CARD, highlightthickness=0)
            chk.pack(side="left")
            chk.create_oval(1, 1, 15, 15, fill=INACTIVE_ICON, outline=INACTIVE_ICON)
            tk.Label(row, text=item, fg=INACTIVE_TEXT, bg=INACTIVE_CARD,
                     font=self.f_body).pack(side="left", padx=4)
 
        self._bind_card_click(card, "island")
        return card
 
    def _bind_card_click(self, widget, region):
        widget.bind("<Button-1>", lambda e: self._select_region(region))
        for child in widget.winfo_children():
            self._bind_card_click(child, region)
 
    # ── Budget row ─────────────────────────────────────────────────────────────
    def _budget_row(self, parent, placeholder):
        row = tk.Frame(parent, bg=MAIN_BG)
        row.pack(anchor="w", pady=3)
 
        naira = tk.Canvas(row, width=22, height=28, bg=MAIN_BG, highlightthickness=0)
        naira.pack(side="left")
        naira.create_text(11, 14, text="₦", fill=NAIRA_GREEN,
                          font=tkfont.Font(family="Helvetica", size=13, weight="bold"))
 
        # Validate: only allow digits and commas
        vcmd = (self.register(self._validate_budget), "%P")
 
        entry_bg = tk.Frame(row, bg=BUDGET_BG, bd=0)
        entry_bg.pack(side="left")
        entry = tk.Entry(entry_bg, font=self.f_input, fg="#AAAAAA", bg=BUDGET_BG,
                         relief="flat", bd=4, width=20, insertbackground=HEADING,
                         validate="key", validatecommand=vcmd)
        entry.insert(0, placeholder)
        entry.pack(ipady=6, ipadx=6)
 
        def on_focus_in(e):
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.config(fg=HEADING)
 
        def on_focus_out(e):
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.config(fg="#AAAAAA")
 
        entry.bind("<FocusIn>",  on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
 
    @staticmethod
    def _validate_budget(value):
        """Allow only digits, commas, and empty string."""
        return all(c.isdigit() or c == "," for c in value) or value == ""
 
    # ── Explore button handler ──────────────────────────────────────────────────
    def _on_explore_click(self, event=None):
        messagebox.showinfo(
            "Dwello",
            f"Exploring properties in {self.selected_region.replace('mainland','Lagos Mainland').replace('island','Lagos Island')}!"
        )
 
 
if __name__ == "__main__":
    app = DwelloApp()
    app.mainloop()