import pygame as pg
from constants import *
from tool import *
from crop import *
import loaders

class Farmer():
    def __init__(self, name):
        self.name = name
        self.max_energy = 30
        self.energy = 30
        self.money = 0
        self.inventory = []
        self.active_tile = None
        self.active_object = Seed(CROP_ID.STRAWBERRY)
    
    # will be called by game.py to reset the farmer for the next day
    def next_day(self):
        self.energy = self.max_energy
    
    # rudimentary selling
    def sell_crop(self):
        if len(self.inventory) > 0:
            crop = self.inventory.pop()
            self.money += loaders.ID_TO_CROPS[crop].sell_price
            print(self.money)

    # return True if active is used
    def use_active(self, tile):
        if self.active_object.type == CATEGORY.TOOL:
            return self.use_tool(tile)
        elif self.active_object.type == CATEGORY.SEED:
            return tile.plant(self.active_object.crop)
        else:
            return False

    # Returns true if farmer has energy to use the tool
    # Also adds to inventory if tool is used and harvests
    def use_tool(self, tile):
        if self.energy > 0:
            self.energy -= self.active_object.energy
            output_item = tile.perform_tool(self.active_object)
            if output_item != None:
                self.inventory.append(output_item)
                print(self.inventory)
            
            return True
        else:
            return False