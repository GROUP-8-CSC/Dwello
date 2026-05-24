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

FALLBACK_CARD_IMGS = [_p(f"{i}.jpeg") for i in range(1, 7)]

# ── Palette ────────────────────────────────────────────────────────────────────
SB_BG       = "#1B3A2D"
SB_ACTIVE   = "#2E6B45"
SB_TEXT     = "#FFFFFF"
SB_MUTED    = "#8FBB9E"
MAIN_BG     = "#FFFFFF"
PANEL_BG    = "#F0F0F0"
ACCENT      = "#2E7D52"
ACCENT_DARK = "#1F5C3A"
PRICE_BG    = "#D6EFE0"
PRICE_TEXT  = "#1F6B3E"
HEADING     = "#111111"
SUBTEXT     = "#666666"
CARD_BG     = "#FFFFFF"
CARD_BORDER = "#E0E0E0"
BTN_TEXT_C  = "#FFFFFF"
BTN_OUTLINE = "#2E7D52"
BTN_ADDED_FG= "#2E7D52"
SUMM_BG     = "#FFFFFF"
SUMM_BORDER = "#DDDDDD"
ICON_SZ     = 26
LOGO_SZ     = 80
PROP_W      = 217
PROP_H      = 216

BENEFITS = {
    "mainland": [
        "Central location",
        "Lower cost of living",
        "Easy interstate access",
    ],
    "island": [
        "Business proximity",
        "Upscale amenities",
        "Coastal lifestyle",
    ],
}

# ── Image helpers ──────────────────────────────────────────────────────────────
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
class MarketplaceScreen(tk.Toplevel):
    """
    Marketplace / search results window.

    Public functions (per UI breakdown):
        display_properties(properties)            – render property cards dynamically
        create_property_card(parent, data, cb)    – reusable card component
        handle_save_property(property_id)         – save to cart via controller
        load_cart()                               – fetch + display cart items
        remove_cart_item(property_id)             – remove item via controller
        update_benefits_panel(region)             – swap benefits text panel
    """

    def __init__(self, master=None, user=None, region="mainland", properties=None):
        super().__init__(master)
        self.title("Dwello – Marketplace")
        self.geometry("1200x760")
        self.minsize(1100, 680)
        self.configure(bg=SB_BG)

        self.user         = user
        self.region       = region
        self.properties   = properties or []
        self._cart_ids    = set()     # track which property_ids are in cart
        self._benefits_labels = []

        self._init_fonts()
        self._preload_images()
        self._build_layout()

        # Load cart on open
        self.load_cart()

    # ── Fonts ─────────────────────────────────────────────────────────────────
    def _init_fonts(self):
        F = tkfont.Font
        self.fnt = {
            "logo"    : F(family="Helvetica", size=15, weight="bold"),
            "nav"     : F(family="Helvetica", size=11),
            "nav_b"   : F(family="Helvetica", size=11, weight="bold"),
            "logout"  : F(family="Helvetica", size=11, weight="bold"),
            "heading" : F(family="Helvetica", size=14, weight="bold"),
            "title"   : F(family="Helvetica", size=11, weight="bold"),
            "sub"     : F(family="Helvetica", size=9),
            "price"   : F(family="Helvetica", size=9,  weight="bold"),
            "btn"     : F(family="Helvetica", size=10, weight="bold"),
            "summ_h"  : F(family="Helvetica", size=13, weight="bold"),
            "summ_lbl": F(family="Helvetica", size=10, weight="bold"),
            "summ_val": F(family="Helvetica", size=10),
            "search"  : F(family="Helvetica", size=11),
        }

    # ── Pre-load images ────────────────────────────────────────────────────────
    def _preload_images(self):
        self.img_logo      = _logo()
        self.img_home_w    = _icon_white(ICON_HOME)
        self.img_home_g    = _icon_dark(ICON_HOME)
        self.img_explore_w = _icon_white(ICON_EXPLORE)
        self.img_cart_w    = _icon_white(ICON_CART)
        # Fallback property images if DB returned none
        self.fallback_imgs = [_prop_img(p) for p in FALLBACK_CARD_IMGS]

    # ── Layout ────────────────────────────────────────────────────────────────
    def _build_layout(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg=SB_BG, width=210)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        self._build_sidebar()

        # Right summary panel
        self.rpanel = tk.Frame(self, bg=PANEL_BG, width=220)
        self.rpanel.pack(side="right", fill="y")
        self.rpanel.pack_propagate(False)
        self._build_right_panel()

        # Centre scrollable area
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

        self._nav_item(sb, self.img_home_g,    "Dashboard", active=True)
        self._nav_item(sb, self.img_explore_w, "Explore",   active=False)
        self._nav_item(sb, self.img_cart_w,    "Cart",      active=False)

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

    # ── Centre: search bar + scrollable cards ─────────────────────────────────
    def _build_centre(self):
        c = self.centre

        # Search bar
        search_row = tk.Frame(c, bg=MAIN_BG, pady=18)
        search_row.pack(fill="x", padx=30)

        sb_frame = tk.Frame(search_row, bg=PANEL_BG, bd=1,
                            highlightbackground="#CCCCCC", highlightthickness=1)
        sb_frame.pack(side="left")
        tk.Label(sb_frame, text="🔍", bg=PANEL_BG,
                 font=self.fnt["search"], fg="#888888").pack(side="left", padx=(10, 4), pady=8)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(sb_frame, textvariable=self.search_var,
                                font=self.fnt["search"], fg="#888888",
                                bg=PANEL_BG, relief="flat", bd=0, width=32)
        search_entry.insert(0, "Search properties")
        search_entry.pack(side="left", ipady=8, padx=(0, 12))
        self._placeholder(search_entry, "Search properties")

        # Scrollable card area
        scroll_wrap = tk.Frame(c, bg=MAIN_BG)
        scroll_wrap.pack(fill="both", expand=True, padx=30, pady=(0, 10))

        self._canvas_scroll = tk.Canvas(scroll_wrap, bg=MAIN_BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(scroll_wrap, orient="vertical",
                                 command=self._canvas_scroll.yview)
        self._canvas_scroll.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self._canvas_scroll.pack(side="left", fill="both", expand=True)

        self.card_frame = tk.Frame(self._canvas_scroll, bg=MAIN_BG)
        self._card_window = self._canvas_scroll.create_window(
            (0, 0), window=self.card_frame, anchor="nw")

        self.card_frame.bind("<Configure>",
            lambda e: self._canvas_scroll.configure(
                scrollregion=self._canvas_scroll.bbox("all")))
        self._canvas_scroll.bind("<Configure>",
            lambda e: self._canvas_scroll.itemconfig(
                self._card_window, width=e.width))
        self._canvas_scroll.bind_all("<MouseWheel>",
            lambda e: self._canvas_scroll.yview_scroll(-1*(e.delta//120), "units"))

        self.display_properties(self.properties)

    # ══════════════════════════════════════════════════════════════════════════
    # PUBLIC: display_properties
    # ══════════════════════════════════════════════════════════════════════════
    def display_properties(self, properties: list):
        """
        Render property cards dynamically from a list of property dicts.
        Each dict should have: id, title, location, price, image_path (optional).
        Falls back to static sample data if list is empty.
        """
        # Clear existing cards
        for w in self.card_frame.winfo_children():
            w.destroy()

        # Use DB properties or fallback sample data
        if not properties:
            properties = [
                {"id": i+1, "title": t, "location": l, "price": p, "image_path": None}
                for i, (t, l, p) in enumerate([
                    ("2 Bedroom Apartment",  "Yaba, Lagos Mainland",            "₦4,000,000.00"),
                    ("Luxury House",         "Victoria Island, Lagos Mainland", "₦4,500,000.00"),
                    ("Standard Duplex",      "Yaba, Lagos Mainland",            "₦3,800,000.00"),
                    ("3 Bedroom Terrace",    "Ikeja, Lagos Mainland",           "₦4,200,000.00"),
                    ("Mini Flat",            "Surulere, Lagos Mainland",        "₦2,500,000.00"),
                    ("Penthouse Suite",      "Lekki, Lagos Mainland",           "₦4,900,000.00"),
                ])
            ]

        for idx, prop in enumerate(properties):
            col = idx % 3
            row = idx // 3
            self.create_property_card(
                parent=self.card_frame,
                prop_data=prop,
                save_callback=self.handle_save_property,
                grid_row=row,
                grid_col=col,
                fallback_img_idx=idx,
            )

    # ══════════════════════════════════════════════════════════════════════════
    # PUBLIC: create_property_card
    # ══════════════════════════════════════════════════════════════════════════
    def create_property_card(self, parent, prop_data: dict,
                             save_callback, grid_row=0, grid_col=0,
                             fallback_img_idx=0):
        """
        Reusable property card component.
        prop_data keys: id, title, location, price, image_path
        """
        prop_id    = prop_data.get("id")
        title      = prop_data.get("title", "Property")
        location   = prop_data.get("location", "Lagos")
        price      = prop_data.get("price", "₦0")
        image_path = prop_data.get("image_path")

        card = tk.Frame(parent, bg=CARD_BG, bd=1,
                        highlightbackground=CARD_BORDER, highlightthickness=1,
                        cursor="hand2")
        card.grid(row=grid_row, column=grid_col, padx=8, pady=8, sticky="nsew")
        parent.grid_columnconfigure(grid_col, weight=1)

        # Property image (from DB path or fallback asset)
        img = None
        if image_path and os.path.exists(image_path):
            img = _prop_img(image_path)
        elif fallback_img_idx < len(self.fallback_imgs):
            img = self.fallback_imgs[fallback_img_idx]

        if img:
            lbl = tk.Label(card, image=img, bg=CARD_BG)
            lbl.image = img   # prevent GC
        else:
            lbl = tk.Label(card, bg="#CCCCCC", width=PROP_W, height=PROP_H,
                           text="No image", fg="#888888")
        lbl.pack()

        # Content
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

        # Save / Added to Cart button
        already_in_cart = (prop_id in self._cart_ids)
        btn_canvas = tk.Canvas(content, bg=CARD_BG, highlightthickness=0,
                               height=38, width=PROP_W - 24)
        btn_canvas.pack(pady=(10, 2))
        btn_canvas._prop_id = prop_id

        def _draw_btn(canvas, in_cart):
            canvas.delete("all")
            if in_cart:
                canvas.create_rectangle(0, 0, PROP_W-24, 38,
                                        fill=CARD_BG, outline=BTN_OUTLINE, width=1.5)
                canvas.create_text((PROP_W-24)//2, 19, text="Added to Cart",
                                   fill=BTN_ADDED_FG, font=self.fnt["btn"])
            else:
                canvas.create_rectangle(0, 0, PROP_W-24, 38,
                                        fill=ACCENT, outline=ACCENT)
                canvas.create_text((PROP_W-24)//2, 19, text="Add to Cart",
                                   fill=BTN_TEXT_C, font=self.fnt["btn"])

        _draw_btn(btn_canvas, already_in_cart)

        def on_btn_click(e, canvas=btn_canvas, pid=prop_id):
            save_callback(pid)
            _draw_btn(canvas, True)

        btn_canvas.bind("<Button-1>", on_btn_click)
        btn_canvas.bind("<Enter>",
            lambda e, b=btn_canvas: b.itemconfig(1, fill=ACCENT_DARK)
            if prop_id not in self._cart_ids else None)
        btn_canvas.bind("<Leave>",
            lambda e, b=btn_canvas: b.itemconfig(1, fill=ACCENT)
            if prop_id not in self._cart_ids else None)

        return card

    # ══════════════════════════════════════════════════════════════════════════
    # PUBLIC: handle_save_property
    # ══════════════════════════════════════════════════════════════════════════
    def handle_save_property(self, property_id):
        """
        Save property to cart.
        Wires to: controllers/cart_controller.py :: add_to_cart_controller()
        """
        if property_id in self._cart_ids:
            return  # already saved

        from controllers.cart_controller import add_to_cart_controller

        result = add_to_cart_controller(
            user=self.user,
            property_id=property_id,
        )

        if result["success"]:
            self._cart_ids.add(property_id)
            self._update_cart_count()
        else:
            messagebox.showerror("Cart Error", result.get("message", "Could not save property"))

    # ══════════════════════════════════════════════════════════════════════════
    # PUBLIC: load_cart
    # ══════════════════════════════════════════════════════════════════════════
    def load_cart(self):
        """
        Fetch saved cart items from DB and update summary panel.
        Wires to: controllers/cart_controller.py :: load_cart_controller()
        """
        from controllers.cart_controller import load_cart_controller

        result = load_cart_controller(user=self.user)

        if result["success"]:
            cart_items = result.get("items", [])
            self._cart_ids = {item["id"] for item in cart_items}
            self._update_cart_count()
        # Silently fail on first load if DB not connected yet

    # ══════════════════════════════════════════════════════════════════════════
    # PUBLIC: remove_cart_item
    # ══════════════════════════════════════════════════════════════════════════
    def remove_cart_item(self, property_id):
        """
        Remove a property from the cart.
        Wires to: controllers/cart_controller.py :: remove_from_cart_controller()
        """
        from controllers.cart_controller import remove_from_cart_controller

        result = remove_from_cart_controller(user=self.user, property_id=property_id)

        if result["success"]:
            self._cart_ids.discard(property_id)
            self._update_cart_count()
            self.display_properties(self.properties)  # re-render to clear "Added" state
        else:
            messagebox.showerror("Error", result.get("message", "Could not remove item"))

    # ══════════════════════════════════════════════════════════════════════════
    # PUBLIC: update_benefits_panel
    # ══════════════════════════════════════════════════════════════════════════
    def update_benefits_panel(self, region: str):
        """Swap the benefits text in the right panel based on selected region."""
        self.region = region
        items = BENEFITS.get(region, [])
        for i, lbl in enumerate(self._benefits_labels):
            lbl.config(text=items[i] if i < len(items) else "")

    # ── Right summary panel ───────────────────────────────────────────────────
    def _build_right_panel(self):
        rp = self.rpanel

        tk.Label(rp, text="Search Summary", font=self.fnt["summ_h"],
                 fg=HEADING, bg=PANEL_BG).pack(anchor="w", padx=20, pady=(30, 14))

        self._summ_card(rp)

        # Benefits panel (region-specific)
        tk.Label(rp, text="Area Benefits", font=self.fnt["summ_lbl"],
                 fg=HEADING, bg=PANEL_BG).pack(anchor="w", padx=20, pady=(18, 4))

        self._benefits_labels = []
        for _ in range(3):
            lbl = tk.Label(rp, text="", fg=SUBTEXT, bg=PANEL_BG,
                           font=self.fnt["summ_val"], anchor="w", wraplength=180)
            lbl.pack(fill="x", padx=20, pady=1)
            self._benefits_labels.append(lbl)

        self.update_benefits_panel(self.region)

        self._action_btn(rp, "🔍  Change Search",   top_pad=18)
        self._action_btn(rp, "🔄  Refresh Results", top_pad=8)

    def _summ_card(self, parent):
        card = tk.Frame(parent, bg=SUMM_BG, bd=1,
                        highlightbackground=SUMM_BORDER, highlightthickness=1)
        card.pack(fill="x", padx=20)

        inner = tk.Frame(card, bg=SUMM_BG, padx=14, pady=12)
        inner.pack(fill="x")

        # Region row
        region_row = tk.Frame(inner, bg=SUMM_BG)
        region_row.pack(fill="x", pady=(0, 10))
        pin = tk.Canvas(region_row, bg=SUMM_BG, highlightthickness=0, width=22, height=26)
        pin.pack(side="left", padx=(0, 8))
        pin.create_oval(5, 2, 17, 14, outline="#333", width=1.5, fill="")
        pin.create_line(11, 14, 11, 24, fill="#333", width=1.5)
        txt = tk.Frame(region_row, bg=SUMM_BG)
        txt.pack(side="left")
        tk.Label(txt, text="Region", font=self.fnt["summ_lbl"],
                 fg=HEADING, bg=SUMM_BG).pack(anchor="w")
        region_display = self.region.replace("mainland", "Lagos Mainland").replace("island", "Lagos Island")
        tk.Label(txt, text=region_display.title(), font=self.fnt["summ_val"],
                 fg=ACCENT, bg=SUMM_BG).pack(anchor="w")

        tk.Frame(inner, bg=SUMM_BORDER, height=1).pack(fill="x", pady=4)

        # Cart count row
        budget_row = tk.Frame(inner, bg=SUMM_BG)
        budget_row.pack(fill="x", pady=(6, 0))
        bag = tk.Canvas(budget_row, bg=SUMM_BG, highlightthickness=0, width=22, height=26)
        bag.pack(side="left", padx=(0, 8))
        bag.create_oval(4, 8, 18, 22, outline="#333", width=1.5, fill="")
        bag.create_line(9, 8, 11, 4, fill="#333", width=1.5)
        bag.create_line(13, 8, 11, 4, fill="#333", width=1.5)
        txt2 = tk.Frame(budget_row, bg=SUMM_BG)
        txt2.pack(side="left")
        tk.Label(txt2, text="Cart", font=self.fnt["summ_lbl"],
                 fg=HEADING, bg=SUMM_BG).pack(anchor="w")
        self._cart_count_lbl = tk.Label(txt2, text="0 items", font=self.fnt["summ_val"],
                                        fg=ACCENT, bg=SUMM_BG)
        self._cart_count_lbl.pack(anchor="w")

    def _update_cart_count(self):
        n = len(self._cart_ids)
        if hasattr(self, "_cart_count_lbl"):
            self._cart_count_lbl.config(text=f"{n} item{'s' if n != 1 else ''}")

    def _action_btn(self, parent, label, top_pad=8):
        btn = tk.Frame(parent, bg=SUMM_BG, bd=1,
                       highlightbackground=SUMM_BORDER, highlightthickness=1,
                       cursor="hand2")
        btn.pack(fill="x", padx=20, pady=(top_pad, 0))
        inner = tk.Frame(btn, bg=SUMM_BG, padx=14, pady=12)
        inner.pack(fill="x")
        tk.Label(inner, text=label, font=self.fnt["nav_b"],
                 fg=HEADING, bg=SUMM_BG).pack(anchor="w")
        btn.bind("<Enter>", lambda e: btn.configure(highlightbackground=ACCENT))
        btn.bind("<Leave>", lambda e: btn.configure(highlightbackground=SUMM_BORDER))

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
    app = MarketplaceScreen(master=root)
    app.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()
