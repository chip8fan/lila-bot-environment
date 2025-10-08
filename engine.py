import chess
import sys
import time
import random
import chess.engine
class Engine():
    def get_material(self, board: chess.Board): # material code taken from https://chess.stackexchange.com/questions/39004/python-efficient-board-scoring-function-to-use-as-placeholder
        if board.is_game_over() or board.can_claim_draw():
            if board.is_checkmate():
                if board.result() == "1-0":
                    return 100000
                elif board.result() == "0-1":
                    return -100000
            else:
                return 0
        material_difference = 0
        pieces = [[chess.PAWN, 100], [chess.KNIGHT, 300], [chess.BISHOP, 300], [chess.ROOK, 500], [chess.QUEEN, 900]]
        colors = [chess.WHITE, chess.BLACK]
        for piece in pieces:
            for color in colors:
                if color == chess.WHITE:
                    material_difference += piece[1]*len(board.pieces(piece[0], color))
                elif color == chess.BLACK:
                    material_difference -= piece[1]*len(board.pieces(piece[0], color))
        return material_difference
    def negamax(self, board: chess.Board, depth: int, color: int, start_time: float, max_time: float): # psuedocode taken from https://www.chessprogramming.org/Negamax
        if depth == 0 or board.is_game_over() or board.can_claim_draw():
            return self.get_material(board)*color
        elif start_time+max_time <= time.time():
            return None
        max = -sys.maxsize
        for move in list(board.legal_moves):
            board.push(move)
            try:
                score = -self.negamax(board, depth-1, -color, start_time, max_time)
                board.pop()
            except TypeError:
                board.pop()
                return None
            if score > max:
                max = score
        return max
    def play(self, board: chess.Board, max_time: float): # root negamax function
        color = None
        current_depth = 1
        if board.turn == chess.WHITE:
            color = 1
        elif board.turn == chess.BLACK:
            color = -1
        start = time.time()
        lists = []
        break_flag = False
        while True:
            best_moves = []
            max_score = -sys.maxsize
            for move in list(board.legal_moves):
                board.push(move)
                try:
                    score = -self.negamax(board, current_depth, -color, start, max_time)
                    if score > max_score:
                        max_score = score
                        best_moves.clear()
                        best_moves.append(move)
                    elif score == max_score:
                        best_moves.append(move)
                except TypeError:
                    break_flag = True
                    break
                board.pop()
            if break_flag or max_score == 100000:
                if max_score == 100000 and break_flag == False:
                    lists.append(best_moves)
                break
            current_depth += 1
            lists.append(best_moves)
        return random.choice(lists[-1])
class AlternateEngine():
    def get_material(self, board: chess.Board): # material code taken from https://chess.stackexchange.com/questions/39004/python-efficient-board-scoring-function-to-use-as-placeholder
        if board.is_game_over() or board.can_claim_draw():
            if board.is_checkmate():
                if board.result() == "1-0":
                    return 100000
                elif board.result() == "0-1":
                    return -100000
            else:
                return 0
        material_difference = 0
        pieces = [[chess.PAWN, 100], [chess.KNIGHT, 300], [chess.BISHOP, 300], [chess.ROOK, 500], [chess.QUEEN, 900]]
        colors = [chess.WHITE, chess.BLACK]
        for piece in pieces:
            for color in colors:
                if color == chess.WHITE:
                    material_difference += piece[1]*len(board.pieces(piece[0], color))
                elif color == chess.BLACK:
                    material_difference -= piece[1]*len(board.pieces(piece[0], color))
        return material_difference
    def filter_moves(self, board: chess.Board, moves_list: list):
        new_moves = []
        for move in moves_list:
            if board.gives_check(move) or board.is_capture(move):
                new_moves.append(move)
        if len(new_moves) == 0:
            return list(board.legal_moves)
        return new_moves
    def negamax(self, board: chess.Board, depth: int, color: int, start_time: float, max_time: float): # psuedocode taken from https://www.chessprogramming.org/Negamax
        if depth == 0 or board.is_game_over() or board.can_claim_draw():
            return self.get_material(board)*color
        elif start_time+max_time <= time.time():
            return None
        max = -sys.maxsize
        for move in self.filter_moves(board, list(board.legal_moves)):
            board.push(move)
            try:
                score = -self.negamax(board, depth-1, -color, start_time, max_time)
                board.pop()
            except TypeError:
                board.pop()
                return None
            if score > max:
                max = score
        return max
    def play(self, board: chess.Board, max_time: float): # root negamax function
        color = None
        current_depth = 1
        if board.turn == chess.WHITE:
            color = 1
        elif board.turn == chess.BLACK:
            color = -1
        start = time.time()
        lists = []
        break_flag = False
        while True:
            best_moves = []
            max_score = -sys.maxsize
            for move in self.filter_moves(board, list(board.legal_moves)):
                board.push(move)
                try:
                    score = -self.negamax(board, current_depth, -color, start, max_time)
                    if score > max_score:
                        max_score = score
                        best_moves.clear()
                        best_moves.append(move)
                    elif score == max_score:
                        best_moves.append(move)
                except TypeError:
                    break_flag = True
                    break
                board.pop()
            if break_flag or max_score == 100000:
                if max_score == 100000 and break_flag == False:
                    lists.append(best_moves)
                break
            current_depth += 1
            lists.append(best_moves)
        return random.choice(lists[-1])
class Stockfish():
    def play(self, board: chess.Board, max_time: float):
        self.engine = chess.engine.SimpleEngine.popen_uci("/opt/homebrew/bin/stockfish")
        self.move = self.engine.play(board, chess.engine.Limit(time=max_time)).move
        self.engine.quit()
        return self.move
class LeelaChessZero():
    def play(self, board: chess.Board, max_time: float):
        self.engine = chess.engine.SimpleEngine.popen_uci("/opt/homebrew/bin/lc0")
        self.move = self.engine.play(board, chess.engine.Limit(time=max_time)).move
        self.engine.quit()
        return self.move