class OthelloGame:
    def __init__(self, player_mode="friend"):
        """
        A class representing the Othello game board and its rules.

        Args:
            player_mode (str): The mode of the game, either "friend" or "ai" (default is "friend").
        """
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        self.board[3][3] = 1
        self.board[3][4] = -1
        self.board[4][3] = -1
        self.board[4][4] = 1
        self.current_player = 1
        self.player_mode = player_mode

    def count_stones(self):
        """Count the number of white, black, and empty stones on the board."""
        whites = sum(row.count(1) for row in self.board)  # Count white stones
        blacks = sum(row.count(-1) for row in self.board)  # Count black stones
        empty = sum(row.count(0) for row in self.board)  # Count empty spaces
        return whites, blacks, empty

    def get_board(self):
        return self.board  # Returns the current board state as a 2D list.

    def compare(self, start_board):
        """
        Compare the current board with a start board.

        Args:
            start_board (list): The board to compare against, must be a 2D list.

        Returns:
            list: A list representing the changes (differences) between the two boards.
        """
        if not isinstance(start_board, list) or not all(isinstance(row, list) for row in start_board):
            raise ValueError("start_board must be a 2D list representing the game board.")

        changes = []
        for r in range(8):
            for c in range(8):
                if self.board[r][c] != start_board[r][c]:
                    changes.append((r, c))
        return changes

    def is_valid_move(self, row, col):
      """
      Check if the move is valid and results in flipping opponent disks.

      Args:
          row (int): The row index of the move.
          col (int): The column index of the move.

      Returns:
          bool: True if the move is valid and flips opponent disks, False otherwise.
      """
      # First, ensure the move is within the board boundaries
      if not (0 <= row < 8 and 0 <= col < 8):
          return False

      if self.board[row][col] != 0:
          return False

      # Check in all eight directions for opponent disks to flip
      directions = [
          (-1, -1), (-1, 0), (-1, 1),
          (0, -1),         (0, 1),
          (1, -1), (1, 0), (1, 1),
      ]
      for dr, dc in directions:
          r, c = row + dr, col + dc
          # Make sure the first step is within bounds and is an opponent's disk
          if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == -self.current_player:
              # Continue checking in this direction
              r += dr
              c += dc
              while 0 <= r < 8 and 0 <= c < 8:
                  if self.board[r][c] == self.current_player:
                      return True
                  if self.board[r][c] == 0:
                      break
                  r += dr
                  c += dc

      return False


    def flip_disks(self, row, col):
        """
        Flip the opponent's disks after placing a disk at the given position.

        Args:
            row (int): The row index of the move.
            col (int): The column index of the move.
        """
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            flip_list = []
            while (
                0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == -self.current_player
            ):
                flip_list.append((r, c))
                r += dr
                c += dc
                if (
                    0 <= r < 8
                    and 0 <= c < 8
                    and self.board[r][c] == self.current_player
                ):
                    for fr, fc in flip_list:
                        self.board[fr][fc] = self.current_player

    def make_move(self, row, col):
        """
        Make a move at the given position for the current player if it's a valid move.

        Args:
            row (int): The row index of the move.
            col (int): The column index of the move.
        """
        if self.is_valid_move(row, col):
            self.board[row][col] = self.current_player
            self.flip_disks(row, col)
            self.current_player *= -1

    def is_game_over(self):
        """
        Check if the game is over (no more valid moves or board is full).

        Returns:
            bool: True if the game is over, False otherwise.
        """
        return not self.get_valid_moves() or all(
            all(cell != 0 for cell in row) for row in self.board
        )

    def get_winner(self):
        """
        Get the winner of the game (1 for Black, -1 for White, 0 for a tie).

        Returns:
            int: The winner of the game (1 for Black, -1 for White, 0 for a tie).
        """
        black_count = sum(row.count(1) for row in self.board)
        white_count = sum(row.count(-1) for row in self.board)

        if black_count > white_count:
            return 1
        elif black_count < white_count:
            return -1
        else:
            return 0

    def get_valid_moves(self):
        """
        Get a list of valid moves for the current player.

        Returns:
            list: A list of valid moves represented as tuples (row, col).
        """
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col):
                    valid_moves.append((row, col))
        return valid_moves
