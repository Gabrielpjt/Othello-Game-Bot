from othello_game import OthelloGame

def get_best_move(game, max_depth=8):
    """
    Given the current game state, this function returns the best move for the AI player using the Alpha-Beta Pruning
    algorithm with a specified maximum search depth.
    """
    valid_moves = game.get_valid_moves()

    if not valid_moves:
        return None  # No valid moves available

    _, best_move = alphabeta(game, max_depth)
    return best_move


def alphabeta(game, depth, maximizing_player=True, alpha=float("-inf"), beta=float("inf"), cache={}):
    """
    Alpha-Beta Pruning algorithm for selecting the best move for the AI player.
    """
    game_state_key = tuple(map(tuple, game.board))  # Convert board to tuple for caching

    if depth == 0 or game.is_game_over():
        return evaluate_game_state(game), None

    # Use cached evaluation if available
    if game_state_key in cache:
        return cache[game_state_key]

    valid_moves = game.get_valid_moves()

    if maximizing_player:
        max_eval = float("-inf")
        best_move = None

        for move in sorted(valid_moves, key=lambda mv: heuristic_sort(game, mv), reverse=True):
            # Make move in place
            original_board = [row[:] for row in game.board]
            game.make_move(*move)

            eval, _ = alphabeta(game, depth - 1, False, alpha, beta, cache)
            eval = eval[0] if isinstance(eval, tuple) else eval  # Ensure eval is not a tuple

            # Undo the move
            game.board = original_board
            game.current_player *= -1  # Revert player

            if eval > max_eval:
                max_eval = eval
                best_move = move

            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        cache[game_state_key] = (max_eval, best_move)
        return max_eval, best_move

    else:
        min_eval = float("inf")
        best_move = None

        for move in sorted(valid_moves, key=lambda mv: heuristic_sort(game, mv)):
            # Make move in place
            original_board = [row[:] for row in game.board]
            game.make_move(*move)

            eval, _ = alphabeta(game, depth - 1, True, alpha, beta, cache)
            eval = eval[0] if isinstance(eval, tuple) else eval  # Ensure eval is not a tuple

            # Undo the move
            game.board = original_board
            game.current_player *= -1  # Revert player

            if eval < min_eval:
                min_eval = eval
                best_move = move

            beta = min(beta, eval)
            if beta <= alpha:
                break

        cache[game_state_key] = (min_eval, best_move)
        return min_eval, best_move

def heuristic_sort(game, move):
    """
    Heuristic to prioritize good moves first, such as corner moves.
    """
    row, col = move
    # Prioritize corner moves or edge moves
    if (row, col) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
        return 100  # Highest priority for corners
    if row == 0 or row == 7 or col == 0 or col == 7:
        return 10  # Priority for edges
    return 0  # Default for other moves

def evaluate_game_state(game):
    """
    Evaluates the current game state for the AI player based on various factors like coin parity, mobility, and corner/edge occupancy.
    """
    coin_parity_weight = 1.0
    mobility_weight = 2.0
    corner_weight = 5.0
    edge_weight = 2.0

    player = game.current_player
    opponent = -game.current_player

    # Coin parity
    player_count = sum(row.count(player) for row in game.board)
    opponent_count = sum(row.count(opponent) for row in game.board)
    coin_parity = (player_count - opponent_count) * coin_parity_weight

    # Mobility
    player_moves = len(game.get_valid_moves())
    opponent_moves = len(OthelloGame(player_mode=opponent).get_valid_moves())
    mobility = (player_moves - opponent_moves) * mobility_weight

    # Corners
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    player_corners = sum(1 for (r, c) in corners if game.board[r][c] == player)
    opponent_corners = sum(1 for (r, c) in corners if game.board[r][c] == opponent)
    corner_occupancy = (player_corners - opponent_corners) * corner_weight

    # Edge occupancy
    edges = [(i, j) for i in [0, 7] for j in range(1, 7)] + [(i, j) for i in range(1, 7) for j in [0, 7]]
    player_edges = sum(1 for (r, c) in edges if game.board[r][c] == player)
    opponent_edges = sum(1 for (r, c) in edges if game.board[r][c] == opponent)
    edge_occupancy = (player_edges - opponent_edges) * edge_weight

    # Final evaluation
    evaluation = coin_parity + mobility + corner_occupancy + edge_occupancy
    return evaluation
