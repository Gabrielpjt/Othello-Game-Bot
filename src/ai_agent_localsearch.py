import time
import random
import math
from othello_game import OthelloGame

class ai_agent_localsearch:

    def __init__(self) -> None:
        pass

    def scheduling_function(self, end_time, max_time):
        return (end_time - time.time()) / max_time
    
    def get_best_move(self, game, ai_agent_name, max_time=4):
        start_time = time.time()
        end_time = start_time + max_time
        current_move = random.choice(game.get_valid_moves())
        current_score = self.evaluate_game_state(game, current_move)
        T = 1.0 
        while T > 0:
            T = self.scheduling_function(end_time, max_time)
            if(T<=0):
                break
            new_move = random.choice(game.get_valid_moves())
            new_score = self.evaluate_game_state(game, new_move)
            if (new_score > current_score):
                current_move = new_move
                current_score = new_score
            else:
                delta_score = new_score - current_score
                acceptance_probability = math.exp(delta_score / T)
                if (acceptance_probability) > 0.5:
                    current_move = new_move
                    current_score = new_score
        return current_move
    
    def evaluate_game_state(self, game, move):
        new_game = OthelloGame(player_mode=game.player_mode)
        new_game.board = [row[:] for row in game.board]
        new_game.current_player = game.current_player
        new_game.make_move(*move)
        
        coin_parity_weight = 1.0
        mobility_weight = 2.0
        corner_occupancy_weight = 5.0
        stability_weight = 3.0
        edge_occupancy_weight = 2.5
        player_disk_count = sum(row.count(new_game.current_player) for row in new_game.board)
        opponent_disk_count = sum(row.count(-new_game.current_player) for row in new_game.board)
        coin_parity = player_disk_count - opponent_disk_count
        player_valid_moves = len(new_game.get_valid_moves())
        opponent_valid_moves = len(
            OthelloGame(player_mode=-new_game.current_player).get_valid_moves()
        )
        mobility = player_valid_moves - opponent_valid_moves
        corner_occupancy = sum(
            new_game.board[i][j] for i, j in [(0, 0), (0, 7), (7, 0), (7, 7)]
        )
        stability = self.calculate_stability(new_game)
        edge_occupancy = sum(new_game.board[i][j] for i in [0, 7] for j in range(1, 7)) + sum(
            new_game.board[i][j] for i in range(1, 7) for j in [0, 7]
        )
        evaluation = (
            coin_parity * coin_parity_weight
            + mobility * mobility_weight
            + corner_occupancy * corner_occupancy_weight
            + stability * stability_weight
            + edge_occupancy * edge_occupancy_weight
        )
        return evaluation
    def calculate_stability(self, game):
        def neighbors(row, col):
            return [
                (row + dr, col + dc)
                for dr in [-1, 0, 1]
                for dc in [-1, 0, 1]
                if (dr, dc) != (0, 0) and 0 <= row + dr < 8 and 0 <= col + dc < 8
            ]
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        edges = [(i, j) for i in [0, 7] for j in range(1, 7)] + [
            (i, j) for i in range(1, 7) for j in [0, 7]
        ]
        inner_region = [(i, j) for i in range(2, 6) for j in range(2, 6)]
        regions = [corners, edges, inner_region]
        stable_count = 0
        def is_stable_disk(row, col):
            return (
                all(game.board[r][c] == game.current_player for r, c in neighbors(row, col))
                or (row, col) in edges + corners
            )
        for region in regions:
            for row, col in region:
                if (game.board[row][col] == game.current_player and is_stable_disk(row, col)):
                    stable_count += 1
        return stable_count