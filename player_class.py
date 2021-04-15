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
        
        
    def update(self):
        self.pix_pos += self.direction
        
        # tracking du joueur (rectangle sur cercle)
        # grille position en réfence de la position des pixels
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER + self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER + self.app.cell_height // 2) // self.app.cell_height + 1
        
    def draw(self):
        pygame.draw.circle(
            # surface
            self.app.screen, 
            # color
            PLAYER_COLOUR, 
            # vecteur
            (int(self.pix_pos.x), int(self.pix_pos.y)), 
            self.app.cell_width//2 - 2 )
        
        # grille possition
        pygame.draw.rect(
            # surface
            self.app.screen,
            # color 
                RED, 
            # positions 
                (self.grid_pos[0] * self.app.cell_width + TOP_BOTTOM_BUFFER//2 ,
                self.grid_pos[1] * self.app.cell_height + TOP_BOTTOM_BUFFER//2, 
            # dimensions
                self.app.cell_width,
                self.app.cell_height), 
            # width : 
            # if width == 0, (default) fill the rectangle
            # if width > 0, used for line thickness
            # if width < 0, nothing will be drawn
            1)
        
    def move(self, direction):
        self.direction = direction
        
    # Position en pixel dans une cellule
    def get_pix_pos(self):
        return  vec((self.grid_pos.x * self.app.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2 ,
                    (self.grid_pos.y * self.app.cell_height) + TOP_BOTTOM_BUFFER //2 + self.app.cell_height // 2)
        print(self.grid_pos, self.pix_pos)