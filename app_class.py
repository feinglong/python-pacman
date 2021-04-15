import sys
import pygame
from settings import *
from player_class import *


pygame.init()
vec = pygame.math.Vector2

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = MAZE_WIDTH//28
        self.cell_height = MAZE_HEIGHT//30
        self.walls = []
        self.coins = []
        self.p_pos = None
        
        self.load()
        self.player = Player(self, self.p_pos)

        
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

    # Ecriture d'un texte
    def draw_text(self, words, screen, pos, size, colour, font_name, centered = False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0]//2
            pos[1] = pos[1] - text_size[1]//2
        screen.blit(text, pos)
    
    # Chargement de la map en background
    def load(self):
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))
        
        # On ouvre le fichier walls.txt et on crée les coordonées des murs
        with open('walls.txt',  'r' ) as file :
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx , yidx))
                    elif char == "C":
                        self.coins.append(vec(xidx, yidx))
                    elif char == "P":
                        self.p_pos =vec(xidx,yidx)
        # print(len(self.walls))
    
        
    # Grillage du jeu
    def draw_grid(self):
        # les cellules grises
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, GREY, (x*self.cell_width , 0), ( x*self.cell_width, HEIGHT))
    
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.background, GREY, (0 , x*self.cell_height), ( WIDTH, x*self.cell_height))
        
        
        # for wall in self.walls:
        #     pygame.draw.rect(self.background, (112,55,163), (wall.x * self.cell_width, 
        #                                                      wall.y * self.cell_height,
        #                                                      self.cell_width,
        #                                                      self.cell_height))    
        # for coin in self.coins:
        #     pygame.draw.rect(self.background, YELLOW, (coin.x * self.cell_width, 
        #                                                      coin.y * self.cell_height,
        #                                                      self.cell_width,
        #                                                      self.cell_height))    



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
        self.draw_text('HIGH SCORE', self.screen, [4,0], 12 , WHITE, START_FONT)
        pygame.display.update()     
        


# Fonctions jeu

    def playing_events(self):
        for event in pygame.event.get():
            # si le joueur clic sur l'icone fermer alors le jeu quitte
            if event.type == pygame.QUIT:
                self.running = False
            # mouvements du joueur en appuyant sur les fleches directionnels
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1,0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0,-1))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1,0))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0,1))
            
    
    def playing_update(self):
        self.player.update()
    
    def playing_draw(self):
        self.screen.fill(BLACK)
        # affiche l'image de la map
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        
        self.draw_grid()
        self.draw_coins()
        
        # affiche HUD
        self.draw_text("CURRENT SCORE : {}".format(self.player.current_score), self.screen, [25,2], START_TEXT_SIZE , WHITE, START_FONT)
        self.draw_text('HIGH SCORE : 0', self.screen, [WIDTH//2,2], START_TEXT_SIZE , WHITE, START_FONT)
        # affiche le joueur
        self.player.draw()
        pygame.display.update()
        
    # crée les pieces
    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, 
                               GREEN, 
                               (int(coin.x*self.cell_width) + self.cell_width//2 + TOP_BOTTOM_BUFFER//2,
                                int( coin.y*self.cell_height)+ self.cell_height//2 + TOP_BOTTOM_BUFFER//2),
                               3)