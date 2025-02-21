

language_data = {}
language_file = ''

def set_language(file, value):
    global language_data
    global language_file

    language_file = file
    language_data = value

class Word:
    def __init__(self, word, translation):
        self.word = word
        self.translation = translation

    def to_dict(self):
        return {
            'word': self.word,
            'translation': self.translation
        }

class Language:
    def __init__(self, name, word_list):
        self.name = name
        self.word_list = word_list

    def to_dict(self):
        return {
            'name': self.name,
            'word_list': self.word_list
        }


