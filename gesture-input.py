# gesture input program for first task
# gestures recognized are triangle, x, rectangle, circle, check, caret, arrow, left square bracket, right square bracket,
#                         v, delete, right curly brace, star and pigtail

import pyglet
from pyglet import app, shapes
from pyglet.window import Window

from helper_classes.point_class import Point
from recognizer import Recognizer

# window size
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

# width of line (input points are represented as a line)
WIDTH_INPUT_LINE = 5

# width/height of the first input point represented as a rectangle
RECT_SIZE = 30

# correction of the coordinates of the rectange to start the line from the center of the rectangle
RECT_CORRECTION = RECT_SIZE / 2

# colors
COLOR_INPUT_LINE = (50, 225, 30)
COLOR_FIRST_INPUT = (250,128,114)

# recognizer class
recognizer = Recognizer()

# creating a batch object
batch = pyglet.graphics.Batch()

# stored points
input_points:list[Point] = []

# create game window
window = Window(WINDOW_WIDTH, WINDOW_HEIGHT)

# save input points
def save_point(x:float, y:float):
    new_point = Point(x, y)
    # for drawing the points
    input_points.append(new_point)
    # add the new point (raw data of x and y) to the input points array in the recognizer
    recognizer.add_point(new_point.x, WINDOW_HEIGHT - new_point.y) # y value needs to be inverted/mirrored

# reset for every new attempt
def reset():
    global input_points
    window.clear()
    input_points = []
    recognizer.reset_recognizer()

@window.event
def on_draw():
    window.clear()
    draw_input()
    # after user finished drawing show the results
    if recognizer.get_matching_template() != "":
        draw_result()

# draw the input points
def draw_input():
    # wait till the user starts drawing
    if len(input_points) >= 1:
        # draw first input point as a rectangle
        draw_first_input()
        if len(input_points) > 1:
            # draw all input points as a line
            for i in range(len(input_points) - 1):
                input_line = shapes.Line(input_points[i].x, input_points[i].y, input_points[i + 1].x, input_points[i + 1].y, \
                                    WIDTH_INPUT_LINE, COLOR_INPUT_LINE, batch = batch)
                input_line.opacity = 255
                input_line.draw()

# draw first input point as a rectangle
def draw_first_input():
    first_input = shapes.Rectangle(input_points[0].x - RECT_CORRECTION, input_points[0].y - RECT_CORRECTION, RECT_SIZE, RECT_SIZE, COLOR_FIRST_INPUT, batch = batch)
    first_input.draw()

# draw results: matching template, score and inference time for the recognition
def draw_result():
    result_label = pyglet.text.Label('Result: ' + recognizer.get_matching_template() + ' (' + recognizer.get_score() + ') ' + 'in ' + recognizer.get_inference_time(),
                          font_name='Times New Roman',
                          font_size=20,
                          x = WINDOW_WIDTH - WINDOW_WIDTH / 2, y = WINDOW_HEIGHT - WINDOW_HEIGHT / 20,
                          anchor_x='center', anchor_y='center')
    result_label.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    reset()
    save_point(float(x), float(y))

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    save_point(float(x), float(y))

@window.event
def on_mouse_release(x, y, button, modifiers):   
    recognizer.recognize()

# run game
app.run()
