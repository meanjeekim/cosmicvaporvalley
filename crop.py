from enum import Enum
import json
import pygame as pg
from constants import CATEGORY

# Using an enum as an identifer cuts down on memory usage
# That way, a tile wouldn't store individual crops
class CROP_ID(Enum):
    STRAWBERRY = 1

# This Crop class is mostly just a model that stores all the relevant data
class Crop():
    def __init__(self, id, name, days, stage_to_image, item_image, sell_price):
        self.type = CATEGORY.CROP
        self.id = id
        self.days_to_grow = days
        self.name = name
        self.stages_to_image = stage_to_image
        self.item_image = item_image
        self.sell_price = sell_price
    
    def __str__(self):
        return self.name
    
    def get_image(self, day):
        for stage, img in sorted(self.stages_to_image.items()):
            if day <= stage:
                return img

# This Seed class is mostly just a model that stores the CROP_ID
class Seed():
    def __init__(self, CROP_ID):
        self.type = CATEGORY.SEED
        self.crop = CROP_ID