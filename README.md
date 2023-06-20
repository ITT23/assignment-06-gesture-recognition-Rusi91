[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/aaWv-gak)

**recognizer.py**
- class for recognizing gestures based on templates
- templates are stored in a dictionary (material\dictionary\gesture_templates_dict.py)

**gesture-input.py**
- pyglet is used for the gesture drawing process
- the recognizer class is used to save the input points and the recognition process
- gestures recognized are triangle, x, rectangle, circle, check, caret, arrow, left square bracket, right square bracket
    v, delete, right curly brace, star and pigtail
- results: matching template, score and inference time

**gesture-application**
- recogizer class is used for the recognition process
- pyglet for drawing

GAME:
- users need to draw runes
- runes are the gestures arrow, check, delete, star, x, pigtail, rectangle and triangle
- the rune to be drawn is shown as a template (template doesn't disapear) [templates: material\images\]{helper_class: helper_classes\rune_class.py}
- to draw the rune the player has 20 seconds {helper_class: helper_classes\timer_class.py}
- after every suggestfully drawn rune the player gets less time to draw the next rune (1 second less after each rune; limit is 2 seconds)
- if the timer runs out or the drawn rune is incorrect, the player loses 1 life/point (has 5 lifes)
- if the drawn rune is correct, the player gets 1 point
- if the player loses all lifes, the results are shown (achieved points)
          -> to start a new game after the results -> left mouse click
- timer, score and remainig lifes are shown in the corners
- sounds are played for success or fails [sound-files: material\music\]{helper_class: helper_classes\rune_class.py}

**helper_classes folder**
contains classes i wrote to maintain the code clear and legible

point_class.py -> class for a point (x, y)
rune_class.py -> class for a rune (game for task 3)
timer_class.py -> class for the timer (game for task 3)
player_class.py -> class for player attributes (game for task 3)

**material folder**
contains the gesture templates for the 1 dollar recognizer and the image material (images and soundtracks)