
import mode
import language
import json
import os
import random
from app import APP_VERSION

home = os.path.expanduser("~")
file_path = os.path.join(home, ".local", "share", "verbo")

FOLDER = file_path + "/"
kill = False

# code from a guy in stackoverflow
# dont rembember who it was and cant find it
class CmdColor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def run_command(value, cmode):
    
    if cmode == mode.Mode.NORMAL:

        match value:
            case "version":
                print(APP_VERSION)

            case "hello":
                print("Hello, world!")

            case "help":

                print("create - creates a new language file")
                print("open - opens a language file")
                print("exit - closes program")
                print("")

            case "create":
                if not os.path.exists(FOLDER):
                    os.makedirs(FOLDER)

                language_name = input("name: ")
                with open(FOLDER + language_name + ".json", 'w') as file:
                    data = language.Language(language_name, [])
                    file.write(json.dumps(data.to_dict(), indent=4))

                    print("File written successfully!")

            case "open":
                file = input("file: ")
                if (not os.path.exists(FOLDER + file + ".json")):
                    print("File not found, or file is not a json file")
                    return False

                
                with open(FOLDER + file + ".json", 'r') as data:
                    content = json.loads(data.read())
                    print(file + " loaded with " + str(len(content['word_list'])) + " words!")

                    mode.set_mode(mode.Mode.LANGUAGE)
                    language.set_language(FOLDER + file + ".json", content)

            case "mode":
                print(cmode)

            case "exit":
                global kill
                kill = True

            case _:
                print("Command not found")


    if cmode == mode.Mode.LANGUAGE:

        match value:
            case "help":
                print("g - gets a random word with it's translation")
                print("gg - gets a random word, that you have to guess")
                print("add - adds a new word to the database")
                print("exit - leaves LANGUAGE mode")

            case "mode":
                print(cmode)

            case "g":
                if len(language.language_data) == 0: 
                    print("Language has no words")
                    return False

                index = random.randint(0, len(language.language_data['word_list'])-1)

                token = language.language_data['word_list'][index]
                print("Word: " + token['word'])
                print("Translation: " + token['translation'])

            case "gg":
                if len(language.language_data) == 0: 
                    print("Language has no words")
                    return False

                index = random.randint(0, len(language.language_data['word_list'])-1)
                token = language.language_data['word_list'][index]

                print("Word: " + token['word'])
                guess = input("Guess: ")
                if guess == token['translation']:
                    print(CmdColor.OKGREEN + "Right answer!" + CmdColor.ENDC)
                else:
                    print(CmdColor.FAIL + "Wrong answer!" + CmdColor.ENDC)
                    print(CmdColor.FAIL + "Translation: " + token['translation'], CmdColor.ENDC)

            case "add":
                print("Add a word and it's translation to the language's database")
                word = input("word: ")
                translation = input("translation: ")

                #new_word = {'word': word, 'translation': translation}
                new_word = language.Word(word, translation).to_dict() 

                language.language_data['word_list'].append( new_word )

                # save to file
                with open(language.language_file, 'w') as file:
                    json.dump(language.language_data, file, indent=4)
                    print("Added a new word!")

            case "del":
                word = input("word to delete: ")
                for i in language.language_data['word_list']:
                    if i['word'] == word or i['translation'] == word:
                        language.language_data['word_list'].remove(i)
                        
                        with open(language.language_file, 'w') as file:
                            json.dump(language.language_data, file, indent=4)
                            print("deleted word '" + str(i) + "'")

                            return False
                
                print("Could't find: " + word)

            case "exit":
                mode.set_mode(mode.Mode.NORMAL)
                print(mode.mode)

            case "info":
                print(language.language_file + " loaded with " + str(len(language.language_data['word_list'])) + " words!")

                for i in language.language_data['word_list']:
                    print(i)

            case _:
                print("Command not found")


