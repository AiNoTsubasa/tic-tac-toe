import numpy as np
import random

class TicTacToe:
  def __init__(self):
    self.__O_MOVES = []
    self.__X_MOVES = []
    self.__o_player = "human"
    self.__x_player = "ai"
    self.__WIN_PATTERNS = [
      [0, 3, 6],
      [1, 4, 7],
      [2, 5, 8],
      [0, 1, 2],
      [3, 4, 5],
      [7, 8, 9],
      [0, 4, 8],
      [2, 4, 6]
    ]
    self.__boards = np.array(["_"] * 9)
    self.__debug_mode = False
    self.__is_o_player_win = False
    self.__is_x_player_win = False
  
  def set_debug_mode(self, debug_mode):
    self.__debug_mode = debug_mode
  
  def __display_board(self):
    if len(self.__O_MOVES) > 0:
      self.__boards[self.__O_MOVES] = ["O"]
    if len(self.__X_MOVES) > 0:
      self.__boards[self.__X_MOVES] = ["X"]
    print(self.__boards.reshape([3, 3]), "\n")

  def __check_win(self, player_moves):
    for win_pattern in self.__WIN_PATTERNS:
      if all(x in player_moves for x in win_pattern):
        return True
    return False
  
  def __check_win(self, player_moves):
    for win_pattern in self.__WIN_PATTERNS:
      if all(w in player_moves for w in win_pattern):
        return True
    return False

  def __get_available_moves(self, moved):
    boards = np.array(range(0, 9))
    return np.setdiff1d(boards, moved)
  
  def __check_game_end(self):
    boards = np.array(range(0, 9))
    moved = self.__O_MOVES + self.__X_MOVES
    return len(boards) == len(moved) or self.__is_o_player_win or self.__is_x_player_win
  
  def __get_random_move(self):
    avaliable_moves = self.__get_available_moves(self.__O_MOVES + self.__X_MOVES)
    return random.choice(avaliable_moves)
  
  def __minimax(self, o_moves, x_moves, player, depth):
    result = { 'score': 0, 'move': None }
    available_moves = self.__get_available_moves(o_moves + x_moves)
    if self.__check_win(o_moves):
      result['score'] = 10 - depth
      return result
    elif self.__check_win(x_moves):
      result['score'] = depth -10 
      return result
    elif len(available_moves) == 0:
      result['score'] = 0
      return result
    else:
      best_moves = []
      if player == self.__o_player:
        indicator = -100
        for next_move in available_moves:
          next_o_moves = o_moves.copy()
          next_o_moves.append(next_move)
          path_result = self.__minimax(next_o_moves, x_moves, self.__x_player, depth + 1)
          path_result['move'] = next_move
          if path_result['score'] > indicator:
            best_moves = [path_result]
            indicator = path_result['score']
          elif path_result['score'] == indicator:
            best_moves.append(path_result)
        
        return random.choice(best_moves)
      else:
        indicator = 100
        for next_move in available_moves:
          next_x_moves = x_moves.copy()
          next_x_moves.append(next_move)
          path_result = self.__minimax(o_moves, next_x_moves, self.__o_player, depth + 1)
          path_result['move'] = next_move
          if path_result['score'] < indicator:
            best_moves = [path_result]
            indicator = path_result['score']
          elif path_result['score'] == indicator:
            best_moves.append(path_result)
          
          if self.__debug_mode and depth == 0:
            print('Next move score: ', path_result)

        if self.__debug_mode and depth == 0:
            print('Best next move score: ', best_moves)
        return random.choice(best_moves)


  
  def __find_ai_next_move(self):
    next_move_result = self.__minimax(self.__O_MOVES, self.__X_MOVES, self.__x_player, 0)
    return next_move_result['move']
  
  def __execute_human_turn(self):
    print("Your turn...")
    move = int(input("\tPlease enter your move (1~9): ")) - 1
    while move in (self.__O_MOVES + self.__X_MOVES):
      available_moves = self.__get_available_moves(self.__O_MOVES + self.__X_MOVES)
      move = int(input("\tInvalid move!! Please enter your move ("+ ", ".join([str(m + 1) for m in available_moves]) +"): ")) - 1
    self.__O_MOVES.append(move)
    self.__is_o_player_win = self.__check_win(self.__O_MOVES)

  def __execute_ai_turn(self):
    print("AI's turn...")
    if len(self.__X_MOVES) == 0:
      move = self.__get_random_move()
    else:
      move = self.__find_ai_next_move()
    
    self.__X_MOVES.append(move)
    self.__is_x_player_win = self.__check_win(self.__X_MOVES)
  
  def start(self):
    print("===== GAME START! =====")
    self.__display_board()
    while not self.__check_game_end():
      count_turn = len(self.__O_MOVES + self.__X_MOVES)
      if count_turn % 2 == 0:
        self.__execute_human_turn()
      else:
        self.__execute_ai_turn()
      self.__display_board()
    
    if self.__is_o_player_win:
      print("You win!!!")
    elif self.__is_x_player_win:
      print("AI win!!!")
    else:
      print("### Draw!!! ###")
    print("===== GAME END! =====")