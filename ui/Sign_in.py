import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageOps
import os
import sys

# ── Asset paths (Raw string protects backslashes) ──────────────────────────────
UPLOADS = "C:/Users/LENOVO T14/Documents/Dwello/assets/images"
BG_IMAGE_PATH    = os.path.join(UPLOADS, "lagos_bg.png")
LOGO_DARK_PATH   = os.path.join(UPLOADS, "dwello_logo.png")
LOGO_LIGHT_PATH  = os.path.join(UPLOADS, "white.jpeg")
ICON_USER_PATH   = os.path.join(UPLOADS, "icon_user.png")
ICON_EYE_SHOW    = os.path.join(UPLOADS, "icon_eye_show.png")
ICON_EYE_HIDE    = os.path.join(UPLOADS, "icon_eye_hide.png")
 
# ── Colours ────────────────────────────────────────────────────────────────────
C_BG          = "#F5F5F5"
C_PANEL_BG    = "#FFFFFF"
C_DARK_NAVY   = "#1B2A4A"
C_ACCENT      = "#1B2A4A"   
C_TAB_ACTIVE  = "#1B2A4A"
C_TAB_IDLE    = "#9E9E9E"
C_INPUT_BG    = "#F0F0F0"
C_INPUT_FG    = "#333333"
C_HINT        = "#AAAAAA"
C_WHITE       = "#FFFFFF"
C_GREEN       = "#2E7D32"
C_DIVIDER     = "#E0E0E0"
C_LINK        = "#1B2A4A"
 
# ── Window size ────────────────────────────────────────────────────────────────
WIN_W, WIN_H   = 820, 520
LEFT_W         = 340          
RIGHT_W        = WIN_W - LEFT_W
 
ICON_SZ        = 34
INPUT_H        = 42
RADIUS         = 8            
 
 
class RoundedEntry(tk.Frame):
    """Entry widget with a rounded background, left icon slot, optional right button."""
    def __init__(self, parent, placeholder="", icon_img=None,
                 right_img=None, show="", **kw):
        super().__init__(parent, bg=C_BG)
        self.placeholder   = placeholder
        self._show_char    = show
        self._showing      = (show == "")   
 
        self.container = tk.Frame(self, bg=C_INPUT_BG, bd=0,
                                  highlightthickness=1,
                                  highlightbackground=C_DIVIDER,
                                  highlightcolor="#7986CB")
        self.container.pack(fill="x", ipady=0)
 
        if icon_img:
            lbl = tk.Label(self.container, image=icon_img, bg=C_INPUT_BG, cursor="arrow")
            lbl.image = icon_img
            lbl.pack(side="left", padx=(10, 4))
 
        self.var = tk.StringVar()
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
            self._eye_label = tk.Label(self.container, image=right_img, bg=C_INPUT_BG, cursor="hand2")
            self._eye_label.image = right_img
            self._eye_label.pack(side="right", padx=(4, 10))
 
    def _set_placeholder(self):
        self.entry.delete(0, "end")
        self.entry.insert(0, self.placeholder)
        self.entry.config(fg=C_HINT, show="")
        self._is_placeholder = True
 
    def _on_focus_in(self, _event=None):
        if self._is_placeholder:
            self.entry.delete(0, "end")
            self.entry.config(fg=C_INPUT_FG, show=self._show_char if self._show_char else "")
            self._is_placeholder = False
 
    def _on_focus_out(self, _event=None):
        if not self.entry.get():
            self._set_placeholder()
 
    def get(self):
        if self._is_placeholder:
            return ""
        return self.entry.get()
 
    def toggle_visibility(self, show_img, hide_img):
        if self._is_placeholder:
            return
        if self._show_char:                  
            self.entry.config(show="")
            self._show_char = ""
            self._showing = True
            self._eye_label.config(image=hide_img)
            self._eye_label.image = hide_img
        else:                                
            self.entry.config(show="•")
            self._show_char = "•"
            self._showing = False
            self._eye_label.config(image=show_img)
            self._eye_label.image = show_img
 
 
class DwelloApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dwello – Find Your Perfect Lagos Home")
        self.resizable(False, False)
 
        self._load_assets()
 
        self.configure(bg=C_BG)
        self.geometry(f"{WIN_W}x{WIN_H}")
 
        self._build_left()
        self._build_right()
 
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x  = (sw - WIN_W) // 2
        y  = (sh - WIN_H) // 2
        self.geometry(f"{WIN_W}x{WIN_H}+{x}+{y}")
 
    def _load_assets(self):
        def load_resize(path, w, h):
            img = Image.open(path).convert("RGBA").resize((w, h), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
 
        self.tk_bg        = load_resize(BG_IMAGE_PATH,   LEFT_W,  WIN_H)
        self.tk_logo_dark = load_resize(LOGO_DARK_PATH,  130,     130)
        self.tk_logo_lite = load_resize(LOGO_LIGHT_PATH, 52,      52)
 
        def icon(path, color=(150, 150, 150)):
            raw  = Image.open(path).convert("RGB").resize((ICON_SZ, ICON_SZ), Image.LANCZOS)
            gray = raw.convert("L")
            alpha = ImageOps.invert(gray)
            result = Image.new("RGBA", raw.size, color + (255,))
            result.putalpha(alpha)
            return ImageTk.PhotoImage(result)
 
        self.tk_user_icon  = icon(ICON_USER_PATH)
        self.tk_eye_show   = icon(ICON_EYE_SHOW)
        self.tk_eye_hide   = icon(ICON_EYE_HIDE)
 
    def _build_left(self):
        canvas = tk.Canvas(self, width=LEFT_W, height=WIN_H, bd=0, highlightthickness=0)
        canvas.place(x=0, y=0)
        canvas.create_image(0, 0, anchor="nw", image=self.tk_bg)
 
        overlay = Image.new("RGBA", (LEFT_W, WIN_H), (0, 0, 0, 0))
        draw    = ImageDraw.Draw(overlay)
        for i in range(WIN_H):
            alpha = int(140 + 80 * i / WIN_H)
            draw.line([(0, i), (LEFT_W, i)], fill=(10, 20, 50, alpha))
        self._tk_overlay = ImageTk.PhotoImage(overlay)
        canvas.create_image(0, 0, anchor="nw", image=self._tk_overlay)
 
        canvas.create_image(LEFT_W - 20, 20, anchor="ne", image=self.tk_logo_dark)
        canvas.create_text(28, 190, anchor="nw", text="Find Your\nPerfect\nLagos Home", fill=C_WHITE, font=("Georgia", 26, "bold"), width=260)
 
        def bullet(y, text):
            canvas.create_text(28, y, anchor="w", text="✅  " + text, fill=C_WHITE, font=("Helvetica", 12))
 
        bullet(360, "Affordable.")
        bullet(390, "Personalized.")
 
    def _build_right(self):
        panel = tk.Frame(self, bg=C_PANEL_BG, width=RIGHT_W, height=WIN_H)
        panel.place(x=LEFT_W, y=0)
        panel.pack_propagate(False)
 
        hdr = tk.Frame(panel, bg=C_PANEL_BG)
        hdr.pack(fill="x", padx=28, pady=(28, 0))
 
        logo_lbl = tk.Label(hdr, image=self.tk_logo_lite, bg=C_PANEL_BG)
        logo_lbl.pack(side="left")
 
        name_frame = tk.Frame(hdr, bg=C_PANEL_BG)
        name_frame.pack(side="left", padx=(10, 0))
        tk.Label(name_frame, text="Dwello", font=("Georgia", 18, "bold"), fg=C_DARK_NAVY, bg=C_PANEL_BG).pack(anchor="w")
        tk.Label(name_frame, text="Find Your Perfect Lagos Home", font=("Helvetica", 9), fg=C_TAB_IDLE, bg=C_PANEL_BG).pack(anchor="w")
 
        card = tk.Frame(panel, bg=C_INPUT_BG, highlightbackground=C_DIVIDER, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=20, pady=18)
 
        tab_frame = tk.Frame(card, bg=C_INPUT_BG)
        tab_frame.pack(fill="x")
 
        self._active_tab = tk.StringVar(value="signup")
 
        tab_container = tk.Frame(tab_frame, bg=C_INPUT_BG)
        tab_container.pack(fill="x")
 
        self._signup_tab = self._make_tab(tab_container, "Sign Up",  "signup")
        self._login_tab  = self._make_tab(tab_container, "Log In",   "login")
        self._signup_tab.pack(side="left", fill="x", expand=True)
        self._login_tab.pack(side="left",  fill="x", expand=True)
 
        self._form_body = tk.Frame(card, bg=C_INPUT_BG)
        self._form_body.pack(fill="both", expand=True, padx=16, pady=(6, 16))
 
        self._build_signup_form()
 
    def _make_tab(self, parent, label, key):
        f = tk.Frame(parent, bg=C_INPUT_BG, cursor="hand2")
 
        lbl = tk.Label(f, text=label,
                       font=("Helvetica", 12, "bold" if key == "signup" else "normal"),
                       fg=C_TAB_ACTIVE if key == "signup" else C_TAB_IDLE,
                       bg=C_INPUT_BG, pady=10)
        lbl.pack()
 
        line_color = C_ACCENT if key == "signup" else C_INPUT_BG
        line = tk.Frame(f, bg=line_color, height=2)
        line.pack(fill="x")
 
        if key == "signup":
            self._su_lbl  = lbl
            self._su_line = line
        else:
            self._li_lbl  = lbl
            self._li_line = line
 
        f.bind("<Button-1>", lambda e, k=key: self._switch_tab(k))
        lbl.bind("<Button-1>", lambda e, k=key: self._switch_tab(k))
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
            self._build_signup_form()
        else:
            self._li_lbl.config(fg=C_TAB_ACTIVE, font=("Helvetica", 12, "bold"))
            self._li_line.config(bg=C_ACCENT)
            self._su_lbl.config(fg=C_TAB_IDLE,   font=("Helvetica", 12, "normal"))
            self._su_line.config(bg=C_INPUT_BG)
            self._build_login_form()
 
    def _clear_form(self):
        for w in self._form_body.winfo_children():
            w.destroy()
 
    def _build_signup_form(self):
        self._clear_form()
        fb = self._form_body
 
        email_icon = self._make_email_icon()
 
        self._name_entry = self._row(fb, "Full name",     self.tk_user_icon)
        self._email_entry= self._row(fb, "Email Address", email_icon)
        self._pass_entry = self._row(fb, "Password",      None, password=True)
 
        btn = tk.Button(fb, text="Create Account",
                        bg=C_DARK_NAVY, fg=C_WHITE,
                        font=("Helvetica", 12, "bold"),
                        relief="flat", bd=0, cursor="hand2",
                        activebackground="#2C3E6A",
                        activeforeground=C_WHITE,
                        command=self._on_create)
        btn.pack(fill="x", pady=(14, 0), ipady=10)
 
        footer = tk.Frame(fb, bg=C_INPUT_BG)
        footer.pack(pady=(10, 0))
        tk.Label(footer, text="Already have an account?", fg=C_TAB_IDLE, bg=C_INPUT_BG, font=("Helvetica", 9)).pack(side="left")
        lnk = tk.Label(footer, text=" Log In", fg=C_LINK, bg=C_INPUT_BG, font=("Helvetica", 9, "bold"), cursor="hand2")
        lnk.pack(side="left")
        lnk.bind("<Button-1>", lambda e: self._switch_tab("login"))
 
    def _build_login_form(self):
        self._clear_form()
        fb = self._form_body
 
        email_icon = self._make_email_icon()
        self._email_entry = self._row(fb, "Email Address", email_icon)
        self._pass_entry  = self._row(fb, "Password",      None, password=True)
 
        tk.Frame(fb, bg=C_INPUT_BG, height=8).pack()
 
        btn = tk.Button(fb, text="Log In",
                        bg=C_DARK_NAVY, fg=C_WHITE,
                        font=("Helvetica", 12, "bold"),
                        relief="flat", bd=0, cursor="hand2",
                        activebackground="#2C3E6A",
                        activeforeground=C_WHITE,
                        command=self._on_login)
        btn.pack(fill="x", pady=(6, 0), ipady=10)
 
        footer = tk.Frame(fb, bg=C_INPUT_BG)
        footer.pack(pady=(10, 0))
        tk.Label(footer, text="Don't have an account?", fg=C_TAB_IDLE, bg=C_INPUT_BG, font=("Helvetica", 9)).pack(side="left")
        lnk = tk.Label(footer, text=" Sign Up", fg=C_LINK, bg=C_INPUT_BG, font=("Helvetica", 9, "bold"), cursor="hand2")
        lnk.pack(side="left")
        lnk.bind("<Button-1>", lambda e: self._switch_tab("signup"))
 
    def _row(self, parent, placeholder, icon_img, password=False):
        if password:
            entry = RoundedEntry(
                parent,
                placeholder=placeholder,
                icon_img=self._make_lock_icon(),
                right_img=self.tk_eye_show,
                show="•"
            )
            entry._eye_label.bind("<Button-1>", lambda e: entry.toggle_visibility(self.tk_eye_show, self.tk_eye_hide))
        else:
            entry = RoundedEntry(parent, placeholder=placeholder, icon_img=icon_img)
        entry.pack(fill="x", pady=5)
        return entry
 
    def _make_email_icon(self):
        img = Image.new("RGBA", (ICON_SZ, ICON_SZ), (0, 0, 0, 0))
        d   = ImageDraw.Draw(img)
        m   = 6
        d.rectangle([m, m+4, ICON_SZ-m, ICON_SZ-m-4], outline="#AAAAAA", width=2)
        d.line([m, m+4, ICON_SZ//2, ICON_SZ//2, ICON_SZ-m, m+4], fill="#AAAAAA", width=2)
        return ImageTk.PhotoImage(img)
 
    def _make_lock_icon(self):
        img = Image.new("RGBA", (ICON_SZ, ICON_SZ), (0, 0, 0, 0))
        d   = ImageDraw.Draw(img)
        cx  = ICON_SZ // 2
        d.arc([cx-7, 3, cx+7, 18], start=0, end=180, fill="#AAAAAA", width=2)
        d.rounded_rectangle([cx-10, 15, cx+10, ICON_SZ-5], radius=3, outline="#AAAAAA", width=2)
        d.ellipse([cx-3, 19, cx+3, 25], fill="#AAAAAA")
        return ImageTk.PhotoImage(img)
 
    def _on_create(self):
        print("Create Account →", self._name_entry.get(), self._email_entry.get())
 
    def _on_login(self):
        print("Log In →", self._email_entry.get())
 
 
if __name__ == "__main__":
    app = DwelloApp()
    app.mainloop()