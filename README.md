# Logic Magnets Game

This project is a logic magnet game where players move colored balls across a grid to solve a board. It uses `pygame` for the graphical interface and implements Depth-First Search (DFS) and Breadth-First Search (BFS) algorithms for automated solving.

## File Overview

### magnets_game.py

This file contains the main logic and classes for the game. It is organized into the following classes:

---

### **1. `Board` Class**

The `Board` class manages the game grid, initializes pieces, updates the board state, and handles drawing the grid.

#### **Attributes**

- `size`: The size of the grid (default is 3x3).
- `cell_size`: The size of each cell in the grid.
- `board`: A 2D list representing the current state of the board.
- `solution_positions`: Predefined positions where iron balls need to be placed to win.
- `red_ball_pos`: Current position of the red ball (not yet used in this game).
- `purple_ball_pos`: Current position of the purple ball.
- `iron_ball_positions`: A list of positions for iron balls.

#### **Functions**

1. **`__init__(self, size=3)`**: Initializes the board with default pieces and sets up the grid.
2. **`initial_pieces(self)`**: Places the initial red, purple, and iron balls on the grid.
3. **`draw(self, screen, cursor_x, cursor_y)`**: Renders the game grid and pieces on the screen. Highlights the current cursor position.
4. **`update_board(self, new_purple_pos)`**: Moves the purple ball to a new position and updates the grid state.
5. **`move_iron_ball(self)`**: Automatically moves iron balls when the purple ball is moved in the same row or column.

---

### **2. `GameSolver` Class**

The `GameSolver` class implements algorithms to solve the game automatically using DFS or BFS.

#### **Attributes**

- `board`: The `Board` object being solved.
- `visited_states`: A set to keep track of visited board states to avoid cycles.

#### **Functions**

1. **`__init__(self, board)`**: Initializes the solver with the given board.
2. **`is_win_state(self)`**: Checks if the current board state meets the win condition (all iron balls are in solution positions).
3. **`dfs(self, position)`**: Uses the Depth-First Search algorithm to find a solution.
4. **`bfs(self, position)`**: Uses the Breadth-First Search algorithm to find a solution.
5. **`get_valid_moves(self, position)`**: Returns a list of valid moves for a given position on the grid.

---

### **3. `Game` Class**

The `Game` class manages the overall gameplay, including the game loop, user input, and displaying the win message.

#### **Attributes**

- `board`: The `Board` object for the current game.
- `cursor_x`, `cursor_y`: The current cursor position on the grid.
- `selected_piece`: Keeps track of the currently selected piece.
- `win_message_displayed`: A flag to track whether the win message has been shown.
- `window_size`: The size of the game window.
- `screen`: The `pygame` display surface.
- `solver`: The `GameSolver` object for automated solving.

#### **Functions**

1. **`__init__(self)`**: Sets up the game window and initializes the board and solver.
2. **`display_message(self)`**: Displays a "You Won" message when the game is solved.
3. **`start_solver_thread(self, algorithm="dfs")`**: Starts a thread to run the solver (DFS or BFS).
4. **`solve_game(self, algorithm)`**: Solves the game using the specified algorithm (DFS or BFS).
5. **`run(self)`**: The main game loop that handles user input, draws the grid, and processes events.

---

## How to Use the Game

1. **Run the game**:

   ```bash
   python magnets_game.py
