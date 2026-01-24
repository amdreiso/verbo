
import json
import random

class Language:
    def __init__(self, name) -> None:
        self.token_list = []
        self.streak = 0
        self.name = name

    def add(self, native, translation):
        for token in self.token_list:
            if token.native == native:
                print("native word already added")
                return
        self.token_list.append(
                Token(native, translation)
                )
        print("added word", native, "=", translation)

    def rem(self, tkn):
        for token in self.token_list:
            if token == tkn:
                self.token_list.remove(token)

    def edit(self, tkn, n, t):
        for token in self.token_list:
            if token == tkn:
                token.native = n
                token.translation = t

    def get_random_token(self):
        if len(self.token_list) == 0: return None
        return random.choice(self.token_list)

    def list(self):
        for token in self.token_list:
            print("native:", 
                  token.native, 
                  "translation:", 
                  token.translation
                  )

    def save(self):
        with open("./languages/"+self.name+".json", "w", encoding="utf-8") as f:
            data = {}
            data["name"] = self.name
            data["streak"] = self.streak
            data["token_list"] = [t.to_dict() for t in self.token_list]
            json.dump(data, f)

    def load(path):
        with open(path, "r", encoding="utf-8") as f:
            dt = json.load(f)

        lang = Language(dt["name"])
        lang.streak = dt["streak"]
        lang.token_list = [Token.from_dict(d) for d in dt["token_list"]]
        return lang


class Token:
    def __init__(self, native, translation) -> None:
        self.native = native
        self.translation = translation

    def to_dict(self):
        return {
            "n": self.native,
            "t": self.translation
        }

    @staticmethod
    def from_dict(d):
        return Token(d["n"], d["t"])




