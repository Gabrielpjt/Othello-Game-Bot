from othello_game import OthelloGame
import random

def get_best_move(game, max_generations=50, population_size=20):
    """
    Given the current game state, this function returns the best move for the AI player using the Genetic Algorithm.

    Parameters:
        game (OthelloGame): The current game state.
        max_generations (int): The maximum number of generations for the genetic algorithm.
        population_size (int): The size of the population.

    Returns:
        tuple: A tuple containing the evaluation value of the best move and the corresponding move (row, col).
    """
    return genetic_algorithm(game, max_generations, population_size)

def genetic_algorithm(game, max_generations, population_size):
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
    population = [random.choice(game.get_valid_moves()) for _ in range(population_size)]

    # Evolve the population over generations
    for generation in range(max_generations):
        # Evaluate the fitness of each individual (move) in the population
        fitness_scores = [(move, evaluate_move(game, move)) for move in population]

        # Select parents based on fitness scores (higher scores have higher chance of being selected)
        parents = selection(fitness_scores)

        # Create the next generation through crossover and mutation
        next_generation = []
        for i in range(0, len(parents), 2):
            parent1 = parents[i]
            parent2 = parents[(i + 1) % len(parents)]
            offspring1, offspring2 = crossover(parent1, parent2)
            next_generation.append(mutate(offspring1, game))
            next_generation.append(mutate(offspring2, game))

        # Update population with the new generation
        population = next_generation

    # Return the best move from the final population
    best_move = max(population, key=lambda move: evaluate_move(game, move))
    best_eval = evaluate_move(game, best_move)
    return best_eval, best_move

def selection(fitness_scores):
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

def crossover(parent1, parent2):
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

def mutate(move, game):
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

def evaluate_move(game, move):
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
    return evaluate_game_state(new_game)

# The functions evaluate_game_state and calculate_stability remain the same as in the original code.
