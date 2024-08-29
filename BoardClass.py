from PiecesClasses import *


WIDTH = 800
HEIGHT = 800
SQUARE_SIZE = 100
BOARD_SIZE = 8
gameActive = False

class Board():
    def __init__(self):

        # Load and scale images for dark and light squares
        self.darkSquare = pygame.image.load("Pieces/square_brown_dark.png").convert_alpha()
        self.lightSquare = pygame.image.load("Pieces/square_brown_light.png").convert_alpha()
        
        self.darkSquare = pygame.transform.scale(self.darkSquare,(SQUARE_SIZE,SQUARE_SIZE))
        self.lightSquare = pygame.transform.scale(self.lightSquare,(SQUARE_SIZE,SQUARE_SIZE))

        # Initialize a 3D list to store the rectangles of squares and their associated pieces
        # squaresRect[row][col][0] stores the square's rectangle
        # squaresRect[row][col][1] will be used to store the piece on that square
        self.squaresRect = [[[None for _ in range(2)] for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        # Create a sprite group to manage and update all pieces on the board
        self.allPieces = pygame.sprite.Group()

        
        # Iterate over each row and column to assign the correct square (light or dark) based on the row and column index
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 0:
                    # Light square (even sum of row and column indices)
                    self.squaresRect[row][col][0] = self.lightSquare.get_rect(topleft=(col * SQUARE_SIZE, row * SQUARE_SIZE))
                else:
                    # Dark square (odd sum of row and column indices)
                    self.squaresRect[row][col][0] = self.darkSquare.get_rect(topleft=(col * SQUARE_SIZE, row * SQUARE_SIZE))
        
        # Initialize all chess pieces on the board
        self.init_pieces()

        # Variables to manage the state of the game
        self.selectedPiece = None   # To keep track of the currently selected piece
        self.originalPos = None     # To store the original position of the selected piec
        self.playerActive = 'w'     # 'w' for white's turn, 'b' for black's turn
        self.gameOver = False       # Flag to check if the game is over
        self.lastMove = None        # To store the last move made in the game

        
    # Initialize all the chess pieces on the board.
    def init_pieces(self):
        self.init_pawns()
        self.init_rooks()
        self.init_knights()
        self.init_bishops()
        self.init_king_and_queen()
    
    def init_pawns(self):
        for col in range(BOARD_SIZE):
            # Initialize white pawns on the 7th row
            x,y = self.squaresRect[6][col][0].center
            pawn = Pawn('w', (x, y))
            self.squaresRect[6][col][1] = pawn
            self.allPieces.add(pawn)

             # Initialize black pawns on the 2nd row
            x,y = self.squaresRect[1][col][0].center
            pawn = Pawn('b',(x,y))
            self.squaresRect[1][col][1] = pawn
            self.allPieces.add(pawn)

    def init_rooks(self):
        for row in [0, 7]:
            for col in [0, 7]:
                x,y = self.squaresRect[row][col][0].center

                # Add black rooks 
                if row == 0:
                    rook = Rook('b',(x,y))
                    self.squaresRect[row][col][1] = rook
                    self.allPieces.add(rook)

                # Add white rooks 
                else:
                    rook = Rook('w',(x,y))
                    self.squaresRect[row][col][1] = rook
                    self.allPieces.add(rook)

    def init_knights(self):
        for row in [0, 7]:
            for col in [1, 6]:
                x,y = self.squaresRect[row][col][0].center

                #Add black knights
                if row == 0:
                    knight = Knight('b',(x,y))
                    self.squaresRect[row][col][1] = knight
                    self.allPieces.add(knight)
                    
                #Add white knights
                else:
                    knight = Knight('w',(x,y))
                    self.squaresRect[row][col][1] = knight
                    self.allPieces.add(knight)

    def init_bishops(self):
        for row in [0, 7]:
            for col in [2, 5]:
                x,y = self.squaresRect[row][col][0].center

                #Add black bishops
                if row == 0:
                    bishop = Bishop('b',(x,y))
                    self.squaresRect[row][col][1] = bishop
                    self.allPieces.add(bishop)

                #Add white bishops
                else:
                    bishop = Bishop('w',(x,y))
                    self.squaresRect[row][col][1] = bishop
                    self.allPieces.add(bishop)

    def init_king_and_queen(self):
        #Add black queen and king
        x,y = self.squaresRect[0][3][0].center
        queen = Queen('b',(x,y))
        self.squaresRect[0][3][1] = queen
        self.allPieces.add(queen)

        x,y = self.squaresRect[0][4][0].center
        king = King('b',(x,y))
        self.squaresRect[0][4][1] = king
        self.allPieces.add(king)
        
        #Add white queen and king
        x,y = self.squaresRect[7][3][0].center
        queen = Queen('w',(x,y))
        self.squaresRect[7][3][1] = queen
        self.allPieces.add(queen)

        x,y = self.squaresRect[7][4][0].center
        king = King('w',(x,y))
        self.squaresRect[7][4][1] = king
        self.allPieces.add(king)


    """
    Draw the chessboard on the given surface.
    
    This method iterates over each square of the board and blits the appropriate square image 
    (light or dark) onto the surface based on the row and column indices.
    
    Arguments:
    surface -- The Pygame surface where the board will be drawn.
    """
    def init_board(self,surface):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 0: 
                    surface.blit(self.lightSquare, self.squaresRect[row][col][0])
                else: 
                    surface.blit(self.darkSquare, self.squaresRect[row][col][0])


    # Get the position on the board over which mouse is hovering returns row column on the board
    def get_square_from_mouse(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                square = self.squaresRect[row][col][0]
                if square.collidepoint(pygame.mouse.get_pos()):
                    return row,col
        return None
    
    def get_valid_moves(self,piece):
        if isinstance(piece, Pawn):
            return self.get_valid_pawn_moves(piece)
        elif isinstance(piece, Knight):
            return self.get_valid_knight_moves(piece)
        elif isinstance(piece, Bishop) or isinstance(piece,Rook) or isinstance(piece, Queen):
            return self.get_valid_queen_bishop_rook_moves(piece)
        elif isinstance(piece, King):
            return self.get_valid_king_moves(piece)
    
    # Returns piece position on the board 
    def get_piece_position(self, piece):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.squaresRect[row][col][1] == piece:
                    return row, col
        # Return None if the piece is not found
        return None, None

    # Returns an array of valid moves for given pawn
    def get_valid_pawn_moves(self, pawn):
        validMoves = []
        rowDirection = -1 if pawn.color == 'w' else 1  # White moves up (-1), Black moves down (+1)
        startRow = 6 if pawn.color == 'w' else 1

        # Get current position on the board
        currentRow, currentCol = self.get_piece_position(pawn)
        
        # Move one square forward
        nextRow = currentRow + rowDirection
        if 0 <= nextRow < BOARD_SIZE and self.squaresRect[nextRow][currentCol][1] is None:
            validMoves.append((nextRow,currentCol))
            
        # Move two squares forward (first move)
        nextNextRow = currentRow + 2 * rowDirection
        if currentRow == startRow and self.squaresRect[nextNextRow][currentCol][1] is None:
            validMoves.append((nextNextRow,currentCol))

        # Diagonal takes
        for colOffset in [-1, 1]:  
            nextCol = currentCol + colOffset
            if 0 <= nextCol < BOARD_SIZE:
                diagonalPiece = self.squaresRect[nextRow][nextCol][1]

                # Normal diagonal take
                if diagonalPiece is not None and diagonalPiece.color != pawn.color:
                    validMoves.append((nextRow,nextCol))
                
                # En passant move
                if self.lastMove:
                    lastPiece, (startRowLastPiece, startColLastPiece),(endRowLastPiece, endColLastPiece) = self.lastMove
                    if isinstance(lastPiece, Pawn):
                        if abs(startRowLastPiece - endRowLastPiece) == 2:
                            if startColLastPiece == nextCol: 
                                if endRowLastPiece == currentRow:
                                    validMoves.append((nextRow,nextCol))
                    
        return validMoves

    # Moves pieces to the given square and perfomes takes if needed
    def move_piece(self, piece, targetPos):
        # Get the target row and column from the target center
        targetRow, targetCol = targetPos

        
        targetPiece = self.squaresRect[targetRow][targetCol][1]

        # If the target square is occupied
        if targetPiece is not None:
            self.allPieces.remove(targetPiece)  # Remove the piece from the sprite group

        # Get the original position of the piece and move the piece in allPieces
        currentRow, currentCol = self.get_piece_position(piece)

        # Update the squaresRect with the new position
        self.squaresRect[targetRow][targetCol][1] = piece
        self.squaresRect[currentRow][currentCol][1] = None
        piece.rect.center = self.squaresRect[targetRow][targetCol][0].center

        #This is special check if the move is en passant
        if isinstance(piece,Pawn):
            direction = 1 if piece.color == 'w' else -1
            if isinstance(self.squaresRect[targetRow + direction][targetCol][1],Pawn):
                # Remove the opponent pawn which moved 2 squares front
                toDel = self.squaresRect[targetRow + direction][targetCol][1]
                self.squaresRect[targetRow + direction][targetCol][1] = None
                self.allPieces.remove(toDel)

        # Check for promotion
        if isinstance(piece, Pawn) and (targetRow == 0 or targetRow == 7):
            self.promote_pawn(piece, targetRow, targetCol)


        self.playerActive = 'w' if self.playerActive == 'b' else 'b'
        self.lastMove = (piece, (currentRow, currentCol), (targetRow, targetCol))
        self.originalPos = None
        self.selectedPiece = None
        return self

    # Returns an array of valid moves for given knight
    def get_valid_knight_moves(self, knight):
        validMoves = []

        # Define the possible moves for a knight
        knightMoves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        # Get current position on the board
        currentRow, currentCol = self.get_piece_position(knight)

        # Calculate all possible valid moves
        for move in knightMoves:
            targetRow = currentRow + move[0]
            targetCol = currentCol + move[1]

            # Check if the move is within the board limits
            if 0 <= targetRow < BOARD_SIZE and 0 <= targetCol < BOARD_SIZE:
                targetPiece = self.squaresRect[targetRow][targetCol][1]
                # Add the move if the target square is empty or contains an opponent's piece
                if targetPiece is None or targetPiece.color != knight.color:
                    validMoves.append((targetRow,targetCol))

        return validMoves

    # Returns an array of valid moves for given queen bishop or rook
    def get_valid_queen_bishop_rook_moves(self, piece):
        validMoves = []

        # Get current position on the board
        currentRow, currentCol = self.get_piece_position(piece)
            
        # Determine directions based on the type of piece
        if isinstance(piece, Rook):
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        elif isinstance(piece, Bishop):
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)] 
        elif isinstance(piece, Queen):
            directions = [
                (1, 0), (-1, 0), (0, 1), (0, -1),  
                (1, 1), (1, -1), (-1, 1), (-1, -1)
            ]
            
        else:
            return validMoves  # Return empty list if the piece is not a Rook, Bishop, or Queen

        # Check all the possible directions for the piece
        for direction in directions:
            for step in range(1, BOARD_SIZE):
                targetRow = currentRow + step * direction[0]
                targetCol = currentCol + step * direction[1]

                # Check if the move is within the board limits
                if 0 <= targetRow < BOARD_SIZE and 0 <= targetCol < BOARD_SIZE:
                    targetPiece = self.squaresRect[targetRow][targetCol][1]
                    
                    # If the square is empty it is a valid move
                    if targetPiece is None:

                        validMoves.append((targetRow,targetCol))
                    # If the square is occupied by an opponent's piece it is a valid move but stop further movement in this direction
                    elif targetPiece.color != piece.color:

                        validMoves.append((targetRow,targetCol))
                        break
                    # If the square is occupied by a piece of the same color stop further movement in this direction
                    else:
                        break
                else:
                    break

        return validMoves

    # Returns an array of valid moves for given king
    def get_valid_king_moves(self, king):
        validMoves = []
        
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),  
            (1, 1), (1, -1), (-1, 1), (-1, -1)  
        ]
        # Get current position on the board
        currentRow, currentCol = self.get_piece_position(king)

        # Calculate all possible valid moves
        for move in directions:
            targetRow = currentRow + move[0]
            targetCol = currentCol + move[1]

            # Check if the move is within the board limits
            if 0 <= targetRow < BOARD_SIZE and 0 <= targetCol < BOARD_SIZE:
                targetPiece = self.squaresRect[targetRow][targetCol][1]

                # Add the move if the target square is empty or contains an opponent's piece
                if targetPiece is None or targetPiece.color != king.color:
                    validMoves.append((targetRow,targetCol))

        return validMoves

    def is_square_under_attack(self, color, targetPos):

        opponentColor = 'b' if color == 'w' else 'w'
        
        # Check all squares for opponent pieces that could attack the given square
        for piece in self.allPieces:
            if piece and piece.color == opponentColor:
                # Special case for pawns
                if isinstance(piece, Pawn):
                    # Calculate pawn's attack squares
                    pawnRow, pawnCol = self.get_piece_position(piece)
                    if pawnRow and pawnCol: 
                        rowDirection = -1 if piece.color == 'w' else 1
                        attackMoves = []

                        for colOffset in [-1, 1]:
                            attackRow = pawnRow + rowDirection
                            attackCol = pawnCol + colOffset

                            if 0 <= attackRow < BOARD_SIZE and 0 <= attackCol < BOARD_SIZE:
                                attackMoves.append((attackRow,attackCol))
                        # If the move we want to make is under attack of pawn return true
                        if targetPos in attackMoves:
                            return True
                else:   # Other pieces
                    validMoves = self.get_valid_moves(piece)
                    if targetPos in validMoves:
                        return True

        return False


    def is_check(self, king):
        targetPos = self.get_piece_position(king)
        return self.is_square_under_attack(king.color, targetPos)

    def get_king_by_color(self,color):
        for king in self.allPieces:
            if isinstance(king, King) and color == king.color:
                return king
    
    def is_pinned(self, piece,move):
        # Get the current position of the piece
        currentRow, currentCol = self.get_piece_position(piece)
        

        king = self.get_king_by_color(piece.color)

        # Simulate moving the piece
        moveRow, moveCol = move

        # Keep track of any captured piece
        captured_piece = self.squaresRect[moveRow][moveCol][1]  
        self.allPieces.remove(captured_piece)
        # Temporarily move the piece to the new position
        self.squaresRect[currentRow][currentCol][1] = None
        self.squaresRect[moveRow][moveCol][1] = piece
        piece.rect.center = self.squaresRect[moveRow][moveCol][0].center
        
        # Check if the king is in check after the move
        if self.is_check(king):
            # If the king is in check, the piece is pinned; restore the original state
            self.squaresRect[currentRow][currentCol][1] = piece
            self.squaresRect[moveRow][moveCol][1] = captured_piece
            if captured_piece:
                self.allPieces.add(captured_piece)
            piece.rect.center = self.squaresRect[currentRow][currentCol][0].center

            return True
        
        # Restore the original state
        self.squaresRect[currentRow][currentCol][1] = piece
        self.squaresRect[moveRow][moveCol][1] = captured_piece
        if captured_piece:
            self.allPieces.add(captured_piece)
        piece.rect.center = self.squaresRect[currentRow][currentCol][0].center
        
        # If no move puts the king in check, the piece is not pinned
        return False

    # If checkmate return True
    def is_checkmate(self):
            king = self.get_king_by_color(self.playerActive)
            if not self.is_check(king):
                return False

            for piece in self.allPieces:
                if piece.color == self.playerActive:
                    validMoves = self.get_valid_moves(piece)
                    for move in validMoves:
                        if not self.is_pinned(piece, move):
                            return False
            self.gameOver = True
            return True
    
    def promote_pawn(self, pawn, row, col):
        # Create a small window for promotion
        promotion_rect = pygame.Rect((WIDTH // 2) - 100, (HEIGHT // 2) - 100, 200, 200)
        pygame.draw.rect(screen, (200, 200, 200), promotion_rect)
        
        font = pygame.font.Font(None, 50)
        options = ["Queen", "Rook", "Bishop", "Knight"]
        
        for i, option in enumerate(options):
            option_surface = font.render(f"{i + 1}. {option}", True, "black")
            screen.blit(option_surface, (promotion_rect.x + 10, promotion_rect.y + 10 + i * 50))
        
        pygame.display.update()
        
        # Wait for player to choose the promotion piece
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        selected_option = event.key - pygame.K_1
                        self.replace_pawn(pawn, row, col, options[selected_option])
                        return
    
    # When pawn get to end of the board ask player to which piece he wants to change the pawn and replace it
    def replace_pawn(self, pawn, row, col, chosen_piece):
        self.allPieces.remove(pawn)
        self.squaresRect[row][col][1] = None
        
        if chosen_piece == "Queen":
            new_piece = Queen(pawn.color, self.squaresRect[row][col][0].center)
        elif chosen_piece == "Rook":
            new_piece = Rook(pawn.color, self.squaresRect[row][col][0].center)
        elif chosen_piece == "Bishop":
            new_piece = Bishop(pawn.color, self.squaresRect[row][col][0].center)
        elif chosen_piece == "Knight":
            new_piece = Knight(pawn.color, self.squaresRect[row][col][0].center)
        
        self.squaresRect[row][col][1] = new_piece
        self.allPieces.add(new_piece)
