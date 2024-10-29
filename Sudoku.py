"""
This is a program for solving Sudoku.

Algorithm used for the solving is Depth-first search with backtracking.

The program contains GUI with a Solve button which solves the initial board.
"""

# Library used for GUI
import tkinter as tk

# A class representing the Sudoku grid
class SudokuGrid:
    def __init__(self, initial_numbers):
        # Initialize an empty grid
        self.grid = []
        # Iterate over each row in the grid
        for i in range(9):
            # Initialize an empty list to represent the row
            row = []
            # Iterate over each cell in the row
            for j in range(9):
                # If the cell contains an initial number, add it to the row
                if initial_numbers[i][j] == 0:
                    row.append(None)
                else:
                    row.append(initial_numbers[i][j])
            # Add the completed row to the grid
            self.grid.append(row)

    # Get the value in a particular cell of the grid
    def get(self, i, j):
        return self.grid[i][j]

    # Set the value in a particular cell of the grid
    def set(self, i, j, value):
        self.grid[i][j] = value

    # Solve the sodoku board
    def solve(self):
        # Define a helper function to check if a number is valid in a given position
        def is_valid(num, row, col):
            # Check row
            for i in range(9):
                if self.grid[row][i] == num:
                    return False
            # Check column
            for i in range(9):
                if self.grid[i][col] == num:
                    return False
            # Check box
            box_row = (row // 3) * 3
            box_col = (col // 3) * 3
            for i in range(3):
                for j in range(3):
                    if self.grid[box_row+i][box_col+j] == num:
                        return False
            return True

        # Define a helper function to find the next empty cell
        def find_empty_cell():
            for i in range(9):
                for j in range(9):
                    if self.grid[i][j] == None:
                        return (i, j)
            return None
        
        # Use recursion to solve the puzzle
        def solve_helper():
            empty_cell = find_empty_cell()
            # If there are no empty cells, the puzzle is solved
            if not empty_cell:
                return True
            row, col = empty_cell
            # Try each possible value for the empty cell
            for num in range(1, 10):
                if is_valid(num, row, col):
                    self.grid[row][col] = num
                    # Recursively solve the puzzle with the new number in place
                    if solve_helper():
                        return True
                    # If the new number leads to an unsolvable puzzle, backtrack and try a different number
                    self.grid[row][col] = None
            # If no valid number can be placed in the empty cell, backtrack and try a different value for the previous empty cell
            return False
    
        # Call the helper function to solve the puzzle
        solve_helper()
        # Return the solved grid
        return self.grid
    

# A class representing the graphical user interface for the Sudoku game
class SudokuGUI:
    def __init__(self, initial_numbers):
        # Initialize a SudokuGrid object based on the provided initial numbers
        self.grid = SudokuGrid(initial_numbers)
        # Create a new window for the GUI
        self.window = tk.Tk()
        # Set the title of the window
        self.window.title('Sudoku')
        # Set the size of the window
        self.window.geometry('450x450')
        # Create a canvas on which to draw the Sudoku grid
        self.canvas = tk.Canvas(self.window, width=450, height=450)
        # Add the canvas to the window
        self.canvas.pack()
        # Set the position of a canvas
        self.canvas.place(x=45, y=50)
        # Draw the Sudoku grid
        self.draw_grid()
        # Create a button to solve the Sudoku puzzle
        self.solve_button = tk.Button(self.window, text="Solve", font=("Arial", 15), bg="#ADD8E6", command=lambda: self.solve_sudoku())
        # Add the button to the window
        self.solve_button.pack()
        # Set the position of the button
        self.solve_button.place(x=195, y=5)
        # Start the main event loop for the GUI
        self.window.mainloop()

    # Update the solved values on the grid 
    def solve_sudoku(self):
        # Delete any previous numbers on the canvas
        self.canvas.delete("numbers")
        # Check is button is clicked
        print("Button clicked!")
        # Call the solve method of the SudokuGrid object
        solved_grid = self.grid.solve()
        if solved_grid:
            # Update the grid with the solved values
            for i in range(9):
                for j in range(9):
                    value = solved_grid[i][j]
                    if value is not None:
                        self.canvas.create_text(2+j * 40 + 20,2+i * 40 + 20, text=str(value), font=("Arial", 20), tags="numbers")

        else:
            # Display an error message if the puzzle cannot be solved
            error_label = tk.Label(self.window, text="Unable to solve puzzle", font=("Arial", 20), fg="red")
            error_label.pack()

    # Draw the sudoku grid
    def draw_grid(self):
        self.canvas.create_line(2, 2, 2, 9*40)
        self.canvas.create_line(2, 2, 9*40, 2)
        # Iterate over each row in the grid
        for i in range(9):
            # Iterate over each cell in the row
            for j in range(9):
                # Calculate the coordinates of the top-left and bottom-right corners of the cell
                x1 = 40 * j+2
                y1 = 40 * i+2
                x2 = x1 + 40
                y2 = y1 + 40

                # Check if cell is in the first row of a 3x3 block
                if i % 3 == 0:
                    # Draw a thicker black line above the block
                    self.canvas.create_line(x1, y1, x2, y1, width=2, fill='black')
                
                # Check if cell is in the first column of a 3x3 block
                if j % 3 == 0:
                    # Draw a thicker black line to the left of the block
                    self.canvas.create_line(x1, y1, x1, y2, width=2, fill='black')
                
                # Check if the cell is empty
                if self.grid.get(i, j) is None:
                    # If the cell is empty, draw a black rectangle around it
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline='black')
                else:
                    # If the cell contains a number, fill it with light gray and draw the number inside
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='light gray', outline='black')
                    self.canvas.create_text(x1 + 20, y1 + 20, text=str(self.grid.get(i, j)), font=("Arial", 20), tags="numbers")



if __name__ == '__main__':
    # initial board (2 more provided in the end of the code)
    initial_numbers = [    
        [0, 7, 5, 0, 9, 0, 0, 0, 6],
        [0, 2, 3, 0, 8, 0, 0, 4, 0],
        [8, 0, 0, 0, 0, 3, 0, 0, 1],
        [5, 0, 0, 7, 0, 2, 0, 0, 0],
        [0, 4, 0, 8, 0, 6, 0, 2, 0],
        [0, 0, 0, 9, 0, 1, 0, 0, 3],
        [9, 0, 0, 4, 0, 0, 0, 0, 7],
        [0, 6, 0, 0, 7, 0, 5, 8, 0],
        [7, 0, 0, 0, 1, 0, 3, 9, 0]
    ]
    
    gui = SudokuGUI(initial_numbers)
    grid = SudokuGrid(initial_numbers)
    solved_grid = grid.solve()
    print(solved_grid)


    """
    [                                                          
        [3, 0, 0, 4, 1, 5, 2, 6, 0],
        [4, 0, 9, 7, 6, 0, 0, 0, 1],
        [0, 6, 0, 0, 2, 8, 4, 0, 0],
        [1, 0, 0, 0, 8, 0, 0, 5, 7],
        [0, 4, 5, 3, 0, 0, 0, 0, 0],
        [8, 0, 2, 1, 0, 0, 6, 0, 0],
        [0, 5, 0, 0, 0, 0, 0, 0, 6],
        [9, 0, 4, 0, 0, 0, 1, 3, 5],
        [6, 1, 0, 5, 0, 0, 7, 2, 8]
    ]
    [    
        [0, 0, 7, 4, 9, 1, 6, 0, 5],
        [2, 0, 0, 0, 6, 0, 3, 0, 9],
        [0, 0, 0, 0, 0, 7, 0, 1, 0],
        [0, 5, 8, 6, 0, 0, 0, 0, 4],
        [0, 0, 3, 0, 0, 0, 0, 9, 0],
        [0, 0, 6, 2, 0, 0, 1, 8, 7],
        [9, 0, 4, 0, 7, 0, 0, 0, 2],
        [6, 7, 0, 8, 3, 0, 0, 0, 0],
        [8, 1, 0, 0, 4, 5, 0, 0, 0]
    ]
    """


