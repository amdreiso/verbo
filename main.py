

import os
import json
import mode
from cmd import run_command
import cmd



# Greetings
print("")
print("Welcome to Verbo!")
print("An application made for memorizing and guessing vocabulary!")
print("Type 'help' for instructions.")
print("")



# Application
def loop():
    value = input("- ")
    run_command(value, mode.mode)

    if not cmd.kill:
        loop()

loop()

