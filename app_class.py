import sys
import pygame
from settings import *


pygame.init()
# vec = pygame.math.Vector2

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = MAZE_WIDTH//27
        self.cell_height = MAZE_HEIGHT//30
        
        self.load()
        
    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            else:
                pass
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
        
# Fonctions Helper
    def draw_text(self, words, screen, pos, size, colour, font_name, centered = False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0]//2
            pos[1] = pos[1] - text_size[1]//2
        screen.blit(text, pos)
        
    def load(self):
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        
    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.screen, GREY, (x*self.cell_width , 0), ( x*self.cell_width, HEIGHT))
    
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.screen, GREY, (0 , x*self.cell_height), ( WIDTH, x*self.cell_height))
    


# Fonctions intro

    def start_events(self):
        for event in pygame.event.get():
            # si le joueur clic sur l'icone fermer alors le jeu quitte
            if event.type == pygame.QUIT:
                self.running = False
            # si le joueur appuie sur la barre espace alors le jeu peut se lancer
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'
    
    def start_update(self):
        pass       
    
    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PUSH SPACE BAR', self.screen, [WIDTH//2, HEIGHT//2], START_TEXT_SIZE , (170,132,58), START_FONT, centered=True)
        self.draw_text('1 PLAYER ONLY', self.screen, [WIDTH//2, HEIGHT//2+50], START_TEXT_SIZE , (44,167,195), START_FONT,  centered=True)
        self.draw_text('HIGH SCORE', self.screen, [4,0], 12 , (255,255,255), START_FONT)
        pygame.display.update()     
        


# Fonctions jeu

    def playing_events(self):
        for event in pygame.event.get():
            # si le joueur clic sur l'icone fermer alors le jeu quitte
            if event.type == pygame.QUIT:
                self.running = False
    
    def playing_update(self):
        pass       
    
    def playing_draw(self):
        self.screen.blit(self.background, (0,0))
        self.draw_grid()
        pygame.display.update()  