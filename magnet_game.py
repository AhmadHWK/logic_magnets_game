import pygame
import sys
from collections import deque
import threading

pygame.init()

WHITE = "white"
BLACK = "black"
HIGHLIGHT_COLOR = (100, 100, 200)
RED_COLOR = "red"
PURPLE_COLOR = "purple"
IRON_COLOR = "grey"
SOLUTION_COLOR = "green"

class Board:
    def __init__(self, size):
        self.size = size
        self.cell_size = 500 // size  
        self.board = [["*" for _ in range(size)] for _ in range(size)]
        self.solution_positions = [(0, 3), (size - 1, 2)]  
        self.initial_pieces()

    def initial_pieces(self):
        initial_positions = {
            (2, 0): "R",  
            (2, self.size - 1): "P", 
            (1, 2): "I",
            (3, 2): "I"
        }
        for position, value in initial_positions.items():
            if position[0] < self.size and position[1] < self.size:
                self.board[position[0]][position[1]] = value
        self.red_ball_pos = (2, 0)
        self.purple_ball_pos = (2, self.size - 1)
        self.iron_ball_positions = [(1, 2), (3, 2)]

    def draw(self, screen, cursor_x, cursor_y):
        screen.fill(WHITE)
        for row in range(self.size):
            for col in range(self.size):
                rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                color = HIGHLIGHT_COLOR if (row, col) == (cursor_y, cursor_x) else BLACK
                if (row, col) in self.solution_positions:
                    pygame.draw.rect(screen, SOLUTION_COLOR, rect) 
                else:
                    pygame.draw.rect(screen, color, rect, 1) 
                piece = self.board[row][col]
                if piece == "R": 
                    pygame.draw.circle(screen, RED_COLOR, (col * self.cell_size + self.cell_size // 2, row * self.cell_size + self.cell_size // 2), self.cell_size // 3)
                elif piece == "P": 
                    pygame.draw.circle(screen, PURPLE_COLOR, (col * self.cell_size + self.cell_size // 2, row * self.cell_size + self.cell_size // 2), self.cell_size // 3)
                elif piece == "I":  
                    pygame.draw.circle(screen, IRON_COLOR, (col * self.cell_size + self.cell_size // 2, row * self.cell_size + self.cell_size // 2), self.cell_size // 3)

    def update_board(self, red_pos, purple_pos, iron_positions):
        self.board = [["*" for _ in range(self.size)] for _ in range(self.size)]
        for pos in iron_positions:
            self.board[pos[0]][pos[1]] = "I"
        self.board[red_pos[0]][red_pos[1]] = "R"
        self.board[purple_pos[0]][purple_pos[1]] = "P"

    def move_iron_balls(self, red_pos, purple_pos, iron_positions):
        new_iron_positions = []
        for iron_pos in iron_positions:
            y, x = iron_pos
            if red_pos[0] == y:  
                if x < red_pos[1]: 
                    new_iron_positions.append((y, x + 1))  
                elif x > red_pos[1]: 
                    new_iron_positions.append((y, x - 1))  
            elif red_pos[1] == x:  
                if y < red_pos[0]: 
                    new_iron_positions.append((y + 1, x))  
                elif y > red_pos[0]: 
                    new_iron_positions.append((y - 1, x))  
            else:
                new_iron_positions.append(iron_pos)

            if purple_pos[0] == y:  
                if x < purple_pos[1]:
                    new_iron_positions.append((y, x + 1))  
                elif x > purple_pos[1]:
                    new_iron_positions.append((y, x - 1))  
            elif purple_pos[1] == x:  
                if y < purple_pos[0]:
                    new_iron_positions.append((y + 1, x))  
                elif y > purple_pos[0]:
                    new_iron_positions.append((y - 1, x))  
        return new_iron_positions

class GameSolver:
    def __init__(self, game):
        self.game = game

    def is_win_state(self, iron_positions):
        return set(iron_positions) == set(self.game.board.solution_positions)

    def get_possible_moves(self, piece_pos):
       
        y, x = piece_pos
        moves = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  

        for dy, dx in directions:
            new_y, new_x = y + dy, x + dx
            if 0 <= new_y < self.game.board.size and 0 <= new_x < self.game.board.size:
                if self.game.board.board[new_y][new_x] == "*":  
                    moves.append((new_y, new_x))
        return moves
    def dfs(self):
        stack = [(self.game.board.red_ball_pos, self.game.board.purple_ball_pos, self.game.board.iron_ball_positions)]
        visited = set()

        while stack:
            red_pos, purple_pos, iron_positions = stack.pop()
            state = (red_pos, purple_pos, tuple(iron_positions))

            if state in visited:
                continue
            visited.add(state)

            if self.is_win_state(iron_positions):
                return state  

            for new_pos in self.get_possible_moves(red_pos):
                new_iron_positions = self.game.board.move_iron_balls(new_pos, purple_pos, iron_positions)
                self.game.board.update_board(new_pos, purple_pos, new_iron_positions)
                pygame.time.delay(1000)  
                self.game.board.draw(self.game.screen, 0, 0)  
                pygame.display.flip()
                stack.append((new_pos, purple_pos, new_iron_positions))

            for new_pos in self.get_possible_moves(purple_pos):
                new_iron_positions = self.game.board.move_iron_balls(red_pos, new_pos, iron_positions)
                self.game.board.update_board(red_pos, new_pos, new_iron_positions)
                pygame.time.delay(1000)  
                self.game.board.draw(self.game.screen, 0, 0)  
                pygame.display.flip()
                stack.append((red_pos, new_pos, new_iron_positions))

        return None  

    def bfs(self):
        queue = deque([(self.game.board.red_ball_pos, self.game.board.purple_ball_pos, self.game.board.iron_ball_positions)])
        visited = set()

        while queue:
            red_pos, purple_pos, iron_positions = queue.popleft()
            state = (red_pos, purple_pos, tuple(iron_positions))

            if state in visited:
                continue
            visited.add(state)

            if self.is_win_state(iron_positions):
                return state  

            for new_pos in self.get_possible_moves(red_pos):
                new_iron_positions = self.game.board.move_iron_balls(new_pos, purple_pos, iron_positions)
                self.game.board.update_board(new_pos, purple_pos, new_iron_positions)
                pygame.time.delay(1000)  
                self.game.board.draw(self.game.screen, 0, 0)  
                pygame.display.flip()
                queue.append((new_pos, purple_pos, new_iron_positions))

            for new_pos in self.get_possible_moves(purple_pos):
                new_iron_positions = self.game.board.move_iron_balls(red_pos, new_pos, iron_positions)
                self.game.board.update_board(red_pos, new_pos, new_iron_positions)
                pygame.time.delay(1000)  
                self.game.board.draw(self.game.screen, 0, 0)  
                pygame.display.flip()
                queue.append((red_pos, new_pos, new_iron_positions))

        return None 

class Game:
    def __init__(self, size):
        self.board = Board(size)
        self.cursor_x, self.cursor_y = 0, 0  
        self.selected_piece = None
        self.win_message_displayed = False
        self.window_size = 500
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption("Logic Magnets")
        self.solver = GameSolver(self)

    def display_message(self):
        font = pygame.font.Font(None, 74)
        text = font.render("You Won", True, (0, 128, 0))
        text_rect = text.get_rect(center=(self.window_size // 2, self.window_size // 2))
        self.screen.fill(WHITE)
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(3000)
        pygame.quit()
        sys.exit()

    def start_solver_thread(self, algorithm="dfs"):
        solver_thread = threading.Thread(target=self.solve_game, args=(algorithm,))
        solver_thread.start()

    def solve_game(self, algorithm):
        if algorithm == "dfs":
            self.solver.dfs()
        elif algorithm == "bfs":
            self.solver.bfs()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        result = self.start_solver_thread(algorithm="dfs")
                        if result:
                            self.display_message()  
                    elif event.key == pygame.K_b:
                        result = self.start_solver_thread(algorithm="bfs")
                        if result:
                            self.display_message()  
            
            self.board.draw(self.screen, self.cursor_x, self.cursor_y)
            pygame.display.flip()

if __name__ == "__main__":
    game_size = int(input("Select Board Size: "))
    game = Game(game_size)
    game.run()
