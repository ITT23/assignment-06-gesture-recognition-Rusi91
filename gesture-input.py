# gesture input program for first task

import pyglet
import time
from pyglet import app, image, clock, shapes
from pyglet.window import Window

from point_class import Point
from recognizer import Recognizer

# https://pyglet.readthedocs.io/en/latest/programming_guide/mouse.html

# window size
WINDOW_WIDTH = 250
WINDOW_HEIGHT = 250

input_points:list[Point] = []

# create game window
window = Window(WINDOW_WIDTH, WINDOW_HEIGHT)

# creating a batch object
batch = pyglet.graphics.Batch()

# width of line
width = 5

# color = green
color = (50, 225, 30)

# width of rectangle
width_rect = 10
 
# height of rectangle
height_rect = 10

def save_point(x:float, y:float):
    new_point = Point(x, y)
    input_points.append(new_point)

recognizer = Recognizer()

@window.event
def on_draw():
    window.clear()
    draw_input()

def draw_input():
    
    if len(input_points) > 1:
        for i in range(len(input_points) - 1):
            line1 = shapes.Line(input_points[i].x, input_points[i].y, input_points[i + 1].x, input_points[i + 1].y, width, color = (50, 225, 30), batch = batch)
            line1.opacity = 255
            line1.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    window.clear()
    #save_point(float(x), float(y))
    print("blabla")

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    save_point(float(x), float(y))
    print(str(x) + "und" + str(y))
    print(len(input_points))
    

@window.event
def on_mouse_release(x, y, button, modifiers):
    print(input_points)
    recognizer.recognize(input_points)
    #print(matching_template)
    #print(score)

# run game
app.run()
