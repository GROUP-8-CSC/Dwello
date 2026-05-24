import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageOps
import os, pathlib, sys

# ── Asset paths ────────────────────────────────────────────────────────────────
_HERE        = pathlib.Path(__file__).parent
_ASSETS      = _HERE.parent / "assets" / "images"

BG_IMAGE_PATH  = str(_ASSETS / "lagos_bg.png")
LOGO_DARK_PATH = str(_ASSETS / "dwello_logo.png")
LOGO_LITE_PATH = str(_ASSETS / "white.jpeg")
ICON_USER_PATH = str(_ASSETS / "icon_user.png")
ICON_EYE_SHOW  = str(_ASSETS / "icon_eye_show.png")
ICON_EYE_HIDE  = str(_ASSETS / "icon_eye_hide.png")

# ── Colours ────────────────────────────────────────────────────────────────────
C_BG         = "#F5F5F5"
C_PANEL_BG   = "#FFFFFF"
C_DARK_NAVY  = "#1B2A4A"
C_ACCENT     = "#1B2A4A"
C_TAB_ACTIVE = "#1B2A4A"
C_TAB_IDLE   = "#9E9E9E"
C_INPUT_BG   = "#F0F0F0"
C_INPUT_FG   = "#333333"
C_HINT       = "#AAAAAA"
C_WHITE      = "#FFFFFF"
C_DIVIDER    = "#E0E0E0"
C_LINK       = "#1B2A4A"

# ── Window size ────────────────────────────────────────────────────────────────
WIN_W, WIN_H = 820, 520
LEFT_W       = 340
RIGHT_W      = WIN_W - LEFT_W
ICON_SZ      = 34


# ══════════════════════════════════════════════════════════════════════════════
class RoundedEntry(tk.Frame):
    """Entry widget with rounded background, left icon, optional right eye button."""

    def __init__(self, parent, placeholder="", icon_img=None,
                 right_img=None, show="", **kw):
        super().__init__(parent, bg=C_BG)
        self.placeholder  = placeholder
        self._show_char   = show
        self._is_placeholder = True

        self.container = tk.Frame(self, bg=C_INPUT_BG, bd=0,
                                  highlightthickness=1,
                                  highlightbackground=C_DIVIDER,
                                  highlightcolor="#7986CB")
        self.container.pack(fill="x", ipady=0)

        if icon_img:
            lbl = tk.Label(self.container, image=icon_img, bg=C_INPUT_BG)
            lbl.image = icon_img
            lbl.pack(side="left", padx=(10, 4))

        self.var   = tk.StringVar()
        self.entry = tk.Entry(self.container, textvariable=self.var,
                              bg=C_INPUT_BG, fg=C_HINT,
                              relief="flat", bd=0,
                              font=("Helvetica", 11),
                              insertbackground=C_INPUT_FG,
                              show="")
        self.entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 4))

        self._set_placeholder()
        self.entry.bind("<FocusIn>",  self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)

        if right_img:
            self._eye_label = tk.Label(self.container, image=right_img,
                                       bg=C_INPUT_BG, cursor="hand2")
            self._eye_label.image = right_img
            self._eye_label.pack(side="right", padx=(4, 10))

    def _set_placeholder(self):
        self.entry.delete(0, "end")
        self.entry.insert(0, self.placeholder)
        self.entry.config(fg=C_HINT, show="")
        self._is_placeholder = True

    def _on_focus_in(self, _=None):
        if self._is_placeholder:
            self.entry.delete(0, "end")
            self.entry.config(fg=C_INPUT_FG,
                              show=self._show_char if self._show_char else "")
            self._is_placeholder = False

    def _on_focus_out(self, _=None):
        if not self.entry.get():
            self._set_placeholder()

    def get(self):
        return "" if self._is_placeholder else self.entry.get()

    def toggle_visibility(self, show_img, hide_img):
        if self._is_placeholder:
            return
        if self._show_char:
            self.entry.config(show="")
            self._show_char = ""
            self._eye_label.config(image=hide_img)
            self._eye_label.image = hide_img
        else:
            self.entry.config(show="•")
            self._show_char = "•"
            self._eye_label.config(image=show_img)
            self._eye_label.image = show_img


# ══════════════════════════════════════════════════════════════════════════════
class AuthScreen(tk.Tk):
    """
    Entry-point window. Shows Sign Up / Log In tabs.

    Public functions (per UI breakdown):
        create_login_form()        – builds the login fields
        create_signup_form()       – builds the signup fields
        handle_login()             – validates and delegates to controller
        handle_signup()            – validates and delegates to controller
        open_preference_screen()   – destroys this window and opens preference screen
    """

    def __init__(self):
        super().__init__()
        self.title("Dwello – Find Your Perfect Lagos Home")
        self.resizable(False, False)
        self.configure(bg=C_BG)
        self.geometry(f"{WIN_W}x{WIN_H}")

        self._active_tab = tk.StringVar(value="signup")

        self._load_assets()
        self._build_left_panel()
        self._build_right_panel()
        self._centre_window()

    # ── Asset loading ─────────────────────────────────────────────────────────
    def _load_assets(self):
        def resize(path, w, h):
            img = Image.open(path).convert("RGBA").resize((w, h), Image.LANCZOS)
            return ImageTk.PhotoImage(img)

        def icon(path, color=(150, 150, 150)):
            raw  = Image.open(path).convert("RGB").resize((ICON_SZ, ICON_SZ), Image.LANCZOS)
            gray = raw.convert("L")
            alpha = ImageOps.invert(gray)
            result = Image.new("RGBA", raw.size, color + (255,))
            result.putalpha(alpha)
            return ImageTk.PhotoImage(result)

        self.tk_bg        = resize(BG_IMAGE_PATH,  LEFT_W, WIN_H)
        self.tk_logo_dark = resize(LOGO_DARK_PATH, 130, 130)
        self.tk_logo_lite = resize(LOGO_LITE_PATH, 52, 52)
        self.tk_user_icon = icon(ICON_USER_PATH)
        self.tk_eye_show  = icon(ICON_EYE_SHOW)
        self.tk_eye_hide  = icon(ICON_EYE_HIDE)

    def _centre_window(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x  = (sw - WIN_W) // 2
        y  = (sh - WIN_H) // 2
        self.geometry(f"{WIN_W}x{WIN_H}+{x}+{y}")

    # ── Left panel (hero image + overlay text) ────────────────────────────────
    def _build_left_panel(self):
        canvas = tk.Canvas(self, width=LEFT_W, height=WIN_H,
                           bd=0, highlightthickness=0)
        canvas.place(x=0, y=0)
        canvas.create_image(0, 0, anchor="nw", image=self.tk_bg)

        # Gradient overlay
        overlay = Image.new("RGBA", (LEFT_W, WIN_H), (0, 0, 0, 0))
        draw    = ImageDraw.Draw(overlay)
        for i in range(WIN_H):
            alpha = int(140 + 80 * i / WIN_H)
            draw.line([(0, i), (LEFT_W, i)], fill=(10, 20, 50, alpha))
        self._tk_overlay = ImageTk.PhotoImage(overlay)
        canvas.create_image(0, 0, anchor="nw", image=self._tk_overlay)

        canvas.create_image(LEFT_W - 20, 20, anchor="ne", image=self.tk_logo_dark)
        canvas.create_text(28, 190, anchor="nw",
                           text="Find Your\nPerfect\nLagos Home",
                           fill=C_WHITE, font=("Georgia", 26, "bold"), width=260)
        canvas.create_text(28, 360, anchor="w",
                           text="✅  Affordable.",  fill=C_WHITE, font=("Helvetica", 12))
        canvas.create_text(28, 390, anchor="w",
                           text="✅  Personalized.", fill=C_WHITE, font=("Helvetica", 12))

    # ── Right panel (card with tabs) ──────────────────────────────────────────
    def _build_right_panel(self):
        panel = tk.Frame(self, bg=C_PANEL_BG, width=RIGHT_W, height=WIN_H)
        panel.place(x=LEFT_W, y=0)
        panel.pack_propagate(False)

        # Header: logo + brand text
        hdr = tk.Frame(panel, bg=C_PANEL_BG)
        hdr.pack(fill="x", padx=28, pady=(28, 0))
        tk.Label(hdr, image=self.tk_logo_lite, bg=C_PANEL_BG).pack(side="left")
        nf = tk.Frame(hdr, bg=C_PANEL_BG)
        nf.pack(side="left", padx=(10, 0))
        tk.Label(nf, text="Dwello", font=("Georgia", 18, "bold"),
                 fg=C_DARK_NAVY, bg=C_PANEL_BG).pack(anchor="w")
        tk.Label(nf, text="Find Your Perfect Lagos Home",
                 font=("Helvetica", 9), fg=C_TAB_IDLE, bg=C_PANEL_BG).pack(anchor="w")

        # Card
        card = tk.Frame(panel, bg=C_INPUT_BG,
                        highlightbackground=C_DIVIDER, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=20, pady=18)

        # Tabs
        tab_frame = tk.Frame(card, bg=C_INPUT_BG)
        tab_frame.pack(fill="x")
        tab_container = tk.Frame(tab_frame, bg=C_INPUT_BG)
        tab_container.pack(fill="x")

        self._su_tab = self._make_tab(tab_container, "Sign Up", "signup")
        self._li_tab = self._make_tab(tab_container, "Log In",  "login")
        self._su_tab.pack(side="left", fill="x", expand=True)
        self._li_tab.pack(side="left", fill="x", expand=True)

        # Form body
        self._form_body = tk.Frame(card, bg=C_INPUT_BG)
        self._form_body.pack(fill="both", expand=True, padx=16, pady=(6, 16))

        self.create_signup_form()

    # ── Tab widget ────────────────────────────────────────────────────────────
    def _make_tab(self, parent, label, key):
        f   = tk.Frame(parent, bg=C_INPUT_BG, cursor="hand2")
        lbl = tk.Label(f, text=label,
                       font=("Helvetica", 12, "bold" if key == "signup" else "normal"),
                       fg=C_TAB_ACTIVE if key == "signup" else C_TAB_IDLE,
                       bg=C_INPUT_BG, pady=10)
        lbl.pack()
        line_color = C_ACCENT if key == "signup" else C_INPUT_BG
        line = tk.Frame(f, bg=line_color, height=2)
        line.pack(fill="x")

        if key == "signup":
            self._su_lbl, self._su_line = lbl, line
        else:
            self._li_lbl, self._li_line = lbl, line

        for w in (f, lbl):
            w.bind("<Button-1>", lambda e, k=key: self._switch_tab(k))
        return f

    def _switch_tab(self, key):
        if self._active_tab.get() == key:
            return
        self._active_tab.set(key)
        if key == "signup":
            self._su_lbl.config(fg=C_TAB_ACTIVE, font=("Helvetica", 12, "bold"))
            self._su_line.config(bg=C_ACCENT)
            self._li_lbl.config(fg=C_TAB_IDLE,   font=("Helvetica", 12, "normal"))
            self._li_line.config(bg=C_INPUT_BG)
            self.create_signup_form()
        else:
            self._li_lbl.config(fg=C_TAB_ACTIVE, font=("Helvetica", 12, "bold"))
            self._li_line.config(bg=C_ACCENT)
            self._su_lbl.config(fg=C_TAB_IDLE,   font=("Helvetica", 12, "normal"))
            self._su_line.config(bg=C_INPUT_BG)
            self.create_login_form()

    def _clear_form(self):
        for w in self._form_body.winfo_children():
            w.destroy()

    # ══════════════════════════════════════════════════════════════════════════
    # PUBLIC: create_signup_form
    # ══════════════════════════════════════════════════════════════════════════
    def create_signup_form(self):
        """Build the Sign Up fields (Full Name, Email, Password) + CTA button."""
        self._clear_form()
        fb = self._form_body

        self._name_entry  = self._entry_row(fb, "Full name",     self.tk_user_icon)
        self._email_entry = self._entry_row(fb, "Email Address", self._make_email_icon())
        self._pass_entry  = self._entry_row(fb, "Password",      None, password=True)

        btn = tk.Button(fb, text="Create Account",
                        bg=C_DARK_NAVY, fg=C_WHITE,
                        font=("Helvetica", 12, "bold"),
                        relief="flat", bd=0, cursor="hand2",
                        activebackground="#2C3E6A",
                        activeforeground=C_WHITE,
                        command=self.handle_signup)
        btn.pack(fill="x", pady=(14, 0), ipady=10)

        footer = tk.Frame(fb, bg=C_INPUT_BG)
        footer.pack(pady=(10, 0))
        tk.Label(footer, text="Already have an account?",
                 fg=C_TAB_IDLE, bg=C_INPUT_BG, font=("Helvetica", 9)).pack(side="left")
        lnk = tk.Label(footer, text=" Log In", fg=C_LINK, bg=C_INPUT_BG,
                       font=("Helvetica", 9, "bold"), cursor="hand2")
        lnk.pack(side="left")
        lnk.bind("<Button-1>", lambda e: self._switch_tab("login"))

    # ══════════════════════════════════════════════════════════════════════════
    # PUBLIC: create_login_form
    # ══════════════════════════════════════════════════════════════════════════
    def create_login_form(self):
        """Build the Log In fields (Email, Password) + CTA button."""
        self._clear_form()
        fb = self._form_body

        self._email_entry = self._entry_row(fb, "Email Address", self._make_email_icon())
        self._pass_entry  = self._entry_row(fb, "Password",      None, password=True)

        tk.Frame(fb, bg=C_INPUT_BG, height=8).pack()

        btn = tk.Button(fb, text="Log In",
                        bg=C_DARK_NAVY, fg=C_WHITE,
                        font=("Helvetica", 12, "bold"),
                        relief="flat", bd=0, cursor="hand2",
                        activebackground="#2C3E6A",
                        activeforeground=C_WHITE,
                        command=self.handle_login)
        btn.pack(fill="x", pady=(6, 0), ipady=10)

        footer = tk.Frame(fb, bg=C_INPUT_BG)
        footer.pack(pady=(10, 0))
        tk.Label(footer, text="Don't have an account?",
                 fg=C_TAB_IDLE, bg=C_INPUT_BG, font=("Helvetica", 9)).pack(side="left")
        lnk = tk.Label(footer, text=" Sign Up", fg=C_LINK, bg=C_INPUT_BG,
                       font=("Helvetica", 9, "bold"), cursor="hand2")
        lnk.pack(side="left")
        lnk.bind("<Button-1>", lambda e: self._switch_tab("signup"))

    # ══════════════════════════════════════════════════════════════════════════
    # PUBLIC: handle_signup
    # ══════════════════════════════════════════════════════════════════════════
    def handle_signup(self):
        """
        Collect signup fields → call signup_controller() → open preference screen.
        Wires to: controllers/auth_controller.py :: signup_controller()
        """
        from controllers.auth_controller import signup_controller

        name     = self._name_entry.get().strip()
        email    = self._email_entry.get().strip()
        password = self._pass_entry.get()

        result = signup_controller(name=name, email=email, password=password)

        if result["success"]:
            self.open_preference_screen(user=result.get("user"))
        else:
            tk.messagebox.showerror("Sign Up Failed", result.get("message", "Unknown error"))

    # ══════════════════════════════════════════════════════════════════════════
    # PUBLIC: handle_login
    # ══════════════════════════════════════════════════════════════════════════
    def handle_login(self):
        """
        Collect login fields → call login_controller() → open preference screen.
        Wires to: controllers/auth_controller.py :: login_controller()
        """
        from controllers.auth_controller import login_controller

        email    = self._email_entry.get().strip()
        password = self._pass_entry.get()

        result = login_controller(email=email, password=password)

        if result["success"]:
            self.open_preference_screen(user=result.get("user"))
        else:
            tk.messagebox.showerror("Login Failed", result.get("message", "Invalid credentials"))

    # ══════════════════════════════════════════════════════════════════════════
    # PUBLIC: open_preference_screen
    # ══════════════════════════════════════════════════════════════════════════
    def open_preference_screen(self, user=None):
        """
        Hide this window and launch the preference / explore screen.
        Wires to: ui/preference_screen.py :: PreferenceScreen
        """
        from ui.preference_screen import PreferenceScreen
        self.withdraw()
        pref = PreferenceScreen(master=self, user=user)
        pref.protocol("WM_DELETE_WINDOW", self.destroy)

    # ── Entry row helper ──────────────────────────────────────────────────────
    def _entry_row(self, parent, placeholder, icon_img, password=False):
        if password:
            entry = RoundedEntry(parent, placeholder=placeholder,
                                 icon_img=self._make_lock_icon(),
                                 right_img=self.tk_eye_show, show="•")
            entry._eye_label.bind(
                "<Button-1>",
                lambda e: entry.toggle_visibility(self.tk_eye_show, self.tk_eye_hide))
        else:
            entry = RoundedEntry(parent, placeholder=placeholder, icon_img=icon_img)
        entry.pack(fill="x", pady=5)
        return entry

    # ── Icon factories ────────────────────────────────────────────────────────
    def _make_email_icon(self):
        img = Image.new("RGBA", (ICON_SZ, ICON_SZ), (0, 0, 0, 0))
        d   = ImageDraw.Draw(img)
        m   = 6
        d.rectangle([m, m+4, ICON_SZ-m, ICON_SZ-m-4], outline="#AAAAAA", width=2)
        d.line([m, m+4, ICON_SZ//2, ICON_SZ//2, ICON_SZ-m, m+4],
               fill="#AAAAAA", width=2)
        return ImageTk.PhotoImage(img)

    def _make_lock_icon(self):
        img = Image.new("RGBA", (ICON_SZ, ICON_SZ), (0, 0, 0, 0))
        d   = ImageDraw.Draw(img)
        cx  = ICON_SZ // 2
        d.arc([cx-7, 3, cx+7, 18], start=0, end=180, fill="#AAAAAA", width=2)
        d.rounded_rectangle([cx-10, 15, cx+10, ICON_SZ-5],
                            radius=3, outline="#AAAAAA", width=2)
        d.ellipse([cx-3, 19, cx+3, 25], fill="#AAAAAA")
        return ImageTk.PhotoImage(img)


# ── Stand-alone entry point ────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
    app = AuthScreen()
    app.mainloop()
