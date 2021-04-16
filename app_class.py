import sys
import pygame
from settings import *
from player_class import *
from enemy_class import *

# initialise tuos les modules pygames importés
pygame.init()
# Vecteur 2D
vec = pygame.math.Vector2

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = MAZE_WIDTH//COLUMNS
        self.cell_height = MAZE_HEIGHT//ROWS
        self.walls = []
        self.coins = []
        self.enemies = []
        self.e_pos = []
        self.p_pos = None
        
        self.load()
        # self.player = Player(self, self.p_pos)
        self.player = Player(self, vec(self.p_pos))
        self.make_enemies()

        
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
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
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
                        self.p_pos = [xidx,yidx]
                    elif char in ["2","3","4","5"]:
                        self.e_pos.append([xidx, yidx])
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (xidx * self.cell_width, yidx * self.cell_height, self.cell_width, self.cell_height))
        # print(len(self.walls))
    
    def make_enemies(self):
        # self.enemies.append(Enemy())
        for idx, pos in enumerate(self.e_pos) :
            self.enemies.append(Enemy(self, vec(pos), idx))
            print('enemy spawned')
            
        
    # Grillage du jeu
    def draw_grid(self):
        # les cellules grises
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, GREY, (x*self.cell_width , 0), ( x*self.cell_width, HEIGHT))
    
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.background, GREY, (0 , x*self.cell_height), ( WIDTH, x*self.cell_height))
        
        
        for wall in self.walls:
            pygame.draw.rect(self.background, BLUE, (wall.x * self.cell_width, 
                                                             wall.y * self.cell_height,
                                                             self.cell_width,
                                                             self.cell_height))      

     # reset le jeu
    def reset(self):
        self.player.lives = 3
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0
        
        self.coins = []
        with open('walls.txt',  'r' ) as file :
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
        self.state = "playing"


# Fonctions intro

    def start_events(self):
        for event in pygame.event.get():
            # si le joueur clic sur l'icone fermer alors le jeu quitte
            if event.type == pygame.QUIT:
                self.running = False
            # si le joueur appuie sur la barre espace alors le jeu peut se lancer
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.running = False
    
    
    def start_update(self):
        pass       
    
    
    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PUSH SPACE BAR', self.screen, [WIDTH//2, HEIGHT//2], START_TEXT_SIZE , (170,132,58), START_FONT, centered=True)
        self.draw_text('1 PLAYER ONLY', self.screen, [WIDTH//2, HEIGHT//2+50], START_TEXT_SIZE , (44,167,195), START_FONT,  centered=True)
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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.running = False
            
    
    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            # print(enemy)
            enemy.update()
            
        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()
    
    def playing_draw(self):
        self.screen.fill(BLACK)
        # affiche l'image de la map
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        
        self.draw_grid()
        self.draw_coins()
        
        # affiche HUD
        self.draw_text("CURRENT SCORE : {}".format(self.player.current_score), self.screen, [25,2], START_TEXT_SIZE , WHITE, START_FONT)
        # affiche le joueur
        self.player.draw()
        
        # dessinne les enemies
        for enemy in self.enemies:
            enemy.draw() 
            
        pygame.display.update()
        
        
    # crée les pieces
    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, 
                               GREEN, 
                               (int(coin.x*self.cell_width) + self.cell_width//2 + TOP_BOTTOM_BUFFER//2,
                                int( coin.y*self.cell_height)+ self.cell_height//2 + TOP_BOTTOM_BUFFER//2),
                               3)
            
    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = "game over"
            # self.running = False
        else :
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0
            

# Fonctions Game Over
    def game_over_events(self):
        for event in pygame.event.get():
            # si le joueur clic sur l'icone fermer alors le jeu quitte
            if event.type == pygame.QUIT:
                self.running = False
            # si le joueur appuie sur la barre espace alors le jeu peut se lancer
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.running = False
    
    
    def game_over_update(self):
        pass       
    
    
    def game_over_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('GAME OVER', self.screen, [WIDTH//2, 100], 25 , RED, START_FONT, centered=True)
        self.draw_text('PUSH SPACE BAR', self.screen, [WIDTH//2, HEIGHT//2], START_TEXT_SIZE , (170,132,58), START_FONT, centered=True)

        
        pygame.display.update()
        