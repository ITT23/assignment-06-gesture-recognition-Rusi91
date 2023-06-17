from os import path

# img sources
# https://stock.adobe.com/at/search?k=%22spell%20book%22
# https://www.freeimages.com/premium-vector/old-open-magic-book-5706544?ref=365psd

class Rune():

    def __init__(self, name:str) -> None:
        self.name = name
        self.path = path.join(path.dirname(__file__), f"game_images\\{name}.png")

    def get_rune_name(self):
        return self.name
    
    def get_rune_path(self):
        return self.path
    
    def get_rune_draw_background():
        return path.join(path.dirname(__file__), f"game_images\\book.png")