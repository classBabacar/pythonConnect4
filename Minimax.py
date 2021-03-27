from Connect4 import Connect4
import random

class Minimax(Connect4):
    def __init__(self, player1, player2, screen):
        super().__init__(player1, player2, screen)

    def generateMove(self):
        return random.randint(0,6)

