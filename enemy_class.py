import pygame, random
from settings import *
from queue import PriorityQueue

vec = pygame.math.Vector2

class Enemy:
    def __init__(self, app , pos , number):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.radius = int(self.app.cell_width//2.3)
        self.number = number
        self.colour = self.set_colour()
        self.direction = vec(0,0)
        self.personality = self.set_personality()
        # self.personality = "speedy"
        # print(self.personality)
        self.target = None
        self.speed = self.set_speed()
        self.starting_pos = [pos.x, pos.y]
    
          
    def update(self):
        self.target = self.set_target()
        # si l'ennemi n'est pas sur le joueur
        if self.target != self.grid_pos:
            # aller dans la direction du joueur + la vitesse
            self.pix_pos += self.direction * self.speed
            if self.time_to_move():
                self.move()
        
        # Set grid position in ref to pix position
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER + self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER + self.app.cell_height // 2) // self.app.cell_height + 1
        
    
    def draw(self):
        pygame.draw.circle(self.app.screen, 
                           self.colour, 
                           (int(self.pix_pos.x), int(self.pix_pos.y)), 
                           self.radius)

    def set_target(self):
        
        # Cible le joueur
        # if self.personality == "speedy" or self.personality == "slow" :
            return self.app.player.grid_pos
        # S'eloigne du joueur
        # else : 
        #     if self.app.player.grid_pos[0] > COLUMNS//2 and self.app.player.grid_pos[1] > ROWS//2:
        #         return vec(1,1)
        #     if self.app.player.grid_pos[0] > COLUMNS//2 and self.app.player.grid_pos[1] < ROWS//2:
        #         return vec(1, ROWS - 2)
        #     #    return vec(1, -1)
        #     if self.app.player.grid_pos[0] < COLUMNS//2 and self.app.player.grid_pos[1] > ROWS//2:
        #         return vec( COLUMNS - 2 , 1 )
        #     #     return vec( -1 , 1 )
        #     else :
        #         return vec( COLUMNS-2 , ROWS-2 )
        #     # return vec( -1, -1 )
        
    def set_speed(self):
        if self.personality ==  "speedy":
            speed =2
        else:
            speed = 1
        return  speed
        
    def get_pix_pos(self):
        return  vec((self.grid_pos.x * self.app.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2 ,
                (self.grid_pos.y * self.app.cell_height) + TOP_BOTTOM_BUFFER //2 + self.app.cell_height // 2)


    def set_colour(self):
        if self.number == 0:
            return ORANGE
        if self.number == 1:
            return PINK
        # if self.number == 2:
        #     return BROWN
        # if self.number == 3:
        #     return BLUE
        
    
    def set_personality(self):
        if self.number == 0 :
            return "speedy"
        if self.number == 1 :
            return "slow"
        
    
    def time_to_move(self):
        # colision avec les murs
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0 :
            if self.direction == vec(1,0) or self.direction == vec(-1, 0) or self.direction == vec(0,0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0 :
            if self.direction == vec(0,1) or self.direction == vec(0, -1) or self.direction == vec(0,0):
                return True
        return False

    
    def move(self):
        if self.personality == "slow":
            self.direction = self.get_path_direction(self.target)
        if self.personality == "speedy":
            self.direction = self.get_path_direction(self.target)
            
    
    # IA enemy
    def get_path_direction(self ,target):
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]
        return vec(xdir, ydir)
    
    def find_next_cell_in_path(self, target):
        path = self.bfs(
                        # start
                        [int(self.grid_pos.x), int(self.grid_pos.y)], 
                        # target
                        [int(target[0]), int(target[1])])
        return path[1]
        # path = self.dfs(
        #                 # start
        #                 [int(self.grid_pos.x), int(self.grid_pos.y)], 
        #                 # target
        #                 [int(target[0]), int(target[1])])
        # return path[1]
    
    # depth first search *** pas fini ***
    def dfs(self,start, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
                
        for y in range(30):
            for x in range(28):
                print(grid[int(y)][int(x)], end=' ')
            print()
                
        visited = []
        path = []
        queue = PriorityQueue()
        queue.put(( 0 , start, path , visited))
        
        # print('visited' , visited)
        # print('path' , path)
        print('queue empty' , queue.empty())
        
        while not queue.empty():
            depth , current_node , path, visited = queue.get() 
            visited.append(current_node)
            
            print('visited' , visited)
            
            # child_nodes = grid[current_node[0]][current_node[1]]

            
            # print('current_node == target' , current_node , target)

            if current_node == target:
                print(path + [current_node])
                break
                
            
            child_nodes = [[0, -1], [1, 0], [0, 1], [-1, 0]]
            print('child_nodes = ' , child_nodes)

            for node in child_nodes:
                print("****** ", node , " ******")
                if node not in visited:
                    print('visited' , visited)
                    if node == target:
                        return path + [node]
                    depth_of_node = len(path)
                    queue.put((-depth_of_node, node, path + [node], visited))
                    print(queue.get())
        
        print(path)
        return path  
        # return 'rien'  
                
            
    
    # breadth first search
    def bfs(self , start, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
                
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            # Si la current cellule et sur la cellule cible
            if current == target:
                break
            else:
                # verifications des noeuds enfants
                # [ HAUT , DROIT , BAS , GAUCHE]
                nodes = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for node in nodes:
                    # Si noeud[pos_x] + current[pos_x] sup ou egale à 0 et inf à len(grid[0])=28
                    if node[0]+current[0] >= 0 and node[0] + current[0] < len(grid[0]):
                        # Si noeud[pos_y] + current[pos_x] sup ou egale à 0 et inf à len(grid)=30
                        if node[1]+current[1] >= 0 and node[1] + current[1] < len(grid):
                            # nouvelle position
                            next_cell = [node[0] + current[0], node[1] + current[1]]
                            # Si la nouvelle position n'a pas ete visité
                            if next_cell not in visited:
                                # Si la prochaine position n'est pas un mur
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest 
        # print('shortest', shortest)      
                        
                        
            
        