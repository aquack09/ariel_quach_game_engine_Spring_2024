# This file was created by: Ariel Quach
# Added this comment to prove that github is listening to my conversations
# import libraries and modules
'''
Game design truths:
goals, rules, feedback. freedom

Moving enemies
    dodge the enemies, dont die to the enemies
Additional types of powerups
    get more powerups
Menu/Start Screen
'''
import pygame as pg
from settings import *
from sprites import *
from utils import *
from random import randint
import sys
from os import path
from math import floor

LEVEL1 = "level1.txt"
LEVEL2 = "level2.txt"

# Creating the base bleprints
class Game:
    # Initializer -- sets up the game
    def __init__(self):
        # Setting -- set canvas, width, eght, and title
        pg.init()
        # set size of screen and be the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting pygame clock 
        self.clock = pg.time.Clock()
        self.load_data()
    
    def load_data(self):
        # game_folder = path.dirname(__file__)
        # self.img_folder = path.join(game_folder, 'images')
        # self.snd_folder = path.join(game_folder, 'sounds')
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        self.snd_folder = path.join(self.game_folder, 'sounds')

        self.player_img = pg.image.load(path.join(self.img_folder, 'zesty_drake.png')).convert_alpha()
        self.mob_img = pg.image.load(path.join(self.img_folder, 'peter_griffin.png')).convert_alpha()
        self.mob2_img = pg.image.load(path.join(self.img_folder, 'python.png')).convert_alpha()
        self.map_data = []
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(self.game_folder, LEVEL1), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)


    def change_level(self, lvl):
        # kill all existing sprites first to save memory
        for s in self.all_sprites:
            s.kill()
        # reset criteria for changing level
        self.player.moneybag = 0
        # reset map data list to empty
        self.map_data = []
        # open next level
        with open(path.join(self.game_folder, lvl), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
        # repopulate the level with stuff
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'm':
                    Mob2(self, col, row)
                if tile == 'U':
                    PowerUp(self, col, row)
    
    # Create run method which runs the whole GAME
    def new(self):
        # loading sound for use...not used yet
        # pg.mixer.music.load(path.join(self.snd_folder, 'soundtrack2.mp3'))
        # self.collect_sound = pg.mixer.Sound(path.join(self.snd_folder, 'sfx_sounds_powerup16.wav'))
        # create timer
        
        self.cooldown = Timer(self)
        self.testclass = Test()
        print("start the game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.pew_pews = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()

        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'U':
                    PowerUp(self, col, row)
                if tile == 'm':
                    Mob2(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'B':
                    BossMob(self, col, row)
    
    # Runs our game
    def run(self):
        # start playing sound on infinite loop (loops=-1)
        # pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    
    def quit(self):
         pg.quit()
         sys.exit()

    def update(self):
        # Updates self
        self.cooldown.ticking()
        self.all_sprites.update()
        if self.player.moneybag > 2:
            self.change_level(LEVEL2)
    
    def draw_grid(self):
         for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
         for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        surface.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(BGCOLOR)
        # self.draw_grid()
        self.all_sprites.draw(self.screen)
        # draw the timer
        self.draw_text(self.screen, str(self.cooldown.current_time), 24, WHITE, WIDTH/2 - 32, 2)
        self.draw_text(self.screen, str(self.cooldown.event_time), 24, WHITE, WIDTH/2 - 32, 80)
        self.draw_text(self.screen, str(self.cooldown.get_countdown()), 24, WHITE, WIDTH/2 - 32, 120)
        pg.display.flip()

    def events(self):
         for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_a:
            #         Allows for the character to move lefts
            #         self.player1.move(dx=-1)
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_w:
            #         Allows for the character to move up
            #         self.player1.move(dy=-1)
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_d:
            #         Allows for the character to move right
            #         self.player1.move(dx=1)
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_s:
            #         Allows for the character to move down
            #         self.player1.move(dy=1)

    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "Press any key to start the game", 24, WHITE, WIDTH/2.75, HEIGHT/2.25)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting =  False

# Create a new game
g = Game()
# use game method run to run
g.show_start_screen()
while True:
    # create new game
    g.new()
    # run the game
    g.run()
    # g.show_go_scrren()