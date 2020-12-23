# from farm import *
import pygame as pg
import json
from crop import *

ID_TO_CROPS = dict()

file_start = 'assets/'

# ideally, make some loader class so that the game can have its own instance?
# ideally, only load images as called
def load_crops():
    with open('assets/crops.json') as f:
        id_to_crop_json = json.load(f)
        images = dict()
        for id, crop in id_to_crop_json.items():
            images[CROP_ID[id]] = Crop(CROP_ID[id], crop['name'], crop['days_to_grow'], {int(day): pg.image.load(file_start+filename).convert_alpha() for day, filename in crop['stages_to_image'].items()}, pg.image.load(file_start+crop['item_image']).convert_alpha(), crop['sell_price'])
        
        print(images)
        return images