
import pygame
from sys import exit


WIDTH = 800
HEIGHT = 800
SQUARE_SIZE = 100
BOARD_SIZE = 8
gameActive = False


class Board():
    def __init__(self):
        self.darkSquare = pygame.image.load("Pieces/square_brown_dark.png").convert_alpha()
        self.lightSquare = pygame.image.load("Pieces/square_brown_light.png").convert_alpha()
        
        self.darkSquare = pygame.transform.scale(self.darkSquare,(SQUARE_SIZE,SQUARE_SIZE))
        self.lightSquare = pygame.transform.scale(self.lightSquare,(SQUARE_SIZE,SQUARE_SIZE))

        #store squares and pieces like positions on board
        self.squaresRect = [[[None for _ in range(2)] for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        #Sprite group for pieces
        self.allPieces = pygame.sprite.Group()

        
        # Fill in the squaresRect with proper coordinates for squares
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 0:
                    self.squaresRect[row][col][0] = self.lightSquare.get_rect(topleft=(col * SQUARE_SIZE, row * SQUARE_SIZE))
                else:
                    self.squaresRect[row][col][0] = self.darkSquare.get_rect(topleft=(col * SQUARE_SIZE, row * SQUARE_SIZE))
        
        self.init_pieces()
        self.selectedPiece = None
        self.originalPos = None
        self.playerActive = 'w'
        self.gameOver = False
        self.lastMove = None

        

    def init_pieces(self):
        self.init_pawns()
        self.init_rooks()
        self.init_knights()
        self.init_bishops()
        self.init_king_and_queen()
    
    def init_pawns(self):
        for col in range(BOARD_SIZE):
            #white pawns
            x,y = self.squaresRect[6][col][0].center
            pawn = Pawn('w', (x, y))
            self.squaresRect[6][col][1] = pawn
            self.allPieces.add(pawn)

            #black pawns
            x,y = self.squaresRect[1][col][0].center
            pawn = Pawn('b',(x,y))
            self.squaresRect[1][col][1] = pawn
            self.allPieces.add(pawn)

    def init_rooks(self):
        for row in [0, 7]:
            for col in [0, 7]:
                x,y = self.squaresRect[row][col][0].center

                #Add black rooks
                if row == 0:
                    rook = Rook('b',(x,y))
                    self.squaresRect[row][col][1] = rook
                    self.allPieces.add(rook)

                #Add white rooks
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
        #Black
        x,y = self.squaresRect[0][3][0].center
        queen = Queen('b',(x,y))
        self.squaresRect[0][3][1] = queen
        self.allPieces.add(queen)

        x,y = self.squaresRect[0][4][0].center
        king = King('b',(x,y))
        self.squaresRect[0][4][1] = king
        self.allPieces.add(king)
        
        #White
        x,y = self.squaresRect[7][3][0].center
        queen = Queen('w',(x,y))
        self.squaresRect[7][3][1] = queen
        self.allPieces.add(queen)

        x,y = self.squaresRect[7][4][0].center
        king = King('w',(x,y))
        self.squaresRect[7][4][1] = king
        self.allPieces.add(king)

    #Draw the board
    def init_board(self,surface):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 0: 
                    surface.blit(self.lightSquare, self.squaresRect[row][col][0])
                else: 
                    surface.blit(self.darkSquare, self.squaresRect[row][col][0])

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
        
    def get_piece_position(self, piece):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.squaresRect[row][col][1] == piece:
                    return row, col
        # Return None if the piece is not found
        return None, None

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

    def move_piece(self, piece, targetPos):
        # Get the target row and column from the target center
        targetRow, targetCol = targetPos

        targetPiece = self.squaresRect[targetRow][targetCol][1]
        if targetPiece is not None:
            self.allPieces.remove(targetPiece)  # Remove the piece from the sprite group

        # Get the original position of the piece and move the piece in allPieces
        currentRow, currentCol = self.get_piece_position(piece)

        # Update the squaresRect with the new position
        self.squaresRect[targetRow][targetCol][1] = piece
        self.squaresRect[currentRow][currentCol][1] = None
        piece.rect.center = self.squaresRect[targetRow][targetCol][0].center

        # Check en passant
        if isinstance(piece,Pawn):
            direction = 1 if piece.color == 'w' else -1
            if isinstance(self.squaresRect[targetRow + direction][targetCol][1],Pawn):
                toDel = self.squaresRect[targetRow + direction][targetCol][1]
                self.squaresRect[targetRow + direction][targetCol][1] = None
                self.allPieces.remove(toDel)
        # Check for promotion
        if isinstance(piece, Pawn) and (targetRow == 0 or targetRow == 7):
            self.promote_pawn(piece, targetRow, targetCol)


        board.playerActive = 'w' if board.playerActive == 'b' else 'b'
        self.lastMove = (piece, (currentRow, currentCol), (targetRow, targetCol))
        board.originalPos = None
        board.selectedPiece = None
        return self

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

                        if targetPos in attackMoves:
                            return True
                else:
                    validMoves = self.get_valid_moves(piece)
                    if targetPos in validMoves:
                        return True

        return False

    def take(self, piece):
        currentRow, currentCol = self.get_piece_position(piece)

        # Remove the piece from the squaresRect
        self.squaresRect[currentRow][currentCol][1] = None

        # Remove the piece from the allPieces sprite group
        self.allPieces.remove(piece)

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

    def get_row_col_from_move(self, move):
        for row in range(len(self.squaresRect)):
            for col in range(len(self.squaresRect[row])):
                if move == self.squaresRect[row][col][0].center:
                    return row, col
        return None, None

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


class Piece(pygame.sprite.Sprite):
    def __init__(self,color,initial_position, image_file):  #input color as "b" or "w", and initial position as tuple for the center of square coordinates
        super().__init__()
        self.image = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(self.image,(100,100))
        self.rect = self.image.get_rect(center = initial_position)
        self.color = color


class Pawn(Piece):
    def __init__(self,color,initial_position):   
        super().__init__(color, initial_position, f"Pieces/{color}_pawn.png")
        self.name = "Pawn"
        self.moved_two_squares = False  # Track if the pawn moved two squares forward


class King(Piece):
    def __init__(self,color,initial_position):
        super().__init__(color, initial_position, f"Pieces/{color}_king.png")
        self.name = "King"


class Queen(Piece):
    def __init__(self,color,initial_position):
        super().__init__(color, initial_position, f"Pieces/{color}_queen.png")
        self.name = "Queen"


class Bishop(Piece):
    def __init__(self,color,initial_position):
        super().__init__(color, initial_position, f"Pieces/{color}_bishop.png")
        self.name = "Bishop"


class Knight(Piece):
    def __init__(self,color,initial_position):
        super().__init__(color, initial_position, f"Pieces/{color}_knight.png")
        self.name = "Knight"


class Rook(Piece):
    def __init__(self,color,initial_position):
        super().__init__(color, initial_position, f"Pieces/{color}_rook.png")
        self.name = "Rook"

# Display game over screen
def game_over(loser):
    if loser == 'w':
        surfaceGameOver = font.render(f"Checkmate black wins!",True, "black")
    else:
        surfaceGameOver = font.render(f"Checkmate white wins!",True, "black")
    screen.fill((118,150,86))
    screen.blit(surfaceGameOver,(200,400))


pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)

board = Board()

#Initial Screeen
surfaceGameStart = font.render("Press SPACE to start playing",True, "black")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
        #Press space to start the game
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            gameActive = True
        
         #if player picks up a piece
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
             for sprite in board.allPieces:
                if sprite.rect.collidepoint(event.pos) and sprite.color == board.playerActive:
                    board.selectedPiece = sprite
                    board.originalPos = board.get_square_from_mouse()
                    break
        
        #if player lets go of piece
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if board.selectedPiece:
                targetPos = board.get_square_from_mouse()
                validMoves = board.get_valid_moves(board.selectedPiece)
                
                # If the piece is pinned restrict its movement
                if board.is_pinned(board.selectedPiece, targetPos):
                    validMoves = []
                    
                #If king seleceted remove squares which are under attack
                if isinstance(board.selectedPiece,King):
                    safe_moves = []
                    for move in validMoves:
                        if not board.is_square_under_attack(board.selectedPiece.color,targetPos):
                            safe_moves.append(move)
                    validMoves = safe_moves

                if  targetPos in validMoves:
                    board.move_piece(board.selectedPiece, targetPos)
                    if board.is_checkmate():
                        board.gameActive = False
                    
                else:
                    board.selectedPiece.rect.center = board.squaresRect[board.originalPos[0]][board.originalPos[1]][0].center
                    board.originalPos = None
                    board.selectedPiece = None

        #Piece moving after the cursor
        if board.selectedPiece:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            board.selectedPiece.rect.center = (x_mouse, y_mouse)

    if gameActive and not board.gameOver:
        board.init_board(screen)
        board.allPieces.draw(screen)
        board.allPieces.update()

    elif board.gameOver:
        game_over(board.playerActive)
    else:
        screen.fill((118,150,86))
        screen.blit(surfaceGameStart,(150,400))


    pygame.display.update()
    clock.tick(60)