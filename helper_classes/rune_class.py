from os import path

# img sources
# https://www.freeimages.com/premium-vector/old-open-magic-book-5706544?ref=365psd

class Rune():

    def __init__(self, name:str) -> None:
        self.name = name
        self.path = path.join(path.dirname(__file__), f"..\material\game\images\\{name}.png")

    def get_rune_name(self):
        return self.name
    
    def get_rune_path(self):
        return self.path