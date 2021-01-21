import pygame, sys  # same as turtle graphic, we have to import pygame and system library
from pygame.locals import *  # import all pygame modules
clock = pygame.time.Clock()  # set up the clock

pygame.init()  # initialize pygame
pygame.display.set_caption("Among Us")  # name the window to "Among Us"
WINDOW_SIZE = (1200, 600)  # set up the window size to 1200 pixels width and 600 pixels height
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initialize the window for display
display = pygame.Surface((400, 200))  # zoom the surface three times so it's easy for people to see what's going on

student_name = ''

pygame.mixer.music.load('background_music.wav')  # load the background music
pygame.mixer.music.play(-1)  # play the music for infinite times
screaming_sound = pygame.mixer.Sound('screaming_sound.wav')  # load the sound effect

def change_dimensions(image, width, height):
    """Changes an image's dimensions

       Preconditions:
       image: string (the path of image + .png)
       width: int with value > 0
       height: int with value > 0

       :param image: the path of image
       :param width: the width of image you want to change to
       :param height: the height of image you want to change to
       :return: an new image with width and height inputted
    """
    new_image = pygame.transform.scale(pygame.image.load(image), (width, height))  # change the image's width and height
    return new_image


student = pygame.image.load('student.png').convert()  # This image is downloaded from the tutorial, load the image
student.set_colorkey((255, 255, 255))  # make colour white in this image transparent
scream = pygame.image.load('scream.png')
scream1 = pygame.transform.scale(pygame.image.load('scream.png'), (803, 600))

## load all images needed for this game
grass = change_dimensions('grass.png', 16, 16)
ground = change_dimensions('stone.png', 16, 16)
wall = change_dimensions('wall.png', 16, 16)
instrument = change_dimensions('music.png', 16, 16)
desk = change_dimensions('desk.png', 16, 16)
car = change_dimensions('car.png', 16, 16)
sculpture = change_dimensions('art.png', 16, 16)
basketball = change_dimensions('basketball.png', 16, 16)
labs = change_dimensions('chem.png', 16, 16)
books = change_dimensions('books.png', 16, 16)
computer = change_dimensions('computer.png', 16, 16)
tree = change_dimensions('tree.png', 16, 16)
globe = change_dimensions('globe.png', 16, 16)
net = change_dimensions('net.png', 16, 16)
toilet = change_dimensions('toilet.png', 16, 16)
corridor = change_dimensions('corridor.png', 16, 16)
court = change_dimensions('court.png', 16, 16)

TILE_SIZE = grass.get_width()  # the size of each tile, since width == height in this case, I only need to write it once


def load_tss_map(path):
    """Reads the map that I have wrote in notepad

    Preconditions:
    path: string (the file name)

    :param path: the path of tss map
    :return: the game map
    """
    file = open(path + '.txt', 'r')  # open the file
    data = file.read()  # set data to the content of file
    file.close()  # close the file
    data = data.split('\n')  # spilt the data
    game_map = []  # create a new list
    for row in data:
        game_map.append(list(row))  # turn strings to lists
    return game_map


game_map = load_tss_map('tss')  # load the tss map


def create_rect(x_coordinate1, y_coordinate1, x_coordinate2, y_coordinate2):
    """Create rectangles based on each room's top left corner's x and y coordinates and bottom right
    corner's x and y coordinates
    Preconditions:
    x_coordinate1: int with value >= 0
    y_coordinate1: int with value >= 0
    x_coordinate2: int with value > 0
    y_coordinate2: int with value > 0
    :param x_coordinate1: the value of x coordinate of the top left corner
    :param y_coordinate1: the value of y coordinate of the top left corner
    :param x_coordinate2: the value of x coordinate of the bottom right corner
    :param y_coordinate1: the value of x coordinate of the bottom right corner
    :return: a rectangle based on the value inputted
    """
    return pygame.Rect(((x_coordinate1 - 1) * 16), ((y_coordinate1 - 1) * 16), (x_coordinate2 * 16 - x_coordinate1 * 16), (y_coordinate2 * 16 - (y_coordinate1 - 1) * 16))  # create a rectangle


## create a rectangle for each room, the purpose of this is to test collision
gym = create_rect(2, 73, 25, 89)
computer_science = create_rect(2, 38, 10, 53)
english = create_rect(43, 38, 51, 53)
auto = create_rect(2, 21, 10, 36)
music = create_rect(2, 13, 23, 19)
math = create_rect(54, 2, 97, 9)
physics = create_rect(57, 17, 85, 22)
chemistry = create_rect(86, 17, 100, 31)
biology = create_rect(57, 29, 85, 31)
geography = create_rect(57, 38, 65, 53)
history = create_rect(57, 55, 65, 71)
art = create_rect(42, 78, 65, 89)
library = create_rect(16, 29, 33, 36)
male_washroom1 = create_rect(43, 29, 51, 36)
male_washroom2 = create_rect(43, 55, 51, 62)
female_washroom1 = create_rect(34, 29, 42, 36)
female_washroom2 = create_rect(43, 64, 51, 71)
male_changing_room = create_rect(6, 64, 10, 71)
female_changing_room1 = create_rect(2, 55, 10, 62)
female_changing_room2 = create_rect(2, 63, 5, 71)
stage = create_rect(26, 73, 31, 89)
cafeteria = create_rect(16, 38, 28, 66)
main_office = create_rect(37, 68, 42, 71)
quadrangle = create_rect(29, 38, 42, 66)
office = create_rect(29, 19, 56, 22)


def test_collision():
    """Test collision to see if the player enters a specific room, if so, print the corresponding room name on screen
    Preconditions: NA
    :parameter: NA
    :return: NA
    """
    room = [gym, stage, math, english, computer_science, auto, music, physics, chemistry, biology, geography, history, art, library, male_washroom1, male_washroom2, female_washroom1, female_washroom2, male_changing_room, female_changing_room1, female_changing_room2, cafeteria, main_office, quadrangle, office]  # a list of variables for each room
    room_name = ['gym', 'stage', 'math classroom', 'english classroom', 'computer science classroom', 'auto body shop', 'music classroom', 'physics classroom', 'chemistry classroom', 'biology classroom', 'geography classroom', 'history classroom', 'art classroom', 'library', 'male washroom', 'male washroom', 'female washroom', 'female washroom', 'male changing room', 'female changing room', 'female changing room', 'cafeteria', 'main office', 'quadrangle', 'teachers office']  # a list of all rooms' name
    check = 0  # set the initial value for check
    while check <= 24:
        if student_rect.colliderect(room[check]):  # collision check
            location = pygame.font.SysFont("Microsoft Yahei UI Light", 60).render(room_name[check], True, (255, 255, 255))  # set the font and size of the text, and then set the content and colour of the text
            screen.blit(location, (int((WINDOW_SIZE[0] - location.get_width()) / 2), int((WINDOW_SIZE[1] - location.get_height()) / 2 + 270)))  # print the text on screen, and set the location of the text
        check += 1


colliding = False  # set the initial value of colliding
current_time = 0  # set the initial value of time
start = False  # set the initial value of start
answer = False  # set the initial value of answer
end = False  # set the initial value of end


def start_task(room_name):
    global colliding
    global current_time

    if student_rect.colliderect(room_name) and not colliding:  # check collision
        current_time = pygame.time.get_ticks()  # get the game running time
        colliding = True
    if pygame.time.get_ticks() < current_time + 5000 and colliding:  # check whether the time has passed 5 seconds or not
        ## print "press f to start task" for five seconds
        text = pygame.font.SysFont("Microsoft Yahei UI Light", 60).render('press f to start task', True, (0, 0, 0))
        screen.blit(text, (int((WINDOW_SIZE[0] - text.get_width()) / 2), int((WINDOW_SIZE[1] - text.get_height()) / 2)))
    if not student_rect.colliderect(room_name):  # make colliding be False again when the player is not in gym
        colliding = False


def introduce(introduction, time1, time2):
    global colliding
    global current_time
    global start
    if start and colliding:
        if pygame.time.get_ticks() > current_time + time1 and pygame.time.get_ticks() < current_time + time2 and colliding:
            text = pygame.font.SysFont("Microsoft Yahei UI Light", 35).render(introduction, True, (255, 255, 255))
            screen.blit(text, (int((WINDOW_SIZE[0] - text.get_width()) / 2), int((WINDOW_SIZE[1] - text.get_height()) / 2)))


def text1(question, choices, time1, time2, time3):
    global colliding
    global current_time
    global start
    global end
    if start and colliding and not end:
        if pygame.time.get_ticks() > current_time + time1 and pygame.time.get_ticks() < current_time + time2 and colliding:
            text = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render(question, True, (255, 255, 255))
            screen.blit(text, (int((WINDOW_SIZE[0] - text.get_width()) / 2), int((WINDOW_SIZE[1] - text.get_height()) / 2)))
        if pygame.time.get_ticks() > current_time + time2 and pygame.time.get_ticks() < current_time + time3 and colliding:
            text = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render(choices, True, (255, 255, 255))
            screen.blit(text, (int((WINDOW_SIZE[0] - text.get_width()) / 2), int((WINDOW_SIZE[1] - text.get_height()) / 2)))


def wrong_answer(reply, number, time1, time2, time3, time4):
    global colliding
    global current_time
    global start
    global answer
    global end
    if start and colliding:
        if answer == number:
            if pygame.time.get_ticks() > current_time + time1 and pygame.time.get_ticks() < current_time + time2 and colliding:
                text = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render(reply, True, (255, 255, 255))
                screen.blit(text, (int((WINDOW_SIZE[0] - text.get_width()) / 2), int((WINDOW_SIZE[1] - text.get_height()) / 2)))
                pygame.mixer.music.fadeout(500)
                end = True
            if pygame.time.get_ticks() > current_time + time2 and pygame.time.get_ticks() < current_time + time3 and colliding:
                screen.blit(scream1, (198, 0))
                screaming_sound.play()
            if pygame.time.get_ticks() > current_time + time4 and colliding:
                pygame.quit()
                sys.exit()


def correct_answer(reply, number, time1, time2):
    global colliding
    global current_time
    global start
    global answer
    global end
    if start and colliding:
        if answer == number:
            if pygame.time.get_ticks() > current_time + time1 and pygame.time.get_ticks() < current_time + time2 and colliding:
                text = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render(reply, True, (255, 255, 255))
                screen.blit(text, (int((WINDOW_SIZE[0] - text.get_width()) / 2), int((WINDOW_SIZE[1] - text.get_height()) / 2)))


def no_answer(reply, time1, time2, time3, time4, number1, number2, number3):
    global colliding
    global current_time
    global start
    global answer
    global end
    if start and colliding:
        if answer != number1 and answer != number2 and answer != number3 and pygame.time.get_ticks() > current_time + time1:
            if pygame.time.get_ticks() > current_time + time1 and pygame.time.get_ticks() < current_time + time2 and colliding:
                text = pygame.font.SysFont("Microsoft Yahei UI Light", 50).render(reply, True, (255, 255, 255))
                screen.blit(text, (int((WINDOW_SIZE[0] - text.get_width()) / 2), int((WINDOW_SIZE[1] - text.get_height()) / 2)))
                pygame.mixer.music.fadeout(500)
                end = True
            if pygame.time.get_ticks() > current_time + time2 and pygame.time.get_ticks() < current_time + time3 and colliding:
                screen.blit(scream1, (198, 0))
                screaming_sound.play()
            if pygame.time.get_ticks() > current_time + time4 and colliding:
                pygame.quit()
                sys.exit()


def gym_task():
    """fgdsssssssggggggggggggggggdgdfsssgggggfffffffffffffffffffffffffffffffffffffffffffffffffffff
    Preconditions: NA
    :parameter: NA
    :return: NA
    """

    start_task(gym)
    introduce('Mr. MacNeil: Welcome to gym class, I am your coach Mr. MacNeil. I prepared a quiz for you, good luck!', 5000, 10000)
    text1('Mr. MacNeil: What is Toronto Maple Leafs?', '1. A kind of maple leaf 2. An ice hockey team 3. A basketball team', 10000, 13000, 18000)
    wrong_answer('Mr. MacNeil: ??? Are you kidding me? You lose!', "1", 18000, 20000, 22500, 25000)
    correct_answer("Mr. MacNeil: That's correct!", "2", 18000, 20000)
    wrong_answer('Mr. MacNeil: That is wrong! You lose!', "3", 18000, 20000, 22500, 25000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 18000, 20000, 22500, 25000, '1', '2', '3')
    ## Second Question
    text1('Mr. MacNeil: Where is deltoid located?', '4. Shoulders 5. Legs 6. Arms', 20000, 23000, 28000)
    correct_answer("Mr. MacNeil: That's correct!", "4", 28000, 30000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "5", 28000, 30000, 32500, 35000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "6", 28000, 30000, 32500, 35000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 28000, 30000, 32500, 35000, '4', '5', '6')
    ## Third Question
    text1('Mr. MacNeil: How many players are there for each soccer team in a game?', '7. 10 players 8. 11 players 9. 12 players', 30000, 33000, 38000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "7", 38000, 40000, 42500, 45000)
    correct_answer("Mr. MacNeil: That's correct! You completed your quiz!", "8", 38000, 40000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "9", 38000, 40000, 42500, 45000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 38000, 40000, 42500, 45000, '7', '8', '9')


def computer_science_task():
    start_task(computer_science)
    introduce('Mr. Benum: Good morning, how are you doing today? I am your computer science teacher Mr. Benum.', 5000, 8000)
    introduce("Mr. Benum: Here's a computer basic quiz for you.", 8000, 10000)
    text1('Mr. MacNeil: What is Toronto Maple Leafs?', '1. A kind of maple leaf 2. An ice hockey team 3. A basketball team', 10000, 13000, 18000)
    wrong_answer('Mr. MacNeil: ??? Are you kidding me? You lose!', "1", 18000, 20000, 22500, 25000)
    correct_answer("Mr. MacNeil: That's correct!", "2", 18000, 20000)
    wrong_answer('Mr. MacNeil: That is wrong! You lose!', "3", 18000, 20000, 22500, 25000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 18000, 20000, 22500, 25000, '1', '2', '3')
    ## Second Question
    text1('Mr. MacNeil: Where is deltoid located?', '4. Shoulders 5. Legs 6. Arms', 20000, 23000, 28000)
    correct_answer("Mr. MacNeil: That's correct!", "4", 28000, 30000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "5", 28000, 30000, 32500, 35000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "6", 28000, 30000, 32500, 35000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 28000, 30000, 32500, 35000, '4', '5', '6')
    ## Third Question
    text1('Mr. MacNeil: How many players are there for each soccer team in a game?', '7. 10 players 8. 11 players 9. 12 players', 30000, 33000, 38000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "7", 38000, 40000, 42500, 45000)
    correct_answer("Mr. MacNeil: That's correct! You completed your quiz!", "8", 38000, 40000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "9", 38000, 40000, 42500, 45000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 38000, 40000, 42500, 45000, '7', '8', '9')

def english_task():
    start_task(computer_science)
    introduce('Mr. MacNeil: Welcome to gym class, I am your coach Mr. MacNeil. I prepared a quiz for you, good luck!', 5000, 10000)
    text1('Mr. MacNeil: What is Toronto Maple Leafs?', '1. A kind of maple leaf 2. An ice hockey team 3. A basketball team', 10000, 13000, 18000)
    wrong_answer('Mr. MacNeil: ??? Are you kidding me? You lose!', "1", 18000, 20000, 22500, 25000)
    correct_answer("Mr. MacNeil: That's correct!", "2", 18000, 20000)
    wrong_answer('Mr. MacNeil: That is wrong! You lose!', "3", 18000, 20000, 22500, 25000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 18000, 20000, 22500, 25000, '1', '2', '3')
    ## Second Question
    text1('Mr. MacNeil: Where is deltoid located?', '4. Shoulders 5. Legs 6. Arms', 20000, 23000, 28000)
    correct_answer("Mr. MacNeil: That's correct!", "4", 28000, 30000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "5", 28000, 30000, 32500, 35000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "6", 28000, 30000, 32500, 35000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 28000, 30000, 32500, 35000, '4', '5', '6')
    ## Third Question
    text1('Mr. MacNeil: How many players are there for each soccer team in a game?', '7. 10 players 8. 11 players 9. 12 players', 30000, 33000, 38000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "7", 38000, 40000, 42500, 45000)
    correct_answer("Mr. MacNeil: That's correct! You completed your quiz!", "8", 38000, 40000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "9", 38000, 40000, 42500, 45000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 38000, 40000, 42500, 45000, '7', '8', '9')


def auto_task():
    start_task(computer_science)
    introduce('Mr. MacNeil: Welcome to gym class, I am your coach Mr. MacNeil. I prepared a quiz for you, good luck!', 5000, 10000)
    text1('Mr. MacNeil: What is Toronto Maple Leafs?', '1. A kind of maple leaf 2. An ice hockey team 3. A basketball team', 10000, 13000, 18000)
    wrong_answer('Mr. MacNeil: ??? Are you kidding me? You lose!', "1", 18000, 20000, 22500, 25000)
    correct_answer("Mr. MacNeil: That's correct!", "2", 18000, 20000)
    wrong_answer('Mr. MacNeil: That is wrong! You lose!', "3", 18000, 20000, 22500, 25000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 18000, 20000, 22500, 25000, '1', '2', '3')
    ## Second Question
    text1('Mr. MacNeil: Where is deltoid located?', '4. Shoulders 5. Legs 6. Arms', 20000, 23000, 28000)
    correct_answer("Mr. MacNeil: That's correct!", "4", 28000, 30000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "5", 28000, 30000, 32500, 35000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "6", 28000, 30000, 32500, 35000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 28000, 30000, 32500, 35000, '4', '5', '6')
    ## Third Question
    text1('Mr. MacNeil: How many players are there for each soccer team in a game?', '7. 10 players 8. 11 players 9. 12 players', 30000, 33000, 38000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "7", 38000, 40000, 42500, 45000)
    correct_answer("Mr. MacNeil: That's correct! You completed your quiz!", "8", 38000, 40000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "9", 38000, 40000, 42500, 45000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 38000, 40000, 42500, 45000, '7', '8', '9')


def music_task():
    start_task(computer_science)
    introduce('Mr. MacNeil: Welcome to gym class, I am your coach Mr. MacNeil. I prepared a quiz for you, good luck!', 5000, 10000)
    text1('Mr. MacNeil: What is Toronto Maple Leafs?', '1. A kind of maple leaf 2. An ice hockey team 3. A basketball team', 10000, 13000, 18000)
    wrong_answer('Mr. MacNeil: ??? Are you kidding me? You lose!', "1", 18000, 20000, 22500, 25000)
    correct_answer("Mr. MacNeil: That's correct!", "2", 18000, 20000)
    wrong_answer('Mr. MacNeil: That is wrong! You lose!', "3", 18000, 20000, 22500, 25000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 18000, 20000, 22500, 25000, '1', '2', '3')
    ## Second Question
    text1('Mr. MacNeil: Where is deltoid located?', '4. Shoulders 5. Legs 6. Arms', 20000, 23000, 28000)
    correct_answer("Mr. MacNeil: That's correct!", "4", 28000, 30000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "5", 28000, 30000, 32500, 35000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "6", 28000, 30000, 32500, 35000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 28000, 30000, 32500, 35000, '4', '5', '6')
    ## Third Question
    text1('Mr. MacNeil: How many players are there for each soccer team in a game?', '7. 10 players 8. 11 players 9. 12 players', 30000, 33000, 38000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "7", 38000, 40000, 42500, 45000)
    correct_answer("Mr. MacNeil: That's correct! You completed your quiz!", "8", 38000, 40000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "9", 38000, 40000, 42500, 45000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 38000, 40000, 42500, 45000, '7', '8', '9')


def math_task():
    start_task(computer_science)
    introduce('Mr. MacNeil: Welcome to gym class, I am your coach Mr. MacNeil. I prepared a quiz for you, good luck!', 5000, 10000)
    text1('Mr. MacNeil: What is Toronto Maple Leafs?', '1. A kind of maple leaf 2. An ice hockey team 3. A basketball team', 10000, 13000, 18000)
    wrong_answer('Mr. MacNeil: ??? Are you kidding me? You lose!', "1", 18000, 20000, 22500, 25000)
    correct_answer("Mr. MacNeil: That's correct!", "2", 18000, 20000)
    wrong_answer('Mr. MacNeil: That is wrong! You lose!', "3", 18000, 20000, 22500, 25000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 18000, 20000, 22500, 25000, '1', '2', '3')
    ## Second Question
    text1('Mr. MacNeil: Where is deltoid located?', '4. Shoulders 5. Legs 6. Arms', 20000, 23000, 28000)
    correct_answer("Mr. MacNeil: That's correct!", "4", 28000, 30000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "5", 28000, 30000, 32500, 35000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "6", 28000, 30000, 32500, 35000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 28000, 30000, 32500, 35000, '4', '5', '6')
    ## Third Question
    text1('Mr. MacNeil: How many players are there for each soccer team in a game?', '7. 10 players 8. 11 players 9. 12 players', 30000, 33000, 38000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "7", 38000, 40000, 42500, 45000)
    correct_answer("Mr. MacNeil: That's correct! You completed your quiz!", "8", 38000, 40000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "9", 38000, 40000, 42500, 45000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 38000, 40000, 42500, 45000, '7', '8', '9')


def physics_task():
    start_task(computer_science)
    introduce('Mr. MacNeil: Welcome to gym class, I am your coach Mr. MacNeil. I prepared a quiz for you, good luck!', 5000, 10000)
    text1('Mr. MacNeil: What is Toronto Maple Leafs?', '1. A kind of maple leaf 2. An ice hockey team 3. A basketball team', 10000, 13000, 18000)
    wrong_answer('Mr. MacNeil: ??? Are you kidding me? You lose!', "1", 18000, 20000, 22500, 25000)
    correct_answer("Mr. MacNeil: That's correct!", "2", 18000, 20000)
    wrong_answer('Mr. MacNeil: That is wrong! You lose!', "3", 18000, 20000, 22500, 25000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 18000, 20000, 22500, 25000, '1', '2', '3')
    ## Second Question
    text1('Mr. MacNeil: Where is deltoid located?', '4. Shoulders 5. Legs 6. Arms', 20000, 23000, 28000)
    correct_answer("Mr. MacNeil: That's correct!", "4", 28000, 30000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "5", 28000, 30000, 32500, 35000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "6", 28000, 30000, 32500, 35000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 28000, 30000, 32500, 35000, '4', '5', '6')
    ## Third Question
    text1('Mr. MacNeil: How many players are there for each soccer team in a game?', '7. 10 players 8. 11 players 9. 12 players', 30000, 33000, 38000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "7", 38000, 40000, 42500, 45000)
    correct_answer("Mr. MacNeil: That's correct! You completed your quiz!", "8", 38000, 40000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "9", 38000, 40000, 42500, 45000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 38000, 40000, 42500, 45000, '7', '8', '9')


def chemistry_task():
    start_task(computer_science)
    introduce('Mr. MacNeil: Welcome to gym class, I am your coach Mr. MacNeil. I prepared a quiz for you, good luck!', 5000, 10000)
    text1('Mr. MacNeil: What is Toronto Maple Leafs?', '1. A kind of maple leaf 2. An ice hockey team 3. A basketball team', 10000, 13000, 18000)
    wrong_answer('Mr. MacNeil: ??? Are you kidding me? You lose!', "1", 18000, 20000, 22500, 25000)
    correct_answer("Mr. MacNeil: That's correct!", "2", 18000, 20000)
    wrong_answer('Mr. MacNeil: That is wrong! You lose!', "3", 18000, 20000, 22500, 25000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 18000, 20000, 22500, 25000, '1', '2', '3')
    ## Second Question
    text1('Mr. MacNeil: Where is deltoid located?', '4. Shoulders 5. Legs 6. Arms', 20000, 23000, 28000)
    correct_answer("Mr. MacNeil: That's correct!", "4", 28000, 30000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "5", 28000, 30000, 32500, 35000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "6", 28000, 30000, 32500, 35000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 28000, 30000, 32500, 35000, '4', '5', '6')
    ## Third Question
    text1('Mr. MacNeil: How many players are there for each soccer team in a game?', '7. 10 players 8. 11 players 9. 12 players', 30000, 33000, 38000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "7", 38000, 40000, 42500, 45000)
    correct_answer("Mr. MacNeil: That's correct! You completed your quiz!", "8", 38000, 40000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "9", 38000, 40000, 42500, 45000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 38000, 40000, 42500, 45000, '7', '8', '9')


def biology_task():
    start_task(computer_science)
    introduce('Mr. MacNeil: Welcome to gym class, I am your coach Mr. MacNeil. I prepared a quiz for you, good luck!', 5000, 10000)
    text1('Mr. MacNeil: What is Toronto Maple Leafs?', '1. A kind of maple leaf 2. An ice hockey team 3. A basketball team', 10000, 13000, 18000)
    wrong_answer('Mr. MacNeil: ??? Are you kidding me? You lose!', "1", 18000, 20000, 22500, 25000)
    correct_answer("Mr. MacNeil: That's correct!", "2", 18000, 20000)
    wrong_answer('Mr. MacNeil: That is wrong! You lose!', "3", 18000, 20000, 22500, 25000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 18000, 20000, 22500, 25000, '1', '2', '3')
    ## Second Question
    text1('Mr. MacNeil: Where is deltoid located?', '4. Shoulders 5. Legs 6. Arms', 20000, 23000, 28000)
    correct_answer("Mr. MacNeil: That's correct!", "4", 28000, 30000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "5", 28000, 30000, 32500, 35000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "6", 28000, 30000, 32500, 35000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 28000, 30000, 32500, 35000, '4', '5', '6')
    ## Third Question
    text1('Mr. MacNeil: How many players are there for each soccer team in a game?', '7. 10 players 8. 11 players 9. 12 players', 30000, 33000, 38000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "7", 38000, 40000, 42500, 45000)
    correct_answer("Mr. MacNeil: That's correct! You completed your quiz!", "8", 38000, 40000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "9", 38000, 40000, 42500, 45000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 38000, 40000, 42500, 45000, '7', '8', '9')


def geography_task():
    start_task(computer_science)
    introduce('Mr. MacNeil: Welcome to gym class, I am your coach Mr. MacNeil. I prepared a quiz for you, good luck!', 5000, 10000)
    text1('Mr. MacNeil: What is Toronto Maple Leafs?', '1. A kind of maple leaf 2. An ice hockey team 3. A basketball team', 10000, 13000, 18000)
    wrong_answer('Mr. MacNeil: ??? Are you kidding me? You lose!', "1", 18000, 20000, 22500, 25000)
    correct_answer("Mr. MacNeil: That's correct!", "2", 18000, 20000)
    wrong_answer('Mr. MacNeil: That is wrong! You lose!', "3", 18000, 20000, 22500, 25000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 18000, 20000, 22500, 25000, '1', '2', '3')
    ## Second Question
    text1('Mr. MacNeil: Where is deltoid located?', '4. Shoulders 5. Legs 6. Arms', 20000, 23000, 28000)
    correct_answer("Mr. MacNeil: That's correct!", "4", 28000, 30000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "5", 28000, 30000, 32500, 35000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "6", 28000, 30000, 32500, 35000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 28000, 30000, 32500, 35000, '4', '5', '6')
    ## Third Question
    text1('Mr. MacNeil: How many players are there for each soccer team in a game?', '7. 10 players 8. 11 players 9. 12 players', 30000, 33000, 38000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "7", 38000, 40000, 42500, 45000)
    correct_answer("Mr. MacNeil: That's correct! You completed your quiz!", "8", 38000, 40000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "9", 38000, 40000, 42500, 45000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 38000, 40000, 42500, 45000, '7', '8', '9')


def history_task():
    start_task(computer_science)
    introduce('Mr. MacNeil: Welcome to gym class, I am your coach Mr. MacNeil. I prepared a quiz for you, good luck!', 5000, 10000)
    text1('Mr. MacNeil: What is Toronto Maple Leafs?', '1. A kind of maple leaf 2. An ice hockey team 3. A basketball team', 10000, 13000, 18000)
    wrong_answer('Mr. MacNeil: ??? Are you kidding me? You lose!', "1", 18000, 20000, 22500, 25000)
    correct_answer("Mr. MacNeil: That's correct!", "2", 18000, 20000)
    wrong_answer('Mr. MacNeil: That is wrong! You lose!', "3", 18000, 20000, 22500, 25000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 18000, 20000, 22500, 25000, '1', '2', '3')
    ## Second Question
    text1('Mr. MacNeil: Where is deltoid located?', '4. Shoulders 5. Legs 6. Arms', 20000, 23000, 28000)
    correct_answer("Mr. MacNeil: That's correct!", "4", 28000, 30000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "5", 28000, 30000, 32500, 35000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "6", 28000, 30000, 32500, 35000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 28000, 30000, 32500, 35000, '4', '5', '6')
    ## Third Question
    text1('Mr. MacNeil: How many players are there for each soccer team in a game?', '7. 10 players 8. 11 players 9. 12 players', 30000, 33000, 38000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "7", 38000, 40000, 42500, 45000)
    correct_answer("Mr. MacNeil: That's correct! You completed your quiz!", "8", 38000, 40000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "9", 38000, 40000, 42500, 45000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 38000, 40000, 42500, 45000, '7', '8', '9')


def art_task():
    start_task(computer_science)
    introduce('Mr. MacNeil: Welcome to gym class, I am your coach Mr. MacNeil. I prepared a quiz for you, good luck!', 5000, 10000)
    text1('Mr. MacNeil: What is Toronto Maple Leafs?', '1. A kind of maple leaf 2. An ice hockey team 3. A basketball team', 10000, 13000, 18000)
    wrong_answer('Mr. MacNeil: ??? Are you kidding me? You lose!', "1", 18000, 20000, 22500, 25000)
    correct_answer("Mr. MacNeil: That's correct!", "2", 18000, 20000)
    wrong_answer('Mr. MacNeil: That is wrong! You lose!', "3", 18000, 20000, 22500, 25000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 18000, 20000, 22500, 25000, '1', '2', '3')
    ## Second Question
    text1('Mr. MacNeil: Where is deltoid located?', '4. Shoulders 5. Legs 6. Arms', 20000, 23000, 28000)
    correct_answer("Mr. MacNeil: That's correct!", "4", 28000, 30000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "5", 28000, 30000, 32500, 35000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "6", 28000, 30000, 32500, 35000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 28000, 30000, 32500, 35000, '4', '5', '6')
    ## Third Question
    text1('Mr. MacNeil: How many players are there for each soccer team in a game?', '7. 10 players 8. 11 players 9. 12 players', 30000, 33000, 38000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "7", 38000, 40000, 42500, 45000)
    correct_answer("Mr. MacNeil: That's correct! You completed your quiz!", "8", 38000, 40000)
    wrong_answer("Mr. MacNeil: That's wrong! You lose!", "9", 38000, 40000, 42500, 45000)
    no_answer("Mr. MacNeil: mhm, you don't know the answer? You lose!", 38000, 40000, 42500, 45000, '7', '8', '9')





## set the initial value of moving to four directions to False
moving_right = False
moving_left = False
moving_up = False
moving_down = False


def move():
    """Let the player move around and stop moving when he reaches one side of the map border or there is an object in
    front of him, for example a wall, a desk
    Preconditions: NA
    :parameter: NA
    :return: NA
    """
    if moving_right:  # when d is pressed, moving_right == True
        can_move = True
        temp_rect = pygame.Rect(student_rect.x + 2, student_rect.y, student_rect.width, student_rect.height)  # create a rectangle for the player based on his x and y coordinates and width and height
        for i in tile_rects:
            if i[1] == '3' or i[1] == '0' or i[1] == '4' or i[1] == '8':  # if the tile is grass, ground, corridor or basketball court, the player can move
                continue
            if i[0].colliderect(temp_rect):  # if the tile is not one of these tiles above, the play cannot move
                can_move = False
                break
        if can_move and student_rect.x < 1595:  # when the player can move and he does not reach the map border, he can move right by two pixels
            student_rect.x += 2
    if moving_left:  # when a is pressed, moving_left == True
        can_move = True
        temp_rect = pygame.Rect(student_rect.x - 2, student_rect.y, student_rect.width, student_rect.height)  # create a rectangle for the player based on his x and y coordinates and width and height
        for i in tile_rects:
            if i[1] == '3' or i[1] == '0' or i[1] == '4' or i[1] == '8':  # if the tile is grass, ground, corridor or basketball court, the player can move
                continue
            if i[0].colliderect(temp_rect):  # if the tile is not one of these tiles above, the play cannot move
                can_move = False
                break
        if can_move and student_rect.x > 0:  # when the player can move and he does not reach the map border, he can move left by two pixels
            student_rect.x -= 2
    if moving_up:  # when w is pressed, moving_up == True
        can_move = True
        temp_rect = pygame.Rect(student_rect.x, student_rect.y - 2, student_rect.width, student_rect.height)  # create a rectangle for the player based on his x and y coordinates and width and height
        for i in tile_rects:
            if i[1] == '3' or i[1] == '0' or i[1] == '4' or i[1] == '8':  # if the tile is grass, ground, corridor or basketball court, the player can move
                continue
            if i[0].colliderect(temp_rect):  # if the tile is not one of these tiles above, the play cannot move
                can_move = False
                break
        if can_move and student_rect.y > 0:  # when the player can move and he does not reach the map border, he can move up by two pixels
            student_rect.y -= 2
    if moving_down:  # when s is pressed, moving_down == True
        can_move = True
        temp_rect = pygame.Rect(student_rect.x, student_rect.y + 2, student_rect.width, student_rect.height)  # create a rectangle for the player based on his x and y coordinates and width and height
        for i in tile_rects:
            if i[1] == '3' or i[1] == '0' or i[1] == '4' or i[1] == '8':  # if the tile is grass, ground, corridor or basketball court, the player can move
                continue
            if i[0].colliderect(temp_rect):  # if the tile is not one of these tiles above, the play cannot move
                can_move = False
                break
        if can_move and student_rect.y < 1490:  # when the player can move and he does not reach the map border, he can move down by two pixels
            student_rect.y += 2


student_location = [600, 1480]  # set player's initial location to 600, 1480 when the game starts
student_rect = pygame.Rect(student_location[0], student_location[1], student.get_width(), student.get_height())  # create a rectangle for the player

scroll = [0, 0]  # set the initial list of camera scroll

while True:  # the main loop of this game to keep it running, it is an infinite loop
    display.fill((255, 255, 255))  # fill the screen with colour white

    scroll[0] += (student_rect.x - scroll[0] - 202) / 20  # make the player always stay on the middle of the screen and keep following the player with a little bit delay
    scroll[1] += (student_rect.y - scroll[1] - 106) / 20  # make the player always stay on the middle of the screen and keep following the player with a little bit delay

    tile_rects = []  # set the initial list of tiles
    y = 0  # set the initial value of y
    for row in game_map:
        x = 0  # set the initial value of x
        ## build the map by matching numbers and letters to each image that I loaded before, it first build the first column, and then the second column and so on
        for tile in row:
            if tile == '0':
                display.blit(ground, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))  # show the ground image in right place
            if tile == '3':
                display.blit(grass, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))  # show the grass image in right place
            if tile == '2':
                display.blit(wall, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))  # show the wall image in right place
            if tile == '4':
                display.blit(corridor, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))  # show the corridor image in right place
            if tile == '5':
                display.blit(tree, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))  # show the tree image in right place
            if tile == '6':
                display.blit(desk, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))  # show the desk image in right place
            if tile == '8':
                display.blit(court, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))  # show the court image in right place
            if tile == '9':
                display.blit(toilet, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))  # show the toilet image in right place
            if tile == 'a':
                display.blit(computer, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))  # show the computer image in right place
            if tile == 'b':
                display.blit(basketball, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))  # show the basketball image in right place
            if tile == 'c':
                display.blit(net, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))  # show the net image in right place
            if tile == 'd':
                display.blit(car, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))  # show the car image in right place
            if tile == 'e':
                display.blit(instrument, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))  # show the instrument image in right place
            if tile == 'f':
                display.blit(globe, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))  # show the globe image in right place
            if tile == 'g':
                display.blit(sculpture, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))  # show the sculpture image in right place
            if tile == 'h':
                display.blit(books, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))  # show the books image in right place
            if tile == 'p':
                display.blit(labs, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))  # show the labs image in right place
            if tile != '0' or tile != '3' or tile != '4' or tile != '8':
                tile_rects.append((pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), tile))  # create a list to put all barriers/objects together
            x += 1
        y += 1

    display.blit(student, (student_rect.x - scroll[0], student_rect.y - scroll[1]))  # show the player on screen

    for event in pygame.event.get():  # event loop, it can check keyboard events
        if event.type == QUIT:  # check for window quit
            pygame.quit()  # stop pygame
            sys.exit()  # stop script
        if event.type == KEYDOWN:  # check if a particular key is pressed
            if event.key == K_d:  # check if d is pressed
                moving_right = True
            if event.key == K_a:  # check if a is pressed
                moving_left = True
            if event.key == K_w:  # check if w is pressed
                moving_up = True
            if event.key == K_s:  # check if s is pressed
                moving_down = True
            if event.key == K_m:  # check if m is pressed
                pygame.mixer.music.fadeout(500)  # the music will fade out with a 0.5 second delay after m is pressed
            if event.key == K_n:  # check if n is pressed
                pygame.mixer.music.play(-1)  # play the music for infinite times
            student_name += event.unicode  #
            if event.key == K_BACKSPACE:  # check if backspace is pressed
                student_name = student_name[:-1]  #
            if event.key == K_f:
                start = True
            if event.key == K_1:
                answer = "1"
            if event.key == K_2:
                answer = "2"
            if event.key == K_3:
                answer = "3"
            if event.key == K_4:
                answer = "4"
            if event.key == K_5:
                answer = "5"
            if event.key == K_6:
                answer = "6"
            if event.key == K_7:
                answer = "7"
            if event.key == K_8:
                answer = "8"
            if event.key == K_9:
                answer = "9"

        if event.type == KEYUP:  # check if a particular key is up
            if event.key == K_d:  # check if d key is up
                moving_right = False
            if event.key == K_a:  # check if a key is up
                moving_left = False
            if event.key == K_w:  # check if w key is up
                moving_up = False
            if event.key == K_s:  # check if s key is up
                moving_down = False
    move()  # call the "move" function


    surf = pygame.transform.scale(display, WINDOW_SIZE)  #
    screen.blit(surf, (0, 0))  #

    if pygame.time.get_ticks() < 4000:  # check if the game is started between 0 seconds and 4 seconds
        ## print "Hey TSS Tigers, welcome back to school!" on screen during this time period
        intro = pygame.font.SysFont("Microsoft Yahei UI Light",60).render("Hey TSS Tigers, welcome back to school!", True, (0, 0, 0))
        screen.blit(intro, (int((WINDOW_SIZE[0] - intro.get_width()) / 2), int((WINDOW_SIZE[1] - intro.get_height()) / 2)))
    if pygame.time.get_ticks() > 4000 and pygame.time.get_ticks() < 10000:  # check if the game is started between 4 seconds and 10 seconds
        ## print "Controls: w: up, s: down, a: left, d: right, m: mute, n: unmute" on screen during this time period
        control = pygame.font.SysFont("Microsoft Yahei UI Light",60).render("Controls: w: up, s: down, a: left, d: right, m: mute, n: unmute", True, (0, 0, 0))
        screen.blit(control, (int((WINDOW_SIZE[0] - control.get_width()) / 2), int((WINDOW_SIZE[1] - control.get_height()) / 2)))
    if pygame.time.get_ticks() > 10000 and pygame.time.get_ticks() < 14000:  # check if the game is started between 10 seconds and 14 seconds
        ## print "Please enter your name:" on screen during this time period
        ask_name = pygame.font.SysFont("Microsoft Yahei UI Light",60).render("Please enter your name:", True, (0, 0, 0))
        screen.blit(ask_name, (int((WINDOW_SIZE[0] - ask_name.get_width()) / 2), int((WINDOW_SIZE[1] - ask_name.get_height()) / 2)))


    test_collision()  # call the "test_collision" function
    gym_task()  # call the "gym_task" function
    computer_science_task()


    pygame.display.update()  # update the screen
    clock.tick(60)  # set the frame to 60 fps