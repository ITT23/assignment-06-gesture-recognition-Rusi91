# application for task 3

# GAME:
# - users need to draw runes
# - runes are the gestures arrow, check, delete, star, x, pigtail, rectangle and triangle
# - the rune to be drawn is shown as a template (template doesn't disapear) [templates: material\images\]{helper_class: helper_classes\rune_class.py}
# - to draw the rune the player has 20 seconds {helper_class: helper_classes\timer_class.py}
# - after every suggestfully drawn rune the player gets less time to draw the next rune (1 second less after each rune; limit is 2 seconds)
# - if the timer runs out or the drawn rune is incorrect, the player loses 1 life/point (has 5 lifes)
# - if the drawn rune is correct, the player gets 1 point
# - if the player loses all lifes, the results are shown (achieved points)
#           -> to start a new game after the results -> left mouse click
# - timer, score and remainig lifes are shown in the corners
# - sounds are played for success or fails [material\music\]{helper_class: helper_classes\rune_class.py}

import pyglet
import random

from pyglet import app, shapes, image
from pyglet.window import Window
from os import path

from helper_classes.point_class import Point
from helper_classes.rune_class import Rune
from helper_classes.timer_class import Timer
from helper_classes.player_class import Player

from recognizer import Recognizer



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

# path for sounds (sound if user achieves or not achieves to draw the correct rune)
    # sound source: https://www.youtube.com/watch?v=_q8QmJadSEE -Piano Note C Sound Effect - @Sound Effects
SUCCESS_SOUND_PATH = path.join(path.dirname(__file__), "..\material\game\music\success_sound.mp3")
    # https://www.youtube.com/watch?v=_XRnENg_QI0 -Error Sound Effect (HD) - @Servus
FAIL_SOUND_PATH = path.join(path.dirname(__file__), "..\material\game\music\\fail_sound.mp3")
# path for background image for results
    # https://www.freeimages.com/premium-vector/old-open-magic-book-5706544?ref=365psd
RESULTS_BACKGROUND_PATH = path.join(path.dirname(__file__), "..\material\game\images\\book.png")

# creating a batch object
batch = pyglet.graphics.Batch()

# stored points
input_points:list[Point] = []

# runes
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

# player attributes
PLAYER_LIFES = 5
player = Player(PLAYER_LIFES)

# timer
duration = 20.0
DURATION_LIMIT = 2
timer = Timer(duration)

# recognizer class
recognizer = Recognizer()

# create game window
window = Window(WINDOW_WIDTH, WINDOW_HEIGHT)

# save input points
def save_point(x:float, y:float):
    new_point = Point(x, y)
    input_points.append(new_point)
    recognizer.add_point(new_point.x, WINDOW_HEIGHT - new_point.y)

# reset for every new attempt
def restart():
    global input_points
    window.clear()
    input_points = []
    recognizer.reset_recognizer()

# if trial is failed
def trial_failed():
    play_fail_sound()
    player.decrease_lifes()
    timer.reset_timer()
    restart()

# play success sound if user achieved to draw the correct rune
def play_success_sound():
    success_sound = pyglet.media.load(SUCCESS_SOUND_PATH, streaming=False)
    success_sound.play()

# play fail sound if user don't achieved to draw the correct rune
def play_fail_sound():
    fail_sound = pyglet.media.load(FAIL_SOUND_PATH, streaming=False)
    fail_sound.play()

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
        # draw rune template
        background_image = image.load(current_rune.get_rune_path())
    else:
        # draw results background
        background_image = image.load(RESULTS_BACKGROUND_PATH)
    background_image.blit(0, 0)

# display of the player's remaining lives
def draw_remaining_tries():
    player_lifes_label = pyglet.text.Label("Tries: " + str(player.get_lifes_amount()),
                          font_name='Times New Roman',
                          font_size=25,
                          x = WINDOW_WIDTH - WINDOW_WIDTH / 8, y = WINDOW_HEIGHT / 15,
                          anchor_x='center', anchor_y='center')
    player_lifes_label.draw()

# draw remaining time
def draw_timer():
    timer_label = pyglet.text.Label("Timer: " + timer.get_timer_string(),
                          font_name='Times New Roman',
                          font_size=25,
                          x = WINDOW_WIDTH - WINDOW_WIDTH / 7, y = WINDOW_HEIGHT - WINDOW_HEIGHT / 15,
                          anchor_x='center', anchor_y='center')
    timer_label.draw()

# draw achieved points
def draw_score():
    score_label = pyglet.text.Label("Score: " + str(player.get_score()),
                          font_name='Times New Roman',
                          font_size=25,
                          x = WINDOW_WIDTH / 7, y = WINDOW_HEIGHT / 15,
                          anchor_x='center', anchor_y='center')
    score_label.draw()

# draw input points
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
    if player.get_lifes_amount() <= 0:
        player.reset()
        timer.reset_timer()
        timer.set_duration(duration)
        restart()
    else:
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
    # if timer runs out
    if timer.get_timer() <= 0:
        trial_failed()
    else:
        recognizer.recognize()
        # if rune was drawn correctly
        if recognizer.get_matching_template() == current_rune.get_rune_name():
            # show next rune to draw
            old_rune = current_rune
            current_rune = random.choice(runes_arr)
            timer.reset_timer()
            timer.decrease_timer_duration(1, DURATION_LIMIT)
            player.increase_score()
            play_success_sound()
            restart()
            # next rune is random but should not be the same
            while current_rune.get_rune_name() == old_rune.get_rune_name():
                current_rune = random.choice(runes_arr)
        else:
            # if rune was drawn incorrectly
            trial_failed()

# run game
app.run()
