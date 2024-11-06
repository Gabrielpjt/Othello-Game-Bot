from othello_game import OthelloGame
from evaluator import Evaluator
import random

class ai_agent_genetic:

  def __init__(self) -> None:
        pass

  def get_best_move(self, game, max_generations=50, population_size=20):
      """
      Given the current game state, this function returns the best move for the AI player using the Genetic Algorithm.
      """
      _, best_move = self.genetic_algorithm(game, max_generations, population_size)
      return self.genetic_algorithm(game, max_generations, population_size)

  def genetic_algorithm(self, game, max_generations, population_size):
      """
      Genetic algorithm for selecting the best move for the AI player.
      """
      population = [random.choice(game.get_valid_moves()) for _ in range(population_size)]

      for generation in range(max_generations):
          fitness_scores = [(move, self.evaluate_move(game, move)) for move in population]
          parents = self.selection(fitness_scores)

          next_generation = []
          for i in range(0, len(parents), 2):
              parent1 = parents[i]
              parent2 = parents[(i + 1) % len(parents)]
              offspring1, offspring2 = self.crossover(parent1, parent2)
              next_generation.append(self.mutate(offspring1, game))
              next_generation.append(self.mutate(offspring2, game))

          population = next_generation

      best_move = max(population, key=lambda move: self.evaluate_move(game, move))
      best_eval = self.evaluate_move(game, best_move)
      return best_eval, best_move

  def evaluate_move(self, game, move):
      """
      Evaluates a move using the Evaluator class and returns a score.
      """
      # Create a new game instance to simulate the move
      new_game = OthelloGame(player_mode=game.player_mode)
      new_game.board = [row[:] for row in game.board]  # Copy the current board
      new_game.current_player = game.current_player  # Set the current player
      new_game.make_move(*move)  # Make the move in the simulated game

      evaluator = Evaluator()

      # Create a new board state for the evaluation
      start_board = new_game.board  # Directly use the board's state

      # Get the current player and opponent
      player = new_game.current_player
      opponent = -player

      # Evaluate the score using the evaluator
      return evaluator.score(start_board, new_game, currentDepth=0, player=player, opponent=opponent)



  # Selection, crossover, and mutation functions remain the same as in your previous code.
  def selection(self, fitness_scores):
      fitness_scores.sort(key=lambda x: x[1], reverse=True)
      return [move for move, _ in fitness_scores[:len(fitness_scores)//2]]

  def crossover(self, parent1, parent2):
      row1, col1 = parent1
      row2, col2 = parent2
      offspring1 = ((row1 + row2) // 2, (col1 + col2) // 2)
      offspring2 = ((row2 + row1) // 2, (col2 + col1) // 2)
      return offspring1, offspring2

  def mutate(self, move, game):
      valid_moves = game.get_valid_moves()
      if random.random() < 0.1:  # 10% chance of mutation
          return random.choice(valid_moves)
      return move

  def evaluate_game_state(self, game):
      """
      Evaluates the current game state for the AI player.

      Parameters:
          game (OthelloGame): The current game state.

      Returns:
          float: The evaluation value representing the desirability of the game state for the AI player.
      """
      # Weights for various factors
      weights = self.dynamic_weights(len(game.get_valid_moves()))

      # Coin parity (difference in disk count)
      player_disk_count = sum(row.count(game.current_player) for row in game.board)
      opponent_disk_count = sum(row.count(-game.current_player) for row in game.board)
      coin_parity = player_disk_count - opponent_disk_count

      # Mobility (number of valid moves for the current player)
      player_valid_moves = len(game.get_valid_moves())
      opponent_valid_moves = len(OthelloGame(player_mode=-game.current_player).get_valid_moves())
      mobility = player_valid_moves - opponent_valid_moves

      # Corner occupancy
      corner_occupancy = sum(game.board[i][j] == game.current_player for i, j in [(0, 0), (0, 7), (7, 0), (7, 7)])

      # Stability
      stability = self.calculate_stability(game)

      # Edge occupancy
      edge_occupancy = sum(game.board[i][j] == game.current_player for i in [0, 7] for j in range(1, 7)) + \
                      sum(game.board[i][j] == game.current_player for i in range(1, 7) for j in [0, 7])

      # Final evaluation
      evaluation = (
          coin_parity * weights["coin_parity"] +
          mobility * weights["mobility"] +
          corner_occupancy * weights["corner_occupancy"] +
          stability * weights["stability"] +
          edge_occupancy * weights["edge_occupancy"]
      )

      return evaluation

  def calculate_stability(self, game):
      """
      Calculate the number of stable pieces on the board.
      """
      def neighbors(row, col):
          return [
              (row + dr, col + dc)
              for dr in [-1, 0, 1]
              for dc in [-1, 0, 1]
              if (dr, dc) != (0, 0) and 0 <= row + dr < 8 and 0 <= col + dc < 8
          ]

      stable_count = 0
      for i in range(8):
          for j in range(8):
              if game.board[i][j] == game.current_player and all(
                  game.board[r][c] == game.current_player for r, c in neighbors(i, j)
              ):
                  stable_count += 1
      return stable_count

  def dynamic_weights(self, num_moves_left):
      """
      Adjusts weights dynamically based on the game phase.
      """
      if num_moves_left > 40:
          return {"coin_parity": 1.0, "mobility": 3.0, "corner_occupancy": 5.0, "stability": 2.0, "edge_occupancy": 2.0}
      elif num_moves_left > 20:
          return {"coin_parity": 1.5, "mobility": 2.5, "corner_occupancy": 6.0, "stability": 3.0, "edge_occupancy": 2.5}
      else:
          return {"coin_parity": 2.0, "mobility": 1.5, "corner_occupancy": 7.0, "stability": 4.0, "edge_occupancy": 3.0}
