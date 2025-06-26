import pygame
import sys
import chess
from pygame.locals import *
import time
from kewgame import wholeechess  # Import the correct class

# Initialize pygame
pygame.init()
pygame.font.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BOARD_SIZE = 480
MARGIN = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
HIGHLIGHT = (247, 247, 105, 150)
MOVE_HIGHLIGHT = (106, 168, 79, 150)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
ACCENT_COLOR = (50, 168, 82)  # Vibrant green for buttons
SHADOW_COLOR = (30, 30, 30, 100)  # Subtle shadow for depth

# Fonts
TITLE_FONT = pygame.font.SysFont('Georgia', 64, bold=True)
SUBTITLE_FONT = pygame.font.SysFont('Arial', 28, italic=True)
BUTTON_FONT = pygame.font.SysFont('Arial', 36, bold=True)

class ChessGUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Waleed's Chess Game")
        self.clock = pygame.time.Clock()
        self.state = "welcome"
        self.selected_piece = None
        self.valid_moves = []
        self.game = None
        self.load_images()
        self.button_scale = 1.0  # For button hover animation

    def load_images(self):
        """Load chess piece images"""
        self.piece_images = {}
        pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
        colors = ['white', 'black']
        
        for color in colors:
            for piece in pieces:
                try:
                    image = pygame.image.load(f'images/{color}_{piece}.png')
                    self.piece_images[f'{color}_{piece}'] = pygame.transform.scale(image, (60, 60))
                except:
                    self.piece_images = None
                    return

    def draw_welcome_screen(self):
        """Draw a world-class welcome screen"""
        # Background with gradient
        gradient = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            t = y / SCREEN_HEIGHT
            r = int(LIGHT_SQUARE[0] * (1 - t) + DARK_SQUARE[0] * t)
            g = int(LIGHT_SQUARE[1] * (1 - t) + DARK_SQUARE[1] * t)
            b = int(LIGHT_SQUARE[2] * (1 - t) + DARK_SQUARE[2] * t)
            pygame.draw.line(gradient, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        self.screen.blit(gradient, (0, 0))

        # Chessboard pattern overlay (subtle)
        square_size = BOARD_SIZE // 8
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for row in range(8):
            for col in range(8):
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                color = (*color[:3], 20)  # Low opacity for subtle effect
                pygame.draw.rect(overlay, color, 
                                (MARGIN + col * square_size, 
                                 MARGIN + row * square_size, 
                                 square_size, square_size))
        self.screen.blit(overlay, (0, 0))

        # Title with shadow effect
        title = TITLE_FONT.render("Waleed's Chess Game", True, BLACK)
        title_shadow = TITLE_FONT.render("Waleed's Chess Game", True, SHADOW_COLOR)
        self.screen.blit(title_shadow, (SCREEN_WIDTH//2 - title.get_width()//2 + 5, 155))
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))

        # Subtitle with animation (slight pulse)
        subtitle = SUBTITLE_FONT.render("Master the Board, Challenge the World!", True, BLACK)
        subtitle_scale = 1.0 + 0.05 * (1 + time.time() % 2)  # Gentle pulse
        scaled_subtitle = pygame.transform.smoothscale(subtitle, 
            (int(subtitle.get_width() * subtitle_scale), int(subtitle.get_height() * subtitle_scale)))
        self.screen.blit(scaled_subtitle, 
                        (SCREEN_WIDTH//2 - scaled_subtitle.get_width()//2, 250))

        # Start button with hover effect
        start_button = pygame.Rect(SCREEN_WIDTH//2 - 120 * self.button_scale, 
                                 350, 240 * self.button_scale, 70 * self.button_scale)
        pygame.draw.rect(self.screen, SHADOW_COLOR, start_button.move(5, 5), border_radius=15)
        pygame.draw.rect(self.screen, ACCENT_COLOR, start_button, border_radius=15)
        start_text = BUTTON_FONT.render("Start Game", True, WHITE)
        self.screen.blit(start_text, 
                        (SCREEN_WIDTH//2 - start_text.get_width()//2, 
                         365 - start_text.get_height()//2 + 35 * (self.button_scale - 1)))

        # Decorative chess pieces
        if self.piece_images:
            for i, piece in enumerate(['white_king', 'black_queen', 'white_bishop', 'black_knight']):
                img = self.piece_images.get(piece)
                if img:
                    self.screen.blit(img, (MARGIN + i * 150, MARGIN + 400))

        # Update button scale for hover animation
        mouse_pos = pygame.mouse.get_pos()
        if start_button.collidepoint(mouse_pos):
            self.button_scale = min(self.button_scale + 0.02, 1.1)
        else:
            self.button_scale = max(self.button_scale - 0.02, 1.0)

        return start_button

    def draw_board(self):
        """Draw the chess board"""
        square_size = BOARD_SIZE // 8
        
        for row in range(8):
            for col in range(8):
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                pygame.draw.rect(self.screen, color, 
                                (MARGIN + col * square_size, 
                                 MARGIN + row * square_size, 
                                 square_size, square_size))
                
                if self.selected_piece:
                    file, rank = chess.square_file(self.selected_piece), chess.square_rank(self.selected_piece)
                    if col == file and row == 7 - rank:
                        highlight = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
                        highlight.fill(HIGHLIGHT)
                        self.screen.blit(highlight, 
                                        (MARGIN + col * square_size, 
                                         MARGIN + row * square_size))
                
                for move in self.valid_moves:
                    if col == chess.square_file(move.to_square) and row == 7 - chess.square_rank(move.to_square):
                        highlight = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
                        highlight.fill(MOVE_HIGHLIGHT)
                        self.screen.blit(highlight, 
                                        (MARGIN + col * square_size, 
                                         MARGIN + row * square_size))

    def draw_pieces(self):
        """Draw chess pieces on the board"""
        if not self.game:
            return
            
        square_size = BOARD_SIZE // 8
        
        for row in range(8):
            for col in range(8):
                piece = self.game.board.piece_at(chess.square(col, row))
                if piece:
                    piece_name = f"{'white' if piece.color == chess.WHITE else 'black'}_{piece.symbol().lower()}"
                    
                    if self.piece_images and piece_name in self.piece_images:
                        self.screen.blit(self.piece_images[piece_name], 
                                       (MARGIN + col * square_size + 10, 
                                        MARGIN + (7 - row) * square_size + 10))
                    else:
                        piece_text = BUTTON_FONT.render(piece.symbol(), True, 
                                                       WHITE if piece.color == chess.WHITE else BLACK)
                        self.screen.blit(piece_text, 
                                        (MARGIN + col * square_size + square_size//2 - piece_text.get_width()//2, 
                                         MARGIN + (7 - row) * square_size + square_size//2 - piece_text.get_height()//2))

    def draw_game_info(self):
        """Draw game information"""
        if not self.game:
            return
            
        turn_text = f"Current Turn: {'White' if self.game.board.turn == chess.WHITE else 'Black'}"
        turn_surface = BUTTON_FONT.render(turn_text, True, BLACK)
        self.screen.blit(turn_surface, (MARGIN + BOARD_SIZE + 20, MARGIN))
        
        move_history = []
        temp_board = chess.Board()
        for move in self.game.board.move_stack:
            if move in temp_board.legal_moves:
                move_history.append(temp_board.san(move))
                temp_board.push(move)
        
        for i, move in enumerate(move_history[-10:]):
            move_text = MOVE_FONT.render(f"{i+1}. {move}", True, BLACK)
            self.screen.blit(move_text, (MARGIN + BOARD_SIZE + 20, MARGIN + 50 + i * 20))

    def draw_end_screen(self):
        """Draw the end game screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        if self.game.board.is_checkmate():
            winner = "Black" if self.game.board.turn == chess.WHITE else "White"
            result_text = f"Checkmate! {winner} wins!"
        elif self.game.board.is_stalemate():
            result_text = "Stalemate! Game drawn."
        else:
            result_text = "Game Over"
            
        text = TITLE_FONT.render(result_text, True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - 50))
        
        again_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 50, 200, 60)
        pygame.draw.rect(self.screen, DARK_SQUARE, again_button, border_radius=10)
        again_text = BUTTON_FONT.render("Play Again", True, WHITE)
        self.screen.blit(again_text, (SCREEN_WIDTH//2 - again_text.get_width()//2, SCREEN_HEIGHT//2 + 65))
        
        return again_button

    def handle_click(self, pos):
        """Handle mouse clicks"""
        square_size = BOARD_SIZE // 8
        
        if (MARGIN <= pos[0] < MARGIN + BOARD_SIZE and 
            MARGIN <= pos[1] < MARGIN + BOARD_SIZE):
            col = (pos[0] - MARGIN) // square_size
            row = (pos[1] - MARGIN) // square_size
            square = chess.square(col, 7 - row)
            
            if self.game.board.turn == chess.WHITE:
                piece = self.game.board.piece_at(square)
                
                if self.selected_piece:
                    move = chess.Move(self.selected_piece, square)
                    if move in self.game.board.legal_moves:
                        self.game.board.push(move)
                        self.selected_piece = None
                        self.valid_moves = []
                        
                        if not self.game.board.is_game_over():
                            self.ai_move()
                    else:
                        if piece and piece.color == chess.WHITE:
                            self.selected_piece = square
                            self.valid_moves = [m for m in self.game.board.legal_moves 
                                              if m.from_square == square]
                        else:
                            self.selected_piece = None
                            self.valid_moves = []
                elif piece and piece.color == chess.WHITE:
                    self.selected_piece = square
                    self.valid_moves = [m for m in self.game.board.legal_moves 
                                      if m.from_square == square]

    def ai_move(self):
        """Let the AI make a move"""
        if self.game.board.turn == chess.BLACK and not self.game.board.is_game_over():
            start_time = time.time()
            move = self.game.ai.bestMoveornot(self.game.board)
            if move in self.game.board.legal_moves:
                self.game.board.push(move)
                print(f"AI moved: {self.game.board.san(move)} (took {time.time() - start_time:.2f}s)")

    def run(self):
        """Main game loop"""
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == MOUSEBUTTONDOWN:
                    if self.state == "welcome":
                        start_button = self.draw_welcome_screen()
                        if start_button.collidepoint(event.pos):
                            self.game = wholeechess()  # Use the correct class
                            self.state = "game"
                    
                    elif self.state == "game":
                        self.handle_click(event.pos)
                        if self.game.board.is_game_over():
                            self.state = "end"
                    
                    elif self.state == "end":
                        again_button = self.draw_end_screen()
                        if again_button.collidepoint(event.pos):
                            self.game = wholeechess()  # Use the correct class
                            self.state = "game"
                            self.selected_piece = None
                            self.valid_moves = []
            
            self.screen.fill(WHITE)
            
            if self.state == "welcome":
                start_button = self.draw_welcome_screen()
            elif self.state == "game":
                self.draw_board()
                self.draw_pieces()
                self.draw_game_info()
            elif self.state == "end":
                self.draw_board()
                self.draw_pieces()
                self.draw_game_info()
                again_button = self.draw_end_screen()
            
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    gui = ChessGUI()
    gui.run()