# $1 gesture recognizer

import math
import numpy as np


class Point():
    # define parameter type: https://docs.python.org/3/library/typing.html [15.06.23]
    def __init__(self, x:float, y:float, angle_range:float=45.0, angle_step:float=2.0):
        self.x = x
        self.y = y

class Rectangle():

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height



class Recognizer():

    def __init__(self) -> None:
        pass

    def recognize(points, templates):
        b = math.inf



def resample(points, n=64):
    
    I = get_path_length(points) / float(n - 1)
    D = 0.0
    new_points = [points[0]]
    
    for i in range(len(points)):
        distance = get_distance(points[i], points[i + 1])
        if D + distance >= I:
            
            new_point_x = points[i].x + ((I - D) / distance) * (points[i].x - points[i].x)
            new_point_y = points[i].y + ((I - D) / distance) * (points[i].y - points[i].y)
            new_point = Point(new_point_x, new_point_y)
            new_points.append(new_point)
            points.insert(i, new_point)
            D = 0.0
        else:
            D += distance
            
    if len(new_points) == n - 1:  # prevent a roundoff error
        new_points.append(Point(points[len(points) - 1].x, points[len(points - 1)].y))

    return new_points
    
def get_path_length(points):
    distance = 0.0

    for i in range(len(points)):
        distance += get_distance(points[i], points[i + 1]) 
    
    return distance
	
# Calculate Euclidean distance between two point: https://www.w3schools.com/python/ref_math_dist.asp#:~:text=The%20math.,be%20of%20the%20same%20dimensions.[15.06.23]
def get_distance(point_1, point_2):
    return math.dist([point_1.x, point_1.y], [point_2.x, point_2.y])

def get_indicative_angle(points):
    centroid_point = centroid(points)
    return math.atan2(centroid_point.y - points[0].y, centroid_point.x - points[0].x)

def rotate_by(points, radians):
    centroid_point = centroid(points)
    cos = math.cos(radians)
    sin = math.sin(radians)
    new_points = []
    for i in range(len(points)):
        new_point_x = (points[i].x - centroid_point.x) * cos - (points[i].y - centroid_point.y) * sin + centroid_point.x
        new_point_y = (points[i].x - centroid_point.x) * sin + (points[i].y - centroid_point.y) * cos + centroid_point.y
        new_points.append(Point(new_point_x, new_point_y))

    return new_points

def scale_to(points, size):
    bbox= bounding_box(points)
    new_points = []
    for i in range(len(points)):
        new_point_x = points[i].x * (size / bbox.width)
        new_point_y = points[i].y * (size / bbox.height)
        new_points.append(Point(new_point_x, new_point_y))

    return new_points

def translate_to(points, point_k):
    centroid_point = centroid(points)
    new_points = []
    for i in range(len(points)):
        new_point_x = points[i].x + point_k.x - centroid_point.x
        new_point_y = points[i].y + point_k.y - centroid_point.y
        new_points.append(Point(new_point_x, new_point_y))
    
    return new_points

def centroid(points):
    x_sum, y_sum = 0.0, 0.0
    for i in range(len(points)):
        x_sum += points[i].x
        y_sum += points[i].y

    x_sum /= len(points)
    y_sum /= len(points)

    return Point(x_sum, y_sum)

def bounding_box(points):
    # infinity represenation in python: https://www.geeksforgeeks.org/python-infinity/ [15.06.23]
    min_x, max_x = math.inf, -math.inf
    min_y, max_y = math.inf, -math.inf

    for i in range(len(points)):
        min_x = np.min(min_x, points[i].x)
        min_y = np.min(min_y, points[i].y)
        max_x = np.max(max_x, points[i].x)
        max_y = np.max(max_x, points[i].y)
    
    return Rectangle(min_x, min_y, max_x - min_x, max_y - min_y)


    
        
        
    
	

