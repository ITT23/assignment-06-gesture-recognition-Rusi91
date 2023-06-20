class Player():

    def __init__(self, start_lifes):
        self.start_lifes = start_lifes
        self.lifes = start_lifes
        self.score = 0
    
    def reset(self):
        self.lifes = self.start_lifes
        self.score = 0

    def decrease_lifes(self):
        self.lifes -= 1

    def get_lifes_amount(self):
        return self.lifes
    
    def increase_score(self):
        self.score += 1

    def get_score(self):
        return self.score