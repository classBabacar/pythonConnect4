from Connect4 import Connect4
import random
from copy import copy, deepcopy
import pygame
import math

class Minimax(Connect4):
    def __init__(self, player1, player2, screen):
        super().__init__(player1, player2, screen)
    
    def is_game_over(self, board):
        if self.who_won(board, 1) or self.who_won(board, 0):
            return True
        return False

    def generate_move(self, board, depth, computerPlayer, humanPlayer, maximizingPlayer, moveNumber):
        """
        Minimax algorithm to generate computer move
        """
        if depth == 0 or self.is_game_over(board) or self.check_if_tie(board):
            if self.is_game_over(board):
                if self.who_won(board, computerPlayer):
                    return (None, 1000000)
                elif self.who_won(board, humanPlayer):
                    return (None, -1000000)
                elif self.check_if_tie(board):
                    return (None, 0)
            else:
                return (None, self.get_game_score(board, computerPlayer, humanPlayer))

        if maximizingPlayer:
            maxValue = -math.inf
            for move in range(0, self.COLUMNS):
                tmpBoard = self.copyBoard(board)
                if self.is_legal_move(move, tmpBoard):
                    self.drop_piece_computer(move, tmpBoard, moveNumber)
                    result = self.generate_move(tmpBoard, depth - 1, computerPlayer, humanPlayer, False, moveNumber + 1)[1]
                    if float(result) > float(maxValue):
                        maxValue = result
                        bestMove = move
            return bestMove, maxValue
        else:
            minValue = math.inf
            for move in range(0,self.COLUMNS):
                tmpBoard = self.copyBoard(board)
                if self.is_legal_move(move, tmpBoard):
                    self.drop_piece_computer(move, tmpBoard, moveNumber)
                    result = self.generate_move(tmpBoard, depth - 1, computerPlayer, humanPlayer, True, moveNumber + 1)[1]
                    if float(result) < float(minValue):
                        minValue = result
                        bestMove = move
            return bestMove, minValue

    def copyBoard(self, board):
        """
        Copying a replica of the board for the AI to use
        """
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

    def get_game_score(self, board, computerPlayer, humanPlayer):
        """
        Heuristic Algorithm
        """
        score = 0
        score += self.get_center_score(board, computerPlayer, humanPlayer)
        score += self.get_hori_score(board, computerPlayer, humanPlayer)
        score += self.get_vert_score(board, computerPlayer, humanPlayer)
        score += self.get_upright_score(board, computerPlayer, humanPlayer)
        score += self.get_upleft_score(board, computerPlayer, humanPlayer)
        return score

    def get_center_score(self, board, computerPlayer, humanPlayer):
        """
        Making the AI prioritize moving in the center which gives the best odds
        """
        score = counter = 0
        for row in range(0, self.ROWS):
            if board[row][3] == computerPlayer:
                counter += 1
        score += (counter + 1) * 100
        return score

    def get_hori_score(self, board, computerPlayer, humanPlayer):
        """
        Collect all the groupings of 4(Horizontally) for the given board
        """
        score = 0
        groupingFourList = []
        for col in range(0, self.COLUMNS - 3):
            for row in range(0, self.ROWS):
                groupingFourList.append(board[row][col])
                groupingFourList.append(board[row][col + 1])
                groupingFourList.append(board[row][col + 2])
                groupingFourList.append(board[row][col + 3])

                computerPieces = self.count_player_pieces(groupingFourList, computerPlayer)
                humanPieces = self.count_player_pieces(groupingFourList, humanPlayer)
                emptyPieces = self.count_player_pieces(groupingFourList, self.EMPTY)

                score += self.score_metric(computerPieces, humanPieces, emptyPieces)
                groupingFourList = []
        return score

    def get_upright_score(self, board, computerPlayer, humanPlayer):
        """
        Collect all the groupings of 4(Diagonally (Upright)) for the given board
        """
        score = 0
        groupingFourList = []
        for col in range(0, self.COLUMNS - 3):
            for row in range(3, self.ROWS):
                groupingFourList.append(board[row][col])
                groupingFourList.append(board[row - 1][col + 1])
                groupingFourList.append(board[row - 2][col + 2])
                groupingFourList.append(board[row - 3][col + 3])

                computerPieces = self.count_player_pieces(groupingFourList, computerPlayer)
                humanPieces = self.count_player_pieces(groupingFourList, humanPlayer)
                emptyPieces = self.count_player_pieces(groupingFourList, self.EMPTY)

                score += self.score_metric(computerPieces, humanPieces, emptyPieces)
                groupingFourList = []
        return score

    def get_upleft_score(self, board, computerPlayer, humanPlayer):
        """
        Collect all the groupings of 4(Diagonally (Upleft)) for the given board
        """
        score = 0
        groupingFourList = []
        for col in range(3, self.COLUMNS):
            for row in range(3, self.ROWS):
                groupingFourList.append(board[row][col])
                groupingFourList.append(board[row - 1][col - 1])
                groupingFourList.append(board[row - 2][col - 2])
                groupingFourList.append(board[row - 3][col - 3])

                computerPieces = self.count_player_pieces(groupingFourList, computerPlayer)
                humanPieces = self.count_player_pieces(groupingFourList, humanPlayer)
                emptyPieces = self.count_player_pieces(groupingFourList, self.EMPTY)

                score += self.score_metric(computerPieces, humanPieces, emptyPieces)
                groupingFourList = [] 
        return score

    def get_vert_score(self, board, computerPlayer, humanPlayer):
        """
        Collect all the groupings of 4(Vertically) for the given board
        """
        score = 0
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
        """
        For each grouping of 4 we want to count number of AI/Human/Empty Pieces
        """
        totalPieces = 0
        for piece in groupingFourList:
            if piece == playerPiece:
                totalPieces += 1
        return totalPieces

    def score_metric(self, computerPieces, humanPieces, emptyPieces):
        #Idea behind here is I want the AI to prioritize defense over offense, hench why sequences where human player is advantageous force it consider the move
        
        score = 0
        if computerPieces == 3 and emptyPieces == 1:
            score += 200
        elif (computerPieces == 2 and emptyPieces == 2):
            score += 75

        if (humanPieces == 3 and emptyPieces == 1):
            score -= 350
        elif (humanPieces == 2 and emptyPieces == 2):
            score -= 131
        return score
        