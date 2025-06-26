import chess
import time
import math
from typing import Optional

class Compooterchess:
    def __init__(self, thinkinlevel: int = 3):
        self.thinkinlevel = thinkinlevel

    def bestMoveornot(self, board: chess.Board) -> chess.Move:
        bestmove = None
        bestval = -math.inf
        alpha = -math.inf
        beta = math.inf

        for move in board.legal_moves:
            board.push(move)
            moveval = self.minimax(board, self.thinkinlevel - 1, alpha, beta, False)
            board.pop()

            if moveval > bestval or bestmove is None:
                bestval = moveval
                bestmove = move

            alpha = max(alpha, bestval)
            if beta <= alpha:
                break

        return bestmove

    def minimax(self, board: chess.Board, depth: int, alpha: float, beta: float, checkbest: bool) -> float:
        if depth == 0 or board.is_game_over():
            return self.checkboard(board)

        if checkbest:
            worstmove = -math.inf
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                worstmove = max(worstmove, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return worstmove
        else:
            bestmove = math.inf
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                bestmove = min(bestmove, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return bestmove

    def checkboard(self, board: chess.Board) -> float:
        if board.is_checkmate():
            return -math.inf if board.turn == chess.WHITE else math.inf
        if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
            return 0

        scorepieces = {
            chess.PAWN: 10,
            chess.KNIGHT: 30,
            chess.BISHOP: 30,
            chess.ROOK: 50,
            chess.QUEEN: 90,
            chess.KING: 0
        }

        score = 0
        
        # Material score
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = scorepieces[piece.piece_type]
                score += value if piece.color == chess.WHITE else -value

        if board.is_capture(board.peek()):
            captured_piece = board.piece_at(board.peek().to_square)
            if captured_piece:
                score += scorepieces[captured_piece.piece_type] * 0.5  # Bonus for capturing

        for move in board.legal_moves:
            if board.is_capture(move):
                captured_piece = board.piece_at(move.to_square)
                if captured_piece:
                    score += scorepieces[captured_piece.piece_type] * 0.1  # Small bonus for possible captures

        mobility = len(list(board.legal_moves))
        score += mobility * 0.1 if board.turn == chess.WHITE else -mobility * 0.1

        center_squares = [chess.E4, chess.D4, chess.E5, chess.D5]
        for square in center_squares:
            piece = board.piece_at(square)
            if piece and piece.color == (board.turn == chess.WHITE):
                score += 2

        return score
    # def checkboard(self, board: chess.Board) -> float:
    #     if board.is_checkmate():
    #         return -math.inf if board.turn == chess.WHITE else math.inf
    #     if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
    #         return 0

    #     scorepieces = {
    #         chess.PAWN: 1,
    #         chess.KNIGHT: 3,
    #         chess.BISHOP: 3,
    #         chess.ROOK: 5,
    #         chess.QUEEN: 9,
    #         chess.KING: 0
    #     }

    #     score = 0
    #     for square in chess.SQUARES:
    #         piece = board.piece_at(square)
    #         if piece:
    #             value = scorepieces[piece.piece_type]
    #             score += value if piece.color == chess.WHITE else -value

    #     mobility = len(list(board.legal_moves))
    #     score += mobility * 0.01 if board.turn == chess.WHITE else -mobility * 0.01

    #     return score

class wholeechess:
    def __init__(self):
        self.board = chess.Board()
        self.ai = Compooterchess(thinkinlevel=3)

    def showboard(self):
        print("  a b c d e f g h")
        for rank in range(7, -1, -1):
            print(rank + 1, end=" ")
            for file in range(8):
                square = chess.square(file, rank)
                piece = self.board.piece_at(square)
                print(self.piecesymbol(piece), end=" ")
            print(rank + 1)
        print("  a b c d e f g h")

    def piecesymbol(self, piece: Optional[chess.Piece]) -> str:
        if piece is None:
            return "."
        symbols = {
            chess.PAWN: "♙♟",
            chess.KNIGHT: "♘♞",
            chess.BISHOP: "♗♝",
            chess.ROOK: "♖♜",
            chess.QUEEN: "♕♛",
            chess.KING: "♔♚"
        }
        return symbols[piece.piece_type][0 if piece.color == chess.WHITE else 1]

    def play(self):
        print("Hellllioo goizz Welkoom To Waleed's Chess game!!!")
        print(" You are supposed to enter moves like dis: e2e4, Nf3, O-O, etc")
        print("Or if you feel like youre about to lose enter 'quit' to get away wit it")
        print("\n")

        while not self.board.is_game_over():
            self.showboard()

            if self.board.turn == chess.WHITE:
                nowmove = input("White's move: ").strip()
                if nowmove.lower() == 'quit':
                    print("Noice youve decided to endgame")
                    return

                try:
                    move = self.board.parse_san(nowmove)
                    if move not in self.board.legal_moves:
                        print("Sorry but the move you entered is not only dumb but also not allowed. Try again hehe")
                        continue
                    self.board.push(move)
                except ValueError:
                    print("Yo you dreamin or wot. told you enter in this notation: e2e4, Nf3, O-O, etc")
                    continue
            else:
                print("Wait compoooter is thinkin")
                start_time = time.time()
                move = self.ai.bestMoveornot(self.board)
                end_time = time.time()
                print(f"the bleck compooter has moved: {self.board.san(move)}")
                print(f"Tiem taken for da move is: {end_time - start_time:.2f} seconds")
                self.board.push(move)

        self.showboard()
        if self.board.is_checkmate():
            print("Checkmate! {} wins!".format("Black" if self.board.turn == chess.WHITE else "White"))
        elif self.board.is_stalemate():
            print("Stalemate! The game is a draw.")
        elif self.board.is_insufficient_material():
            print("Draw by insufficient material.")
        elif self.board.is_seventyfive_moves():
            print("Draw by 75-move rule.")
        elif self.board.is_fivefold_repetition():
            print("Draw by fivefold repetition.")

if __name__ == "__main__":
    game = wholeechess()
    game.play()