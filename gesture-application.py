# application for task 3

# gesture input program for first task

import pyglet
import random

from pyglet import app, shapes, image
from pyglet.window import Window

from point_class import Point
from recognizer import Recognizer
from rune_class import Rune
from timer_class import Timer
from player_class import Player

# https://pyglet.readthedocs.io/en/latest/programming_guide/mouse.html

# window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# width of line
WIDTH_INPUT_LINE = 5

# colors
COLOR_INPUT_LINE = (50, 225, 30)
COLOR_FIRST_INPUT = (250,128,114)

# width/height of the first input point represented as a rectangle
RECT_SIZE = 30
# correction of the coordinates of the rectange to start the line from the center of the rectangle
RECT_CORRECTION = RECT_SIZE / 2

# creating a batch object
batch = pyglet.graphics.Batch()

# stored points
input_points:list[Point] = []

arrow_rune = Rune("arrow")
check_rune = Rune("check")
delete_rune = Rune("delete")
pigtail_rune = Rune("pigtail")
rectangle_rune = Rune("rectangle")
star_rune = Rune("star")
triangle_rune = Rune("triangle")
x_rune = Rune("x")

runes_arr = [arrow_rune, check_rune, delete_rune, pigtail_rune, rectangle_rune, star_rune, triangle_rune, x_rune]
current_rune = star_rune

Player_LIFES = 5
player = Player(Player_LIFES)

# timer
duration = 20.0
timer = Timer(duration)


recognizer = Recognizer()

# create game window
window = Window(WINDOW_WIDTH, WINDOW_HEIGHT)

def save_point(x:float, y:float):
    new_point = Point(x, y)
    input_points.append(new_point)
    recognizer.add_point(new_point.x, WINDOW_HEIGHT - new_point.y)

def restart():
    global input_points
    window.clear()
    input_points = []
    recognizer.reset_recognizer()

def trial_failed():
    player.decrease_lifes()
    timer.reset_timer()
    restart()

# play sound if user achieved to draw the correct rune
def play_success_sound():
    success_sound = pyglet.media.load(Rune.success_sound_path(), streaming=False)
    success_sound.play()

@window.event
def on_draw():
    window.clear()
    draw_background()
    if player.get_lifes_amount() > 0:
        draw_remaining_tries()
        draw_timer()
        draw_score()
        draw_input()
    else:
        draw_result()
    

def draw_background():
    if player.get_lifes_amount() > 0:
        background_image = image.load(current_rune.get_rune_path())
    else:
        background_image = image.load(Rune.get_results_background_path())
    background_image.blit(0, 0)

# display of the player's remaining lives
def draw_remaining_tries():
    player_lifes_label = pyglet.text.Label("Tries: " + str(player.get_lifes_amount()),
                          font_name='Times New Roman',
                          font_size=25,
                          x = WINDOW_WIDTH - WINDOW_WIDTH / 8, y = WINDOW_HEIGHT / 15,
                          anchor_x='center', anchor_y='center')
    player_lifes_label.draw()

def draw_timer():
    timer_label = pyglet.text.Label("Timer: " + timer.get_timer_string(),
                          font_name='Times New Roman',
                          font_size=25,
                          x = WINDOW_WIDTH - WINDOW_WIDTH / 7, y = WINDOW_HEIGHT - WINDOW_HEIGHT / 15,
                          anchor_x='center', anchor_y='center')
    timer_label.draw()

def draw_score():
    score_label = pyglet.text.Label("Score: " + str(player.get_score()),
                          font_name='Times New Roman',
                          font_size=25,
                          x = WINDOW_WIDTH / 7, y = WINDOW_HEIGHT / 15,
                          anchor_x='center', anchor_y='center')
    score_label.draw()

def draw_input():
    
    if len(input_points) >= 1:
        draw_first_input()
        if len(input_points) > 1:
            for i in range(len(input_points) - 1):
                input_line = shapes.Line(input_points[i].x, input_points[i].y, input_points[i + 1].x, input_points[i + 1].y, \
                                    WIDTH_INPUT_LINE, COLOR_INPUT_LINE, batch = batch)
                input_line.opacity = 255
                input_line.draw()

def draw_first_input():
    first_input = shapes.Rectangle(input_points[0].x - RECT_CORRECTION, input_points[0].y - RECT_CORRECTION, RECT_SIZE, RECT_SIZE, COLOR_FIRST_INPUT, batch = batch)
    first_input.draw()

def draw_result():
    result_label = pyglet.text.Label('YOUR SCORE: ' + str(player.get_score()),
                          font_name='Times New Roman',
                          font_size=40,
                          x = WINDOW_WIDTH / 2, y = WINDOW_HEIGHT / 2,
                          anchor_x='center', anchor_y='center')
    result_label.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    timer.set_start()
    save_point(float(x), float(y))

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    save_point(float(x), float(y))

    if timer.get_timer() <= 0:
        player.decrease_lifes()
        timer.reset_timer()
        restart()

@window.event
def on_mouse_release(x, y, button, modifiers): 
    global current_rune
    if timer.get_timer() <= 0:
        trial_failed()
    else:
        recognizer.recognize()
        if recognizer.get_matching_template() == current_rune.get_rune_name():
            old_rune = current_rune
            current_rune = random.choice(runes_arr)
            timer.reset_timer()
            timer.decrease_timer_duration(1, 2)
            player.increase_score()
            play_success_sound()
            restart()
            while current_rune.get_rune_name() == old_rune.get_rune_name():
                current_rune = random.choice(runes_arr)
        else:
            trial_failed()

# run game
app.run()
