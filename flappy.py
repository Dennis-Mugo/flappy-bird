import pygame
import random
pygame.init()
pygame.font.init()
width = 900
height = 450

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')

#load images
bg = pygame.image.load('images/background4.jpg')
bg = pygame.transform.scale(bg, (width, height))

#pipe image
pipe_img = pygame.image.load('images/pipe8.png').convert()
pipe_img = pygame.transform.scale(pipe_img, (width//10, height//10*9))

#bird image
bird_img = pygame.image.load('images/bird4.png')
bird_img = pygame.transform.scale(bird_img, (60,50))

#game variables
fps = 100000
blue = (0, 0, 255)
white = (255, 255, 255)
green = (0, 255, 0)
run = True
game_on = False
score = 0
font = pygame.font.SysFont('comicsans', 50)

def reset():
    global score, fossa, pipe_list, screen_list
    score = 0
    fossa = Player(30, 30, width, height)
    pipe_list = []
    screen_list = [[0, 0], [width, 0]]

class Player():
    def __init__(self, width, height, screen_width, screen_height):
        self.reset(width, height, screen_width, screen_height)

    def reset(self, width, height, screen_width, screen_height):
        self.x = screen_width//2 - width//2
        self.y = screen_height//2 - height//2
        self.screen_height = screen_height
        self.width = width
        self.height = height
        self.isJump = False
        self.vel_y = 13


    def draw(self):
        self.body = pygame.Rect(self.x, self.y, self.width, self.height)
        self.body = bird_img.get_rect()
        self.body.topleft = (self.x, self.y)
        screen.blit(bird_img, self.body)

    def move(self):
        if self.y < self.screen_height - self.height:
            self.y += 3

    def jump(self):
        if self.y >= 0:
            if self.vel_y <= 13 and self.vel_y > 0:
                self.y -= self.vel_y
                self.vel_y -= 1
            else:
                self.isJump = False
                self.vel_y = 13
        else:
            self.isJump = False

    def check_death(self, run, obstacles):
        global game_on
        for obstacle in obstacles:
            if bird.body.colliderect(obstacle) or bird.body.colliderect(
                pygame.Rect(
                    obstacle.x,
                    obstacle.y-height*1.25,
                    obstacle.width,
                    obstacle.height
                )):
                    display_text('Game Over', width//2-50, height//2)
                    display_text(str(score), width*0.95, height*0.05)
                    pygame.display.update()
                    pygame.time.wait(2000)
                    game_on = False
                    self.reset(30, 30, width, height)
                    manager.pipe_list = []


class Obstacle_manager():
    def __init__(self):
        self.pipe_list = []

    def generate_obstacles(self):
        can_gen = True
        for pipe in self.pipe_list:
            if pipe.x > 0.75 * width:
                can_gen = False
        if can_gen:
            rand = random.randint(0, height//2)
            self.rect = pipe_img.get_rect()
            self.rect.topleft = width, height * 4//10 + rand
            self.pipe_list.append(self.rect)

    def scroll_screen(self):
        for pipe in self.pipe_list:
            pipe.x -= 2.25

def display_text(text, x, y):
    text = font.render(text, 1, blue)
    screen.blit(text, (x, y))


def update_screen():
    global height, score, run
    screen.fill(white)
    screen.blit(bg, (screen_list[0][0], screen_list[0][1]))
    screen.blit(bg, (screen_list[1][0], screen_list[1][1]))

    if game_on:
        for pos in screen_list:
            pos[0] -= 3

    if screen_list[1][0] + width <= width:
        screen_list.remove(screen_list[0])
        new_pos = [screen_list[0][0]+width, 0]
        screen_list.append(new_pos)


    if game_on == False:
        display_text('Press the space bar to play', width//4, height*0.005)

    if bird.isJump:
        bird.jump()
    elif not bird.isJump and game_on == True:
        bird.move()

    bird.draw()

    #genarate obstacles and begin to scroll
    manager.generate_obstacles()
    if game_on:
        manager.scroll_screen()

    #draw pipes
    for pipe in manager.pipe_list:
        screen.blit(pipe_img, pipe)
        screen.blit(pipe_img, pygame.Rect(
                pipe.x,
                pipe.y-height*1.25,
                pipe.width,
                pipe.height
                )
            )

    bird.check_death(run, obstacles=manager.pipe_list)
    counter = 0
    for pipe in manager.pipe_list:
        if pipe.x + width*0.075 < bird.x:
            counter += 1
    score = counter
    display_text(str(score), width*0.95, height*0.05)


#objects
bird = Player(30, 30, width, height)
manager = Obstacle_manager()
pipe_list = []
screen_list = [[0, 0], [width, 0]]


while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_on = True
            bird.isJump = True

    update_screen()

    pygame.display.flip()

pygame.quit()
