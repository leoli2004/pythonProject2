import pygame, sys, time

clock = pygame.time.Clock()
from pygame.locals import *

pygame.init()
pygame.display.set_caption('Among Us')
WINDOW_SIZE = (1200, 600)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((400, 200))

grass_sound = pygame.mixer.Sound('grass_0.wav')
grass_sound.set_volume(0.3)
pygame.mixer.music.load('grass_0.wav')
pygame.mixer.music.play(-1)

def change_size(image, width, height):
   new_image = pygame.transform.scale(pygame.image.load(image), (width, height))
   return new_image


student = pygame.image.load('student.png').convert()  # This image is downloaded from the tutorial.
student.set_colorkey((255, 255, 255))
grass = change_size('grass.png', 16, 16)
ground = change_size('stone.png', 16, 16)
wall = change_size('wall.png', 16, 16)
instrument = change_size('music.png', 16, 16)
desk = change_size('desk.png', 16, 16)
car = change_size('car.png', 16, 16)
sculpture = change_size('art.png', 16, 16)
basketball = change_size('basketball.png', 16, 16)
labs = change_size('chem.png', 16, 16)
books = change_size('books.png', 16, 16)
computer = change_size('computer.png', 16, 16)
tree = change_size('tree.png', 16, 16)
globe = change_size('globe.png', 16, 16)
net = change_size('net.png', 16, 16)
toilet = change_size('toilet.png', 16, 16)
corridor = change_size('corridor.png', 16, 16)
court = change_size('court.png', 16, 16)
TILE_SIZE = grass.get_width()

moving_right = False
moving_left = False
moving_up = False
moving_down = False


def load_tss_map(path):
   f = open(path + '.txt', 'r')
   data = f.read()
   f.close()
   data = data.split('\n')
   game_map = []
   for row in data:
       game_map.append(list(row))
   return game_map


game_map = load_tss_map('tss')


def move():
   if moving_right:
       canMove = True
       temp_rect = pygame.Rect(student_rect.x + 2, student_rect.y, student_rect.width, student_rect.height)
       for i in tile_rects:
           if i[1] == '3' or i[1] == '0' or i[1] == '4' or i[1] == '8':
               continue
           if i[0].colliderect(temp_rect):
               canMove = False
               break
       if canMove and student_rect.x < 1595:
           student_rect.x += 2
   if moving_left:
       canMove = True
       temp_rect = pygame.Rect(student_rect.x - 2, student_rect.y, student_rect.width, student_rect.height)
       for i in tile_rects:
           if i[1] == '3' or i[1] == '0' or i[1] == '4' or i[1] == '8':
               continue
           if i[0].colliderect(temp_rect):
               canMove = False
               break
       if canMove and student_rect.x > 0:
           student_rect.x -= 2
   if moving_up:
       can_move = True
       temp_rect = pygame.Rect(student_rect.x, student_rect.y - 2, student_rect.width, student_rect.height)
       for i in tile_rects:
           if i[1] == '3' or i[1] == '0' or i[1] == '4' or i[1] == '8':
               continue
           if i[0].colliderect(temp_rect):
               can_move = False
               break
       if can_move and student_rect.y > 0:
           student_rect.y -= 2
   if moving_down:
       can_move = True
       temp_rect = pygame.Rect(student_rect.x, student_rect.y + 2, student_rect.width, student_rect.height)
       for i in tile_rects:
           if i[1] == '3' or i[1] == '0' or i[1] == '4' or i[1] == '8':
               continue
           if i[0].colliderect(temp_rect):
               can_move = False
               break
       if can_move and student_rect.y < 1490:
           student_rect.y += 2


student_location = [200, 100]
student_rect = pygame.Rect(student_location[0], student_location[1], student.get_width(), student.get_height())

scroll = [0,0]

while True:
   display.fill((255, 255, 255))

   scroll[0] += (student_rect.x - scroll[0] - 202)/20
   scroll[1] += (student_rect.y - scroll[1] - 106)/20

   tile_rects = []
   y = 0
   for row in game_map:
       x = 0
       for tile in row:
           if tile == '0':
               display.blit(ground, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
           if tile == '3':
               display.blit(grass, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
           if tile == '2':
               display.blit(wall, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
           if tile == '4':
               display.blit(corridor, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
           if tile == '5':
               display.blit(tree, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
           if tile == '6':
               display.blit(desk, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
           if tile == '8':
               display.blit(court, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
           if tile == '9':
               display.blit(toilet, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
           if tile == 'a':
               display.blit(computer, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
           if tile == 'b':
               display.blit(basketball, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
           if tile == 'c':
               display.blit(net, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
           if tile == 'd':
               display.blit(car, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
           if tile == 'e':
               display.blit(instrument, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
           if tile == 'f':
               display.blit(globe, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
           if tile == 'g':
               display.blit(sculpture, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
           if tile == 'h':
               display.blit(books, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
           if tile == 'p':
               display.blit(labs, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
           if tile != '0' or tile != '3' or tile != '4' or tile != '8':
               tile_rects.append((pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), tile))
           x += 1
       y += 1

   display.blit(student, (student_rect.x - scroll[0], student_rect.y - scroll[1]))

   for event in pygame.event.get():  # event loop
       if event.type == QUIT:  # check for window quit
           pygame.quit()  # stop pygame
           sys.exit()  # stop script
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
   move()

   surf = pygame.transform.scale(display, WINDOW_SIZE)
   screen.blit(surf, (0, 0))
   pygame.display.update()
   clock.tick(60)