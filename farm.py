import pygame as pg
from enum import Enum
from tool import *
from crop import *
import loaders

class TILE_ID(Enum):
    SOIL = 0
    WATERED_SOIL = 1

# For now, the Tile class stores just the CROP_ID and gets the relevant data from the ID_TO_CROPS dict from `loaders.py`
# But ideally, the Tile class would extend pygame.sprite.Sprite? Maybe?
class Tile():
    def __init__(self, px, py):
        self.px = px
        self.py = py
        self.pos = (px, py)

        self.state = TILE_ID.SOIL
        self.is_watered = False
        
        self.crop = None            # type is class Crop
        self.days_until_ripe = -1   # decrements with each day if watered; resets when harvested
    
    def __str__(self):
        if self.is_watered:
            return 'wateredsoil'
        else:
            return 'soil'

    def next_day(self):
        self.grow()

    def harvest(self):
        if self.days_until_ripe == 0:
            harvest_crop = self.crop
            
            self.crop = None
            self.days_until_ripe = -1

            return harvest_crop
        else:
            return
    
    def grow(self):
        if self.is_watered:
            self.is_watered = False
            self.state = TILE_ID.SOIL
            if self.days_until_ripe > 0:
                self.days_until_ripe -= 1
    
    def plant(self, crop_id):
        self.crop = crop_id
        self.days_until_ripe = loaders.ID_TO_CROPS[crop_id].days_to_grow
        
        return True

    def perform_tool(self, tool):
        if tool.tool == TOOL_ID.WATERINGCAN:
            print('farm.py: tool is wateringcan')
            self.is_watered = True
            self.state = TILE_ID.WATERED_SOIL
        elif tool.tool == TOOL_ID.SICKLE:
            print('farm.py: tool is sickle')
            return self.harvest()