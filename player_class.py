from settings import *
import pygame
vec = pygame.math.Vector2


class Player:
    def __init__(self, app, pos):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(1,0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        
        
        
    def update(self):
        if self.able_to_move :
            self.pix_pos += self.direction * self.speed
    
        if self.time_to_move() :
            if self.stored_direction != None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()
            
        # tracking du joueur (rectangle sur cercle)
        # grille position en réfence de la position des pixels
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER + self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER + self.app.cell_height // 2) // self.app.cell_height + 1
        
        if self.on_coin():
            self.eat_coin()

    def draw(self):
        pygame.draw.circle(
            # surface
            self.app.screen, 
            # color
            PLAYER_COLOUR, 
            # vecteur
            (int(self.pix_pos.x), int(self.pix_pos.y)), 
            self.app.cell_width//2 - 2 )
        
        # # grille possition
        # pygame.draw.rect(
        #     # surface
        #     self.app.screen,
        #     # color 
        #         WHITE, 
        #     # positions 
        #         (self.grid_pos[0] * self.app.cell_width + TOP_BOTTOM_BUFFER//2 ,
        #         self.grid_pos[1] * self.app.cell_height + TOP_BOTTOM_BUFFER//2, 
        #     # dimensions
        #         self.app.cell_width,
        #         self.app.cell_height), 
        #     # width : 
        #     # if width == 0, (default) fill the rectangle
        #     # if width > 0, used for line thickness
        #     # if width < 0, nothing will be drawn
        #     1)
        
    def move(self, direction):
        self.stored_direction = direction
        
    # Position en pixel dans une cellule
    def get_pix_pos(self):
        return  vec((self.grid_pos.x * self.app.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2 ,
                    (self.grid_pos.y * self.app.cell_height) + TOP_BOTTOM_BUFFER //2 + self.app.cell_height // 2)
        print(self.grid_pos, self.pix_pos)
    
    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0 :
            if self.direction == vec(1,0) or self.direction == vec(-1, 0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0 :
            if self.direction == vec(0,1) or self.direction == vec(0, -1):
                return True
            
    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True
    
    def on_coin(self):
        if self.grid_pos in self.app.coins :
            # return True
            
            
            # Pour etre plus precis lorsque le joueur touche la coin
            if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0 :
                if self.direction == vec(1,0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y + TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0 :
                if self.direction == vec(0,1) or self.direction == vec(0, -1):
                    return True
        return False
            
    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 1
        # print(self.current_score)
