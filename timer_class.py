import time

class Timer():

    def __init__(self, duration):
        self.timer_start = None
        self.duration = duration

    def set_duration(self, duration):
        self.duration = duration
    
    def set_start(self):
        self.timer_start = time.time()

    def get_passed_time(self):
        return time.time() - self.timer_start
    
    def get_timer(self):
        if self.timer_start == None:
            return self.duration
        else:
            return round(self.duration - self.get_passed_time(), 1)
    
    def get_timer_string(self):
        if self.timer_start == None:
            return str(self.duration)
        else:
            timer = round(self.duration - self.get_passed_time(), 1)
            if timer <= 0:
                timer = 0
            return str(timer)
    
    def increase_timer_duration(self, increase_value, limit):
        if self.duration + increase_value <= limit:
            self.duration += increase_value

    def decrease_timer_duration(self, decrease_value, limit):
        if self.duration - decrease_value >= limit:
            self.duration -= decrease_value

    def reset_timer(self):
        self.timer_start = None