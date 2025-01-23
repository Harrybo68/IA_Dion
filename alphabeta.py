import numpy as np

winner_value = 500
draw_value = 0

def alpha_beta_decision(board, turn, ai_level, queue, max_player):
    node_count = 0
    alpha = -np.inf
    beta = np.inf
    best_score = -np.inf
    best_move = None
    depth = 0

    possible_moves = board.get_possible_moves()

    for move in possible_moves:
        new_board = board.copy()
        new_board.add_disk(move, max_player, update_display=False)
        score, node_count = min_value_ab(new_board, turn + 1, ai_level, alpha, beta, node_count, max_player, depth + 1)

        if score > best_score:
            best_score = score
            best_move = move

    print(f"Nodes evaluated for best move for alphabeta : {node_count} and best score : {best_score} for player : {max_player}")

    queue.put(best_move)
    return best_move

def min_value_ab(board, turn, ai_level, alpha, beta, node_count, max_player, depth):
    node_count += 1

    possible_moves = board.get_possible_moves()

    if board.check_victory():
        return winner_value - depth, node_count
    elif not possible_moves:
        return draw_value - depth, node_count
    elif depth == ai_level:
        return board.eval(max_player) - depth, node_count

    v = np.inf
    for move in possible_moves:
        new_board = board.copy()
        new_board.add_disk(move,  max_player % 2 + 1, update_display=False)
        max_val, node_count = max_value_ab(new_board, turn + 1, ai_level, alpha, beta, node_count, max_player, depth + 1)
        v = min(v, max_val)

        if v <= alpha:
            return v, node_count
        beta = min(beta, v)

    return v, node_count

def max_value_ab(board, turn, ai_level, alpha, beta, node_count, max_player, depth):
    node_count += 1

    possible_moves = board.get_possible_moves()

    if board.check_victory():
        return - winner_value + depth, node_count
    elif not possible_moves:
        return draw_value + depth, node_count
    elif depth == ai_level:
        return - board.eval(max_player) + depth, node_count

    v = -np.inf
    for move in possible_moves:
        new_board = board.copy()
        new_board.add_disk(move, max_player, update_display=False)
        min_val, node_count = min_value_ab(new_board, turn + 1, ai_level, alpha, beta, node_count, max_player, depth + 1)
        v = max(v, min_val)

        if v >= beta:
            return v, node_count
        alpha = max(alpha, v)

    return v, node_count