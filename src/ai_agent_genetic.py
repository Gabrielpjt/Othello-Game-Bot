from othello_game import OthelloGame
from evaluator import Evaluator
import random

class ai_agent_genetic:

    def __init__(self) -> None:
        pass

    def get_best_move(self, game, ai_agent_name, max_generations=50, population_size=20):
        """
        Given the current game state, this function returns the best move for the AI player using the Genetic Algorithm.

        Parameters:
            game (OthelloGame): The current game state.
            max_generations (int): The maximum number of generations for the genetic algorithm.
            population_size (int): The size of the population.

        Returns:
            tuple: A tuple containing the evaluation value of the best move and the corresponding move (row, col).
        """
        _, best_move = self.genetic_algorithm(game, max_generations, population_size)
        return best_move

    def genetic_algorithm(self, game, max_generations, population_size):
        """
        Genetic algorithm for selecting the best move for the AI player.

        Parameters:
            game (OthelloGame): The current game state.
            max_generations (int): The maximum number of generations to evolve.
            population_size (int): The size of the population.

        Returns:
            tuple: A tuple containing the evaluation value of the best move and the corresponding move (row, col).
        """
        # Generate the initial population of random moves
        print(max_generations)
        population = [random.choice(game.get_valid_moves()) for _ in range(population_size)]

        # Evolve the population over generations
        for generation in range(max_generations):
            # Evaluate the fitness of each individual (move) in the population
            fitness_scores = [(move, self.evaluate_move(game, move)) for move in population]

            # Select parents based on fitness scores (higher scores have higher chance of being selected)
            parents = self.selection(fitness_scores)

            # Create the next generation through crossover and mutation
            next_generation = []
            for i in range(0, len(parents), 2):
                parent1 = parents[i]
                parent2 = parents[(i + 1) % len(parents)]
                offspring1, offspring2 = self.crossover(parent1, parent2)
                next_generation.append(self.mutate(offspring1, game))
                next_generation.append(self.mutate(offspring2, game))

            # Update population with the new generation
            population = next_generation

        # Return the best move from the final population
        best_move = max(population, key=lambda move: self.evaluate_move(game, move))
        best_eval = self.evaluate_move(game, best_move)
        return best_eval, best_move

    def selection(self, fitness_scores):
        """
        Selects individuals (moves) based on their fitness scores using tournament selection.

        Parameters:
            fitness_scores (list): List of tuples (move, fitness_score).

        Returns:
            list: Selected individuals for reproduction.
        """
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        # Select the top half of the population
        return [move for move, _ in fitness_scores[:len(fitness_scores)//2]]

    def crossover(self, parent1, parent2):
        """
        Perform crossover between two parent moves.

        Parameters:
            parent1 (tuple): First parent move (row, col).
            parent2 (tuple): Second parent move (row, col).

        Returns:
            tuple: Two offspring moves resulting from the crossover.
        """
        # Simple crossover by averaging the row and col values of parents
        row1, col1 = parent1
        row2, col2 = parent2
        offspring1 = ((row1 + row2) // 2, (col1 + col2) // 2)
        offspring2 = ((row2 + row1) // 2, (col2 + col1) // 2)
        return offspring1, offspring2

    def mutate(self, move, game):
        """
        Mutate a move by slightly altering the row or column.

        Parameters:
            move (tuple): The move to be mutated (row, col).
            game (OthelloGame): The current game state for ensuring the mutation is valid.

        Returns:
            tuple: The mutated move (row, col).
        """
        valid_moves = game.get_valid_moves()
        if random.random() < 0.1:  # 10% chance of mutation
            return random.choice(valid_moves)
        return move

    def evaluate_move(self, game, move):
        """
        Simulate the game state after a move and evaluate it using the heuristic evaluation function.

        Parameters:
            game (OthelloGame): The current game state.
            move (tuple): The move to be evaluated.

        Returns:
            float: The evaluation value representing the desirability of the game state after the move.
        """
        new_game = OthelloGame(player_mode=game.player_mode)
        new_game.board = [row[:] for row in game.board]
        new_game.current_player = game.current_player
        new_game.make_move(*move)
        return self.evaluate_game_state(new_game)

    def evaluate_game_state(self, game):
        """
        Evaluates the current game state for the AI player.

        Parameters:
            game (OthelloGame): The current game state.

        Returns:
            float: The evaluation value representing the desirability of the game state for the AI player.
        """
        # Evaluation weights for different factors
        coin_parity_weight = 1.0
        mobility_weight = 2.0
        corner_occupancy_weight = 5.0
        stability_weight = 3.0
        edge_occupancy_weight = 2.5

        # Coin parity (difference in disk count)
        player_disk_count = sum(row.count(game.current_player) for row in game.board)
        opponent_disk_count = sum(row.count(-game.current_player) for row in game.board)
        coin_parity = player_disk_count - opponent_disk_count

        # Mobility (number of valid moves for the current player)
        player_valid_moves = len(game.get_valid_moves())
        opponent_valid_moves = len(
            OthelloGame(player_mode=-game.current_player).get_valid_moves()
        )
        mobility = player_valid_moves - opponent_valid_moves

        # Corner occupancy (number of player disks in the corners)
        corner_occupancy = sum(
            game.board[i][j] for i, j in [(0, 0), (0, 7), (7, 0), (7, 7)]
        )

        # Stability (number of stable disks)
        stability = self.calculate_stability(game)

        # Edge occupancy (number of player disks on the edges)
        edge_occupancy = sum(game.board[i][j] for i in [0, 7] for j in range(1, 7)) + sum(
            game.board[i][j] for i in range(1, 7) for j in [0, 7]
        )

        # Combine the factors with the corresponding weights to get the final evaluation value
        evaluation = (
            coin_parity * coin_parity_weight
            + mobility * mobility_weight
            + corner_occupancy * corner_occupancy_weight
            + stability * stability_weight
            + edge_occupancy * edge_occupancy_weight
        )

        return evaluation

    def calculate_stability(self, game):
        """
        Calculates the stability of the AI player's disks on the board.

        Parameters:s
            game (OthelloGame): The current game state.

        Returns:
            int: The number of stable disks for the AI player.
        """

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
                if game.board[row][col] == game.current_player and is_stable_disk(row, col):
                    stable_count += 1

        return stable_count
