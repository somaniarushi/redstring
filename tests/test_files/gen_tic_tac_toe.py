from gen.gen import *

def is_terminal_state(board):
    if get_winner(board) is not None:
        return True
    for row in board:
        for col in row:
            if col == ' ':
                return False
    return True

def get_all_possible_actions(board):
    actions = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == ' ':
                actions.append((i, j))
    return actions

def init_board():
    board = [[' ', ' ', ' '],
             [' ', ' ', ' '],
             [' ', ' ', ' ']]
    return board

def edit_board_based_on_action(board, action, player):
    board[action[0]][action[1]] = player
    return board

def action_with_min_value(board, alpha, beta):
    if is_terminal_state(board):
        return None, get_value_of_state(board)

    best_action = None
    min_val = float('inf')
    for action in get_all_possible_actions(board):
        player = 'X'
        board = edit_board_based_on_action(board, action, player)
        action, value = action_with_max_value(board, alpha, beta)
        if value < min_val:
            best_action = action
        min_val = min(min_val, value)
        if min_val <= alpha:
            return action, min_val
        beta = min(beta, min_val)

    return action, min_val

def print_board(board):
    for row in board:
        print(row)

def player_x_takes_action(board):
    action = input("Enter action: ")
    action = action.split(",")
    action = (int(action[0]), int(action[1]))
    board = edit_board_based_on_action(board, action, 'X')
    return board

def get_winner(board):
    for i in range(len(board)):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != ' ':
            return board[i][0]
    for i in range(len(board)):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != ' ':
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]
    return None

def get_value_of_state(board):
    winner = get_winner(board)
    if winner == 'X':
        return -1
    elif winner == 'O':
        return 1
    else:
        return 0

def announce_winner(winner):
    if winner == 'X':
        print("Player X wins!")
    elif winner == 'O':
        print("Player O wins!")
    else:
        print("It's a tie!")

def alpha_beta_search(board):
    action, value = action_with_max_value(board, float('inf'), float('-inf'))
    return action

def action_with_max_value(board, alpha, beta):
    if is_terminal_state(board):
        return None, get_value_of_state(board)

    best_action = None
    max_val = float('-inf')
    for action in get_all_possible_actions(board):
        player = 'O'
        board = edit_board_based_on_action(board, action, player)
        action, value = action_with_min_value(board, alpha, beta)
        if value > max_val:
            best_action = action
        max_val = max(max_val, value)
        if max_val >= beta:
            return best_action, max_val
        alpha = max(alpha, max_val)

    return action, max_val

class TicTacToeAI:

    def make_next_move(self, board):
        best_action_for_player_o = alpha_beta_search(board)
        print(best_action_for_player_o)
        if best_action_for_player_o is None:
            return board
        board = edit_board_based_on_action(board, best_action_for_player_o, 'O')
        return board

def tic_tac_toe():
    board = init_board()
    ai = TicTacToeAI()
    while True:
        print_board(board)
        board = player_x_takes_action(board)
        winner = get_winner(board)
        if winner is not None:
            announce_winner(winner)
            return
        print_board(board)
        # board = player_o_takes_action(board)
        board = ai.make_next_move(board)
        winner = get_winner(board)
        if winner is not None:
            announce_winner(winner)
            return


if __name__ == "__main__":
    tic_tac_toe()