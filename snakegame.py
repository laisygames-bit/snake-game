import pygame
import random
import os

pygame.init()

# colors

white        = (255, 255, 255)
yellow       = (255, 255, 102)
black        = (0,   0,   0)
red          = (213, 50,  80)
blue         = (50,  153, 213)
dark_green   = (0,   100, 0)
dark_green2  = (0,   80,  0)   # darker for head than for body

# window settings

dis_width   = 800
dis_height  = 800
dis         = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake-game')

clock       = pygame.time.Clock()
snake_block = 20
BASE_SPEED  = 3

font_style  = pygame.font.SysFont("arial",       22)
score_font  = pygame.font.SysFont("comicsansms", 35)
info_font   = pygame.font.SysFont("arial",       16)

# uploading textures

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_img(filename):
    path = os.path.join(BASE_DIR, filename)
    img  = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (20, 20))

FOOD_IMAGES = {
    "normal":   load_img("images/green.apple.png"),   # +1 point
    "bonus":    load_img("images/red.apple.png"),      # +2 points
    "speed_up": load_img("images/blueberry.png"),      # speed up
    "speed_dn": load_img("images/orange.png"),         # speed down
    "death":    load_img("images/skull.png"),          # death
}

# food types

FOOD_TYPES = {
    "normal":   {"points": 1, "speed":  0, "lethal": False, "label": "+1 point"},
    "bonus":    {"points": 2, "speed":  0, "lethal": False, "label": "+2 points"},
    "speed_up": {"points": 1, "speed": +3, "lethal": False, "label": "fast"},
    "speed_dn": {"points": 1, "speed": -2, "lethal": False, "label": "slow"},
    "death":    {"points": 0, "speed":  0, "lethal": True,  "label": "death"},
}

# possibilities of spawn food

FOOD_WEIGHTS = {
    "normal":   50,
    "bonus":    20,
    "speed_up": 14,
    "speed_dn": 14,
    "death":    2,
}


# random pick of food type

def pick_food_type():
    types   = list(FOOD_WEIGHTS.keys())
    weights = [FOOD_WEIGHTS[t] for t in types]
    return random.choices(types, weights=weights, k=1)[0]

# creating new food

def new_food(snake_list):
    while True:
        fx = random.randrange(0, dis_width  // snake_block) * snake_block
        fy = random.randrange(0, dis_height // snake_block) * snake_block
        if [fx, fy] not in snake_list:
            break
    return {"x": fx, "y": fy, "type": pick_food_type()}

# creating block to eat under food texture
def draw_food(food):
    dis.blit(FOOD_IMAGES[food["type"]], (food["x"], food["y"]))


def our_snake(snake_block, snake_list):
    for i, x in enumerate(snake_list):
        # head is lighter than body
        color = dark_green if i < len(snake_list) - 1 else (0, 140, 0)
        pygame.draw.rect(dis, color, [x[0], x[1], snake_block, snake_block])
        pygame.draw.rect(dis, dark_green2, [x[0], x[1], snake_block, snake_block], 1)

# score- and speedboard
def Your_score(score, speed):
    txt = score_font.render(f"Score: {score}   Speed: {speed}", True, yellow)
    dis.blit(txt, [0, 0])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width // 6, dis_height // 3])


# game loop
def gameLoop():
    game_over  = False
    game_close = False

    x1, y1          = dis_width // 2, dis_height // 2
    x1_change        = 0
    y1_change        = 0
    snake_List        = []
    Length_of_snake   = 1
    current_speed     = BASE_SPEED

    food = new_food(snake_List)

    while not game_over:

        # lost screen
        while game_close:
            dis.fill(blue)
            message("You lose!  C - again   Q - exit", red)
            Your_score(Length_of_snake - 1, current_speed)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over  = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
                        return

        # movement
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT  and x1_change == 0:
                    x1_change = -snake_block; y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change =  snake_block; y1_change = 0
                elif event.key == pygame.K_UP   and y1_change == 0:
                    y1_change = -snake_block; x1_change = 0
                elif event.key == pygame.K_DOWN  and y1_change == 0:
                    y1_change =  snake_block; x1_change = 0

        x1 += x1_change
        y1 += y1_change

        # walls
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        # background
        dis.fill(blue)
        draw_food(food)

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for seg in snake_List[:-1]:
            if seg == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1, current_speed)
        pygame.display.update()

        # food eating
        if x1 == food["x"] and y1 == food["y"]:
            ftype = FOOD_TYPES[food["type"]]
            if ftype["lethal"]:
                game_close = True
            else:
                Length_of_snake += ftype["points"]
                current_speed = max(3, min(25, current_speed + ftype["speed"]))
            food = new_food(snake_List)

        clock.tick(current_speed)

    pygame.quit()
    quit()


gameLoop()