from Connect4 import Connect4
import random
from copy import copy, deepcopy
import pygame

class Minimax(Connect4):
    def __init__(self, player1, player2, screen):
        super().__init__(player1, player2, screen)
    
    def is_game_over(self, board):
        if self.who_won(board, 1) or self.who_won(board, 0):
            return True
        return False

    def generate_move(self, board, depth, computerPlayer, humanPlayer, maximizingPlayer, moveNumber):
        if depth == 0 or self.is_game_over(board) or self.check_if_tie(board):
            if self.is_game_over(board):
                if self.who_won(board, computerPlayer):
                    return 1000000
                elif self.who_won(board, humanPlayer):
                    return -1000000
                elif self.check_if_tie(board):
                    return 0
            else:
                return self.get_game_score(board, computerPlayer, humanPlayer)

        if maximizingPlayer:
            maxValue = -1000000
            for move in range(0, self.COLUMNS):
                tmpBoard = self.copyBoard(board)
                if self.is_legal_move(move, tmpBoard):
                    self.drop_piece_computer(move, tmpBoard, moveNumber)
                    result = self.generate_move(tmpBoard, depth - 1, computerPlayer, humanPlayer, False, moveNumber + 1)
                    if result >= maxValue:
                        maxValue = result
                        bestMove = move
            return bestMove
        else:
            minValue = 1000000
            for move in range(0,self.COLUMNS):
                tmpBoard = self.copyBoard(board)
                if self.is_legal_move(move, tmpBoard):
                    self.drop_piece_computer(move, tmpBoard, moveNumber)
                    result = self.generate_move(tmpBoard, depth - 1, humanPlayer, humanPlayer, True, moveNumber + 1)
                    if result <= minValue:
                        minValue = result
                        thismove = move
            return thismove

    def copyBoard(self, board):
        tmpList = [[self.EMPTY for x in range(self.COLUMNS)] for y in range(self.ROWS)]
        for row in range(0, self.ROWS):
            for col in range(0, self.COLUMNS):
                tmpList[row][col] = board[row][col]
        
        return tmpList

    def drop_piece_computer(self, position, board, moveNumber):
        """
        Inserting a piece at a given position with the animation of a piece drop
        """
        tmpRow = 5
        while board[tmpRow][position] == 1 or board[tmpRow][position] == 0:
            tmpRow -= 1

        
        board[tmpRow][position] = moveNumber % 2
        # moveNumber += 1

    def get_game_score(self, board, computerPlayer, humanPlayer):
        totalScore = 0
        totalScore += self.get_hori_score(board, computerPlayer, humanPlayer)
        # totalScore += self.get_vert_score(board, computerPlayer, humanPlayer)
        # totalScore += self.get_upright_score(board, computerPlayer, humanPlayer)
        # totalScore += self.get_upleft_score(board, computerPlayer, humanPlayer)

        return totalScore

    def get_hori_score(self, board, computerPlayer, humanPlayer):
        score = 0
        # List to collect all the groupings of 4(Horizontally) out of the current game state
        groupingFourList = []
        for col in range(0, self.COLUMNS - 3):
            for row in range(0, self.ROWS):
                groupingFourList.append(board[row][col])
                groupingFourList.append(board[row][col + 1])
                groupingFourList.append(board[row][col + 2])
                groupingFourList.append(board[row][col + 3])

                computerPieces = self.count_player_pieces(groupingFourList, 1)
                humanPieces = self.count_player_pieces(groupingFourList, 0)
                emptyPieces = self.count_player_pieces(groupingFourList, self.EMPTY)

                score += self.score_metric(computerPieces, humanPieces, emptyPieces)
                groupingFourList = []
        
        return score

    def get_upright_score(self, board, computerPlayer, humanPlayer):
        score = 0
        # List to collect all the groupings of 4(Horizontally) out of the current game state
        groupingFourList = []
        for col in range(0, self.COLUMNS - 3):
            for row in range(3, self.ROWS):
                groupingFourList.append(board[row][col])
                groupingFourList.append(board[row - 1][col + 1])
                groupingFourList.append(board[row - 2][col + 2])
                groupingFourList.append(board[row - 3][col + 3])

                computerPieces = self.count_player_pieces(groupingFourList, 1)
                humanPieces = self.count_player_pieces(groupingFourList, 0)
                emptyPieces = self.count_player_pieces(groupingFourList, self.EMPTY)

                score += self.score_metric(computerPieces, humanPieces, emptyPieces)
                groupingFourList = []
        
        return score

    def get_upleft_score(self, board, computerPlayer, humanPlayer):
        score = 0
        # List to collect all the groupings of 4(Horizontally) out of the current game state
        groupingFourList = []
        for col in range(3, self.COLUMNS):
            for row in range(3, self.ROWS):
                groupingFourList.append(board[row][col])
                groupingFourList.append(board[row - 1][col - 1])
                groupingFourList.append(board[row - 2][col - 2])
                groupingFourList.append(board[row - 3][col - 3])

                computerPieces = self.count_player_pieces(groupingFourList, 1)
                humanPieces = self.count_player_pieces(groupingFourList, humanPlayer)
                emptyPieces = self.count_player_pieces(groupingFourList, self.EMPTY)

                score += self.score_metric(computerPieces, humanPieces, emptyPieces)
                groupingFourList = []
        
        return score

    def get_vert_score(self, board, computerPlayer, humanPlayer):
        score = 0
        # List to collect all the groupings of 4(Horizontally) out of the current game state
        groupingFourList = []
        for col in range(0, self.COLUMNS):
            for row in range(0, self.ROWS -3):
                groupingFourList.append(board[row][col])
                groupingFourList.append(board[row + 1][col])
                groupingFourList.append(board[row + 2][col])
                groupingFourList.append(board[row + 3][col])

                computerPieces = self.count_player_pieces(groupingFourList, computerPlayer)
                humanPieces = self.count_player_pieces(groupingFourList, humanPlayer)
                emptyPieces = self.count_player_pieces(groupingFourList, self.EMPTY)

                score += self.score_metric(computerPieces, humanPieces, emptyPieces)
                groupingFourList = []
        
        return score

    def count_player_pieces(self, groupingFourList, playerPiece):
        totalPieces = 0

        for piece in groupingFourList:
            if piece == playerPiece:
                totalPieces += 1
        
        return totalPieces

    def score_metric(self, computerPieces, humanPieces, emptyPieces):
        score = 0

        # Making bot prioritize playing defense than offense
        # Thats why the score is lower when regarding the enemy: AI chooses highest scoring move
        if (computerPieces == 4):
            score += 100
        elif (computerPieces == 3 and emptyPieces == 1):
            score += 20
        elif (computerPieces == 2 and emptyPieces == 2):
            score += 10
        if (humanPieces == 3 and emptyPieces == 1):
            score -= 100

        return score
