import pygame ,sys
import random

pipe_speed = 6
spawn_pipe_timer = 1000
pipe_height = [200, 250, 300]  
bird_jump_height = 8  
bg_speed = 0.5 
floor_speed = 1  
gravity_weight = 0.25 

def draw_floor():
    screen.blit(floor, (floor_x_pos, 650)) 
    screen.blit(floor, (floor_x_pos + 432, 650)) 

def draw_bg():
    screen.blit(bg, (bg_x_pos, 0))  
    screen.blit(bg, (bg_x_pos + 432, 0)) 

def create_pipe():
    random_pipe_pos = random.choice(pipe_height) 
    bot_pipe = pipe_surface.get_rect(midtop=(432, random_pipe_pos)) 
    top_pipe = pipe_surface.get_rect(midbottom=(432, random_pipe_pos - 190)) 
    return bot_pipe, top_pipe  

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= pipe_speed  
    return pipes  

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 768: 
            screen.blit(pipe_surface, pipe)  
        else:  
            flip_pipe = pygame.transform.flip(pipe_surface, False, True) 
            screen.blit(flip_pipe, pipe)  

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe): 
            die_sound.play()
            return False  
    return True  

def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement*4, 1)  
    return new_bird

def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display():
    score_surface = game_font.render(f'{int(score)}', True, (252, 160, 72))  
    score_rect = score_surface.get_rect(center=(216, 100))  
    screen.blit(score_surface, score_rect)

def gameover_display():
    gameover_rect = gameover_surface.get_rect(center=(216, 384))  
    screen.blit(gameover_surface, gameover_rect)  
    high_score_surface = game_font.render(f"High Score: {high_score}", True, (252, 160, 72))  
    high_score_rect = high_score_surface.get_rect(center=(216, 450))  
    screen.blit(high_score_surface, high_score_rect)

def startgame_display():
    startgame_surface = game_font.render("Press SPACE to Start", True, (252, 160, 72))  
    startgame_rect = startgame_surface.get_rect(center=(216, 384))  
    screen.blit(startgame_surface, startgame_rect)

pygame.mixer.pre_init()
pygame.init()
pygame.display.set_caption("Flappy Bird")
game_font = pygame.font.Font("src/04B_19.TTF", 40)

gravity = gravity_weight  
bird_movement = 0 
game_active = True
score = 0
high_score = 0
point_sound_countdown = 100

screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()

bg = pygame.image.load("src/assets/background-day.png").convert()
bg = pygame.transform.scale(bg, (432, 768)) 
bg_x_pos = 0

floor = pygame.image.load("src/assets/floor.png").convert()
floor = pygame.transform.scale2x(floor) 
floor_x_pos = 0

gameover_surface = pygame.transform.scale2x(pygame.image.load("src/assets/gameover.png").convert_alpha())

bird_down = pygame.transform.scale2x(pygame.image.load("src/assets/yellowbird-downflap.png").convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load("src/assets/yellowbird-midflap.png").convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load("src/assets/yellowbird-upflap.png").convert_alpha())
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 1
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center=(100, 384)) 


bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 200)


pipe_surface = pygame.image.load("src/assets/pipe-green.png").convert()
pipe_surface = pygame.transform.scale(pipe_surface, (100, 600))  

spawn_pipe = pygame.USEREVENT  
pygame.time.set_timer(spawn_pipe, spawn_pipe_timer)  
pipe_list = []

flap_sound = pygame.mixer.Sound("src/sound/sfx_wing.wav")

die_sound = pygame.mixer.Sound("src/sound/sfx_die.wav")

hit_sound = pygame.mixer.Sound("src/sound/sfx_hit.wav")

point_sound = pygame.mixer.Sound("src/sound/sfx_point.wav")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:  
                bird_movement = 0  
                bird_movement = -bird_jump_height  
                flap_sound.play()
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True  
                pipe_list.clear()  
                bird_rect.center = (100, 384)  
                bird_movement = 0
        if event.type == spawn_pipe:
            if game_active:
                pipe_list.extend(create_pipe())
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

    draw_bg() 
    bg_x_pos -= bg_speed  
    if bg_x_pos <= -432:  
        bg_x_pos = 0

    if game_active:  
        bird_movement += gravity  
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement 
        screen.blit(rotated_bird, bird_rect)  
        game_active = check_collision(pipe_list) 
        pipe_list = move_pipes(pipe_list)  
        draw_pipes(pipe_list)
        if bird_rect.centery >= 620:  
            bird_rect.centery = 620  
        elif bird_rect.centery <= 30: 
            bird_rect.centery = 30  
        point_sound_countdown -= 1
        if point_sound_countdown <= 0:  
            score += 1
            point_sound.play()
            point_sound_countdown = 100
        score_display()
    else:
        gameover_display()
        if score > high_score:  
            high_score = int(score)  
        score = 0
    draw_floor() 
    if floor_x_pos <= -432: 
        floor_x_pos = 0
    floor_x_pos -= floor_speed

    pygame.display.update()
    clock.tick(60) 