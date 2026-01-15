import tkinter
from tkinter import filedialog
import customtkinter as ctk
import os
import json
from style import dark_theme
import data

# =======================
# RECENTS
# =======================

RECENTS_PATH = "./recents.json"
recent_files = []

if os.path.exists(RECENTS_PATH):
    with open(RECENTS_PATH, "r", encoding="utf-8") as f:
        recent_files = json.load(f)

def recent_files_save():
    with open(RECENTS_PATH, "w", encoding="utf-8") as f:
        json.dump(recent_files, f)

def recent_files_add(path):
    if path not in recent_files:
        recent_files.append(path)
        recent_files_save()

if not os.path.exists("./languages/"):
    os.mkdir("./languages")

# =======================
# APP SETUP
# =======================

theme = dark_theme

APP = ctk.CTk()
APP.geometry("1280x720")
APP.configure(fg_color=theme.foreground)
APP.title("verbo")
ctk.set_appearance_mode("dark")

FONT = ctk.CTkFont("SauceCodePro Nerd Font", size=28)
FONT_LOGO = ctk.CTkFont("SauceCodePro Nerd Font", size=38)

MAIN = ctk.CTkFrame(APP, fg_color=theme.foreground)
MAIN.pack(fill="both", expand=True)

# =======================
# PAGE SYSTEM
# =======================

pages = {}
current_page = None

def page_create(name):
    page = ctk.CTkFrame(MAIN, fg_color=theme.foreground)
    content = ctk.CTkFrame(page, fg_color="transparent")
    content.place(relx=0.5, rely=0.5, anchor="center")
    pages[name] = (page, content)
    return page, content

def page_set(name):
    global current_page
    if current_page:
        pages[current_page][0].pack_forget()
    pages[name][0].pack(fill="both", expand=True)
    pages[name][0].focus_set()
    current_page = name

# =======================
# FILE ACTIONS
# =======================

current_language = None
current_token = None

def open_recent(path):
    global current_language
    current_language = data.Language.load(path)
    language_title.configure(text=current_language.name)
    page_set("language")

def open_file():
    path = filedialog.askopenfilename()
    if not path:
        return
    open_recent(path)
    recent_files_add(path)

def create_file():
    page_set("create_language")

# =======================
# MENU PAGE
# =======================

menu, menu_c = page_create("menu")

ctk.CTkLabel(menu_c, text="verbo", font=FONT_LOGO).pack(pady=(0, 30))

ctk.CTkButton(menu_c, text="open", width=260, command=open_file, fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0).pack(pady=8)
ctk.CTkButton(menu_c, text="create", width=260, command=create_file, fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0).pack(pady=8)

if recent_files:
    ctk.CTkLabel(menu_c, text="recents", font=FONT).pack(pady=(30, 10))

for path in recent_files:
    if os.path.exists(path):
        name = ""
        with open(path, "r") as file:
            d = json.load(file)
            name = d["name"]

        ctk.CTkButton(
            menu_c,
            text=name,
            width=260,
            command=lambda p=path: open_recent(p), fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0
        ).pack(pady=4)

# =======================
# CREATE LANGUAGE PAGE
# =======================

make_language, make_c = page_create("create_language")

ctk.CTkLabel(make_c, text="create language", font=FONT).pack(pady=(0, 20))

language_name = ctk.CTkEntry(make_c, width=300, placeholder_text="language name...")
language_name.pack(pady=10)


def language_create():
    global current_language
    name = language_name.get().strip()
    if not name:
        return
    current_language = data.Language(name)
    print(name)
    current_language.save()
    language_title.configure(text=name)
    page_set("language")
    recent_files_add("./languages/" + name + ".json")

ctk.CTkButton(make_c, text="create", command=language_create, fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0).pack()

# =======================
# LANGUAGE PAGE
# =======================

language, lang_c = page_create("language")

language_title = ctk.CTkLabel(lang_c, text="language", font=FONT)
language_title.pack(pady=(0, 30))

controls = ctk.CTkFrame(lang_c, fg_color="transparent")
controls.pack(pady=10)

def add_token_popup():
    overlay = ctk.CTkFrame(APP, fg_color="#000000")
    overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

    box = ctk.CTkFrame(overlay, width=420, height=260)
    box.place(relx=0.5, rely=0.5, anchor="center")
    box.pack_propagate(False)

    native = ctk.CTkEntry(box, placeholder_text="Native word")
    native.pack(pady=(30, 10), padx=30, fill="x")

    translation = ctk.CTkEntry(box, placeholder_text="Translation")
    translation.pack(pady=10, padx=30, fill="x")

    btns = ctk.CTkFrame(box, fg_color="transparent")
    btns.pack(pady=25)

    def submit():
        if native.get() and translation.get():
            current_language.add(native.get(), translation.get())
            current_language.save()
            overlay.destroy()

    ctk.CTkButton(btns, text="add", command=submit, fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0).grid(row=0, column=0, padx=10)
    ctk.CTkButton(btns, text="exit", command=overlay.destroy, fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0).grid(row=0, column=1, padx=10)

    btns.bind("<Return>", submit)

def get_token():
    global current_token
    current_token = current_language.get_random_token()
    language_display.configure(text=f"{current_token.native}: ???")

def reveal_token():
    if current_token:
        language_display.configure(
            text=f"{current_token.native}: {current_token.translation}"
        )

ctk.CTkButton(controls, text="add", width=120, command=add_token_popup, fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0).grid(row=0, column=0, padx=5)
ctk.CTkButton(controls, text="get", width=120, command=get_token, fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0).grid(row=0, column=1, padx=5)
ctk.CTkButton(controls, text="reveal", width=120, command=reveal_token, fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0).grid(row=0, column=2, padx=5)

language_display = ctk.CTkLabel(lang_c, text="??? = ???", font=FONT_LOGO)
language_display.pack(pady=60)


# =======================
# START
# =======================

page_set("menu")

APP.bind("<Escape>", lambda e: page_set("menu"))
language.bind("a", lambda e: add_token_popup())

APP.mainloop()

