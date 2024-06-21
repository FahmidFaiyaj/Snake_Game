#import modules
import pygame
import random

#initialize pygame
pygame.init()

#initialize game variables
screen_width = 600
screen_height = 600
cell_size = 20
rows = int(screen_height / cell_size)
cols = int(screen_width / cell_size)
clock = pygame.time.Clock()
fps = 13
levels = 5
level = []
level_data = []
pass_score = [5, 10, 15, 20, 25]
exclude_list = []
exclude_obstacle = []

#initialize logic variables
direction = 1 #1 is up, 2 is right, 3 is down, 4 is left
food = [0, 0]
new_food = True
new_piece = [0, 0]
score = 0
game_over = False
game_win = False
clicked = False
level_current = 1

#fill level_data matrix with data from level_i.txt files
for i in range(levels):
    count = 0
    level = []
    with open("Snake_V3_files/Level_" + str(i+1) + ".txt", 'r') as file:
        for line in file:
            # Split the line into individual numbers, convert them to integers
            row = [int(num) for num in line.split()]
            level.insert(count, row)
            count += 1
    level_data.insert(i, level)

#store the coordinates of all obstacles at each level in exclude_list
for i in range(levels):
    tmp_list = []
    tmp_obstacle = []
    count = 0
    for j in range(rows):
        for k in range(cols):
            if level_data[i][j][k] == 1:
                tmp_list.insert(count, [k, j])
                tmp_obstacle.insert(count, [k * cell_size, j * cell_size])
                count += 1
    exclude_list.insert(i, tmp_list)
    exclude_obstacle.insert(i, tmp_obstacle)     

#define colors
bg = (175, 215, 70)
body_outer = (50, 50, 175)
body_inner = (100, 100, 200)
food_col = (200, 50, 50)
red = (255, 0, 0)
red2 = (200, 0, 0)
blue = (0, 0, 255)
brown = (150, 75, 0)
dark_brown = (175, 100, 0)

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
    
def draw_level():
    for i in range(rows):
        for j in range(cols):
            if level_data[level_current-1][i][j] == 0:
                pygame.draw.rect(screen, bg, (j * cell_size, i * cell_size, cell_size, cell_size))
            if level_data[level_current-1][i][j] == 1:
                pygame.draw.rect(screen, brown, (j * cell_size, i * cell_size, cell_size, cell_size))
                pygame.draw.rect(screen, dark_brown, (j * cell_size + 1, i * cell_size + 1, cell_size - 2, cell_size - 2))

def draw_score():
    level_txt = 'Level: ' + str(level_current)
    level_img = font.render(level_txt, True, blue)
    score_txt = 'Score: ' + str(score)
    score_img = font.render(score_txt, True, blue)
    screen.blit(level_img, (0, 0))
    screen.blit(score_img, (0, 35))
    
def check_game_over(game_over):
    #check if snake head collides with itself
    for segment in snake_pos[1:]:
        if segment == snake_pos[0]:
            return True
    
    if list_in_list(snake_pos[0], exclude_obstacle[level_current - 1]):
        return True
    
    return game_over

def draw_game_over():
    over_txt = 'Game Over!'
    over_img = font.render(over_txt, True, blue)
    screen.blit(over_img, (int(screen_width/2) - 80, int(screen_height/2) - 70))
    
def draw_winner():
    win_txt = 'Winner!'
    win_img = font.render(win_txt, True, blue)
    screen.blit(win_img, (int(screen_width/2) - 50, int(screen_height/2) - 70))
    
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
        with open("Snake_V3_files/snake_highscore.txt", 'r') as file:
            text = file.readlines()
            if (level_current > int(text[0].strip())) or ((level_current == int(text[0].strip())) and score > int(text[1])):
                z = 1
        
        #if current score is higher, overwrite the file
        if z == 1:
            with open("Snake_V3_files/snake_highscore.txt", 'w') as file:
                file.write(str(level_current) + "\n" + str(score))
            
    #if file does not exist, create it
    except FileNotFoundError:
        with open("Snake_V3_files/snake_highscore.txt", 'w') as file:
            file.write(str(level_current) + "\n" + str(score))
            
def draw_highscore():
    with open("Snake_V3_files/snake_highscore.txt", 'r') as file:
        text = file.readlines()
    score_txt = 'Highscore: (L, S) = (' + text[0].strip() + ', ' + text[1] + ')'
    score_img = font.render(score_txt, True, blue)
    gap = 0
    if int(text[1]) >= 10:
        gap = 10
    screen.blit(score_img, (int(screen_width/2) - 155 - gap, int(screen_height/2) - 35))

#function to check if a tuple is within a list of tuples
def list_in_list(list_to_find, list_of_lists):
    return list_to_find in list_of_lists

#game loop
run = True
while run:
    
    draw_screen()
    
    draw_level()
    
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
        if score == pass_score[level_current - 1]:
            level_current += 1
            if level_current == levels + 1:
                level_current -= 1
                game_over = True
                game_win = True
            else :
                #reset logic variables
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
            
    #create food
    if new_food == True:
        new_food = False
        food[0] = random.randint(0, (screen_width / cell_size) - 1)  #subtract 1 to prevent food going off-screen
        food[1] = random.randint(0, (screen_height / cell_size) - 1)
        while 1:
            #check whether food coincides with any obstacle
            if list_in_list(food, exclude_list[level_current - 1]):
                food[0] = random.randint(0, (screen_width / cell_size) - 1)  
                food[1] = random.randint(0, (screen_height / cell_size) - 1)
            else:
                food[0] = cell_size * food[0]
                food[1] = cell_size * food[1]
                break;
        
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
        if game_win:
            draw_winner()
        else: 
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
                #reset logic variables
                direction = 1 #1 is up, 2 is right, 3 is down, 4 is left
                food = [0, 0]
                new_food = True
                new_piece = [0, 0]
                score = 0
                game_over = False
                game_over = False
                clicked = False
                level_current = 1
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