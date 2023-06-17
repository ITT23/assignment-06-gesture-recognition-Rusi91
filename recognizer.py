# $1 gesture recognizer

# class for recognizing gestures based on templates
#
# SOURCES USED:
# Jacob Wobbrock's Website on Gesture RecognitionLink/URL - https://depts.washington.edu/acelab/proj/dollar/index.html [14.06.23]
#   -> Paper for understanding the architecture and functionality: http://faculty.washington.edu/wobbrock/pubs/uist-07.01.pdf [14.06.23]
#   -> Pseudocode: https://depts.washington.edu/acelab/proj/dollar/dollar.pdf [14.06.23]
#   -> source code in JavaScript: https://depts.washington.edu/acelab/proj/dollar/dollar.js [14.06.23]


import math
# point class for the x and y coordinates of a point of a gesture
from point_class import Point
# predefined gesture templates as a dictionary
from gesture_templates_dict import one_dollar_gesture_templates

# golden ratio - phi
# need to calculate the distance at the best angle
PHI = 0.5 * (-1.0 + math.sqrt(5.0))

# Value for resampling a points path into n evenly spaced points
N = 64

# default recognizer parameters
DEFAULT_ANGLE_RANGE = 45.0
DEFAULT_THRESHOLD = 2.0
DEFAULT_SQUARE_SIZE = 250
DEFAULT_ORIGIN = Point(0,0)
DEFAULT_TEMPLATE_DICT:dict = one_dollar_gesture_templates

# used for the bounding box calculation
class Rectangle():
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Recognizer():

    # in case users don't explicitly define a parameter, default parameters are used
    def __init__(self, dollar_templates:dict=DEFAULT_TEMPLATE_DICT, angle:float=DEFAULT_ANGLE_RANGE, threshold:float=DEFAULT_THRESHOLD, \
                 size:float=DEFAULT_SQUARE_SIZE, origin:Point=DEFAULT_ORIGIN):
        self.angle = angle
        self.threshold = threshold
        self.size = size
        self.origin = origin
        self.templates_dict:dict = load_templates(dollar_templates, self.size, self.origin)

    # recognizes input gestures based on the predefined templates and returns the matching template and score
    def recognize(self, input_points:list[Point]):
        # adjusts the input points for the recognition process
        points = adjust_input_data(input_points, self.size, self.origin)
        b = math.inf
        matching_template:dict = None
        for key, value in self.templates_dict.items():
            distance = distance_at_best_angle(points, value, -self.angle, self.angle, self.threshold)
            if distance < b:
                b = distance
                matching_template = key
        template_score = 1 - b / (0.5 * math.sqrt(self.size ** 2 + self.size ** 2))
        # print results
        print(matching_template)
        print(template_score)
        return matching_template, template_score
    
# loads, adjusts and returns predefined templates for the further recognition process
def load_templates(templates_dict:dict, size, origin):
    adjusted_templates:dict = {}
    for key, value in templates_dict.items():
        value = resample(value)
        radians = get_indicative_angle(value)
        value = rotate_by(value, radians)
        value = scale_to(value, size)
        value = translate_to(value, origin)
        adjusted_templates[key] = value
    return adjusted_templates

# adjusts the input points for the recognition process
def adjust_input_data(points:list[Point], square_size, origin):
    points = resample(points)
    radians = get_indicative_angle(points)
    points = rotate_by(points, radians)
    points = scale_to(points, square_size)
    points = translate_to(points, origin)
    return points

# resample a points path into n evenly spaced points
def resample(points:list[Point], n=N):

    I = get_path_length(points) / float(n - 1)
    D = 0.0
    new_points = [points[0]]
    i = 1

    while i < len(points):
        distance = get_distance(points[i - 1], points[i])
        
        if D + distance >= I:
            new_point_x = points[i - 1].x + ((I - D) / distance) * (points[i].x - points[i - 1].x)
            new_point_y = points[i - 1].y + ((I - D) / distance) * (points[i].y - points[i - 1].y)
            new_point = Point(new_point_x, new_point_y)
            new_points.append(new_point)
            points.insert(i, new_point)
            D = 0.0
        else:
            D += distance
        i += 1
    

    if len(new_points) == n - 1:  # prevent a roundoff error
        number:int = 1
        new_points.append(Point(points[len(points)-number].x, points[len(points-number)].y))
        new_points.append(Point(points[len(poins)]))

    return new_points

# returns distance/path between a point p and point p+1
def get_path_length(points:list[Point]):
    distance = 0.0
    for i in range(len(points) - 1):
        distance += get_distance(points[i], points[i + 1]) 
    return distance

# calculate Euclidean distance between two point: https://www.w3schools.com/python/ref_math_dist.asp#:~:text=The%20math.,be%20of%20the%20same%20dimensions.[15.06.23]
def get_distance(point_1:Point, point_2:Point):
    return math.dist([point_1.x, point_1.y], [point_2.x, point_2.y])

# radiant
# find and save the indicative angle ω from the points' centroid to first point
def get_indicative_angle(points:list[Point]):
    centroid_point = centroid(points)
    return math.atan2(centroid_point.y - points[0].y, centroid_point.x - points[0].x)

# n rotate by –ω to set this angle to 0°
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

# scale points so that the resulting bounding box will be of size**2 size
def scale_to(points:list[Point], size):
    bbox = bounding_box(points)
    new_points = []
    for i in range(len(points)):
        new_point_x = points[i].x * (size / bbox.width)
        new_point_y = points[i].y * (size / bbox.height)
        new_points.append(Point(new_point_x, new_point_y))
    return new_points

# translate points to the origin 
def translate_to(points:list[Point], origin:Point):
    centroid_point = centroid(points)
    new_points = []
    for i in range(len(points)):
        new_point_x = points[i].x + origin.x - centroid_point.x
        new_point_y = points[i].y + origin.y - centroid_point.y
        new_points.append(Point(new_point_x, new_point_y))
    return new_points

# returns the centroid point
def centroid(points:list[Point]):
    x_sum, y_sum = 0.0, 0.0
    for i in range(len(points)):
        x_sum += points[i].x
        y_sum += points[i].y

    x_sum /= len(points)
    y_sum /= len(points)

    return Point(x_sum, y_sum)

# needed for the scale_to method
# returns a rectangle defined by (min of x, min of y), (max of x, max of y)
def bounding_box(points:list[Point]):
    # infinity represenation in python: https://www.geeksforgeeks.org/python-infinity/ [15.06.23]
    #min_x, max_x = math.inf, -math.inf
    #min_y, max_y = math.inf, -math.inf

    # infinity (suggested by the pseudocode) leads to some bugs while init the values with 0 performs without problems
    min_x, max_x, min_y, max_y = 0, 0, 0, 0

    for i in range(len(points)):
        min_x = min(min_x, points[i].x)
        min_y = min(min_y, points[i].y)
        max_x = max(max_x, points[i].x)
        max_y = max(max_x, points[i].y)
    
    return Rectangle(min_x, min_y, max_x - min_x, max_y - min_y)

# returns distance at best angle between template and input points
def distance_at_best_angle(points:list[Point], template_values:list[Point], angle_range_neg, angle_range_pos, threshold):
    x1 = PHI * angle_range_neg + (1.0 - PHI) * angle_range_pos
    f1 = distance_at_angle(points, template_values, x1)
    x2 = (1.0 - PHI) * angle_range_neg + PHI * angle_range_pos
    f2 = distance_at_angle(points, template_values, x2)

    while abs(angle_range_pos - angle_range_neg) > threshold:
        if f1 < f2:
            angle_range_pos = x2
            x2 = x1
            f2 = f1
            x1 = PHI * angle_range_neg + (1.0 - PHI) * angle_range_pos
            f1 = distance_at_angle(points, template_values, x1)
        else:
            angle_range_neg = x1
            x1 = x2
            f1 = f2
            x2 = (1.0 - PHI) * angle_range_neg + PHI * angle_range_pos
            f2 = distance_at_angle(points, template_values, x2)

    return min(f1, f2)

# get distance at a specific angle (radians)
def distance_at_angle(points:list[Point], template_values:list[Point], radians):
    new_points = rotate_by(points, radians)
    return path_distance(new_points, template_values)

# get path distance 
def path_distance(points:list[Point], template_values:list[Point]):
    #print("jetzt")
    #print(len(points))
    #print(len(template_values))
    
    d = 0.0
    for i in range(len(points)):
        d += get_distance(points[i], template_values[i])
    return d / len(points)

# test recognizer with 'zick-zack' data
input_points =  [Point(75,250), Point(75,247), Point(77,244), Point(78,242), Point(79,239), Point(80,237), Point(82,234), Point(82,232), Point(84,229), Point(85,225), \
             Point(87,222), Point(88,219), Point(89,216), Point(91,212), Point(92,208), Point(94,204), Point(95,201), Point(96,196), Point(97,194), Point(98,191), Point(100,185), \
                Point(102,178), Point(104,173), Point(104,171), Point(105,164), Point(106,158), Point(107,156), Point(107,152), Point(108,145), Point(109,141), Point(110,139), \
                    Point(112,133), Point(113,131), Point(116,127), Point(117,125), Point(119,122), Point(121,121), Point(123,120), Point(125,122), Point(125,125), Point(127,130), \
                        Point(128,133), Point(131,143), Point(136,153), Point(140,163), Point(144,172), Point(145,175), Point(151,189), Point(156,201), Point(161,213), \
                            Point(166,225), Point(169,233), Point(171,236), Point(174,243), Point(177,247), Point(178,249), Point(179,251), Point(180,253), Point(180,255), \
                                Point(179,257), Point(177,257), Point(174,255), Point(169,250), Point(164,247), Point(160,245), Point(149,238), Point(138,230), Point(127,221), \
                                    Point(124,220), Point(112,212), Point(110,210), Point(96,201), Point(84,195), Point(74,190), Point(64,182), Point(55,175), Point(51,172), \
                                        Point(49,170), Point(51,169), Point(56,169), Point(66,169), Point(78,168), Point(92,166), Point(107,164), Point(123,161), Point(140,162), \
                                            Point(156,162), Point(171,160), Point(173,160), Point(186,160), Point(195,160), Point(198,161), Point(203,163), Point(208,163), \
                                                Point(206,164), Point(200,167), Point(187,172), Point(174,179), Point(172,181), Point(153,192), Point(137,201), Point(123,211), \
                                                    Point(112,220), Point(99,229), Point(90,237), Point(80,244), Point(73,250), Point(69,254), Point(69,252)] 
recognizer = Recognizer()
recognizer.recognize(input_points)


    
        
        
    
	

