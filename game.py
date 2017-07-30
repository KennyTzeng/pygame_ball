import sys
import pygame

# pygame init
pygame.init()
pygame.display.set_caption("Reaction Game")

# window size
window_size = (window_width, window_height) = (400, 600)
# color
black = (0, 0, 0)
white = (255, 255, 255)
# logic control boolean 
game = True
round = True
# fonts
small_font = pygame.font.Font("bold.ttf", 18)
# score control
start_time = 0

# init objects
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()

ball = pygame.image.load("small-ball.png")
ballRect = ball.get_rect()
platform = pygame.image.load("small-platform.png")
platformRect = platform.get_rect()

def text_on_screen(text, color, y_displacement=0):
    
    textSurface = small_font.render(text, True, color, None)
    textRect = textSurface.get_rect()
    textRect.center = (int(window_width / 2), y_displacement)
    screen.blit(textSurface, textRect)

def calcScore(game_time):
    global start_time
    return game_time - start_time

def gameOver(game_time):
    global game
    global round
    # disable the level up timer
    pygame.time.set_timer(24, 0)
    text_on_screen("Game Over", white, 100)
    text_on_screen("Your score is : {}".format(calcScore(game_time)), white, 200)
    text_on_screen("Press 'r' to restart", white, 400)
    text_on_screen("Press 'q' to leave", white, 450)

    while round:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    round = False
                if event.key == pygame.K_q:
                    round = False
                    game = False

        clock.tick(60)
        pygame.display.flip()

def main():

    # element attribute
    global round
    round = True
    global start_time
    start_time = pygame.time.get_ticks()

    # define event.type = 24 to present level up per 10 seconds
    pygame.time.set_timer(24, 10000)

    ball_speed = 4
    ball_direction = [1, 1]
    ball_pos = [0, 0]
    platform_pos = [0, 0]

    ballRect.top = 1
    ballRect.left = 1
    platformRect.center = [0, 500]

    while round:
        for event in pygame.event.get():
            if event.type == 24:
                ball_speed = ball_speed + 1
                print("level up")
            if event.type == pygame.QUIT: sys.exit()
        
        for i in range(ball_speed):
            
            ball_pos = [(ballRect.left + ballRect.right)/2, (ballRect.top + ballRect.bottom)/2]
            mouse_pos = pygame.mouse.get_pos()
            platformRect.center = [mouse_pos[0], 500]
            ballRect.move_ip([ball_direction[0], ball_direction[1]])

            if ballRect.bottom == platformRect.top and platformRect.left <= ball_pos[0] <= platformRect.right:
                ball_direction[1] = -ball_direction[1]
                print("nice catch")
            elif platformRect.colliderect(ballRect):
                ball_direction[0] = -ball_direction[0]
                print("oops")   
            if ballRect.left < 0 or ballRect.right > window_width:
                ball_direction[0] = -ball_direction[0]
            if ballRect.top < 0:
                ball_direction[1] = -ball_direction[1]
            if ballRect.bottom > window_height:
                # game over
                gameOver(pygame.time.get_ticks())
                break
            
        screen.fill(black)
        screen.blit(ball, ballRect)
        screen.blit(platform, platformRect)
        clock.tick(60)
        pygame.display.flip()
    
if(__name__ == "__main__"):
    while game:
        main()