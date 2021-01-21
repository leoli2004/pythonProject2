import pygame, sys, os

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init() # initiates pygame

pygame.display.set_caption('Pygame Platformer')

WINDOW_SIZE = (600,400)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

display = pygame.Surface((300,200)) # used as the surface for rendering, which is scaled

moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0

true_scroll = [0,0]

def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

global animation_frames
animation_frames = {}

def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        # player_animations/idle/idle_0.png
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((255,255,255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame
        

animation_database = {}

animation_database['run'] = load_animation('player_animations/run',[7,7])
animation_database['idle'] = load_animation('player_animations/idle',[7,7,40])

game_map = load_map('map')

grass_img = pygame.image.load('grass.png')
dirt_img = pygame.image.load('dirt.png')

player_action = 'idle'
player_frame = 0
player_flip = False

player_rect = pygame.Rect(100,100,5,13)

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

while True: # game loop
    display.fill((146,244,255)) # clear screen by filling it with blue

    true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20
    true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(display,(7,80,75),pygame.Rect(0,120,300,80))
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display,(14,222,150),obj_rect)
        else:
            pygame.draw.rect(display,(9,91,85),obj_rect)

    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(dirt_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '2':
                display.blit(grass_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x*16,y*16,16,16))
            x += 1
        y += 1

    player_movement = [0,0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3

    if player_movement[0] == 0:
        player_action,player_frame = change_action(player_action,player_frame,'idle')
    if player_movement[0] > 0:
        player_flip = False
        player_action,player_frame = change_action(player_action,player_frame,'run')
    if player_movement[0] < 0:
        player_flip = True
        player_action,player_frame = change_action(player_action,player_frame,'run')

    player_rect,collisions = move(player_rect,player_movement,tile_rects)

    if collisions['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
    else:
        air_timer += 1

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img,player_flip,False),(player_rect.x-scroll[0],player_rect.y-scroll[1]))


    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    vertical_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
        
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(60)


def gym_task():
   """fgdsssssssggggggggggggggggdgdfsssgggggfffffffffffffffffffffffffffffffffffffffffffffffffffff
   Preconditions: NA
   :parameter: NA
   :return: NA
   """
   global colliding
   global current_time
   global start
   global answer
   global end
   if student_rect.colliderect(gym) and not colliding:  # check collision
       current_time = pygame.time.get_ticks()  # get the game running time
       colliding = True
   if pygame.time.get_ticks() < current_time + 5000 and colliding:  # check whether the time has passed 5 seconds or not
       ## print "press f to start task" for five seconds
       text = pygame.font.SysFont("Microsoft Yahei UI Light", 60).render('press f to start task', True, (0, 0, 0))
       screen.blit(text, (int((WINDOW_SIZE[0] - text.get_width()) / 2), int((WINDOW_SIZE[1] - text.get_height()) / 2)))
   if not student_rect.colliderect(gym):  # make colliding be False again when the player is not in gym
       colliding = False
   if start == True and colliding:
       if pygame.time.get_ticks() > current_time + 5000 and pygame.time.get_ticks() < current_time + 10000 and colliding:
           text = pygame.font.SysFont("Microsoft Yahei UI Light", 35).render('Mr. MacNeil: Welcome to gym class, I am your coach Mr. MacNeil. I prepared a quiz for you, good luck!', True, (255, 255, 255))
           screen.blit(text, (int((WINDOW_SIZE[0] - text.get_width()) / 2), int((WINDOW_SIZE[1] - text.get_height()) / 2)))
       if pygame.time.get_ticks() > current_time + 10000 and pygame.time.get_ticks() < current_time + 13000 and colliding:
           text = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render('Mr. MacNeil: What is Toronto Maple Leafs?', True, (255, 255, 255))
           screen.blit(text, (int((WINDOW_SIZE[0] - text.get_width()) / 2), int((WINDOW_SIZE[1] - text.get_height()) / 2)))
       if pygame.time.get_ticks() > current_time + 13000 and pygame.time.get_ticks() < current_time + 18000 and colliding:
           text = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render('1. A kind of maple leaf 2. An ice hockey team 3. A basketball team', True, (255, 255, 255))
           screen.blit(text, (int((WINDOW_SIZE[0] - text.get_width()) / 2), int((WINDOW_SIZE[1] - text.get_height()) / 2)))
       if answer == "1":
           if pygame.time.get_ticks() > current_time + 18000 and pygame.time.get_ticks() < current_time + 20000 and colliding:
               text = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render('Mr. MacNeil: That is wrong! You lose!', True, (255, 255, 255))
               screen.blit(text, (int((WINDOW_SIZE[0] - text.get_width()) / 2), int((WINDOW_SIZE[1] - text.get_height()) / 2)))
               pygame.mixer.music.fadeout(500)
               end = True
           if pygame.time.get_ticks() > current_time + 20000 and pygame.time.get_ticks() < current_time + 22500 and colliding:
               screen.blit(scream1, (198, 0))
               screaming_sound.play()
           if pygame.time.get_ticks() > current_time + 23000 and pygame.time.get_ticks() < current_time + 25000 and colliding:
               pygame.quit()
               sys.exit()
       if answer == "2":
           if pygame.time.get_ticks() > current_time + 18000 and pygame.time.get_ticks() < current_time + 20000 and colliding:
               text = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render('Mr. MacNeil: That is correct!', True, (255, 255, 255))
               screen.blit(text, (int((WINDOW_SIZE[0] - text.get_width()) / 2), int((WINDOW_SIZE[1] - text.get_height()) / 2)))
       if answer == "3":
           if pygame.time.get_ticks() > current_time + 18000 and pygame.time.get_ticks() < current_time + 20000 and colliding:
               text = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render('Mr. MacNeil: That is wrong! You lose!', True, (255, 255, 255))
               screen.blit(text, (int((WINDOW_SIZE[0] - text.get_width()) / 2), int((WINDOW_SIZE[1] - text.get_height()) / 2)))
               pygame.mixer.music.fadeout(500)
               end = True
           if pygame.time.get_ticks() > current_time + 20000 and pygame.time.get_ticks() < current_time + 22500 and colliding:
               screen.blit(scream1, (198, 0))
               screaming_sound.play()
           if pygame.time.get_ticks() > current_time + 25000 and colliding:
               pygame.quit()
               sys.exit()
       if pygame.time.get_ticks() > current_time + 20000 and pygame.time.get_ticks() < current_time + 23000 and colliding and not end:
           text = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render('Mr. MacNeil: Where is deltoid located?', True, (255, 255, 255))
           screen.blit(text, (int((WINDOW_SIZE[0] - text.get_width()) / 2), int((WINDOW_SIZE[1] - text.get_height()) / 2)))
       if pygame.time.get_ticks() > current_time + 23000 and pygame.time.get_ticks() < current_time + 28000 and colliding:
           text = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render('4. Shoulders 5. Legs 6. Arms', True, (255, 255, 255))
           screen.blit(text, (int((WINDOW_SIZE[0] - text.get_width()) / 2), int((WINDOW_SIZE[1] - text.get_height()) / 2)))
       if answer == "4":
           if pygame.time.get_ticks() > current_time + 28000 and pygame.time.get_ticks() < current_time + 30000 and colliding:
               correct_answer = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render('Mr. MacNeil: That is correct!', True, (255, 255, 255))
               screen.blit(correct_answer, (int((WINDOW_SIZE[0] - correct_answer.get_width()) / 2), int((WINDOW_SIZE[1] - correct_answer.get_height()) / 2)))
       if answer == "5":
           if pygame.time.get_ticks() > current_time + 28000 and pygame.time.get_ticks() < current_time + 30000 and colliding:
               text = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render('Mr. MacNeil: That is wrong! You lose!', True, (255, 255, 255))
               screen.blit(text, (int((WINDOW_SIZE[0] - text.get_width()) / 2), int((WINDOW_SIZE[1] - text.get_height()) / 2)))
               pygame.mixer.music.fadeout(500)
               end = True
           if pygame.time.get_ticks() > current_time + 30000 and pygame.time.get_ticks() < current_time + 32500 and colliding:
               screen.blit(scream1, (198, 0))
               screaming_sound.play()
           if pygame.time.get_ticks() > current_time + 35000 and colliding:
               pygame.quit()
               sys.exit()
       if answer == "6":
           if pygame.time.get_ticks() > current_time + 28000 and pygame.time.get_ticks() < current_time + 30000 and colliding:
               text = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render('Mr. MacNeil: That is wrong! You lose!', True, (255, 255, 255))
               screen.blit(text, (int((WINDOW_SIZE[0] - text.get_width()) / 2), int((WINDOW_SIZE[1] - text.get_height()) / 2)))
               pygame.mixer.music.fadeout(500)
               end = True
           if pygame.time.get_ticks() > current_time + 30000 and pygame.time.get_ticks() < current_time + 32500 and colliding:
               screen.blit(scream1, (198, 0))
               screaming_sound.play()
           if pygame.time.get_ticks() > current_time + 35000 and colliding:
               pygame.quit()
               sys.exit()
       if pygame.time.get_ticks() > current_time + 30000 and pygame.time.get_ticks() < current_time + 33000 and colliding and not end:
           text = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render('Mr. MacNeil: How many players are there for each soccer team in a game?', True, (255, 255, 255))
           screen.blit(text, (int((WINDOW_SIZE[0] - text.get_width()) / 2), int((WINDOW_SIZE[1] - text.get_height()) / 2)))
       if pygame.time.get_ticks() > current_time + 33000 and pygame.time.get_ticks() < current_time + 38000 and colliding:
           text = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render('7. 10 players 8. 11 players 9. 12 players', True, (255, 255, 255))
           screen.blit(text, (int((WINDOW_SIZE[0] - text.get_width()) / 2), int((WINDOW_SIZE[1] - text.get_height()) / 2)))
       if answer == "7":
           if pygame.time.get_ticks() > current_time + 38000 and pygame.time.get_ticks() < current_time + 40000 and colliding:
               text = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render('Mr. MacNeil: That is wrong! You lose!', True, (255, 255, 255))
               screen.blit(text, (int((WINDOW_SIZE[0] - text.get_width()) / 2), int((WINDOW_SIZE[1] - text.get_height()) / 2)))
               pygame.mixer.music.fadeout(500)
               end = True
           if pygame.time.get_ticks() > current_time + 40000 and pygame.time.get_ticks() < current_time + 42500 and colliding:
               screen.blit(scream1, (198, 0))
               screaming_sound.play()
           if pygame.time.get_ticks() > current_time + 45000 and colliding:
               pygame.quit()
               sys.exit()
       if answer == "8":
           if pygame.time.get_ticks() > current_time + 38000 and pygame.time.get_ticks() < current_time + 40000 and colliding:
               correct_answer = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render('Mr. MacNeil: That is correct! You completed your quiz!', True, (255, 255, 255))
               screen.blit(correct_answer, (int((WINDOW_SIZE[0] - correct_answer.get_width()) / 2), int((WINDOW_SIZE[1] - correct_answer.get_height()) / 2)))
       if answer == "9":
           if pygame.time.get_ticks() > current_time + 38000 and pygame.time.get_ticks() < current_time + 40000 and colliding:
               text = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render('Mr. MacNeil: That is wrong! You lose!', True, (255, 255, 255))
               screen.blit(text, (int((WINDOW_SIZE[0] - text.get_width()) / 2), int((WINDOW_SIZE[1] - text.get_height()) / 2)))
               pygame.mixer.music.fadeout(500)
               end = True
           if pygame.time.get_ticks() > current_time + 40000 and pygame.time.get_ticks() < current_time + 42500 and colliding:
               screen.blit(scream1, (198, 0))
               screaming_sound.play()
           if pygame.time.get_ticks() > current_time + 45000 and colliding:
               pygame.quit()
               sys.exit()
def library_task():


def male_washroom1_check():
def male_washroom2_check():
def female_washroom1_check():
def female_washroom2_check():
def male_changing_room_check():
def female_changing_room1_check():
def female_changing_room2_check():
def main_office_check():
def office_check():