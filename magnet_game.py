import pygame
import sys
import threading

pygame.init()

WHITE = "white"
BLACK = "black"
HIGHLIGHT_COLOR = (100, 100, 200)
PURPLE_COLOR = "purple"
IRON_COLOR = "grey"
SOLUTION_COLOR = "green"

class Board:
    def __init__(self, size=3):
        self.size = size
        self.cell_size = 500 // self.size  
        self.board = [["*" for _ in range(self.size)] for _ in range(self.size)]
        self.solution_positions = [(0, 2), (1, 2), (1, 0)]  
        self.initial_pieces()

    def initial_pieces(self):
        initial_positions = {
            (2, 0): "P",  
            (0, 1): "I",
            (1, 1): "I"
        }
        for position, value in initial_positions.items():
            if position[0] < self.size and position[1] < self.size:
                self.board[position[0]][position[1]] = value
        self.red_ball_pos = (2, 0)
        self.purple_ball_pos = (2, self.size - 1)
        self.iron_ball_positions = [(1, 2), (2, 2)]


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
                if piece == "P": 
                    pygame.draw.circle(screen, PURPLE_COLOR, (col * self.cell_size + self.cell_size // 2, row * self.cell_size + self.cell_size // 2), self.cell_size // 3)
                elif piece == "I":  
                    pygame.draw.circle(screen, IRON_COLOR, (col * self.cell_size + self.cell_size // 2, row * self.cell_size + self.cell_size // 2), self.cell_size // 3)
                    

    def update_board(self, new_purple_pos):
        old_pos = self.purple_ball_pos
        self.board[old_pos[0]][old_pos[1]] = "*"  
        self.purple_ball_pos = new_purple_pos
        self.board[new_purple_pos[0]][new_purple_pos[1]] = "P"  
        self.move_iron_ball()

    def move_iron_ball(self):
        new_iron_positions = []
        for (row, col) in self.iron_ball_positions:
            if row == self.purple_ball_pos[0]:
                row += 1 if row < self.size - 1 else -1
            elif col == self.purple_ball_pos[1]:
                col += 1 if col < self.size - 1 else -1
            new_iron_positions.append((row, col))
        for r, c in self.iron_ball_positions:
            self.board[r][c] = "*"  
        for r, c in new_iron_positions:
            self.board[r][c] = "I"      
        self.iron_ball_positions = new_iron_positions

class GameSolver:
    def __init__(self, board):
        self.board = board
        self.visited_states = set()

    def is_win_state(self):
        return all(pos in self.board.solution_positions for pos in self.board.iron_ball_positions)

    def dfs(self, position):
        stack = [(position, [position])]
        while stack:
            current_pos, path = stack.pop()
            if self.is_win_state():
                return path
            for new_pos in self.get_valid_moves(current_pos):
                if new_pos not in self.visited_states:
                    self.visited_states.add(new_pos)
                    self.board.update_board(new_pos)  
                    stack.append((new_pos, path + [new_pos]))
        return None  

    def bfs(self, position):
        queue = [(position, [position])]
        while queue:
            current_pos, path = queue.pop(0)
            if self.is_win_state():
                return path
            for new_pos in self.get_valid_moves(current_pos):
                if new_pos not in self.visited_states:
                    self.visited_states.add(new_pos)
                    self.board.update_board(new_pos)  
                    queue.append((new_pos, path + [new_pos]))
        return None  

    def get_valid_moves(self, position):
        row, col = position
        possible_moves = [
            (row - 1, col), (row + 1, col),  
            (row, col - 1), (row, col + 1)   
        ]
        return [(r, c) for r, c in possible_moves if 0 <= r < self.board.size and 0 <= c < self.board.size]
class Game:
    def __init__(self):
        self.board = Board()
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
        board =Board(size=3)
        game_solver = GameSolver(board)
        initial_position = board.purple_ball_pos
        if algorithm == "dfs":
            dfs_solution_path = game_solver.dfs(initial_position)
            if dfs_solution_path:
                print("DFS Solution Path:", dfs_solution_path)
            else:
                print("No solution found with DFS.")
        elif algorithm == "bfs":
            bfs_solution_path = game_solver.bfs(initial_position)
            if bfs_solution_path:
                print("BFS Solution Path:", bfs_solution_path)
            else:
                print("No solution found with BFS.")

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
    game = Game()
    game.run()
