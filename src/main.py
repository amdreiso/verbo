
#!/usr/bin/env python3

import os
import json
import mode
from cmd import run_command
import cmd


# Application
def loop():
    value = input("- ")
    run_command(value, mode.mode)

    if not cmd.kill:
        loop()


# Greetings
def main():
    print("")
    print("Welcome to \033[95mVerbo!\033[0m")
    print("An application made for memorizing and guessing vocabulary!")
    print("Made by amdrei")
    print("Type 'help' for instructions.")
    print("")

    loop()

if __name__ == "__main__":
    main()

