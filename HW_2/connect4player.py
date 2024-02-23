from typing import Tuple
import random

class ComputerPlayer:
    def __init__(self, id: int, difficulty_level: int):
        self.id = id
        self.difficulty_level = difficulty_level

    def pick_move(self, rack: Tuple[Tuple[int, ...], ...]) -> int:
        moves = self.generate_legal_moves(rack)
        if not moves:
            return -1  # No legal moves available
        return random.choice(moves)

    def generate_legal_moves(self, rack: Tuple[Tuple[int, ...], ...]) -> list:
        legal_moves = []
        for col in range(len(rack[0])):
            if rack[0][col] == 0:
                legal_moves.append(col)
        return legal_moves

    def _simulate_move(self, rack: Tuple[Tuple[int, ...], ...], move: int, player: int) -> Tuple[Tuple[int, ...], ...]:
        new_rack = list(rack)
        for row in range(len(new_rack)):
            if new_rack[row][move] == 0:
                new_rack[row] = new_rack[row][:move] + (player,) + new_rack[row][move + 1 :]
                break
        return tuple(new_rack)

    def find_win(self, rack: Tuple[Tuple[int, ...], ...]) -> int:
        """
        Check if a player has won the game.

        Parameters:
            rack (tuple): The current state of the Connect Four board.

        Returns:
            int: The ID of the winning player (1 or 2), or 0 if no player has won.
        """
        # Check horizontal
        for row in rack:
            for col in range(len(row) - 3):
                if row[col] != 0 and row[col] == row[col + 1] == row[col + 2] == row[col + 3]:
                    return row[col]

        # Check vertical
        for col in range(len(rack[0])):
            for row in range(len(rack) - 3):
                if rack[row][col] != 0 and rack[row][col] == rack[row + 1][col] == rack[row + 2][col] == rack[row + 3][col]:
                    return rack[row][col]

        # Check diagonal (up-right)
        for row in range(len(rack) - 3):
            for col in range(len(rack[0]) - 3):
                if rack[row][col] != 0 and rack[row][col] == rack[row + 1][col + 1] == rack[row + 2][col + 2] == rack[row + 3][col + 3]:
                    return rack[row][col]

        # Check diagonal (down-right)
        for row in range(3, len(rack)):
            for col in range(len(rack[0]) - 3):
                if rack[row][col] != 0 and rack[row][col] == rack[row - 1][col + 1] == rack[row - 2][col + 2] == rack[row - 3][col + 3]:
                    return rack[row][col]

        return 0  # No winner

    def negamax(self, rack: Tuple[Tuple[int, ...], ...], depth: int, alpha: float, beta: float, color: int) -> int:
        if depth == 0 or self.find_win(rack) != 0:
            return color * self.evaluate(rack, self.id)

        moves = self.generate_legal_moves(rack)
        for move in moves:
            new_rack = self._simulate_move(rack, move, color)
            score = -self.negamax(new_rack, depth - 1, -beta, -alpha, 3 - color)
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        return alpha

    def evaluate(self, rack: Tuple[Tuple[int, ...], ...], player_id: int) -> int:
        score = 0
        # Evaluate each quartet
        for row in range(len(rack)):
            for col in range(len(rack[0])):
                if col <= len(rack[0]) - 4:
                    score += self.evaluate_quartet(rack[row][col:col+4], player_id)
                if row <= len(rack) - 4:
                    score += self.evaluate_quartet([rack[row+i][col] for i in range(4)], player_id)
                if col <= len(rack[0]) - 4 and row <= len(rack) - 4:
                    score += self.evaluate_quartet([rack[row+i][col+i] for i in range(4)], player_id)
                if col >= 3 and row <= len(rack) - 4:
                    score += self.evaluate_quartet([rack[row+i][col-i] for i in range(4)], player_id)
        return score

    def evaluate_quartet(self, quartet: list, player_id: int) -> int:
        opponent_id = 3 - player_id  # Calculate the opponent's ID
        if quartet.count(player_id) == 4:
            return 1000000
        elif quartet.count(opponent_id) == 4:
            return -1000000
        elif quartet.count(player_id) == 3 and quartet.count(0) == 1:
            return 100
        elif quartet.count(opponent_id) == 3 and quartet.count(0) == 1:
            return -100
        elif quartet.count(player_id) == 2 and quartet.count(0) == 2:
            return 10
        elif quartet.count(opponent_id) == 2 and quartet.count(0) == 2:
            return -10
        elif quartet.count(player_id) == 1 and quartet.count(0) == 3:
            return 1
        elif quartet.count(opponent_id) == 1 and quartet.count(0) == 3:
            return -1
        return 0

