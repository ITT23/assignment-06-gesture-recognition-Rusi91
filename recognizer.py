# $1 gesture recognizer

import math
import numpy as np

from gesture_templates_dict import one_dollar_gesture_templates

# golden ratio - phi
PHI = 0.5 * (-1.0 + math.sqrt(5.0))


class Point():
    # define parameter type: https://docs.python.org/3/library/typing.html [15.06.23]
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

class Rectangle():

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height



class Recognizer():

    def __init__(self, templates:dict, angle:float=45.0, threshold:float=2.0, square_size:float=250, origin:Point=Point(0,0)):
        self.templates_dict = templates
        self.angle = angle
        self.threshold = threshold
        self.square_size = square_size
        self.origin = origin

    def recognize(self, points:list[Point]):
        b = math.inf
        matching_template = None
        for template in self.templates_dict:
            distance = distance_at_best_angle(points, self.templates_dict.values, -self.angle, self.angle, self.threshold)
            if distance < b:
                b = distance
                matching_template = template
        template_score = 1 - b / (0.5 * math.sqrt(self.square_size ** 2 + self.square_size ** 2))

        return matching_template, template_score

def resample(points:list[Point], n=64):
    
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
    
def get_path_length(points:list[Point]):
    distance = 0.0

    for i in range(len(points)):
        distance += get_distance(points[i], points[i + 1]) 
    
    return distance
	
# Calculate Euclidean distance between two point: https://www.w3schools.com/python/ref_math_dist.asp#:~:text=The%20math.,be%20of%20the%20same%20dimensions.[15.06.23]
def get_distance(point_1:Point, point_2:Point):
    return math.dist([point_1.x, point_1.y], [point_2.x, point_2.y])

def get_indicative_angle(points):
    centroid_point = centroid(points)
    return math.atan2(centroid_point.y - points[0].y, centroid_point.x - points[0].x)

def rotate_by(points:list[Point], radians):
    centroid_point = centroid(points)
    cos = math.cos(radians)
    sin = math.sin(radians)
    new_points = []
    for i in range(len(points)):
        new_point_x = (points[i].x - centroid_point.x) * cos - (points[i].y - centroid_point.y) * sin + centroid_point.x
        new_point_y = (points[i].x - centroid_point.x) * sin + (points[i].y - centroid_point.y) * cos + centroid_point.y
        new_points.append(Point(new_point_x, new_point_y))

    return new_points

def scale_to(points:list[Point], size):
    bbox= bounding_box(points)
    new_points = []
    for i in range(len(points)):
        new_point_x = points[i].x * (size / bbox.width)
        new_point_y = points[i].y * (size / bbox.height)
        new_points.append(Point(new_point_x, new_point_y))

    return new_points

def translate_to(points:list[Point], origin:Point):
    centroid_point = centroid(points)
    new_points = []
    for i in range(len(points)):
        new_point_x = points[i].x + origin.x - centroid_point.x
        new_point_y = points[i].y + origin.y - centroid_point.y
        new_points.append(Point(new_point_x, new_point_y))
    
    return new_points

def centroid(points:list[Point]):
    x_sum, y_sum = 0.0, 0.0
    for i in range(len(points)):
        x_sum += points[i].x
        y_sum += points[i].y

    x_sum /= len(points)
    y_sum /= len(points)

    return Point(x_sum, y_sum)

def bounding_box(points:list[Point]):
    # infinity represenation in python: https://www.geeksforgeeks.org/python-infinity/ [15.06.23]
    min_x, max_x = math.inf, -math.inf
    min_y, max_y = math.inf, -math.inf

    for i in range(len(points)):
        min_x = np.min(min_x, points[i].x)
        min_y = np.min(min_y, points[i].y)
        max_x = np.max(max_x, points[i].x)
        max_y = np.max(max_x, points[i].y)
    
    return Rectangle(min_x, min_y, max_x - min_x, max_y - min_y)

def distance_at_best_angle(points:list[Point], template_values:list[Point], angle_range_neg, angle_range_pos, threshold):
    x1 = PHI * angle_range_neg + (1.0 - PHI) * angle_range_pos
    f1 = distance_at_angle(points, template_values, x1)
    x2 = (1.0 - PHI) * angle_range_neg + PHI * angle_range_pos
    f2 = distance_at_angle(points, template_values, x2)

    while np.abs(angle_range_pos - angle_range_neg) > threshold:
        if f1 < f2:
            angle_range_pos = x2
            x2 = x1
            f2 = f1
            x1 = PHI * a + (1.0 - PHI) * angle_range_pos
            f1 = distance_at_angle(points, template_values, x1)
        else:
            angle_range_neg = x1
            x1 = x2
            f1 = f2
            x2 = (1.0 - PHI) * angle_range_neg + PHI * angle_range_pos
            f2 = distance_at_angle(points, template_values, x2)

    return np.min(f1, f2)

def distance_at_angle(points:list[Point], template_values:list[Point], radians):
    new_points = rotate_by(points, radians)

    return path_distance(new_points, template_values)

def path_distance(points:list[Point], template_values:list[Point]):
    d = 0.0
    for i in range(len(points)):
        d += get_distance(points[i], template_values[i])

    return d / len(points)


    
        
        
    
	

