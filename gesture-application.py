# application for task 3

# gesture input program for first task

import pyglet
import time
import random

from pyglet import app, shapes, image
from pyglet.window import Window
from threading import Timer

from point_class import Point
from recognizer import Recognizer
from rune_class import Rune

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
input_points_mirrored:list[Point] = []

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

player_lifes_remaining = 5

# timer
try_timer:Timer = None

# create game window
window = Window(WINDOW_WIDTH, WINDOW_HEIGHT)

def save_point(x:float, y:float):
    new_point = Point(x, y)
    input_points.append(new_point)
    input_points_mirrored.append(Point(x, get_mirrored_y(y)))

def restart():
    global input_points, input_points_mirrored
    window.clear()
    input_points = []
    input_points_mirrored = []
    recognizer.reset_recognizer()

def timer(time_to_count):
    global try_timer
    try_timer = Timer()


recognizer = Recognizer()

# I adopted the get_mirrored_y method from Rosti97 (Sabrina Hößl) - ITT23/assignment-06-gesture-recognition-Rosti97 [17.06.23]
# My input was often incorrectly recognized despite the working recognizer (I tested the recognizer with the templates and everything worked correctly).
# Since at first glance she was trying a similar approach to mine, I compared her piece of code for storing the x and y coordinates to mine and noticed 
# that she subtracts the y value from the height. I tried it out and my recognition was correct.
def get_mirrored_y(y):
    return WINDOW_HEIGHT-y

@window.event
def on_draw():
    window.clear()
    draw_background()
    draw_remaining_tries()
    draw_input()
    #if recognizer.get_matching_template() != "":
        #draw_result()

def draw_background():
    motion_image = image.load(current_rune.get_rune_path())
    motion_image.blit(0, 0)

# display of the player's remaining lives
def draw_remaining_tries():
    player_lifes = pyglet.text.Label("Tries: " + str(player_lifes_remaining),
                          font_name='Times New Roman',
                          font_size=25,
                          x = WINDOW_WIDTH - WINDOW_WIDTH / 8, y = WINDOW_HEIGHT / 15,
                          anchor_x='center', anchor_y='center')
    player_lifes.draw()

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
    result_label = pyglet.text.Label('Result: ' + recognizer.get_matching_template() + ' (' + recognizer.get_score() + ') ' + 'in ' + recognizer.get_inference_time(),
                          font_name='Times New Roman',
                          font_size=20,
                          x = WINDOW_WIDTH - WINDOW_WIDTH / 2, y = WINDOW_HEIGHT - WINDOW_HEIGHT / 20,
                          anchor_x='center', anchor_y='center')
    result_label.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    restart()
    save_point(float(x), float(y))

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    save_point(float(x), float(y))

@window.event
def on_mouse_release(x, y, button, modifiers): 
    global current_rune  
    recognizer.recognize(input_points_mirrored)
    if recognizer.get_matching_template() == current_rune.get_rune_name():
        old_rune = current_rune
        current_rune = random.choice(runes_arr)
        while current_rune.get_rune_name() == old_rune.get_rune_name():
            current_rune = random.choice(runes_arr)
        restart()

# run game
app.run()
