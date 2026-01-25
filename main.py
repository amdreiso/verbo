import tkinter
from tkinter import END, SE, filedialog
import customtkinter as ctk
import os
import json
import asyncio
from googletrans import Translator
from style import dark_theme
from data import LANGUAGE_CODES, Language
from settings import settings


async def translate_text(text, src, dest):
    async with Translator() as translator:
        res = await translator.translate(text=text, dest=dest, src=src)
        return res

# recent opened files

RECENTS_PATH = "./recents.json"
recent_files = []

def check_recents():
    global recent_files
    if os.path.exists(RECENTS_PATH):
        with open(RECENTS_PATH, "r", encoding="utf-8") as f:
            recent_files = json.load(f)

        recent_files_purge()

def recent_files_purge():
    for path in recent_files:
        if not os.path.exists(path):
            recent_files.remove(path)
            recent_files_save()

def recent_files_save():
    with open(RECENTS_PATH, "w", encoding="utf-8") as f:
        json.dump(recent_files, f)

def recent_files_add(path):
    if path not in recent_files:
        recent_files.append(path)
        recent_files_save()

if not os.path.exists("./languages/"):
    os.mkdir("./languages")

check_recents()

# app setup

theme = dark_theme

TOKEN_ORDER = settings.get("token_order", 0)

APP = ctk.CTk()
APP.geometry("1280x720")
APP.configure(fg_color=theme.foreground)
APP.title("verbo")
ctk.set_appearance_mode("dark")

FONT = ctk.CTkFont("JetBrainsMono Nerd Font", size=28)
FONT_LOGO = ctk.CTkFont("JetBrainsMono Nerd Font", size=38)
FONT_BUTTON = ctk.CTkFont("JetBrainsMono Nerd Font", size=18)
FONT_SMALL = ctk.CTkFont("JetBrainsMono Nerd Font", size=12)

MAIN = ctk.CTkFrame(APP, fg_color=theme.foreground)
MAIN.pack(fill="both", expand=True)

# page system

pages = {}
current_page = None

def page_create(name):
    page = ctk.CTkFrame(MAIN, fg_color=theme.foreground)
    content = ctk.CTkFrame(page, fg_color="transparent")
    content.place(relx=0.5, rely=0.5, anchor="center")
    pages[name] = (page, content)
    return page, content

def page_set(name):
    global current_page, language_streak, streak_display
    if current_page:
        pages[current_page][0].pack_forget()
    pages[name][0].pack(fill="both", expand=True)
    pages[name][0].focus_set()
    current_page = name

    language_display.configure(text="??? = ???")

    if name == "language":
        language_streak = 0

    if name == "menu":
        for button in recent_buttons:
            button.pack_forget()
            recent_buttons.remove(button)

        create_recent_buttons()

# files

current_language = None
current_token = None

def language_update_stats():
    global language_title, streak_display, current_language, language_streak
    language_title.configure(text=current_language.name)
    streak_display.configure(text=f"current streak = 0 | max streak = {current_language.streak}")
    language_token_count.configure(text=f"tokens = {len(current_language.token_list)}")

def open_recent(path):
    global current_language, language_streak, streak_display
    current_language = Language.load(path)

    language_update_stats()
    
    page_set("language")
    language_streak = 0

def open_file():
    global language_streak

    path = filedialog.askopenfilename()
    if not path:
        return
    open_recent(path)
    recent_files_add(path)
    language_streak = 0

def create_file():
    page_set("create_language")

# menu

menu, menu_c = page_create("menu")

ctk.CTkLabel(menu_c, text="verbo", font=FONT_LOGO).pack(pady=(0, 30))

ctk.CTkButton(menu_c, text="open", font=FONT_BUTTON, width=260, command=open_file, fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0).pack(pady=8)

ctk.CTkButton(menu_c, text="create", font=FONT_BUTTON, width=260, command=create_file, fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0).pack(pady=8)

def settings_open():
    page_set("settings")

ctk.CTkButton(menu_c, text="settings", font=FONT_BUTTON, width=260, command=settings_open, fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0).pack(pady=8)

ctk.CTkLabel(menu_c, text="recents", font=FONT).pack(pady=(30, 10))

recent_buttons_scroll = ctk.CTkScrollableFrame(menu_c, width=400, height=400, 
                                               fg_color="#090909", 
                                               scrollbar_button_color=theme.button,
                                               scrollbar_button_hover_color=theme.button_hover
                                               )
recent_buttons_scroll.pack(fill="both", expand=True)
recent_buttons = []

def create_recent_buttons():
    for btn in recent_buttons:
        btn.pack_forget()

    for path in recent_files:
        print(path)
        if os.path.exists(path):
            name = ""
            with open(path, "r") as file:
                d = json.load(file)
                name = d["name"]

            recent_button = ctk.CTkButton(
                recent_buttons_scroll,
                text=name,
                width=260,
                command=lambda p=path: open_recent(p), fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0, font=FONT_BUTTON
            )
            recent_button.pack(pady=4)
            recent_buttons.append(recent_button)

create_recent_buttons()


# settings page
settings_page, settings_c = page_create("settings")

ctk.CTkLabel(settings_c, text="Settings", font=FONT).pack(pady=20)

def change_token_order(button):
    global TOKEN_ORDER
    if TOKEN_ORDER == 0:
        TOKEN_ORDER = 1
        button.configure(text="translation: native")
    else:
        TOKEN_ORDER = 0
        button.configure(text="native: translation")
    settings.set("token_order", TOKEN_ORDER)

token_order_button = ctk.CTkButton(
    master=settings_c, 
    text="native: translation", 
    font=FONT_BUTTON, 
    width=260, 
    fg_color=theme.button, 
    hover_color=theme.button_hover, 
    corner_radius=0
)
if TOKEN_ORDER == 0:
    token_order_button.configure(text="native: translation")
else:
    token_order_button.configure(text="translation: native")

token_order_button.pack(pady=8)
token_order_button.configure(command=lambda b=token_order_button: change_token_order(b))

default_code_entry = ctk.CTkEntry(settings_c, placeholder_text="")
default_code_entry.insert(0, settings.get("default_language_code"))
default_code_entry.pack(pady=10)

def settings_save():
    val = default_code_entry.get()
    if val in LANGUAGE_CODES: 
        settings.set("default_language_code", val)

settings_apply = ctk.CTkButton(settings_c, text="apply", command=lambda: settings_save(), font=FONT_BUTTON, hover_color=theme.button_hover, fg_color=theme.button, corner_radius=0)
settings_apply.pack(pady=(100, 0))

# create language file 'popup'

make_language, make_c = page_create("create_language")

ctk.CTkLabel(make_c, text="create language", font=FONT).pack(pady=(0, 20))

language_name = ctk.CTkEntry(make_c, width=300, placeholder_text="language name...")
language_name.pack(pady=10)

language_code = ctk.CTkEntry(make_c, width=300, placeholder_text="language code 'en', 'de', 'ru', 'gr', etc...")
language_code.pack(pady=10)

def language_create():
    global current_language
    name = language_name.get().strip()
    if not name:
        return

    code = language_code.get()
    if not code or not code in LANGUAGE_CODES:
        return

    current_language = Language(name, code)
    current_language.save()
    language_title.configure(text=name)
    page_set("language")
    newpath = os.getcwd() + "/languages/" + name + ".json"
    recent_files_add(newpath)

ctk.CTkButton(make_c, font=FONT_BUTTON, text="create", command=language_create, fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0).pack(pady=10)


# language page

language, lang_c = page_create("language")
language_streak = 0

language_title = ctk.CTkLabel(master=lang_c, text="language", font=FONT)
language_title.pack()

language_token_count = ctk.CTkLabel(master=lang_c, text="tokens = 0", font=FONT_BUTTON)
language_token_count.pack()

current_streak = 0

streak_display = ctk.CTkLabel(
        lang_c, text=f"current streak = 0 | max streak = 0", font=FONT_BUTTON)
streak_display.pack(pady=(0, 50))

controls = ctk.CTkFrame(lang_c, fg_color="transparent")
controls.pack(pady=10)

entry = ctk.CTkEntry(language, placeholder_text="guess here...", font=FONT_BUTTON, justify="center")
entry.place(relx=0.5, rely=0.75, relwidth=0.25, anchor="center")

on_entry = False
def on_focus(b):
    global on_entry
    on_entry = b

entry.bind("<FocusIn>", lambda e: on_focus(True))
entry.bind("<FocusOut>", lambda e: on_focus(False))

popup = False
def add_token_popup():
    global popup, current_page
    if popup == True or current_page != "language": return
    popup = True

    overlay = ctk.CTkFrame(APP, fg_color="#050505")
    overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

    box = ctk.CTkFrame(overlay, width=600, height=400)
    box.place(relx=0.5, rely=0.5, anchor="center")
    box.pack_propagate(False)

    ctk.CTkLabel(master=box, text="native word will be translated when 'translate' button is clicked", font=FONT_SMALL, justify="left").pack(pady=(50, 0))
    native = ctk.CTkEntry(box, placeholder_text="Native word")
    native.pack(pady=(0, 10), padx=30, fill="x")

    ctk.CTkLabel(master=box, text="the result of the translation will be sent here", font=FONT_SMALL, justify="left").pack()
    translation = ctk.CTkEntry(box, placeholder_text="Translation")
    translation.pack(padx=30, fill="x")

    # Translate option
    translate_menu = ctk.CTkFrame(box, fg_color="transparent")
    translate_menu.pack(pady=25)

    def translate():
        if native.get().replace(" ", "") == "" and translate_entry_to.get().replace(" ", "") == "": return

        result = asyncio.run(translate_text(native.get(), translate_entry_from.get(), translate_entry_to.get()))

        translation.delete(0, END)
        translation.insert(0, result.text)

    lang1 = ""
    lang2 = ""

    if TOKEN_ORDER == 0:
        #native
        lang1 = settings.get("default_language_code")
        lang2 = current_language.code
    else:
        #translation
        lang2 = settings.get("default_language_code")
        lang1 = current_language.code

    translate_entry_from = ctk.CTkEntry(translate_menu, placeholder_text="native: 'en' 'es' 'ru' 'pt' 'de'...")
    translate_entry_from.grid(row=0, column=0, padx=10)
    translate_entry_from.insert(0, lang1)

    translate_entry_to = ctk.CTkEntry(translate_menu, placeholder_text="translation: 'en' 'es' 'ru' 'pt' 'de'...")
    translate_entry_to.grid(row=0, column=2, padx=10)
    translate_entry_to.insert(0, lang2)

    translate_button = ctk.CTkButton(translate_menu, text="translate", 
                                     font=FONT_BUTTON, command=translate, fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0)
    translate_button.grid(row=0, column=1, padx=10)


    btns = ctk.CTkFrame(box, fg_color="transparent")
    btns.pack(pady=25)

    def submit():
        if native.get() and translation.get():
            global popup
            popup = False

            t = translation.get()
            if "," in t:
                t = t.replace(" ", "").split(",")
            print(t)
            if len(t) == 1: t = t[0]
            
            n = native.get()
            if "," in t:
                n = n.replace(" ", "").split(",")
            print(n)
            if len(n) == 1: n = n[0]

            current_language.add(n, t)
            current_language.save()
            language_update_stats()
            overlay.destroy()

    def destroy():
        global popup
        popup = False
        overlay.destroy()

    ctk.CTkButton(btns, text="add", font=FONT_BUTTON, command=submit, fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0).grid(row=0, column=0, padx=10)
    ctk.CTkButton(btns, text="exit", command=destroy, font=FONT_BUTTON, fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0).grid(row=0, column=1, padx=10)

    btns.bind("<Return>", submit)

def edit_token_popup():
    global popup, current_page, current_token
    if popup == True or current_page != "language" or current_token == None: return
    popup = True

    overlay = ctk.CTkFrame(APP, fg_color="#050505")
    overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

    box = ctk.CTkFrame(overlay, width=500, height=260)
    box.place(relx=0.5, rely=0.5, anchor="center")
    box.pack_propagate(False)

    native = ctk.CTkEntry(box, placeholder_text="Native word")
    native.insert(0, current_token.native)
    native.pack(pady=(30, 10), padx=30, fill="x")

    ti = ', '.join(str(x) for x in current_token.translation)
    ti = current_token.translation
    if isinstance(ti, list):
        ti = ", ".join(ti)

    translation = ctk.CTkEntry(box, placeholder_text="Translation")
    translation.insert(0, ti)
    translation.pack(pady=10, padx=30, fill="x")

    btns = ctk.CTkFrame(box, fg_color="transparent")
    btns.pack(pady=25)

    def submit():
        if native.get() and translation.get():
            global popup
            popup = False
            
            t = translation.get()
            if "," in t:
                t = t.replace(" ", "").split(",")
            print(t)
            if len(t) == 1: t = t[0]
            
            n = native.get()
            if "," in t:
                n = n.replace(" ", "").split(",")
            print(n)
            if len(n) == 1: n = n[0]

            current_language.edit(current_token, n, t)
            current_language.save()
            #current_language.add(n, t)
            overlay.destroy()

    def remove():
        global popup
        popup = False

        current_language.rem(current_token)
        current_language.save()

        language_display.configure(text="??? = ???")

        overlay.destroy()

    def destroy():
        global popup
        popup = False
        overlay.destroy()

    ctk.CTkButton(btns, text="edit", font=FONT_BUTTON, command=submit, fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0).grid(row=0, column=0, padx=10)
    ctk.CTkButton(btns, text="remove", font=FONT_BUTTON, command=remove, fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0).grid(row=0, column=1, padx=10)
    ctk.CTkButton(btns, text="exit", command=destroy, font=FONT_BUTTON, fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0).grid(row=0, column=2, padx=10)

    btns.bind("<Return>", submit)




token_revealed = False

def get_token():
    global current_token, token_revealed
    if current_page != "language": return
    current_token = current_language.get_random_token()

    token_revealed = False

    word0 = ""
    if TOKEN_ORDER == 0:
            word0 = current_token.native
    else:
        word0 = current_token.translation

    language_display.configure(text=f"{word0}: ???")

    # TODO: display text input for guessing translation

def reveal_token():
    global token_revealed
    if current_page != "language": return
    if current_token:
        word0 = ""
        word1 = ""

        if TOKEN_ORDER == 0:
            word0 = current_token.native
            word1 = current_token.translation
        else:
            word0 = current_token.translation
            word1 = current_token.native

        if isinstance(word0, list):
            word0 = ", ".join(word0)

        if isinstance(word1, list):
            word1 = ", ".join(word1)

        language_display.configure(
            text=f"{word0} = {word1}"
        )

        token_revealed = True


def win():
    global language_streak, token_revealed
    
    if not token_revealed: language_streak += 1
    streak_display.configure(
        text=f"current streak = {language_streak} | max streak = {current_language.streak}")
    #f"current streak = 0 | max streak = {current_streak}

    if language_streak > current_language.streak:
        current_language.streak = language_streak
        current_language.save()
        
        streak_display.configure(
            text=f"current streak = {language_streak} | max streak = {current_language.streak}")


    print("win")
    get_token()

def lose():
    global language_streak
    language_streak = 0
    streak_display.configure(
            text=f"current streak = {language_streak} | max streak = {current_language.streak}")

    print("lose")
    reveal_token()

def check_guess():
    if current_page != "language" or not on_entry or entry.get().replace(" ", "") == "": return

    value = entry.get()

    if current_token:
        word = ""

        if TOKEN_ORDER == 0:
            word = current_token.translation
        else:
            word = current_token.native

        if isinstance(word, list):
            found = False
            for w in word:
                if value.lower() == w.lower():
                    win()
                    found = True
            if not found: 
                lose()
        else:
            if value == word:
                win()
            else:
                lose()
        
        entry.delete(0, 'end')






ctk.CTkButton(controls, text="add", font=FONT_BUTTON, width=120, command=add_token_popup, fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0).grid(row=0, column=0, padx=5)
ctk.CTkButton(controls, text="edit", font=FONT_BUTTON, width=120, command=edit_token_popup, fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0).grid(row=0, column=1, padx=5)
ctk.CTkButton(controls, text="get", width=120, font=FONT_BUTTON, command=get_token, fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0).grid(row=0, column=2, padx=5)
ctk.CTkButton(controls, text="reveal", width=120, font=FONT_BUTTON, command=reveal_token, fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0).grid(row=0, column=3, padx=5)
#ctk.CTkButton(controls, text="guess", width=120, font=FONT_BUTTON, command=reveal_token, fg_color=theme.button, hover_color=theme.button_hover, corner_radius=0).grid(row=0, column=3, padx=5)


language_display = ctk.CTkLabel(lang_c, text="??? = ???", font=FONT_LOGO)
language_display.pack(pady=60)

page_set("menu")

APP.bind("<Escape>", lambda e: page_set("menu"))
APP.bind("<Control-a>", lambda e: add_token_popup())
APP.bind("<Control-e>", lambda e: edit_token_popup())
APP.bind("<Control-g>", lambda e: get_token())
APP.bind("<Control-r>", lambda e: reveal_token())
APP.bind("<Return>", lambda e: check_guess())

def main():
    APP.mainloop()

if __name__ == "__main__":
    main()



