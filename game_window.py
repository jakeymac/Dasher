import pygame
from pygame.locals import *
import random
import os
import time

objectSize = 25

pygame.init()

top_triangle_image = pygame.image.load(os.path.join("images","blue_triangle_black_background.jpeg"))
top_triangle_image = pygame.transform.scale(top_triangle_image,(50,50))
top_triangle_image.set_colorkey((0,0,0))

bottom_triangle_image = pygame.image.load(os.path.join("images","red_triangle_black_background.jpeg"))
bottom_triangle_image = pygame.transform.scale(bottom_triangle_image,(50,50))
bottom_triangle_image.set_colorkey((0,0,0))

class Game_Window():
    def __init__(self,color_choice):
        W = 1000
        H = 600
        self.window = pygame.display.set_mode((W,H))
        pygame.display.set_caption("Dasher")

        self.bg = pygame.image.load(os.path.join("images","bg.png")).convert()
        self.bgX = 0
        self.bgX2 = self.bg.get_width()

        self.clock = pygame.time.Clock()
        pygame.time.set_timer(USEREVENT+1, 500)
        pygame.time.set_timer(USEREVENT+2,random.randrange(2000,3500))

        self.dasher = Dasher(color_choice,50,50)

        self.obstacles = []
        
        self.start_game()
    
    def end_game(self):
        end_screen_open = True
        end_of_game_time = time.time()
        score = end_of_game_time - self.start_of_game_time
        end_game_surface = pygame.display.set_mode((500,500))
        font = pygame.font.Font(None,24)
        first_line = font.render('Game Over!',(255,0,0),(0,0,0))
        second_line = font.render(f"Your time was: {round(score,2)} seconds",(255,0,0),(0,0,0))
        third_line = font.render("Press any key to return to main menu",(255,0,0),(0,0,0))

        while end_screen_open:
            end_game_surface.fill((255,255,255))
            
            end_game_surface.blit(first_line,(170,250))
            end_game_surface.blit(second_line,(100,265))
            end_game_surface.blit(third_line,(95,280))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
    
            # deactivates the pygame library
                    pygame.quit()
                    # quit the program.
                    quit()
                if event.type == pygame.KEYDOWN:
                    print("keysss")
                    end_screen_open = False
           
                pygame.display.update()

    def start_game(self):
       
        playing = True
        self.speed = 30

        self.start_of_game_time = time.time()

        while playing:
            self.update_window()
            self.bgX -= 1.4
            self.bgX2 -= 1.4

            for obstacle in self.obstacles:
                obstacle.x -= 1.4
                if obstacle.x < obstacle.width * -1:
                    self.obstacles.pop(self.obstacles.index(obstacle)) 

                if obstacle.collide(self.dasher):
                    playing = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                if not(self.dasher.jumping):
                    self.dasher.jumping = True

            if self.bgX < self.bg.get_width() * -1:
                self.bgX = self.bg.get_width()
        
            if self.bgX2 < self.bg.get_width() * -1:
                self.bgX2 = self.bg.get_width()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                    pygame.quit()
                    quit()

                if event.type == USEREVENT + 1:
                    self.speed += 1

                if event.type == USEREVENT + 2:
                    choice = random.randrange(0,2)
                    if choice == 0:
                        self.obstacles.append(Triangle(1010,500,50,50,"top"))
                    else:
                        self.obstacles.append(Triangle(1010,550,50,50,"bottom"))
            
        
            self.clock.tick(self.speed)
        self.end_game()
        
    def update_window(self):
        self.window.blit(self.bg,(self.bgX,0))
        self.window.blit(self.bg,(self.bgX2,0))
        self.dasher.draw(self.window)
        
        for obstacle in self.obstacles:
            obstacle.draw(self.window)

        pygame.display.update()
        
class Dasher(object):
    def __init__(self,color_choice,width,height):
        #self.avatar = pygame.image.load(os.path.join("images",avatar_choice+".png"))
        #self.avatar = pygame.transform.scale(self.avatar, (50,50))
        self.avatar = pygame.Rect(50,550,50,50)
        self.color_choice = color_choice

        self.jumplist = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,
                3,3,3,3,3,3,3,3,3,3,3,3,
                4,4,4,4,4,4,4,4,4,4,4,4,
                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                -1,-1,-1,-1,-1,-1,
                -2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,
                -3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,
                -4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]

        self.width = width
        self.height = height

        self.jumping = False
        self.jumpcount = 0

        self.x = 75
        self.y = 575

    def draw(self,window):
        self.hitbox = [self.x-25,self.y-25,50,49]
        if self.jumping:
            self.avatar.move_ip(0,-self.jumplist[self.jumpcount]*1.2)
            self.y -= self.jumplist[self.jumpcount] * 1.2
            self.jumpcount += 1
            if self.jumpcount > len(self.jumplist) - 1:
                self.jumpcount = 0
                self.jumping = False

        pygame.draw.rect(window,self.color_choice,self.avatar,2)

class Triangle():
    def __init__(self,x,y,width,height,side):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 1.4
        self.side = side

    def draw(self,window):
        if self.side == "bottom":
            self.hitbox = (self.x+25,self.y,2,48)
            window.blit(bottom_triangle_image,(self.x,self.y))
        if self.side == "top":
            self.hitbox = (self.x+25,self.y,2,48)
            window.blit(top_triangle_image,(self.x,self.y))

    def collide(self, player):
        if player.x >= self.x and player.x <= self.x+50:
            if self.side == "top":
                if player.y >=self.y and player.y <= self.y+50:
                    return True
            if self.side == "bottom":
                if player.y >= self.y:
                    return True        
        