
import json
import random

LANGUAGE_CODES = ["aa","ab","af","ak","sq","am","ar","an","hy","as","av","ae","ay","az","ba","bm","eu","be","bn","bi","bo","bs","br","bg","my","ca","cs","ch","ce","zh","cu","cv","kw","co","cr","cy","cs","da","de","dv","nl","dz","el","en","eo","et","eu","ee","fo","fa","fj","fi","fr","fr","fy","ff","ka","de","gd","ga","gl","gv","el","gn","gu","ht","ha","he","hz","hi","ho","hr","hu","hy","ig","is","io","ii","iu","ie","ia","id","ik","is","it","jv","ja","kl","kn","ks","ka","kr","kk","km","ki","rw","ky","kv","kg","ko","kj","ku","lo","la","lv","li","ln","lt","lb","lu","lg","mk","mh","ml","mi","mr","ms","mk","mg","mt","mn","mi","ms","my","na","nv","nr","nd","ng","ne","nl","nn","nb","no","ny","oc","oj","or","om","os","pa","fa","pi","pl","pt","ps","qu","rm","ro","ro","rn","ru","sg","sa","si","sk","sk","sl","se","sm","sn","sd","so","st","es","sq","sc","sr","ss","su","sw","sv","ty","ta","tt","te","tg","tl","th","bo","ti","to","tn","ts","tk","tr","tw","ug","uk","ur","uz","ve","vi","vo","cy","wa","wo","xh","yi","yo","za","zh","zu"]

class Language:
    def __init__(self, name, code="en") -> None:
        self.token_list = []
        self.streak = 0
        self.name = name
        self.code = code

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
            data["code"] = self.code
            data["token_list"] = [t.to_dict() for t in self.token_list]
            json.dump(data, f)

    def load(path):
        with open(path, "r", encoding="utf-8") as f:
            dt = json.load(f)

        lang = Language(dt["name"])
        lang.streak = dt["streak"]
        lang.code = dt["code"]
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




