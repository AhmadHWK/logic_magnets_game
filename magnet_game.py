import pygame
import sys

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

class Game:
    def __init__(self, size):
        self.board = Board(size)
        self.cursor_x, self.cursor_y = 0, 0  
        self.selected_piece = None
        self.win_message_displayed = False
        self.window_size = 500
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption("Logic Magnets")

    def select_piece(self, x, y):
        piece = self.board.board[y][x]
        if piece in ["R", "P"]:
            self.selected_piece = (piece, (y, x))
            print(f"Selected '{piece}' at ({y}, {x})")

    def move_piece(self, x, y):
        if self.selected_piece and self.board.board[y][x] == "*":
            piece, (old_y, old_x) = self.selected_piece
            self.board.board[old_y][old_x] = "*"
            self.board.board[y][x] = piece
            print(f"Moved '{piece}' to ({y}, {x})")
            if piece == "P":
                self.move_iron_balls(y, x, direction="P")  
            elif piece == "R":
                self.move_iron_balls(y, x, direction="R")           
            self.selected_piece = None
            self.check_win()  

    def move_iron_balls(self, row, col, direction):
        for r in range(self.board.size):
            for c in range(self.board.size):
                if self.board.board[r][c] == "I":
                    if direction == "P":  
                        if r == row: 
                            if c < col and c + 1 < self.board.size and self.board.board[r][c + 1] == "*":
                                self.board.board[r][c + 1], self.board.board[r][c] = "I", "*"
                            elif c > col and c - 1 >= 0 and self.board.board[r][c - 1] == "*":
                                self.board.board[r][c - 1], self.board.board[r][c] = "I", "*"
                        elif c == col:  
                            if r < row and r + 1 < self.board.size and self.board.board[r + 1][c] == "*":
                                self.board.board[r + 1][c], self.board.board[r][c] = "I", "*"
                            elif r > row and r - 1 >= 0 and self.board.board[r - 1][c] == "*":
                                self.board.board[r - 1][c], self.board.board[r][c] = "I", "*"
                    elif direction == "R":  
                        if r == row: 
                            if c < col and c - 1 >= 0 and self.board.board[r][c - 1] == "*":
                                self.board.board[r][c - 1], self.board.board[r][c] = "I", "*"
                            elif c > col and c + 1 < self.board.size and self.board.board[r][c + 1] == "*":
                                self.board.board[r][c + 1], self.board.board[r][c] = "I", "*"
                        elif c == col:  
                            if r < row and r - 1 >= 0 and self.board.board[r - 1][c] == "*":
                                self.board.board[r - 1][c], self.board.board[r][c] = "I", "*"
                            elif r > row and r + 1 < self.board.size and self.board.board[r + 1][c] == "*":
                                self.board.board[r + 1][c], self.board.board[r][c] = "I", "*"

    def check_win(self):
        iron_positions = [(r, c) for r in range(self.board.size) for c in range(self.board.size) if self.board.board[r][c] == "I"]
        if set(iron_positions) == set(self.board.solution_positions) and not self.win_message_displayed:
            self.win_message_displayed = True
            self.display_message()

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

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.cursor_x = mouse_x // self.board.cell_size
                    self.cursor_y = mouse_y // self.board.cell_size
                    if event.button == 1:  
                        if self.selected_piece is None:
                            self.select_piece(self.cursor_x, self.cursor_y)  
                        else:
                            self.move_piece(self.cursor_x, self.cursor_y)  
            self.board.draw(self.screen, self.cursor_x, self.cursor_y)
            pygame.display.flip()

if __name__ == "__main__":
    game_size =int(input("Select Borad Size : "))
    game = Game(game_size)
    game.run()
