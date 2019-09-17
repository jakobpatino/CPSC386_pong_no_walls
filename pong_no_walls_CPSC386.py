import pygame
import sys
import random
from pygame.locals import*


pygame.init()
mainClock = pygame.time.Clock()

# set up window
WINDOWWIDTH = 800
WINDOWHEIGHT = 550
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Pong No Walls')

# set colors and text font
WHITE = (225, 225, 225)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
basicFont = pygame.font.SysFont(None, 60)

# add sound files
ball_bounce = pygame.mixer.Sound('audio/ball_bounce.wav')
round_win = pygame.mixer.Sound('audio/round_win.wav')
round_lose = pygame.mixer.Sound('audio/round_lose.wav')
match_win = pygame.mixer.Sound('audio/match_win.wav')
match_lose = pygame.mixer.Sound('audio/match_lose.wav')
win = pygame.mixer.Sound('audio/victory.wav')
loss = pygame.mixer.Sound('audio/loss.wav')

# add player paddles and their images
player_right = pygame.Rect(750, 200, 38, 120)
player_paddle_right = pygame.image.load('images/paddle_player.jpg')
player_paddle_right_fit = pygame.transform.scale(player_paddle_right, (38, 120))

player_top = pygame.Rect(600, 12, 120, 38)
player_paddle_top = pygame.image.load('images/paddle_player_top.jpg')
player_paddle_top_fit = pygame.transform.scale(player_paddle_top, (120, 38))

player_bottom = pygame.Rect(600, 500, 120, 38)
player_paddle_bottom = pygame.image.load('images/paddle_player_bottom.jpg')
player_paddle_bottom_fit = pygame.transform.scale(player_paddle_bottom, (120, 38))

# add ai paddles and their images
ai_left = pygame.Rect(12, 200, 38, 120)
ai_paddle_left = pygame.image.load('images/paddle_ai.jpg')
ai_paddle_left_fit = pygame.transform.scale(ai_paddle_left, (38, 120))

ai_top = pygame.Rect(80, 12, 120, 38)
ai_paddle_top = pygame.image.load('images/paddle_ai_top.jpg')
ai_paddle_top_fit = pygame.transform.scale(ai_paddle_top, (120, 38))

ai_bottom = pygame.Rect(80, 500, 120, 38)
ai_paddle_bottom = pygame.image.load('images/paddle_ai_bottom.jpg')
ai_paddle_bottom_fit = pygame.transform.scale(ai_paddle_bottom, (120, 38))

# set up player movement variables
moveLeft = False
moveRight = False
moveUp = False
moveDown = False

# set paddle speeds
PLAYERSPEED = 7
AISPEED = 3

# set up initial ball stats
ball_dir = ['up_right', 'up_left', 'down_right', 'down_left']
curr_dir = ball_dir[random.randrange(0, 4)]
curr_speed = random.randrange(7, 12)
curr_y = random.randrange(100, 450)
curr_x = 400


# function that changes the direction of ball movement when it bounces on a left or right surface
def bounce_side(direction):
    if direction == 'up_right':
        return 'up_left'
    elif direction == 'up_left':
        return 'up_right'
    elif direction == 'down_right':
        return 'down_left'
    elif direction == 'down_left':
        return 'down_right'
    else:
        return direction


# function that changes the direction of ball movement when it bounces on a left or right surface
def bounce_bottom(direction):
    if direction == 'up_right':
        return 'down_right'
    elif direction == 'up_left':
        return 'down_left'
    else:
        return direction


# function that changes the direction of ball movement when it bounces on a bottom surface
def bounce_top(direction):
    if direction == 'down_right':
        return 'up_right'
    elif direction == 'down_left':
        return 'up_left'
    else:
        return direction


# set initial scores
round_score_ai = 0
round_score_player = 0
match_score_ai = 0
match_score_player = 0
victory = False

ai_win = False
player_win = False

# run game loop
while not victory:
    # set up keyboard actions
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            # change the keyboard variables
            if event.key == K_LEFT:
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT:
                moveLeft = False
                moveRight = True
            if event.key == K_UP:
                moveDown = False
                moveUp = True
            if event.key == K_DOWN:
                moveUp = False
                moveDown = True
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT:
                moveLeft = False
            if event.key == K_RIGHT:
                moveRight = False
            if event.key == K_UP:
                moveUp = False
            if event.key == K_DOWN:
                moveDown = False

    # paint background
    windowSurface.fill(BLACK)

    # set the text to read the current score
    round_score_ai_text = basicFont.render(str(round_score_ai), True, WHITE)
    round_score_player_text = basicFont.render(str(round_score_player), True, WHITE)

    # place the score on the screen
    if round_score_ai < 10:
        windowSurface.blit(round_score_ai_text, (350, 50))
    else:
        windowSurface.blit(round_score_ai_text, (335, 50))

    if round_score_player < 10:
        windowSurface.blit(round_score_player_text, (430, 50))
    else:
        windowSurface.blit(round_score_player_text, (415, 50))

    # paint match points on the screen; fill in circles when point scored
    if match_score_ai < 1:
        pygame.draw.circle(windowSurface, WHITE, (380, 100), 5, 1)
    else:
        pygame.draw.circle(windowSurface, WHITE, (380, 100), 5)
    if match_score_ai < 2:
        pygame.draw.circle(windowSurface, WHITE, (360, 100), 5, 1)
    else:
        pygame.draw.circle(windowSurface, WHITE, (360, 100), 5)
    if match_score_ai < 3:
        pygame.draw.circle(windowSurface, WHITE, (340, 100), 5, 1)
    else:
        pygame.draw.circle(windowSurface, WHITE, (340, 100), 5)

    if match_score_player < 1:
        pygame.draw.circle(windowSurface, WHITE, (420, 100), 5, 1)
    else:
        pygame.draw.circle(windowSurface, WHITE, (420, 100), 5)
    if match_score_player < 2:
        pygame.draw.circle(windowSurface, WHITE, (440, 100), 5, 1)
    else:
        pygame.draw.circle(windowSurface, WHITE, (440, 100), 5)
    if match_score_player < 3:
        pygame.draw.circle(windowSurface, WHITE, (460, 100), 5, 1)
    else:
        pygame.draw.circle(windowSurface, WHITE, (460, 100), 5)

    # put the paddles on the screen
    windowSurface.blit(player_paddle_right_fit, player_right)
    windowSurface.blit(player_paddle_top_fit, player_top)
    windowSurface.blit(player_paddle_bottom_fit, player_bottom)

    windowSurface.blit(ai_paddle_left_fit, ai_left)
    windowSurface.blit(ai_paddle_top_fit, ai_top)
    windowSurface.blit(ai_paddle_bottom_fit, ai_bottom)

    # paint the net on screen
    for i in range(27):
        pygame.draw.rect(windowSurface, WHITE, (397, (20 * i) + 10, 6, 10))

    # gives a match point and plays win/lose sound; creates new ball stats
    if round_score_ai > 11 and round_score_ai >= round_score_player + 2:
        if match_score_ai == 0:
            match_score_ai = 1
            round_score_ai = 0
            round_score_player = 0
            match_lose.play()
        elif match_score_ai == 1:
            match_score_ai = 2
            round_score_ai = 0
            round_score_player = 0
            match_lose.play()
        elif match_score_ai == 2:
            ai_win = True
            victory = True
            loss.play()
        curr_dir = ball_dir[random.randrange(0, 4)]
        curr_speed = random.randrange(3, 7)
        curr_y = random.randrange(100, 450)
        curr_x = 400

    if round_score_player > 11 and round_score_player >= round_score_ai + 2:
        if match_score_player == 0:
            match_score_player = 1
            round_score_ai = 0
            round_score_player = 0
            match_win.play()
        elif match_score_player == 1:
            match_score_player = 2
            round_score_ai = 0
            round_score_player = 0
            match_win.play()
        elif match_score_player == 2:
            player_win = True
            victory = True
            win.play()
        curr_dir = ball_dir[random.randrange(0, 4)]
        curr_speed = random.randrange(3, 7)
        curr_y = random.randrange(100, 450)
        curr_x = 400

    # gives round points and plays round win/loss sounds
    if (curr_x > 400 and curr_y > 558) or curr_x > 808 or (curr_x > 400 and curr_y < -8):
        round_score_ai += 1
        curr_dir = ball_dir[random.randrange(0, 4)]
        curr_speed = random.randrange(3, 7)
        curr_y = random.randrange(100, 450)
        curr_x = 400
        if not (round_score_ai > 11 and round_score_ai >= round_score_player + 2):
            round_lose.play()
    if (curr_x <= 400 and curr_y > 558) or curr_x < -8 or (curr_x <= 400 and curr_y < -8):
        round_score_player += 1
        curr_dir = ball_dir[random.randrange(0, 4)]
        curr_speed = random.randrange(3, 7)
        curr_y = random.randrange(100, 450)
        curr_x = 400
        if not (round_score_player > 11 and round_score_player >= round_score_ai + 2):
            round_win.play()

    # moves ball based on current direction
    if curr_dir == 'up_right':
        curr_y -= curr_speed
        curr_x += curr_speed
    if curr_dir == 'up_left':
        curr_y -= curr_speed
        curr_x -= curr_speed
    if curr_dir == 'down_right':
        curr_y += curr_speed
        curr_x += curr_speed
    if curr_dir == 'down_left':
        curr_y += curr_speed
        curr_x -= curr_speed

    # draws ball at current position
    ball = pygame.draw.circle(windowSurface, WHITE, (curr_x, curr_y), 8)

    # bounces ball if it collides with paddles and plays bounce sound
    if (ball.colliderect(player_right) and curr_x <= player_right.left) or\
            (ball.colliderect(player_top) and curr_x <= player_top.left) or\
            (ball.colliderect(player_bottom) and curr_x <= player_bottom.left) or \
            (ball.colliderect(ai_top) and curr_x <= ai_top.left) or \
            (ball.colliderect(ai_bottom) and curr_x <= ai_bottom.left):
        curr_dir = bounce_side(curr_dir)
        ball_bounce.play()
    if (ball.colliderect(ai_left) and curr_x >= ai_left.right) or\
            (ball.colliderect(ai_top) and curr_x >= ai_top.right) or\
            (ball.colliderect(ai_bottom) and curr_x >= ai_bottom.right) or \
            (ball.colliderect(player_top) and curr_x >= player_top.right) or \
            (ball.colliderect(player_bottom) and curr_x >= player_bottom.right):
        curr_dir = bounce_side(curr_dir)
        ball_bounce.play()
    if (ball.colliderect(player_top) and curr_y >= player_top.bottom) or\
            (ball.colliderect(player_right) and curr_y >= player_right.bottom) or\
            (ball.colliderect(ai_top) and curr_y >= ai_top.bottom) or \
            (ball.colliderect(ai_left) and curr_y >= ai_left.bottom):
        curr_dir = bounce_bottom(curr_dir)
        ball_bounce.play()
    if (ball.colliderect(player_bottom) and curr_y <= player_bottom.top) or\
            (ball.colliderect(player_right) and curr_y <= player_right.top) or\
            (ball.colliderect(ai_bottom) and curr_y <= ai_bottom.top) or \
            (ball.colliderect(ai_left) and curr_y <= ai_left.top):
        curr_dir = bounce_top(curr_dir)
        ball_bounce.play()

    # sets up player movement
    if moveUp and player_right.top > 13\
            and not player_right.colliderect(player_top):
        player_right.top -= PLAYERSPEED
    if moveDown and player_right.bottom < 537\
            and not player_right.colliderect(player_bottom):
        player_right.bottom += PLAYERSPEED

    if moveLeft and player_top.left > 400 and player_bottom.left > 400 \
            and not player_top.colliderect(ai_top) and not player_bottom.colliderect(ai_bottom):
        player_top.left -= PLAYERSPEED
        player_bottom.left -= PLAYERSPEED
    if moveRight and player_top.right < WINDOWWIDTH and player_bottom.right < (WINDOWWIDTH - 13)\
            and not player_top.colliderect(player_right) and not player_bottom.colliderect(player_right):
        player_top.right += PLAYERSPEED
        player_bottom.right += PLAYERSPEED

    # sets up ai movement that tracks ball
    if curr_y > (ai_left.top + 60) and ai_left.bottom < (WINDOWHEIGHT - 13) \
            and not ai_left.colliderect(ai_bottom):
        ai_left.top += AISPEED
    if curr_y < (ai_left.top + 60) and ai_left.top > 12 \
            and not ai_left.colliderect(ai_top):
        ai_left.top -= AISPEED

    if curr_x < (ai_top.right - 60) and ai_top.left > 0 and ai_bottom.left > 12 \
            and not ai_top.colliderect(ai_left) and not ai_bottom.colliderect(ai_left):
        ai_top.left -= AISPEED
        ai_bottom.left -= AISPEED
    if curr_x > (ai_top.right - 60) and ai_top.right < 400 and ai_bottom.right < 400 \
            and not ai_top.colliderect(player_top) and not ai_bottom.colliderect(player_bottom):
        ai_top.right += AISPEED
        ai_bottom.right += AISPEED

    # draw window onto screen
    pygame.display.update()
    mainClock.tick(40)

    # sets up play again
    while victory:

        # set background color
        windowSurface.fill(BLACK)

        # reset defaults
        moveLeft = False
        moveRight = False
        moveUp = False
        moveDown = False

        player_right.top = 200
        player_right.left = 750
        player_top.top = 12
        player_top.left = 600
        player_bottom.top = 500
        player_bottom.left = 600

        ai_left.top = 200
        ai_bottom.left = 12
        ai_top.top = 12
        ai_top.left = 80
        ai_bottom.top = 500
        ai_bottom.left = 80

        curr_dir = ball_dir[random.randrange(0, 4)]
        curr_speed = random.randrange(3, 6)
        curr_y = random.randrange(100, 450)
        curr_x = 400

        round_score_ai = 0
        round_score_player = 0
        match_score_ai = 0
        match_score_player = 0

        # display 'play again' prompt and winner
        if ai_win:
            play_again = basicFont.render('AI Wins! Play Again? (y/n)', True, WHITE)
            windowSurface.blit(play_again, (140, 225))
        if player_win:
            play_again2 = basicFont.render('Player Wins! Play Again? (y/n)', True, WHITE)
            windowSurface.blit(play_again2, (95, 225))

        # sets up keyboard functions
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                if event.key == K_ESCAPE or event.key == K_n:
                    pygame.quit()
                    sys.exit()
                if event.key == K_y:
                    ai_win = False
                    player_win = False
                    victory = False

        # draw window onto screen
        pygame.display.update()
        mainClock.tick(40)
