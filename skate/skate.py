""""
to write this kind of level program is a big challenge to me.
I have always interested in how would the Google Chrome offline game work.
all the images achieved by myself with photoshop
some functionality that I can't make it so I read others code first and wrote it by my own way
here is the resource that I have been relied on
https://github.com/AlejoG10/python-dino-yt
"""


import math
import random
import pygame


pygame.init()  # initialise module pygame
pygame.mixer.init()  # initialise speaker
canvas = pygame.display.set_mode((900, 300))  # set the size of canvas with tuple
pygame.display.set_caption('D i n o s a u r   S k a t e b o a r d i n g')  # captions on the canvas


class Background:
    """set a parallax infinite scrolling background
       parameter: x(default parameter)
       attributes: width, height (dimensions for background)
                   x, y (coordinate for scrolling the background)
                   picture (pic of background)
       methods: update() --
                set_picture() -- adding pic to background
                show() -- showing the pic for background
    """

    def __init__(self, x):
        self.width = 900
        self.height = 300
        self.x = x
        self.y = 0
        self.picture = None
        self.set_picture()
        self.show()

    def update(self, dx):  # dx is the speed that how fast we want the pic of bg move(negative num, bg move to left)
        self.x += dx
        if self.x <= -900:
            self.x = 900

    def show(self):  # blit pic on the canvas
        canvas.blit(self.picture, (self.x, self.y))

    def set_picture(self):  # load pic
        self.picture = pygame.image.load('pics/background.png')
        self.picture = pygame.transform.scale(self.picture, (self.width, self.height))


class Dinosaur:
    """set dinosaur
       parameter: self
       attributes: width, height (dimensions for dinosaur)
                   x, y (coordinate for dinosaur)
                   picture (pic of dinosaur)
                   picture_num (pic index)
                   on_ground jumping jump_stop fall_stop(responsible for the movements jump)
       methods: set_sound() -- active the sound
                set_picture() -- adding pic to canvas
                show() -- showing dino on the canvas
    """
    def __init__(self):
        self.width = 70
        self.height = 94
        self.x = 80  # the x position of dino
        self.y = 155  # the y position of dino
        self.picture_num = 0
        self.picture = None
        self.dy = 5
        self.gravity = 1.2
        self.on_ground = True
        self.jumping = False
        self.jump_stop = 10
        self.falling = False
        self.sound = None
        self.fall_stop = self.y
        self.set_picture()
        self.set_sound()
        self.show()

    def update(self, loops):
        # jumping
        if self.jumping:
            self.y -= self.dy
            if self.y <= self.jump_stop:
                self.fall()

        # falling
        elif self.falling:
            self.y += self.gravity * self.dy
            if self.y >= self.fall_stop:
                self.stop()

        # walking
        elif self.on_ground and loops % 4 == 0:
            self.picture_num = (self.picture_num + 1) % 3
            self.set_picture()

    def show(self):
        canvas.blit(self.picture, (self.x, self.y))

    def set_picture(self):
        self.picture = pygame.image.load(f'pics/d{self.picture_num}.png')
        self.picture = pygame.transform.scale(self.picture, (self.width, self.height))

    def set_sound(self):
        self.sound = pygame.mixer.Sound('voices/jumping.wav')

    def jump(self):
        self.sound.play()
        self.jumping = True
        self.on_ground = False

    def fall(self):
        self.jumping = False
        self.falling = True

    def stop(self):
        self.falling = False
        self.on_ground = True


class Cone:
    """set cone
       parameter: x (coordinate for cone)
       attributes: width, height (dimensions for cone)
                   x, y (coordinate for cone)
       methods: set_picture() -- adding pic to canvas
                show() -- showing cone on the canvas
    """
    def __init__(self, x):
        self.width = 37
        self.height = 40
        self.x = x
        self.y = 208
        self.set_picture()
        self.show()

    def update(self, dx):  # dx is velocity
        self.x += dx

    def show(self):
        canvas.blit(self.picture, (self.x, self.y))

    def set_picture(self):
        self.picture = pygame.image.load('pics/cone.png')
        self.picture = pygame.transform.scale(self.picture, (self.width, self.height))


class Collision:
    """set collision
       if distance is less than a certain value, game is over
    """
    def between(self, obj1, obj2):
        distance = math.sqrt((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2)
        return distance < 70


class Game:
    """set game
       parameter: self
       attributes: bg (type:list, make an infinite scrolling background)
                   dino (type: class dinosaur)
                   cone_lst(make a random infinite cone list)

       methods: set_sound() -- set jump sound
                set_fonts() -- set contents when game over
                add_cone() -- add random infinite cones
    """
    def __init__(self):
        self.bg = [Background(0), Background(900)]
        self.dino = Dinosaur()
        self.cone_lst = []
        self.collision = Collision()
        self.speed = 4
        self.playing = False
        self.big_lbl = ''
        self.small_lbl = ''
        self.set_sound()
        self.set_fonts()
        self.add_cone()

    def set_fonts(self):
        big_font = pygame.font.SysFont('comicsansms', 30, bold=True)
        small_font = pygame.font.SysFont('comicsansms', 24)
        self.big_lbl = big_font.render(f'G-A-M-E  O-V-E-R', 1, (255, 0, 0))
        self.small_lbl = small_font.render(f'press s to start again!', 1, (58, 117, 50))

    def set_sound(self):
        self.sound = pygame.mixer.Sound('voices/over.wav')

    def start(self):
        self.playing = True

    def over(self):
        self.sound.play()
        canvas.blit(self.big_lbl, (900 // 2 - self.big_lbl.get_width() // 2, 300 // 4))
        canvas.blit(self.small_lbl, (900 // 2 - self.small_lbl.get_width() // 2, 300 // 2))
        self.playing = False

    def change(self, loops):
        return loops % 100 == 0

    def add_cone(self):
        # list with cone
        if len(self.cone_lst) > 0:
            prev_cone = self.cone_lst[-1]
            x = random.randint(prev_cone.x + self.dino.width + 84, 900 + prev_cone.x + self.dino.width + 84)

        # empty list
        else:
            x = random.randint(900 + 100, 1100)

        # create the new cone
        cone = Cone(x)
        self.cone_lst.append(cone)

    def restart(self):
        self.__init__()


def main():
    # game objects & dino objects
    game = Game()
    dino = game.dino

    # variables
    clock = pygame.time.Clock()  # to control the moving speed
    loops = 0
    over = False

    # mainloop
    while True:
        if game.playing:
            loops += 1
            # --- Background ---
            for bg in game.bg:
                bg.update(-game.speed)
                bg.show()
            # --- dinosaur ---
            dino.update(loops)
            dino.show()
            # --- cone ---
            if game.change(loops):
                game.add_cone()

            for cone in game.cone_lst:
                cone.update(-game.speed)
                cone.show()
                # collision
                if game.collision.between(dino, cone):
                    over = True
            if over:
                game.over()
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # when we press "x" on the canvas, it will close the canvas
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # when we press "space" on the canvas, make dino jump
                    if not over:
                        if dino.on_ground:
                            dino.jump()

                        if not game.playing:
                            game.start()

                if event.key == pygame.K_s:  # when we press "s" restart game
                    game.restart()
                    dino = game.dino
                    loops = 0
                    over = False

        clock.tick(90)  # timer control the speed
        pygame.display.update()  # keep showing the canvas


main()
