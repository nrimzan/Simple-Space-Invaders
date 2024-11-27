import pygame
import random
import time

#Initialize Pygame
pygame.init()

#Screen dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("Space Invaders")
running = True

#Font
font = pygame.font.Font("freesansbold.ttf", 32)
game_over_font = pygame.font.Font("freesansbold.ttf", 100)
game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))

#Background
background = pygame.image.load('Graphics/Items/Background.jpg')
stars_background = pygame.transform.scale(background, (800, 600))

#Player define
player_image = pygame.image.load("Graphics/Items/player.gif")  # Load a spaceship image
player_rect = player_image.get_rect(midbottom = (400, 590)) 
player_speed = 5

#Enemy define
enemy_image = pygame.image.load("Graphics/Items/enemy.png")
enemy_png = pygame.transform.scale(enemy_image, (100, 100))
enemy_rect = enemy_png.get_rect(midbottom = (200, 100))
enemy_speed = 4

#Bullet define
bullet_width, bullet_height = 10, 10
bullet_speed = 4
bullets = []  # List to hold active bullets 
max_bullets = 5

#Score define
score = 0
def show_score():
    score_display = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_display, (10, 10))

#Main game loop
while running:
    #Process player inputs
    for event in pygame.event.get():
        #pygame.QUIT means user clicks 'x' on window tab
        if event.type == pygame.QUIT:
            running = False
        
            #Control bullet
            #Fire bullet on spacebar press
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            if len(bullets) < max_bullets:
                bullet = pygame.Rect(
                player_rect.centerx, player_rect.y, bullet_width, bullet_height
            ) #x pos, y pos, size of bullets
                bullets.append(bullet)
                
    screen.blit(stars_background,(0, 0))

    #Control player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.left -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < screen_width:  # Assuming player width is 64
        player_rect.right += player_speed
    screen.blit(player_image, player_rect)

    #Update bullet positions
    for bullet in bullets[:]:  #Iterate over a copy of the list
        bullet.y -= bullet_speed
        #Collision bullet & enemy
        if bullet.colliderect(enemy_rect):
            enemy_rect = enemy_png.get_rect(midbottom = (random.randint(0,700), 100))
            score += 1
        if bullet.bottom < 0:  #Remove bullet if it moves off screen
            bullets.remove(bullet)

    #Enemy updates movement
    enemy_rect.x += enemy_speed
    if enemy_rect.x <= -50 or enemy_rect.x >= screen_width - 50:
        enemy_speed *= -1  # Change direction
        enemy_rect.y += 50  # Move down when changing direction
    
    #Collision enemy & player
    if player_rect.colliderect(enemy_rect):
        pygame.display.update()
        screen.fill((0, 0, 0))
        screen.blit(game_over_text, (100, 200))
        time.sleep(2)
        pygame.display.update()
        break
    
    #Bullet spawn on screen
    for bullet in bullets:
        pygame.draw.rect(screen, (255,0,0), bullet)
    
    #Render graphics here
    #Update the screen
    screen.blit(enemy_png, enemy_rect)
    #Call show_score() in the game loop
    show_score()
    pygame.display.update()  #refresh screen
    clock.tick(60)  # limits FPS to 60

pygame.quit()