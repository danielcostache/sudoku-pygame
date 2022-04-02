import pygame
import os
import numpy as np

pygame.font.init()
FONT = pygame.font.SysFont('comicsans', 40)
WIDTH, HEIGHT = 800, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sudoku')

CELL_SIZE = WIDTH/9
GRID_SIZE = WIDTH/3

FPS = 60

default_grid = np.transpose(np.array([
        [2, 1, 0, 0, 0, 0, 4, 0, 0],
        [3, 8, 0, 4, 0, 0, 7, 0, 2],
        [0, 0, 0, 7, 2, 0, 0, 0, 0],
        [0, 2, 4, 8, 0, 6, 9, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 2, 0, 3, 5, 4, 0],
        [0, 0, 0, 0, 5, 8, 0, 0, 0],
        [9, 0, 3, 0, 0, 4, 0, 2, 8],
        [0, 0, 8, 0, 0, 0, 0, 5, 7],
    ]))

class Board:
    def __init__(self):
        self.grid = default_grid
        self.seed = np.arange(1, 10)
        
    # FUNCTION FOR GENERATING THE GRID AT THE BEGINNING OF THE GAME
    def generate_grid(self):
        np.random.shuffle(self.seed)
        is_solved = False
        while not is_solved:
            if self.is_solution(0, 0):
                is_solved = True
            
        self.seed = np.arange(1, 10)
                
    # FUNCTION FOR DRAWING THE GRID
    def draw_grid(self) -> None:    
        WINDOW.fill((255, 255, 255))
        for i in range(1, 9):
            VERT_CELL_BORDER = pygame.Rect(i*CELL_SIZE - 1, 0, 2, HEIGHT)    
            pygame.draw.rect(WINDOW, (0, 0, 0), VERT_CELL_BORDER)
            HOR_CELL_BORDER = pygame.Rect(0, i*CELL_SIZE - 1, WIDTH, 2)
            pygame.draw.rect(WINDOW, (0, 0, 0), HOR_CELL_BORDER)
        for i in range(1, 3):
            VERT_GRID_BORDER = pygame.Rect(i*GRID_SIZE -3, 0, 6, HEIGHT)
            pygame.draw.rect(WINDOW, (0, 0, 0), VERT_GRID_BORDER)
            HOR_GRID_BORDER = pygame.Rect(0, i*GRID_SIZE - 3, WIDTH, 6)
            pygame.draw.rect(WINDOW, (0, 0, 0), HOR_GRID_BORDER)
        for i in range(9):
            for j in range(9):
                if self.grid[i][j]:
                    text = FONT.render(str(self.grid[i][j]), 1, (0, 0, 0))
                    WINDOW.blit(text, (i*CELL_SIZE + 30, j*CELL_SIZE + 15))    
                    
    # FUNCTION FOR CHECKING VALIDITY OF AN INPUT
    def is_valid(self, row: int, col: int, value) -> bool:
        for i in range(9):
            if self.grid[row][i] == value:
                return False
            if self.grid[i][col] == value:
                return False
        i = row // 3
        j = col // 3
        for row in range(i*3, i*3 + 3):
            for col in range(j*3, j*3 + 3):
                if self.grid[row][col] == value:
                    return False
        return True
    
    # FUNCTION FOR FINDING A SOLUTION
    def is_solution(self, i, j) -> bool:
        while self.grid[i][j]:
            if i < 8:
                i += 1
            elif i == 8 and j < 8:
                i = 0
                j += 1
            elif i == 8 and j == 8:
                return True
        pygame.event.pump()
        for k in self.seed:
            if self.is_valid(i, j, k):
                self.grid[i][j] = k
                global x, y
                x = i
                y = j           
                WINDOW.fill((255, 255, 255))
                self.draw_grid()
                pygame.display.update()
                pygame.time.delay(25)
                if self.is_solution(i, j):
                    return True
                else:
                    self.grid[i][j] = 0
                WINDOW.fill((0, 0, 0))
                self.draw_grid()
                highlight_cell()
                pygame.display.update()
                pygame.time.delay(25)
        return False
            
# FUNCTION FOR COMPUTING CARTESIAN COORDINATES
def coord(position) -> None:
    global x, y
    x = int(position[0] // CELL_SIZE)
    y = int(position[1] // CELL_SIZE)
    
# FUNCTION FOR HIGHLIGHTING A CELL  
def highlight_cell() -> None:
    for i in range(2):
        pygame.draw.line(WINDOW, (255, 0, 0), (x*CELL_SIZE - 3, (y + i)*CELL_SIZE), (x*CELL_SIZE + CELL_SIZE + 3, (y + i)*CELL_SIZE), 6)    
        pygame.draw.line(WINDOW, (255, 0, 0), ((x + i)*CELL_SIZE, y*CELL_SIZE), ((x + i)*CELL_SIZE, y*CELL_SIZE + CELL_SIZE), 6)

# FUNCTION FOR RENDERING THE VALUE INPUTTED BY PLAYER
def fill_value(value: int) -> None:
    text = FONT.render(str(value), 1, (0, 0, 0))
    WINDOW.blit(text, (x*CELL_SIZE + 15, y*CELL_SIZE + 15))

# FUNCTION FOR RAISING ERROR WHEN THE WRONG ANSWER IS INPUTTED
def mistake_error() -> None:
    text = FONT.render('Wrong answer!', 1, (0, 0, 0,))
    WINDOW.blit(text, (20, 570))
    
# FUNCTION FOR RAISING TYPE ERROR TRIGGERED ON INVALID INPUT
def raise_error() -> None:
    text = FONT.render('Input invalid! Please enter a correct value!', 1, (0, 0, 0))
    WINDOW.blit(text, (20, 570))

# FUNCTION FOR END OF GAME SCREEN
def result() -> None:
    text = FONT.render('Game finished', 1, (0, 0, 0,))
    pygame.draw.circle(WINDOW, (255, 128, 128), (WIDTH/2, HEIGHT/2), text.get_width())
    WINDOW.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(10000)
    
# CORE GAME LOOP       
def main() -> None:
    game_board = Board() 
    game_board.generate_grid()   
    clock = pygame.time.Clock()
    run = True
    click = False 
    solve_cond = False
    res_cond = False
    value = 0
    error = False
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # HANDLES THE USER CLOSING THE GAME
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN: # HANDLES CLICKING ON A CELL
                click = True
                position = pygame.mouse.get_pos()
                coord(position)
            if event.type == pygame.KEYDOWN: # HANDLES PRESSING A KEY
                if event.key == pygame.K_1: 
                    value = 1
                if event.key == pygame.K_2:
                    value = 2
                if event.key == pygame.K_3:
                    value = 3
                if event.key == pygame.K_4:
                    value = 4
                if event.key == pygame.K_5:
                    value = 5
                if event.key == pygame.K_6:
                    value = 6
                if event.key == pygame.K_7:
                    value = 7
                if event.key == pygame.K_8:
                    value = 8
                if event.key == pygame.K_9:
                    value = 9
                if event.key == pygame.K_RETURN:
                    solve_cond = True
                if event.key == pygame.K_r:
                    res_cond = False
                    error = False
                    solve_cond = False
                    game_board.grid = np.zeros((9, 9))
                if event.key == pygame.K_d:
                    res_cond = False
                    error = False
                    solve_cond = False
                    game_board.grid = default_grid
        if solve_cond:
            if not game_board.is_solution(0, 0):
                error = True
            else:
                res_cond = True
            solve_cond = False
        if value:
            fill_value(value)
            if game_board.is_valid(x, y, value):
                game_board.grid[x][y] = value
                click = False
            else:
                raise_error()
            value = 0
        if error:
            mistake_error()
        if res_cond:
            result()
        
        game_board.draw_grid()
        if click:
            highlight_cell()
        pygame.display.update()
    
if __name__ == '__main__':
    main()