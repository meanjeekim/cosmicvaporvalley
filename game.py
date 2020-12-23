import pygame as pg
from pathlib import Path

import sys
import pickle
from constants import *
from farm import *
from farmer import *
import loaders

class CosmicVaporValley:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.HOUR_PASSED = pg.USEREVENT
        self.time = FIRSTHOUR
        self.light_color = pg.Color(255, 189, 51, LIGHT_ALPHA)
        self.dark_color = pg.Color(0, 0, 0, LIGHT_ALPHA)
        self.am = True
        self.dirtytiles = set()
        self.is_time_dirty = True
        self.load_data()

    # Loads tile images and crop data
    def load_data(self):
        self.font = pg.font.Font('assets/Stardew_Valley.ttf', 28)
        self.images = {
            'soil': pg.image.load('assets/soil.png').convert_alpha(),
            'wateredsoil': pg.image.load('assets/wateredsoil.png').convert_alpha(),
        }
        loaders.ID_TO_CROPS = loaders.load_crops()

    # saves to the pickle game file
    def save_game(self):
        # need to store: days, field, farmer
        save_dict = {
            'days': self.days,
            'field': self.field,
            'farmer': self.farmer
        }

        with open(f'{self.farmer.name}.pickle', 'wb') as f:
            pickle.dump(save_dict, f, protocol=pickle.HIGHEST_PROTOCOL)

    # Loads the game in the pickle file
    def load_game(self, name):
        file = Path(f'{name}.pickle')
        if file.is_file():
            with open(f'{name}.pickle', 'rb') as f:
                save_dict = pickle.load(f)
                self.days = save_dict['days']
                self.field = save_dict['field']
                self.farmer = save_dict['farmer']
        else:
            self.new_game(name)
        
        self.dirtytiles.update(self.field.values())
        pg.time.set_timer(self.HOUR_PASSED, HOUR_INTERVAL)     # in-game time increments every 7 seconds

    # New game will overwrite old file with a fresh copy.
    def new_game(self, name):
        self.days = 0
        self.field = {(x, y): Tile(x, y) for y in range(0, HEIGHT, TILESIZE) for x in range(0, WIDTH, TILESIZE)}
        self.farmer = Farmer(name)

        self.save_game()
    
    def run(self):
        self.playing = True

        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000

            self.events()
            self.draw()
    
    def quit(self):
        pg.quit()
        sys.exit()

    # start the next day
    def next_day(self):
        self.time = FIRSTHOUR
        self.days += 1
        self.am = True
        pg.time.set_timer(self.HOUR_PASSED, 0)
        pg.time.set_timer(self.HOUR_PASSED, HOUR_INTERVAL)

        self.farmer.next_day()
        for tile in self.field.values():
            tile.next_day()
        
        self.save_game()

        self.dirtytiles.update(self.field.values())
        self.is_time_dirty = True

    # rounds the given pos (x,y) to nearest coordinates that are multiples of TILESIZE
    def round_pos(self, pos):
        x, y = pos
        return x//TILESIZE*TILESIZE, y//TILESIZE*TILESIZE
    
    # returns list of TILESIZE-rounded coordinates representing the topleft position
    # that the given rect is in
    def round_rect(self, rect):
        left, top = self.round_pos(rect.topleft)
        right, bottom = self.round_pos(rect.bottomright)

        return [(x,y) for y in range(top, bottom, TILESIZE) for x in range(left, right, TILESIZE)]

    # Returns the string of the time to display
    def round_time(self):
        rounded_time = str(self.time%12)
        if self.am:
            rounded_time += 'AM'
        else: 
            rounded_time += 'PM'

        return rounded_time

    def draw(self):
        self.draw_dirtytiles()
        self.draw_grid()
        self.draw_inventory()
        self.draw_text()
        self.draw_time()
        pg.display.flip()
    
    def draw_text(self):
        title = self.font.render('Welcome to Cosmic Vapor Valley!', False, (0,0,0))
        self.screen.blit(title, (0,0))
    
    def draw_inventory(self):
        money_text = self.font.render(f'M: {self.farmer.money}', False, (0,0,0))
        money_topleft = (WIDTH-100, 100)
        money_rect = pg.Rect(money_topleft, money_text.get_size())

        inventory_count_text = self.font.render(f'{len(self.farmer.inventory)}x', False, (0,0,0))
        inv_topleft = (WIDTH-65, HEIGHT-40)
        inv_rect = pg.Rect(inv_topleft, inventory_count_text.get_size())

        self.dirtytiles.update({self.field[pos] for pos in self.round_rect(money_rect)})
        print(self.dirtytiles)
        self.dirtytiles.update({self.field[pos] for pos in self.round_rect(inv_rect)})
        print('inventory')
        print(self.dirtytiles)
        self.draw_dirtytiles()

        self.screen.blit(inventory_count_text, inv_topleft)
        self.screen.blit(money_text, money_topleft)
        self.screen.blit(loaders.ID_TO_CROPS[CROP_ID.STRAWBERRY].item_image, (WIDTH-80, HEIGHT-100))
    
    def draw_time(self):
        # Only redraw time if the time changed
        if self.is_time_dirty:
            pg.draw.rect(self.screen, (255, 255, 255), pg.Rect(WIDTH-110, 0, 110, 80))
            time_text = self.font.render(self.round_time(), False, (0,0,0))
            self.screen.blit(time_text, (WIDTH-70, 10))

            day_text = self.font.render(f'Day {self.days}', False, (0,0,0))
            self.screen.blit(day_text, (WIDTH-90, 40))

            self.is_time_dirty = False

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, (198, 198, 198), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, (198, 198, 198), (0, y), (WIDTH, y))

    def draw_dirtytiles(self):
        # Only redraw tiles that were changed
        while self.dirtytiles:
            tile = self.dirtytiles.pop()
            # Currently drawing the soil and crop explicitly, but won't scale to further features...
            # draw the soil; `tile.state` will determine whetehr tos how dry or watered soil
            self.screen.blit(self.images[str(tile)], tile.pos)

            # draw the crop if it exists
            if tile.crop != None:
                self.screen.blit(loaders.ID_TO_CROPS[tile.crop].get_image(tile.days_until_ripe), tile.pos)
            
            # add light tint
            self.draw_light((TILESIZE, TILESIZE), tile.pos)
    
    # Given a size and position, draw a light tint Rect
    def draw_light(self, size, pos):
        s = pg.Surface(size, pg.SRCALPHA)
        s.fill(self.light_color)
        self.screen.blit(s, pos)

        if not self.am:
            s.fill(self.dark_color)
            self.screen.blit(s, pos)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                tile = self.field[self.round_pos(event.pos)]

                # if active used, then tile is changed and becomes dirty
                # for better stamina display efficiency, maybe use bits to check if tile or stamina bar needs to be redrawn? future health bar too..
                if self.farmer.use_active(tile):
                    print('game.py: used active')
                    self.dirtytiles.add(tile)
            
            # When the HOUR_PASSED event occurs
            elif event.type == self.HOUR_PASSED:
                self.time += 1

                if self.time >= 12:
                    self.am = False
                    self.color = self.dark_color
                    self.dark_color.a += ALPHA_INCR
                else:
                    self.light_color.a += ALPHA_INCR

                if self.time >= 22:
                    self.next_day()
                
                self.dirtytiles.update(self.field.values())
                self.is_time_dirty =  True
            
            # Key responses
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    self.farmer.active_object = Seed(CROP_ID.STRAWBERRY)
                elif event.key == pg.K_2:
                    self.farmer.active_object = Tool(TOOL_ID.WATERINGCAN)
                elif event.key == pg.K_3:
                    self.farmer.active_object = Tool(TOOL_ID.SICKLE)
                elif event.key == pg.K_p:
                    self.farmer.sell_crop()
                elif event.key == pg.K_SPACE:
                    self.next_day()

g = CosmicVaporValley()


g.load_game(input('Enter your name: '))
g.run()