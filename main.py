
from sys import maxsize
import tkinter
from tkinter import filedialog
import customtkinter as ctk
import os
import json
from style import dark_theme
import data

theme = dark_theme

APP = ctk.CTk()
APP.geometry("1280x720")
APP.configure(fg_color=theme.foreground)

ctk.set_appearance_mode("dark")

FONT = ctk.CTkFont("SauceCodePro Nerd Font", size=28)
FONT_LOGO = ctk.CTkFont("SauceCodePro Nerd Font", size=38)

MAIN = ctk.CTkFrame(master=APP, fg_color=theme.header)
MAIN.pack(fill="both", expand=True)

title = ctk.CTkLabel(master=MAIN, text="verbo", font=FONT_LOGO)
title.pack(side="top", pady=40)

pages = {}
currentPage = "menu"

def page_create(name, master):
    global theme
    frame = ctk.CTkFrame(master=master, fg_color=theme.foreground)
    pages[name] = frame
    return frame

def page_set(page):
    global currentPage
    pages[currentPage].pack_forget()

    print("page set to", page)
    pages[page].pack(side="top", fill="both", expand=True)
    pages[page].pack_propagate(False)

    currentPage = page

def open_file():
    global current_language
    path = filedialog.askopenfilename()

    current_language = data.Language.load(path)
    language_open()
    


def open_folder():
    path = filedialog.askdirectory()

    print(path)

def create_file():
    page_set("create_language")
    pass

# MENU
menu = page_create("menu", MAIN)

center = ctk.CTkFrame(menu, fg_color="transparent")
center.grid(row=0, column=0, columnspan=2)

menu.grid_columnconfigure(0, weight=1)
menu.grid_columnconfigure(1, weight=1)

button0 = ctk.CTkButton(master=center, text="open", command=open_file, corner_radius=0)
button0.grid(column=0, row=1, padx=5, pady=20)
button0.grid_propagate(False)

button1 = ctk.CTkButton(master=center, text="create", command=create_file, corner_radius=0)
button1.grid(column=1, row=1, padx=5, pady=20)
button1.grid_propagate(False)


# CREATE LANGUAGE
make_language = page_create("create_language", MAIN)
current_language = None

def language_open():
    global language_title, current_language
    page_set("language")

    language_title.configure(text=current_language.name)

    print("name:", current_language.name)



def language_create():
    # create language
    lang = data.Language(language_name.get())
    lang.save()

    global current_language
    current_language = lang

    language_open()
    


make_language_center = ctk.CTkFrame(make_language, fg_color="transparent")
make_language_center.grid(row=0, column=0, columnspan=2)

make_language.grid_columnconfigure(0, weight=1)
make_language.grid_columnconfigure(1, weight=1)

language_name = ctk.CTkEntry(master=make_language_center, placeholder_text="language name...", bg_color="transparent")
language_name.grid(column=0, row=1, pady=20)

language_apply_button = ctk.CTkButton(master=make_language_center, text="apply", command=language_create)
language_apply_button.grid(column=0, row=2, pady=20)



# LANGUAGE
language = page_create("language", MAIN)

language_center = ctk.CTkFrame(language, fg_color="transparent")
language_center.grid(row=0, column=0, columnspan=3)

language.grid_columnconfigure(0, weight=1)
language.grid_columnconfigure(1, weight=1)
language.grid_columnconfigure(2, weight=1)

language_title = ctk.CTkLabel(master=language_center, text="language name", font=FONT)
language_title.grid(column=0, row=1, pady=50, columnspan=3, sticky="nsew")

def add_token_popup():
    global current_language

    overlay = ctk.CTkFrame(APP, fg_color="#000000")
    overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

    box = ctk.CTkFrame(overlay, width=420, height=260, corner_radius=0)
    box.place(relx=0.5, rely=0.5, anchor="center")
    box.pack_propagate(False)

    native_entry = ctk.CTkEntry(box, placeholder_text="Native word", corner_radius=0)
    native_entry.pack(pady=(30, 10), padx=30, fill="x")

    translation_entry = ctk.CTkEntry(box, placeholder_text="Translation", corner_radius=0)
    translation_entry.pack(pady=10, padx=30, fill="x")

    btns = ctk.CTkFrame(box, fg_color="transparent")
    btns.pack(pady=25)

    def submit():
        native = native_entry.get().strip()
        translation = translation_entry.get().strip()
        # add token
        if native and translation:
            current_language.add(native, translation)
            current_language.save()
            overlay.destroy()

    ctk.CTkButton(btns, text="add", command=submit, corner_radius=0).grid(row=0, column=0, padx=10)
    ctk.CTkButton(btns, text="exit", command=overlay.destroy, corner_radius=0).grid(row=0, column=1, padx=10)

current_token = {}

def get_token():
    global current_language, current_token
    current_token = current_language.get_random_token()
    display = current_token.native + ": ???"
    language_display.configure(text=display)

def reveal_token():
    global current_token
    display = current_token.native + ": " + current_token.translation
    language_display.configure(text=display)


language_add = ctk.CTkButton(master=language_center, text="add", command=add_token_popup)
language_add.grid(column=0, row=2, padx=5)

language_get = ctk.CTkButton(master=language_center, text="get", command=get_token)
language_get.grid(column=1, row=2, padx=5)

language_get = ctk.CTkButton(master=language_center, text="reveal", command=reveal_token)
language_get.grid(column=2, row=2, padx=5)

language_display = ctk.CTkLabel(master=language_center, text="??? = ???", font=FONT_LOGO)
language_display.grid(column=0, row=10, pady=50, columnspan=3, sticky="nsew")

page_set("menu")


APP.mainloop()

