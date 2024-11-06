from config import BLACK, WHITE, EMPTY
import ast

class Evaluator(object):
    WIPEOUT_SCORE = 1000 

    def get_location_weight(self, deltaBoard):
      
      try:
          with open("input.txt", "r") as f:
              weightString = f.readline()
              weightArray = ast.literal_eval(weightString)
      except FileNotFoundError:
          print("The file input.txt was not found. Please ensure it exists in the correct directory.")
          return 0  

      weightBoard = [[0]*8 for _ in range(8)]
      for i in range(0, 4):
          for j in range(0, 4):
              weightBoard[i][j] = weightArray[4*i+(j+1)-1]
      for i in range(0, 4):
          for j in range(4, 8):
              weightBoard[i][j] = weightArray[4*i+(8-j)-1]
      for i in range(4, 8):
          for j in range(0, 4):
              weightBoard[i][j] = weightArray[4*(7-i)+(j+1)-1]
      for i in range(4, 8):
          for j in range(4, 8):
              weightBoard[i][j] = weightArray[4*(7-i)+(8-j)-1]

      myScore = 0
      yourScore = 0
      for i in range(8):
          for j in range(8):
              if deltaBoard[i][j] == self.player:
                  myScore += weightBoard[i][j]
              elif deltaBoard[i][j] == self.enemy:
                  yourScore += weightBoard[i][j]

      return myScore - yourScore

    def score(self, startBoard, board, currentDepth, player, opponent):
        """ Determine the score of the given board for the specified player. """
        self.player = player
        self.enemy = opponent
        sc = 0

        deltaBoard = board.compare(startBoard)
        whites = sum(row.count(WHITE) for row in deltaBoard)
        blacks = sum(row.count(BLACK) for row in deltaBoard)

        if (self.player == WHITE and whites == 0) or (self.player == BLACK and blacks == 0):
            return -Evaluator.WIPEOUT_SCORE
        if (self.enemy == WHITE and whites == 0) or (self.enemy == BLACK and blacks == 0):
            return Evaluator.WIPEOUT_SCORE

        sc += self.get_location_weight(deltaBoard)

        return sc
