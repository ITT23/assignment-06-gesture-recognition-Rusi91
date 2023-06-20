from os import path

# img sources
# https://stock.adobe.com/at/search?k=%22spell%20book%22
# https://www.freeimages.com/premium-vector/old-open-magic-book-5706544?ref=365psd

# path for sounds (sound if user achieves or not achieves to draw the correct rune)
    # sound source: https://www.youtube.com/watch?v=_q8QmJadSEE -Piano Note C Sound Effect - @Sound Effects
SUCCESS_SOUND_PATH = path.join(path.dirname(__file__), "music\success_sound.mp3")
    # https://www.youtube.com/watch?v=_XRnENg_QI0 -Error Sound Effect (HD) - @Servus
FAIL_SOUND_PATH = path.join(path.dirname(__file__), "music\\fail_sound.mp3")
RESULTS_BACKGROUND_PATH = path.join(path.dirname(__file__), "game_images\\book.png")

class Rune():

    def __init__(self, name:str) -> None:
        self.name = name
        self.path = path.join(path.dirname(__file__), f"game_images\\{name}.png")

    def get_rune_name(self):
        return self.name
    
    def get_rune_path(self):
        return self.path
    
    def get_results_background_path():
        return RESULTS_BACKGROUND_PATH
    
    def success_sound_path():
        return SUCCESS_SOUND_PATH
    
    def fail_sound_path():
        return FAIL_SOUND_PATH