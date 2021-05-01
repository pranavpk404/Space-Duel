import pygame

pygame.font.init()

# SOUND 
pygame.mixer.init()
# WINDOW
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# COLORS AND FONT
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

pygame.display.set_caption("Space Wars")  # TITLE

FPS = 60

VEL = 5  # SPEED OF THE SHIP

BULLET_VEL = 8  # SPEED OF THE BULLET

MAX_BULLET_IN_SCREEN = 4  # HOW MANY BULLET IN THE SCREEN AT A TIME

# MAKING SPECIAL EVENT FOR BULLET
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)  # THE MIDDLE BULLET

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 65, 50  # SPACESSHIP SIZE

BULLET_HIT_SOUND = pygame.mixer.Sound("res\\hit.mp3")
BULLET_FIRE_SOUND = pygame.mixer.Sound("res\\fire.mp3")

# IMGs
YELLOW_SHIP_IMG = pygame.image.load('res\\yellow_ship.png')
RED_SHIP_IMG = pygame.image.load('res\\red_ship.png')
BG_IMAGE = pygame.image.load("res\\bg.png")

# RESIZING AND ROTATING
YELLOW_SHIP = pygame.transform.scale(YELLOW_SHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

RED_SHIP = pygame.transform.scale(RED_SHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

BG = pygame.transform.scale(BG_IMAGE, (WIDTH, HEIGHT))


def draw_windows(red, yellow, red_bullets, yellow_bullets, RED_HEALTH, YELLOW_HEALTH):
    WIN.blit(BG, (0, 0))  # BG
    pygame.draw.rect(WIN, (255, 0, 0), BORDER)  # MIDDLE BORDER JUST DRAWING

    red_health_text = HEALTH_FONT.render("Health: " + str(RED_HEALTH), 1, RED)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(YELLOW_HEALTH), 1, YELLOW)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    # SHOWING SPACE SHIPS
    WIN.blit(YELLOW_SHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SHIP, (red.x, red.y))

    # DRAWING BULLETS
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


# MOVEMENT OF YELLOW AND RED SHIP

def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0 - 5:  # LEFT
        yellow.x -= VEL

    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x + 12:  # RIGHT
        yellow.x += VEL

    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL

    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 12:  # DOWN
        yellow.y += VEL


def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width - 5:  # LEFT
        red.x -= VEL

    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH + 12:  # RIGHT
        red.x += VEL

    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL

    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 12:  # DOWN
        red.y += VEL


# BULLET CONFIG
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)  # REMOVING THE BULLET THAT HIT FROM LIST

        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)  # REMOVING THE BULLET THAT GONE IN THE SPACE FROM LIST

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)  # REMOVING THE BULLET THAT HIT FROM LIST
        elif bullet.x < 0:
            red_bullets.remove(bullet)  # REMOVING THE BULLET THAT GONE IN THE SPACE FROM LIST


def draw_winner(text, color):
    draw_text = WINNER_FONT.render(text, 1, True, color)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)
    main()


# EVENT LOOP
def main():
    # DRAWING RECT5 AROUND THE IMGs
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  #
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []

    # HEALTH
    RED_HEALTH = 10
    YELLOW_HEALTH = 10
    # making the game to stay in FPS
    clock = pygame.time.Clock()
    # GAME LOOP
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            # TO QUIT IN CASE WHEN USER PRESS X MARK
            if event.type == pygame.QUIT:
                run = False
                pygame.QUIT()

            # MAKING TH BULLET TO FIRE
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LALT and len(yellow_bullets) < MAX_BULLET_IN_SCREEN:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLET_IN_SCREEN:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                    # IF THE BULLET HIT THE PLAYERS 
            if event.type == RED_HIT:
                RED_HEALTH -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                YELLOW_HEALTH -= 1
                BULLET_HIT_SOUND.play()

        # MAKING THE TEXT TO DISPLAY THE WINNER
        winner_text = ""
        if RED_HEALTH <= 0:
            winner_text = "Yellow Wins!"
            color = YELLOW
        if YELLOW_HEALTH <= 0:
            winner_text = "Red Wins!"
            color = RED
        if winner_text != "":
            draw_winner(winner_text, color)

        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_windows(red, yellow, red_bullets, yellow_bullets, RED_HEALTH, YELLOW_HEALTH)


if __name__ == "__main__":
    main()
