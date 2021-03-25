class Connect4:
    """
    Class used to represent connect4 game
    """

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.moveNumber = 0

        self.COLUMNS = 7
        self.ROWS = 6
        self.EMPTY = 99
        self.board = [[self.EMPTY for x in range(self.COLUMNS)] for y in range(self.ROWS)]


    def play(self):
        print(self.player1.make_move())
        print(self.player2.make_move())