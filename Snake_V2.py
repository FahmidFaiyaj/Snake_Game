#import modules
import pygame
import random

#initialize pygame
pygame.init()

#initialize game variables
screen_width = 600
screen_height = 600
cell_size = 20
clock = pygame.time.Clock()
fps = 13
direction = 1 #1 is up, 2 is right, 3 is down, 4 is left
food = [0, 0]
new_food = True
new_piece = [0, 0]
score = 0
game_over = False
clicked = False

#define colors
bg = (175, 215, 70)
body_outer = (50, 50, 175)
body_inner = (100, 100, 200)
food_col = (200, 50, 50)
red = (255, 0, 0)
red2 = (200, 0, 0)
blue = (0, 0, 255)

#define fonts
font = pygame.font.SysFont(None, 40)

#define rectangles
again_rect = pygame.Rect(int(screen_width/2) - 80, int(screen_height/2), 160, 50)
exit_rect = pygame.Rect(int(screen_width/2) - 80, int(screen_height/2) + 60, 160, 50)

#create game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake')

#create snake
snake_pos = [[int(screen_width/2), int(screen_height/2)]]
snake_pos.append([int(screen_width/2), int(screen_height/2) + cell_size])
snake_pos.append([int(screen_width/2), int(screen_height/2) + cell_size * 2])
snake_pos.append([int(screen_width/2), int(screen_height/2) + cell_size * 3])

#define functions
def draw_screen():
    screen.fill(bg)

def draw_score():
    score_txt = 'Score: ' + str(score)
    score_img = font.render(score_txt, True, blue)
    screen.blit(score_img, (0, 0))
    
def check_game_over(game_over):
    #check if snake has eaten itself
    for segment in snake_pos[1:]:
        if segment == snake_pos[0]:
            game_over = True
        
    return game_over

def draw_game_over():
    over_txt = 'Game Over!'
    over_img = font.render(over_txt, True, blue)
    screen.blit(over_img, (int(screen_width/2) - 80, int(screen_height/2) - 70))
    
def draw_play_again():
    again_txt = 'Play Again'
    again_img = font.render(again_txt, True, blue)
    pos = pygame.mouse.get_pos()
    if again_rect.collidepoint(pos):
        pygame.draw.rect(screen, red2, again_rect)
    else:
        pygame.draw.rect(screen, red, again_rect)
    screen.blit(again_img, (int(screen_width/2) - 73, int(screen_height/2) + 10))
    
def draw_exit():
    exit_txt = 'Exit'
    exit_img = font.render(exit_txt, True, blue)
    pos = pygame.mouse.get_pos()
    if exit_rect.collidepoint(pos):
        pygame.draw.rect(screen, red2, exit_rect)
    else:
        pygame.draw.rect(screen, red, exit_rect)
    screen.blit(exit_img, (int(screen_width/2) - 28, int(screen_height/2) + 70))
    
def update_highscore():
    z = 0
    #if file exists, update it
    try:
        with open("snake_highscore.txt", 'r') as file:
            text = file.readlines()
            if score > int(text[0]):
                z = 1
        
        #if current score is higher, overwrite the file
        if z == 1:
            with open("snake_highscore.txt", 'w') as file:
                file.write(str(score))
            
    #if file does not exist, create it
    except FileNotFoundError:
        with open("snake_highscore.txt", 'w') as file:
            file.write(str(score))
            
def draw_highscore():
    with open("snake_highscore.txt", 'r') as file:
        text = file.readlines()
    score_txt = 'High Score: ' + text[0]
    score_img = font.render(score_txt, True, blue)
    screen.blit(score_img, (int(screen_width/2) - 90, int(screen_height/2) - 35))

#game loop
run = True
while run:
    
    draw_screen()
    
    #iterate through events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 3:
                direction = 1
            if event.key == pygame.K_RIGHT and direction != 4:
                direction = 2
            if event.key == pygame.K_DOWN and direction != 1:
                direction = 3
            if event.key == pygame.K_LEFT and direction != 2:
                direction = 4
            
    #check collision of snake head with food
    if snake_pos[0] == food:
        new_food = True
        #create a new segment at the end of the snake's tail
        if direction == 1:
            new_piece = [snake_pos[-1][0], snake_pos[-1][1] + cell_size]
        if direction == 2:
            new_piece = [snake_pos[-1][0] - cell_size, snake_pos[-1][1]]
        if direction == 3:
            new_piece = [snake_pos[-1][0], snake_pos[-1][1] - cell_size]
        if direction == 4:
            new_piece = [snake_pos[-1][0] + cell_size, snake_pos[-1][1]]
        snake_pos.append(new_piece)
        
        #increase score
        score += 1
            
    #create food
    if new_food == True:
        new_food = False
        food[0] = cell_size * random.randint(0, (screen_width / cell_size) - 1)  #subtract 1 to prevent food going off-screen
        food[1] = cell_size * random.randint(0, (screen_height / cell_size) - 1)
        
    #draw food
    pygame.draw.rect(screen, food_col, (food[0], food[1], cell_size, cell_size))
    
    #update snake position
    if game_over == False:
        z = len(snake_pos)
        #update snake list except the head
        for i in range(z-1):
            #equate each snake segment to it's previous segment except the head
            snake_pos[z-i-1][0] = snake_pos[z-i-2][0] 
            snake_pos[z-i-1][1] = snake_pos[z-i-2][1]
            #reposition snake segments if out of boundary
            if snake_pos[z-i-1][0] < 0:
                snake_pos[z-i-1][0] = screen_width - cell_size
            if snake_pos[z-i-1][0] > (screen_width - cell_size):
                snake_pos[z-i-1][0] = 0
            if snake_pos[z-i-1][1] < 0:
                snake_pos[z-i-1][1] = screen_height - cell_size
            if snake_pos[z-i-1][1] > (screen_height - cell_size):
                snake_pos[z-i-1][1] = 0
      
        #update position of snake head based on direction
        if direction == 1:
            snake_pos[0][0] = snake_pos[1][0]
            snake_pos[0][1] = snake_pos[1][1] - cell_size
            if snake_pos[0][1] < 0:
                snake_pos[0][1] = screen_height - cell_size
        if direction == 2:
            snake_pos[0][0] = snake_pos[1][0] + cell_size
            snake_pos[0][1] = snake_pos[1][1]
            if snake_pos[0][0] > (screen_width - cell_size):
                snake_pos[0][0] = 0
        if direction == 3:
            snake_pos[0][0] = snake_pos[1][0]
            snake_pos[0][1] = snake_pos[1][1] + cell_size
            if snake_pos[0][1] > (screen_height - cell_size):
                snake_pos[0][1] = 0
        if direction == 4:
            snake_pos[0][0] = snake_pos[1][0] - cell_size
            snake_pos[0][1] = snake_pos[1][1]
            if snake_pos[0][0] < 0:
                snake_pos[0][0] = screen_width - cell_size
        
        #check for game over condition
        game_over = check_game_over(game_over)
    
    #draw snake
    for x in snake_pos:
            pygame.draw.rect(screen, body_outer, (x[0], x[1], cell_size, cell_size))
            pygame.draw.rect(screen, body_inner, (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))
    
    #check for game over
    if game_over:
        
        draw_game_over()
        
        draw_play_again()
        
        draw_exit()
        
        update_highscore()
        
        draw_highscore()
        
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            clicked = False
            pos = pygame.mouse.get_pos()
            if again_rect.collidepoint(pos):
                #reset game variables
                direction = 1 #1 is up, 2 is right, 3 is down, 4 is left
                food = [0, 0]
                new_food = True
                new_piece = [0, 0]
                score = 0
                game_over = False
                clicked = False
                #reset snake
                snake_pos = [[int(screen_width/2), int(screen_height/2)]]
                snake_pos.append([int(screen_width/2), int(screen_height/2) + cell_size])
                snake_pos.append([int(screen_width/2), int(screen_height/2) + cell_size * 2])
                snake_pos.append([int(screen_width/2), int(screen_height/2) + cell_size * 3])
            if exit_rect.collidepoint(pos):
                run = False
    
    draw_score()
    
    #update the display
    pygame.display.update()
    clock.tick(fps)
    
#end pygame
pygame.quit()