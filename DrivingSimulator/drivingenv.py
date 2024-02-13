import numpy as np
import matplotlib.pyplot as plt
import math
import time
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Tuple
import cv2

UP_ANGLE = 270
MAX_DISTANCE = 50
OFF_ROAD = 0
ON_ROAD = 1
PIXEL_SPEED = 3
STEER_ANGLE = 12.5

class Action(Enum):
    LEFT= 1
    STRAIGHT = 2
    RIGHT = 3
    
class Environment:
    def __init__(self, position: List[int], angle: float, pixel_map: np.ndarray):
        self.position = position
        self.angle = angle
        self.pixel_map = pixel_map
        
    def get_distance(self, angle: float = 0, draw_map: bool = False, draw_pixel_map: np.ndarray = None) -> int:
        y = self.position[0]
        x = self.position[1]
        
        if draw_map:
            draw_pixel_map[y, x] = 2
        
        x_inc = math.cos(math.radians(self.angle + UP_ANGLE + angle))
        y_inc = math.sin(math.radians(self.angle + UP_ANGLE + angle))
        
        for distance in range(1, MAX_DISTANCE):
            new_x = int(round(x + x_inc * distance))
            new_y = int(round(y + y_inc * distance))
            
            if (new_x < 0) or (new_x >= self.pixel_map.shape[1]) or (new_y < 0) or (new_y >= self.pixel_map.shape[0]):
                return distance - 1
            
            if self.pixel_map[new_y, new_x] == OFF_ROAD:
                return distance - 1
            
            if draw_map:
                draw_pixel_map[new_y, new_x] = 3
        
        return MAX_DISTANCE

    def get_distances(self, draw_map: bool = False, draw_pixel_map: np.ndarray = None) -> List[int]:
        distances = [ self.get_distance(-90, draw_map, draw_pixel_map), self.get_distance(-45, draw_map, draw_pixel_map), self.get_distance(0, draw_map, draw_pixel_map), self.get_distance(45, draw_map, draw_pixel_map), self.get_distance(90, draw_map, draw_pixel_map) ]
        
        return distances
    
    def move(self, pixel_speed: float = PIXEL_SPEED) -> None:
        y = self.position[0]
        x = self.position[1]
        
        x_inc = math.cos(math.radians(self.angle + UP_ANGLE)) * pixel_speed
        y_inc = math.sin(math.radians(self.angle + UP_ANGLE)) * pixel_speed
        
        self.position[1] += int(round(x_inc))
        self.position[0] += int(round(y_inc))
        
    def is_on_road(self) -> bool:
        y = self.position[0]
        x = self.position[1]
        
        if (x < 0) or (x >= self.pixel_map.shape[1]) or (y < 0) or (y >= self.pixel_map.shape[0]):
                return False
        
        return self.pixel_map[y, x] != OFF_ROAD
    
    def steer_left(self, angle: float = STEER_ANGLE) -> None:
        self.angle -= angle
        
    def steer_right(self, angle: float = STEER_ANGLE) -> None:
        self.angle += angle
        
    def act(self, action: Action) -> None:
        if action == Action.LEFT:
            #print('Left')
            self.steer_left()
        elif action == Action.RIGHT:
            #print('Right')
            self.steer_right()
        #else:
            #print('Straight')
            
    def get_status(self, draw_map: bool = False, draw_pixel_map: np.ndarray = None) -> Tuple[bool, List[int]]:
        return ( not self.is_on_road(), self.get_distances(draw_map, draw_pixel_map))
    
    def next(self, action: Action, draw_map: bool = False, draw_pixel_map: np.ndarray = None) -> Tuple[bool, List[int]]:
        self.act(action)
        self.move()
        return self.get_status(draw_map, draw_pixel_map)
    
def load_pixel_map(image_name):
    image = cv2.imread(image_name, cv2.IMREAD_UNCHANGED)
    image = image[:,:,3] // 255
    
    return image