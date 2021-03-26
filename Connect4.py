import pygame
import colors
import tkinter as tk
import pygame_menu

class Connect4:
    """
    Class used to represent connect4 game
    """
    def __init__(self, player1, player2, screen):

        # Use 1 version of the screen instead of trying to create a new one
        self.screen = screen

        # Circle Radius and Width
        self.WIDTH = 0
        self.CIRCLERADIUS = 25

        # Game-Time Variables
        self.player1 = player1
        self.player2 = player2
        self.moveNumber = 0
        self.gameOver = False
        self.COLUMNS = 7
        self.ROWS = 6
        self.EMPTY = 99
        self.board = [[self.EMPTY for x in range(self.COLUMNS)] for y in range(self.ROWS)]

        # The distance between where the window starts and the game board is placed
        self.DISTANCE = 90

        # Space between each circle
        self.DISTANCEGAP = 70

        # Setting rectangle default       
        self.LEFT = 50
        self.TOP = 70
        self.HEIGHT = 470
        self.RECWIDTH = 500

        #Creating new tkinterobject
        self.root = tk.Tk()
        self.scoreboard = {self.player1.name: 0, self.player2.name: 0, "ties": 0}
        
        # Storing locations of available moves given a user clicks the window -- Tuple of locations
        self.POSITIONS = [
            (
                self.DISTANCE + (self.DISTANCEGAP*column) - self.CIRCLERADIUS,
                self.DISTANCE + (self.DISTANCEGAP*column) + self.CIRCLERADIUS
            )
            for column in range(0, self.COLUMNS)
        ] 

    def whoWon(self, board, piece):
        """
        Determines the state of the game and finds if there is a winner
        """
        # Horizontal
        for col in range(0, self.COLUMNS - 3):
            for row in range(0, self.ROWS):
                if board[row][col] == piece and board[row][col + 1] == piece and board[row][col + 2] == piece and board[row][col + 3] == piece:
                    return True

        # Vertical
        for col in range(0, self.COLUMNS):
            for row in range(0, self.ROWS - 3):
                if board[row][col] == piece and board[row + 1][col] == piece and board[row + 2][col] == piece and board[row + 3][col] == piece:
                    return True
                
        # Up-Left/Down-Right
        for col in range(3, self.COLUMNS):
            for row in range(3, self.ROWS):
                if board[row][col] == piece and board[row - 1][col - 1] == piece and board[row - 2][col - 2] == piece and board[row - 3][col - 3] == piece:
                    return True
        
        # Up-Right/Down-Left
        for col in range(0, self.COLUMNS - 3):
            for row in range(3, self.ROWS):
                if board[row][col] == piece and board[row - 1][col + 1] == piece and board[row - 2][col + 2] == piece and board[row - 3][col + 3] == piece:
                    return True
        
        # A winning move is not found
        return False

    def legalMove(self, position):
        """
        Validates if a move is available/legal
        """
        if self.board[0][position] == self.EMPTY:
            return True
        return False

    def displayBoard(self):
        """
        Displaying the game board to the user
        """
        # Function: rect(surface, color, rectangle object, optional width) -- First one forms the outline of the board
        pygame.draw.rect(self.screen, colors.salmon, (self.LEFT, self.TOP, self.RECWIDTH, self.HEIGHT), 13)

        # This forms inner-most rectangle that users play on
        pygame.draw.rect(self.screen, colors.burlywood, (self.LEFT, self.TOP, self.RECWIDTH, self.HEIGHT))
        
        for column in range(0, self.COLUMNS):
            colEq = self.DISTANCE + (self.DISTANCEGAP * column)
            for row in range(0, self.ROWS):
                # 125 is used here to make a the board placed in the center of the board and helps finding a value for self.TOP easier
                rowEq = 125 + (self.DISTANCEGAP * row)
                if self.board[row][column] == self.EMPTY:
                    color = colors.white
                elif self.board[row][column] == 0:
                    color = colors.realBlue
                elif self.board[row][column] == 1:
                    color = colors.red
                pygame.draw.circle(self.screen, color, (colEq, rowEq), self.CIRCLERADIUS, self.WIDTH)
        pygame.display.flip()
    
    def play(self):
        """
        This is the game-loop
        """
        while not self.gameOver:
            self.displayBoard()
            if self.moveNumber % 2 == 0:
                userText, userRect = self.displayName(self.player1.name, colors.realBlue)
            elif self.moveNumber % 2 == 1:
                userText, userRect = self.displayName(self.player2.name, colors.red)
            self.screen.blit(userText, userRect) 

            for event in pygame.event.get():
                self.screen.fill(colors.aquamarine) # Set up background color
                if event.type == pygame.QUIT: 
                    self.gameOver = True 
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    position = self.getColumnPosition(x)
                    if self.moveNumber % 2 == 0 and position != self.EMPTY:
                        if self.legalMove(position):                            
                            self.dropPiece(position)
                            if self.whoWon(self.board, 0):
                                self.gameOver = True
                                self.scoreboard[self.player1.name] = self.scoreboard.get(self.player1.name) + 1
                                userText, userRect = self.displayName(self.player1.name + " " + "Wins!!!", colors.dark_gray)
                            elif self.checkTie(self.board):
                                self.gameOver = True
                                self.scoreboard["ties"] = self.scoreboard.get("ties") + 1
                                userText, userRect = self.displayName("It is a TIE!!!", colors.dark_gray)

                    elif self.moveNumber % 2 == 1 and position != self.EMPTY:
                        if self.legalMove(position):                            
                            self.dropPiece(position)
                            if self.whoWon(self.board, 1):
                                self.gameOver = True
                                self.scoreboard[self.player2.name] = self.scoreboard.get(self.player2.name) + 1
                                userText, userRect = self.displayName(self.player2.name + " " + "Wins!!!", colors.dark_gray)
                            elif self.checkTie(self.board):
                                self.gameOver = True
                                self.scoreboard["ties"] = self.scoreboard.get("ties") + 1
                                userText, userRect = self.displayName("It is a TIE!!!", colors.dark_gray)
        self.displayBoard()
        self.screen.blit(userText, userRect) 
        pygame.display.flip()
        self.displayScore(False)
            
    def displayScore(self, isAi):
        """
        This enables the tkinter object so I can display the user options after : Victory/Loss/Tie
        """
        self.root.geometry('460x150+300+0')
        self.reset()
        self.root.title("Choices")

        # This creates the feedback information screen that the user sees after a game
        tk.Label(self.root, text="Close window to go to main menu", font=(None, 15, 'underline'), anchor='w', justify='left').grid(row=0, column=1, sticky="NSEW")
        tk.Label(self.root, text=self.player1.name + ": " + str(self.scoreboard.get(self.player1.name)), font=(None, 15), anchor='w', justify='left').grid(row=1, column=1, sticky = "NSEW")
        tk.Label(self.root, text=self.player2.name + ": " + str(self.scoreboard.get(self.player2.name)), font=(None, 15), anchor='w', justify='left').grid(row=2, column=1, sticky="NSEW")
        tk.Label(self.root, text="Ties: " + str(self.scoreboard.get("ties")), font=(None, 15), anchor='w', justify='left').grid(row=3, column=1, sticky="NSEW")

        # if isAi == True:
        #     # tk.Button(self.root, text='Rematch!', command=self.playAi, font=(None, 12), fg="blue").grid(row=4, column=1, sticky=tk.W)
        # else:
        tk.Button(self.root, text='Rematch!', command=self.play, font=(None, 12), fg="blue").grid(row=4, column=1, sticky=tk.W)
        
        # tk.Button(self.root, text='Rematch with Swap!', command= lambda: self.swapPlayers(isAi), font=(None, 12), fg="red").grid(row=4, column=2, sticky=tk.W)

        tk.Entry(self.root)
        self.root.mainloop()
    
    def checkTie(self, board):
        """
        A possible game state : Checking for a tie
        """
        totalPieces = 0
        for col in range(0, self.COLUMNS):
            for row in range(0, self.ROWS):
                if board[row][col] == 0 or board[row][col] == 1:
                    totalPieces += 1  
        if totalPieces == 42:
            return True
        else:
            return False

    def displayName(self, name, color):
        """
        A feature to help users know who's turn it is that gets displayed
        """
        font = pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 60) 
        text = font.render(name, True, color)
        textRect = text.get_rect()
        textRect.center = (len(name) * 30, 20)
        return text, textRect

    def dropPiece(self, position):
        """
        Inserting a piece at a given position with the animation of a piece drop
        """
        tmpRow = 5
        while self.board[tmpRow][position] == 1 or self.board[tmpRow][position] == 0:
            tmpRow -= 1

        for i in range(0, tmpRow + 1):
            self.board[i][position] = self.moveNumber % 2
            self.displayBoard()
            pygame.time.delay(200)
            pygame.display.flip()
            self.board[i][position] = self.EMPTY

        self.board[tmpRow][position] = self.moveNumber % 2
        self.moveNumber += 1

    def getColumnPosition(self, position):
        """
        Takes a X coordinate value dependent on a click and determines what column user clicked
        """
        index = 0
        for i in self.POSITIONS:
            if position + self.CIRCLERADIUS/2 >= i[0] and position - self.CIRCLERADIUS/2 <= i[1]:
                return index
            index += 1
        return self.EMPTY

    def reset(self):
        """
        Restoring the game in its original state
        """
        self.moveNumber = 0
        self.board = [[self.EMPTY for x in range(self.COLUMNS)] for y in range(self.ROWS)]
        self.gameOver = False
    