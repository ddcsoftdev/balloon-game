import os
import sys
import pygame
import pygame.camera
from random import randint

SCREEN_WIDTH = 1020
SCREEN_HEIGHT = 900
Y_BOUND = 50
FRAMES = 80
CLOCK_OFFSET = 160


def get_rand_tile(string) -> int:
    num = 0
    if string == "w":
        num = randint(100, SCREEN_WIDTH - 100)
    else:
        num = randint(Y_BOUND + 100, SCREEN_HEIGHT - 100)
    return num


def put_balloons(d):
    placex = 25
    placey = 50
    for i in range(d):
        screen.blit(balloon, (placex, placey))
        placex += 50
        if placex >= SCREEN_WIDTH:
            placey += 50
            placex = 25


def take_picture():
    display = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], 0)
    snapshot = pygame.surface.Surface([SCREEN_WIDTH, SCREEN_HEIGHT], 0, display)
    pygame.camera.init()
    camlist = pygame.camera.list_cameras()
    if camlist:
        # initializing the cam variable with default camera
        cam = pygame.camera.Camera(camlist[1], (SCREEN_WIDTH, SCREEN_HEIGHT))

        # opening the camera
        cam.start()
        snapshot = cam.get_image(snapshot)
        screen.blit(snapshot, (0, 0))
        while True:
            snapshot = cam.get_image(snapshot)
            screen.blit(snapshot, (0, 0))
            text_surface = my_font.render("Press R to take picture", False, (255, 255, 255))
            screen.blit(text_surface, (0, 0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        pygame.image.save(snapshot, "images/player.jpg")
                        return


pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Balloon Game")

take_picture()

image = pygame.image.load("images/background.png").convert()
image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
tile = pygame.image.load("images/player.jpg").convert_alpha()
tile = pygame.transform.scale(tile, (100, 100))
cricket = pygame.image.load("images/cricket.png").convert_alpha()
cricket = pygame.transform.scale(cricket, (100, 100))
balloon = pygame.image.load("images/balloon.png").convert_alpha()
balloon = pygame.transform.scale(balloon, (50, 50))
screen.blit(image, (0, 0))

tile_x = 0
tile_y = Y_BOUND
cri_x = get_rand_tile("w")
cri_y = get_rand_tile("h")

score = 0
best_score = 0
if os.path.exists("save.game"):
    f = open("save.game", "r")
    best_score = int(f.readline())

screen.blit(tile, (tile_x, tile_y))

pygame.display.flip()
put_balloon = False
num_balloon = 0
seed = 0
frame = 0
time_remaining = 1000
while True:

    if time_remaining <= 0:
        if score > best_score:
            f = open("save.game", "w")
            f.write(str(score))
            f.close()
        sys.exit(0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                f = open("save.game", "w")
                f.write(str(0))
                f.close()
                best_score = 0
            elif event.key == pygame.K_ESCAPE:
                if score > best_score:
                    f = open("save.game", "w")
                    f.write(str(score))
                    f.close()
                sys.exit(0)
    is_pressed = False

    if frame > FRAMES:
        frame = 0
        if score <= 50:
            time_remaining -= 1
        else:
            time_remaining -= 5
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            tile_y -= 50
            is_pressed = True
        elif pressed[pygame.K_s]:
            tile_y += 50
            is_pressed = True
        elif pressed[pygame.K_a]:
            tile_x -= 50
            is_pressed = True
        elif pressed[pygame.K_d]:
            tile_x += 50
            is_pressed = True

    if is_pressed:
        if tile_x > SCREEN_WIDTH:
            tile_x = 0
        elif tile_x < 0:
            tile_x = SCREEN_WIDTH
        if tile_y > SCREEN_HEIGHT - Y_BOUND:
            tile_y = Y_BOUND
        elif tile_y < 0:
            tile_y = SCREEN_HEIGHT

        if tile_x in range(cri_x - 50, cri_x + 50) and tile_y in range(cri_y - 50, cri_y + 50):
            cri_x = get_rand_tile('w')
            cri_y = get_rand_tile('h')
            if seed == 0:
                img = "images/cricket2.png"
                seed = 1
            else:
                seed = 0
                score += 1
                time_remaining += 25
                if score > 0:
                    num_balloon += 1
                img = "images/cricket.png"
            cricket = pygame.image.load(img).convert_alpha()
            cricket = pygame.transform.scale(cricket, (100, 100))

    screen.blit(image, (0, 0))
    screen.blit(cricket, (cri_x, cri_y))
    screen.blit(tile, (tile_x, tile_y))
    put_balloons(num_balloon)
    text_surface = my_font.render(
        f"Score: {score}      |||  All Time Best: {best_score}      ||| Time Remaining: {time_remaining}", False,
        (255, 255, 255))
    screen.blit(text_surface, (0, 0))
    pygame.display.flip()
    frame += 1
