import pygame, sys
clock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Among Us')
WINDOW_SIZE = (1200,600)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((1200,600))

def change_size(image,width,height):
    new_image = pygame.transform.scale(pygame.image.load(image),(width,height))
    return new_image

student = pygame.image.load('student.png').convert() # This image is downloaded from the tutorial.
student.set_colorkey((255,255,255))
grass = change_size('grass.png',16,16)
ground = change_size('stone.png',16,16)
wall = change_size('wall.png',16,16)
instrument = change_size('music.png',16,16)
desk = change_size('desk.png',16,16)
car = change_size('car.png',16,16)
sculpture = change_size('art.png',16,16)
basketball = change_size('basketball.png',16,16)
labs = change_size('chem.png',16,16)
books = change_size('books.png',16,16)
computer = change_size('computer.png',16,16)
tree = change_size('tree.png',16,16)
globe = change_size('globe.png',16,16)
net = change_size('net.png',16,16)
toilet = change_size('toilet.png',16,16)
corridor = change_size('corridor.png',16,16)
court = change_size('court.png',16,16)
TILE_SIZE = grass.get_width()

moving_right = False
moving_left = False
moving_up = False
moving_down = False

def load_tss_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map
game_map = load_tss_map('tss')

def collision_test(rect, tiles):
   hit_list = []
   for tile in tiles:
       if rect.colliderect(tile):
           hit_list.append(tile)
   return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

student_location = [200,100]
student_rect = pygame.Rect(student_location[0],student_location[1],student.get_width(),student.get_height())

player_y_momentum = 0
air_timer = 0

while True:
    display.fill((255,255,255))

    tile_rects = []

    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '0':
                display.blit(ground, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '3':
                display.blit(grass, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '2':
                display.blit(wall, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '4':
                display.blit(corridor, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '5':
                display.blit(tree, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '6':
                display.blit(desk, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '8':
                display.blit(court, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '9':
                display.blit(toilet, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == 'a':
                display.blit(computer, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == 'b':
                display.blit(basketball, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == 'c':
                display.blit(net, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == 'd':
                display.blit(car, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == 'e':
                display.blit(instrument, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == 'f':
                display.blit(globe, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == 'g':
                display.blit(sculpture, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == 'h':
                display.blit(books, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == 'p':
                display.blit(labs, (x * TILE_SIZE, y * TILE_SIZE))
            if tile != '0' or tile != '3' or tile != '4' or tile != '8':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3

    display.blit(student, (student_rect.x, student_rect.y))

    if moving_right == True:
        student_location[0] += 4
    if moving_left == True:
        student_location[0] -= 4
    if moving_up == True:
        student_location[1] -= 4
    if moving_down == True:
        student_location[1] += 4

    student_rect, collisions = move(student_rect, player_movement, tile_rects)
    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

    student_rect.x = student_location[0]  # update rect x
    student_rect.y = student_location[1]  # update rect y

    for event in pygame.event.get(): # event loop
        if event.type == QUIT: # check for window quit
            pygame.quit() # stop pygame
            sys.exit() # stop script
        if event.type == KEYDOWN:
            if event.key == K_d:
                moving_right = True
            if event.key == K_a:
                moving_left = True
            if event.key == K_w:
                moving_up = True
            if event.key == K_s:
                moving_down = True

        if event.type == KEYUP:
            if event.key == K_d:
                moving_right = False
            if event.key == K_a:
                moving_left = False
            if event.key == K_w:
                moving_up = False
            if event.key == K_s:
                moving_down = False

    surf = pygame.transform.scale(display,WINDOW_SIZE)
    screen.blit(surf,(0,0))
    pygame.display.update()
    clock.tick(60)