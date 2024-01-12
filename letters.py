# MORI AUTO
import pygame
import sys
import time
import random
import string

# START PYGAME MODULES
pygame.init()
clock = pygame.time.Clock()

# CONSTANTS
DISPLAY_WIDTH = 472
DISPLAY_HEIGHT = 600
FLOOR_X = 0
GRAVITY = 0.15
BACKGROUND_X = 0
boy_movement = 0
letters_pos = [772, 700, 750]
WORDS_LIST = ["BOEK", "RAMP", "BANK", "STOEL", "FIETS", "BIER", "LAMP"]
LETTERS_GOAL = []
BOY_LIST_INDEX = 0
SCORE = 0
COLLISION_CHECK = False  # Renamed the variable
SPEED = 90
LETTER_CREATION_FLAG = False  # Renamed the variable

GAME_FONT = pygame.font.Font('assets/font/aAbstractGroovy.TTF', 50)
WIN_SOUND = pygame.mixer.Sound('assets/sound/smb_stomp.wav')
GAME_OVER_SOUND = pygame.mixer.Sound('assets/sound/beep-06.wav')

CHECK_LIST = []

pygame.time.set_timer(pygame.USEREVENT, 100)
pygame.time.set_timer(pygame.USEREVENT + 1, 50)

main_screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

background_image = pygame.image.load('assets/img/teh10.jpg')

boy_image_1 = pygame.image.load('assets/img/1.png')
boy_image_2 = pygame.image.load('assets/img/2.png')
boy_image_3 = pygame.image.load('assets/img/3.png')
boy_image_4 = pygame.image.load('assets/img/4.png')
boy_image_5 = pygame.image.load('assets/img/5.png')

random_letter = random.choice(string.ascii_letters)
random_letter = random_letter.upper()

letter = GAME_FONT.render(random_letter, True, (255, 0, 255))
letter_goal = letter

boy_list = [boy_image_1, boy_image_2, boy_image_3, boy_image_4, boy_image_5]
boy_image = boy_list[BOY_LIST_INDEX]

floor_image = pygame.transform.scale2x(pygame.image.load('assets/img/floor4.jpg'))

boy_image_rect = boy_image.get_rect(center=(100, 100))


def show_score():
    global SCORE
    text1 = GAME_FONT.render(str(SCORE), True, (255, 0, 255))
    main_screen.blit(text1, (100, 100))


def is_collision():  # Renamed the function
    global boy_image_rect
    collision = boy_image_rect.colliderect(goal)
    return collision


def random_x_y():
    x = random.randrange(600, 772)
    y = random.randrange(600, 772)
    return x, y


def change_letter(random_letter):
    color_letter = [0, 255]
    x = random.choice(color_letter)
    y = random.choice(color_letter)
    z = random.choice(color_letter)
    letter = GAME_FONT.render(random_letter, False, (x, y, z))
    return letter


def change_letter_goal():
    letter_goal = random.choice(string.ascii_letters)
    letter_goal = GAME_FONT.render(random_letter, True, (255, 0, 255))
    return letter_goal


def move_letter_rect(letters):
    for letter in letters:
        letters_pos[0] -= 1
    inside_letters = [letter for letter in letters if letter > 0]
    return inside_letters


def boy_animation():
    new_boy = boy_list[BOY_LIST_INDEX]
    return new_boy


def word_analyze(word_goal2):  # Renamed the function
    letters_goal = []
    anz = len(word_goal2)
    s3 = ""
    s4 = anz
    for a in range(anz):
        s4 -= 1
        letters_goal.append(word_goal2[s4])
        s3 = s3 + word_goal2[s4]
    return letters_goal


def join(check_list):
    return " ".join(map(str, check_list))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if boy_image_rect.top > 350 and boy_image_rect.right < 440:
                    boy_movement = 0
                    boy_image_rect.centery -= 150
                    boy_image_rect.centerx += 120
            if event.key == pygame.K_r:
                word_analyze(word_goal2)  # Modified the function call
                WIN_SOUND.play()

        if event.type == pygame.USEREVENT:
            LETTER_CREATION_FLAG = True  # Renamed the variable
            if len(letters_pos) < 4:
                letters_pos.extend(random_x_y())

        if event.type == pygame.USEREVENT + 1:
            if BOY_LIST_INDEX < 4:
                BOY_LIST_INDEX += 1
            else:
                BOY_LIST_INDEX = 0
            boy_image = boy_animation()

    # BACKGROUND DISPLAY
    BACKGROUND_X -= 1
    main_screen.blit(background_image, (BACKGROUND_X, 0))
    main_screen.blit(background_image, (BACKGROUND_X + 1200, 0))
    if BACKGROUND_X <= -1200:
        BACKGROUND_X = 0

    # DISPLAY LETTERS
    if LETTER_CREATION_FLAG:
        letters_pos = move_letter_rect(letters_pos)
        main_screen.blit(letter, ([letters_pos[0], letters_pos[1] - 350]))
        goal = main_screen.blit(letter, ([letters_pos[0], letters_pos[1] - 350]))

        # DISPLAY SCORE
        text1 = GAME_FONT.render(f'score : {SCORE}', False, (200, 0, 255))
        main_screen.blit(text1, (100, 50))

        text3 = GAME_FONT.render(f'speed : {SPEED}', False, (100, 0, 255))
        main_screen.blit(text3, (100, 10))

        if letters_pos[0] < 5:
            random_letter = random.choice(string.ascii_letters)
            random_letter = random_letter.upper()
            letter = change_letter(random_letter)

        if is_collision() and random_letter in LETTERS_GOAL:
            if random_letter not in CHECK_LIST:
                CHECK_LIST.insert(0, random_letter)
            letters_pos[0] = 0
            random_letter = random.choice(string.ascii_letters)
            random_letter = random_letter.upper()
            letter = change_letter(random_letter)

            WIN_SOUND.play()
            LETTER_CREATION_FLAG = False
            SCORE += 1
            show_score()
            if SPEED > 90:
                SPEED -= 10
        elif is_collision() and random_letter not in LETTERS_GOAL:
            letters_pos[0] = 0
            GAME_OVER_SOUND.play()
            random_letter = random.choice(string.ascii_letters)
            random_letter = random_letter.upper()
            letter = change_letter(random_letter)

            LETTER_CREATION_FLAG = False
            SCORE -= 1
            show_score()
            if SPEED < 110:
                SPEED += 5

    text4 = join(CHECK_LIST)
    text2 = GAME_FONT.render(text4, False, (225, 100, 100))
    main_screen.blit(text2, (100, 100))

    # DISPLAY FLOOR
    FLOOR_X -= 1
    main_screen.blit(floor_image, (FLOOR_X, 472))
    main_screen.blit(floor_image, (FLOOR_X + 472, 472))
    if FLOOR_X <= -471:
        FLOOR_X = 0
    main_screen.blit(boy_image, boy_image_rect)

    if len(CHECK_LIST) == len(LETTERS_GOAL):
        CHECK_LIST = []
        wg = random.randrange(0, 6)

    word_goal2 = WORDS_LIST[wg]
    word_goal = GAME_FONT.render(WORDS_LIST[wg], False, (100, 0, 255))
    LETTERS_GOAL = word_analyze(word_goal2)

    main_screen.blit(word_goal, (150, 550))

    # BOY MOVEMENT
    if (
        boy_image_rect.bottom < 480
        and boy_image_rect.top > 0
        and boy_image_rect.right < 530
    ):
        boy_movement += GRAVITY
        boy_image_rect.centery += boy_movement

    # BOY JUMP
    if boy_image_rect.centerx > 100:
        boy_image_rect.centerx -= 1

    pygame.display.update()

    # SET GAME SPEED
    clock.tick(SPEED)
