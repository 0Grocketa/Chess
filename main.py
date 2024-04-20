import pygame
from sys import exit

SQURE_SIZE = 100
BOARD_SIZE = 8
game_active = False



class Board():
    def __init__(self):

        self.dark_square = pygame.image.load("Pieces\square_brown_dark.png").convert_alpha()
        self.light_square = pygame.image.load("Pieces\square_brown_light.png").convert_alpha()

        self.dark_square = pygame.transform.scale(self.dark_square,(100,100))
        self.light_square = pygame.transform.scale(self.light_square,(100,100))

        #store coordinates of squares
        self.squares_rect = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]  


        #Fill in the  squares_rect with proper coordinates for squares
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 0: self.squares_rect[row][col] = self.light_square.get_rect(topleft = (col * 100, row * 100))
                else: self.squares_rect[row][col] = self.dark_square.get_rect(topleft = (col * 100, row * 100))

        

        #Sprite Groups for pieces
        self.all_pieces = pygame.sprite.Group()
        
        self.init_pieces()
        self.selected_piece = None
        self.original_pos = None
        self.player_active = 'w'


    def init_pieces(self):
        self.init_pawns()
        self.init_rooks()
        self.init_knights()
        self.init_bishops()
        self.init_king_and_queen()


    def init_pawns(self):
        #white pawns

        for col in range(BOARD_SIZE):
            x,y = self.squares_rect[6][col].center

            pawn = Pawn('w', (x, y))

            self.all_pieces.add(pawn)


        
        #black pawns
        for col in range(BOARD_SIZE):
            x,y = self.squares_rect[1][col].center

            pawn = Pawn('b',(x,y))

            self.all_pieces.add(pawn)


    def init_rooks(self):
        for row in [0, 7]:
            for col in [0, 7]:
                x,y = self.squares_rect[row][col].center

                #Add black rooks
                if row == 0:
                    rook = Rook('b',(x,y))

                    self.all_pieces.add(rook)
                   

                #Add white rooks

                else:
                    rook = Rook('w',(x,y))

                    self.all_pieces.add(rook)
                    
                    
    def init_knights(self):
        for row in [0, 7]:
            for col in [1, 6]:
                x,y = self.squares_rect[row][col].center

                #Add black knights
                if row == 0:
                    knight = Knight('b',(x,y))

                    self.all_pieces.add(knight)
                    


                #Add white knights

                else:
                    knight = Knight('w',(x,y))

                    self.all_pieces.add(knight)
                    


    def init_bishops(self):
        for row in [0, 7]:
            for col in [2, 5]:
                x,y = self.squares_rect[row][col].center

                #Add black bishops
                if row == 0:
                    bishop = Bishop('b',(x,y))

                    self.all_pieces.add(bishop)
                    



                #Add white bishops

                else:
                    bishop = Bishop('w',(x,y))

                    self.all_pieces.add(bishop)
                    
    
    def init_king_and_queen(self):
        #Black
        x,y = self.squares_rect[0][3].center
        queen = Queen('b',(x,y))
      

        x,y = self.squares_rect[0][4].center
        king = King('b',(x,y))
        

        self.all_pieces.add(queen,king)
        

        

        #White
        x,y = self.squares_rect[7][3].center
        queen = Queen('w',(x,y))


        x,y = self.squares_rect[7][4].center
        king = King('w',(x,y))


        self.all_pieces.add(queen,king)
       

    #Draw the board
    def init_board(self,surface):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 0: surface.blit(self.light_square, self.squares_rect[row][col])
                else: surface.blit(self.dark_square, self.squares_rect[row][col])


    def get_square_center_from_mouse(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                square = self.squares_rect[row][col]
                if square.collidepoint(pygame.mouse.get_pos()):
                    return square.center
        return None


    def is_square_free(self, pos):
        for sprite in self.all_pieces:
            if sprite.rect.collidepoint(pos):
                if sprite != self.selected_piece:
                    return False
        return True


    def get_color_of_piece_bysquare(self,square_center):
        for sprite in self.all_pieces:
            if sprite.rect.center == square_center:
                return sprite.color
        return None


    #get original positon of the piece which is already picked up
    def get_piece_position(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                square = self.squares_rect[row][col]
                if square.collidepoint(self.original_pos):
                    return square.center
        return None
        

    def get_pawn_valid_moves(self,pawn):
        valid_moves = []
        direction = -1 if pawn.color == 'w' else 1
        start_col = 650 if pawn.color == 'w' else 150

        position = self.get_piece_position()
        
        #Normal forward moves
        if position is not None:
            one_square_forward = (position[0], position[1] + (100 * direction))
            two_squares_forward = (position[0], position[1] + 2 * (100 * direction))


            if self.is_square_free(one_square_forward):
                valid_moves.append(one_square_forward)
            
            if ((pawn.color == 'w') and (self.original_pos[1] == start_col)) or ((pawn.color == 'b' and self.original_pos[1] == start_col)):
                if  self.is_square_free(one_square_forward) and self.is_square_free(two_squares_forward):
                    valid_moves.append(two_squares_forward)
            
            # DIAGONAL CHECK FOR TAKES   
            for x in [-1,1]:
                diagonal = (position[0] + x * 100, position[1] + (direction * 100))

                if diagonal[0] < 0 or diagonal[1] < 0: continue
                
                if self.is_square_free(diagonal) == 0:
                    occupant_color = self.get_color_of_piece_bysquare(diagonal)
                    if occupant_color != pawn.color:
                        valid_moves.append(diagonal)
            return valid_moves

        return valid_moves
    
    #get potential pawn attack moves regardless of opponent positioning
    def get_pawn_attack_moves(self, pawn):
        attack_moves = []
        direction = -1 if pawn.color == 'w' else 1  # Determine movement direction based on color

        # Get the current position of the pawn on the board
        current_pos = pawn.rect.center

        if current_pos is None:
            return attack_moves  # If position is not found, return empty list

        # Diagonal attack positions (potential moves regardless of opponent presence)
        diagonal_offsets = [(-1, direction), (1, direction)]
        for dx, dy in diagonal_offsets:
            # Calculate potential diagonal positions
            potential_x = current_pos[0] + dx * SQURE_SIZE
            potential_y = current_pos[1] + dy * SQURE_SIZE

            # Ensure the potential position is within the board limits
            if 0 <= potential_x < BOARD_SIZE * SQURE_SIZE and 0 <= potential_y < BOARD_SIZE * SQURE_SIZE:
                potential_pos = (potential_x, potential_y)
                attack_moves.append(potential_pos)

        return attack_moves
    

    def get_knight_attack_moves(self, knight):
        attack_moves = []
        start_pos = knight.rect.center  

        # List of all possible "L" moves for a knight
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        # Get the starting coordinates
        start_x, start_y = start_pos

        for dx, dy in directions:
            # Calculate the new position based on each "L" shaped movement
            x = start_x + dx * SQURE_SIZE
            y = start_y + dy * SQURE_SIZE

            # Check if the new position is within the bounds of the chess board
            if 0 <= x < SQURE_SIZE * BOARD_SIZE and 0 <= y < SQURE_SIZE * BOARD_SIZE:
                new_pos = (x, y)

                # Append the position if it's either free or occupied by an opposing piece
                if self.is_square_free(new_pos) or self.get_color_of_piece_bysquare(new_pos) != knight.color:
                    attack_moves.append(new_pos)

        return attack_moves


    def get_knight_valid_moves(self, knight):
        valid_moves = []
        start_pos = self.original_pos  

        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        if start_pos:
            for direction in directions:
                x_increment, y_increment = direction
                x,y = start_pos
                
                while True:
                    x+= x_increment * SQURE_SIZE
                    y+= y_increment * SQURE_SIZE

                    # Check if the landing square is free or occupied by an opposing piece
                    if 0 <= x <= SQURE_SIZE * BOARD_SIZE and 0 <= y <= SQURE_SIZE * BOARD_SIZE:
                        pos = (x,y)
                        
                        if self.is_square_free(pos):
                            valid_moves.append(pos)

                        else:
                            if self.get_color_of_piece_bysquare(pos) != knight.color:
                                valid_moves.append(pos)
                    else:
                        break # Stop if moving further would go off the board
        return valid_moves


    def get_rook_bishop_queen_valid_moves(self,piece):
        if isinstance(piece,Rook):
            directions = [(1,0),(0,1),(-1,0),(0,-1)]
        
        elif isinstance(piece, Bishop):
            directions = [(1,1),(1,-1),(-1,1),(-1,-1)]

        elif isinstance(piece, Queen):
            directions = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]

        valid_moves = []
        start_pos = self.original_pos  

        if start_pos:
            for direction in directions:
                x_increment, y_increment = direction
                x,y = start_pos
                
                while True:
                    x+= x_increment * SQURE_SIZE
                    y+= y_increment * SQURE_SIZE

                    # Check if the landing square is free or occupied by an opposing piece
                    if 0 <= x <= SQURE_SIZE * BOARD_SIZE and 0 <= y <= SQURE_SIZE * BOARD_SIZE:
                        pos = (x,y)
                        
                        if self.is_square_free(pos):
                            valid_moves.append(pos)

                        else:
                            if self.get_color_of_piece_bysquare(pos) != piece.color:
                                valid_moves.append(pos)
                            break # Stop moving in this direction upon hitting a piece
                    else:
                        break # Stop if moving further would go off the board

        return valid_moves


    def get_rook_bishop_queen_attack_moves(self,piece):
        if isinstance(piece,Rook):
            directions = [(1,0),(0,1),(-1,0),(0,-1)]
        
        elif isinstance(piece, Bishop):
            directions = [(1,1),(1,-1),(-1,1),(-1,-1)]

        elif isinstance(piece, Queen):
            directions = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]

        attack_moves = []
        start_pos = piece.rect.center  

        if start_pos:
            for direction in directions:
                x_increment, y_increment = direction
                x,y = start_pos
                
                while True:
                    x+= x_increment * SQURE_SIZE
                    y+= y_increment * SQURE_SIZE

                    # Check if the landing square is free or occupied by an opposing piece
                    if 0 <= x <= SQURE_SIZE * BOARD_SIZE and 0 <= y <= SQURE_SIZE * BOARD_SIZE:
                        pos = (x,y)
                        
                        if self.is_square_free(pos):
                            attack_moves.append(pos)

                        else:
                            if self.get_color_of_piece_bysquare(pos) != piece.color:
                                attack_moves.append(pos)
                            break # Stop moving in this direction upon hitting a piece
                    else:
                        break # Stop if moving further would go off the board

        return attack_moves


    def get_king_valid_moves(self,king):
        valid_moves = []
        start_pos = self.original_pos
        directions = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]

        if start_pos:
            x_start, y_start = start_pos
            for dx, dy in directions:
                x_new = x_start + dx * SQURE_SIZE
                y_new = y_start + dy * SQURE_SIZE
                pos = (x_new,y_new)

                # Ensure the new position is within the board boundaries
                if 0 <= x_new < BOARD_SIZE * SQURE_SIZE and 0 <= y_new < BOARD_SIZE * SQURE_SIZE:
                    pos = (x_new, y_new)

                    if (self.is_square_free(pos) or self.get_color_of_piece_bysquare(pos) != king.color):
                        valid_moves.append(pos)

        return valid_moves
                

    def get_king_attack_moves(self,king):
        attack_moves = []
        start_pos = king.rect.center
        directions = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]

        if start_pos:
            x_start, y_start = start_pos
            for dx, dy in directions:
                x_new = x_start + dx * SQURE_SIZE
                y_new = y_start + dy * SQURE_SIZE
                pos = (x_new,y_new)

                # Ensure the new position is within the board boundaries
                if 0 <= x_new < BOARD_SIZE * SQURE_SIZE and 0 <= y_new < BOARD_SIZE * SQURE_SIZE:
                    pos = (x_new, y_new)

                    if (self.is_square_free(pos) or self.get_color_of_piece_bysquare(pos) != king.color):
                        attack_moves.append(pos)

        return attack_moves


    def take_piece(self, target_center):
        for to_delete in self.all_pieces:  # Iterate over a copy since we're modifying the group
            if to_delete.rect.center == target_center and to_delete != self.selected_piece:
                self.all_pieces.remove(to_delete)
                if to_delete.color == 'w':
                    
                    self.all_pieces.remove(to_delete)
                else:
                    
                    self.all_pieces.remove(to_delete)
                break  
    

    def is_square_under_attack(self, potential_pos, color):
         #Determine the opposing color based on the given color parameter
        opposing_color = 'w' if color == 'b' else 'b'
        attack_moves =[]
        # Loop over all pieces, checking moves of only opposing color pieces
        for sprite in self.all_pieces:
            if sprite.color == opposing_color:  # Only consider pieces of the opposing color
                if isinstance(sprite, Pawn):
                    attack_moves = self.get_pawn_attack_moves(sprite) 
                    
                elif isinstance(sprite, Knight):
                    attack_moves = self.get_knight_attack_moves(sprite)
                   
                    
                elif isinstance(sprite, Queen) or isinstance(sprite, Bishop) or isinstance(sprite, Rook):
                    attack_moves = self.get_rook_bishop_queen_attack_moves(sprite)
                
                    
                elif isinstance(sprite, King):
                    attack_moves = self.get_king_attack_moves(sprite)


                if potential_pos in attack_moves:

                    return True  # Early exit if any piece can attack the position

        return False  # Return False if no pieces can attack the position

    
    def get_valid_moves(self,target_center):
        
        #If pawn picked
        if isinstance(board.selected_piece, Pawn):
            valid_moves = board.get_pawn_valid_moves(board.selected_piece)
                    
        elif isinstance(board.selected_piece, Knight):
            valid_moves = board.get_knight_valid_moves(board.selected_piece)
                
        elif isinstance(board.selected_piece,King):
            valid_moves = board.get_king_valid_moves(board.selected_piece)
            for move in valid_moves:
                if board.is_square_under_attack(move, board.selected_piece.color):
                            
                    valid_moves.remove(move)

        else:
            valid_moves = board.get_rook_bishop_queen_valid_moves(board.selected_piece)
        
        return valid_moves


    def is_check(self,color):
        opposing_color = 'w' if color == 'b' else 'b'
        #find the king 
        for sprite in self.all_pieces:
            if color == sprite.color and isinstance(sprite,King):
                king = sprite
                break
        #check for cheks
        for piece in self.all_pieces:
            if piece.color == opposing_color:
                if self.is_square_under_attack(king.rect.center, king.color):
                    return True


    #Chnage active player
    def swicth_player(self):
        return 'w' if self.player_active == 'b' else 'b'
    
    #Dopili tut 
    def move_resolves_check(self, piece, target_pos):
        #We need this opposing color since we revert color we pass to is_check but here we want
        #  to check if move will resolve a check given to active player
        opposing_color = 'w' if piece.color == 'b' else 'b'

        # Simulate the move
        piece.rect.center = target_pos
        check_status = not self.is_check(opposing_color)
        # Revert the move
        piece.rect.center = self.original_pos
        return check_status


class Piece(pygame.sprite.Sprite):
    def __init__(self,color,initial_position, image_file):  #input color as "b" or "w", and initial position as tuple for the center of square coordinates
        super().__init__()
        self.image = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(self.image,(100,100))
        self.rect = self.image.get_rect(center = initial_position)
        self.color = color


class Pawn(Piece):
    def __init__(self,color,initial_position):   
        super().__init__(color, initial_position, f"Pieces\{color}_pawn.png")
        self.name = "Pawn"


class King(Piece):
    def __init__(self,color,initial_position):
        super().__init__(color, initial_position, f"Pieces\{color}_king.png")
        self.name = "King"


class Queen(Piece):
    def __init__(self,color,initial_position):
        super().__init__(color, initial_position, f"Pieces\{color}_queen.png")
        self.name = "Queen"


class Bishop(Piece):
    def __init__(self,color,initial_position):
        super().__init__(color, initial_position, f"Pieces\{color}_bishop.png")
        self.name = "Bishop"


class Knight(Piece):
    def __init__(self,color,initial_position):
        super().__init__(color, initial_position, f"Pieces\{color}_knight.png")
        self.name = "Knight"


class Rook(Piece):
    def __init__(self,color,initial_position):
        super().__init__(color, initial_position, f"Pieces\{color}_rook.png")
        self.name = "Rook"


pygame.init()
screen = pygame.display.set_mode((800,800))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
test_font = pygame.font.Font(None,50)

board = Board()

#Initial Screeen
surface = test_font.render("Press SPACE to start playing",True, "black")


while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        #Press space to start the game
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_active = True
        
        #if player picks up a piece
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
             for sprite in board.all_pieces:
                if sprite.rect.collidepoint(event.pos) and sprite.color == board.player_active:
                    board.selected_piece = sprite
                    board.original_pos = sprite.rect.center
                    break

        #if player lets go of piece
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if board.selected_piece:

                target_center = board.get_square_center_from_mouse()
                valid_moves = board.get_valid_moves(target_center)

                # If in check, filter the moves to only those that would resolve the check
                if board.is_check(board.player_active):
                    #if selecetd king we also check if we take another 
                    if isinstance(board.selected_piece, King):
                        valid_moves = [move for move in valid_moves if (board.is_square_under_attack(move,board.player_active) and board.move_resolves_check(board.selected_piece,move))]
                    else: 
                        valid_moves = [move for move in valid_moves if board.move_resolves_check(board.selected_piece,move)]

                if target_center in valid_moves: 
                    
                    if not board.is_square_free(target_center):
                        board.take_piece(target_center)

                    board.selected_piece.rect.center = target_center
                    
                    #Switch player after successfull move
                    board.player_active = board.swicth_player()
                     
                else:
                    #if not valid revert to original pos
                    board.selected_piece.rect.center = board.original_pos
                    
                board.selected_piece = None

        
        #Piece moving after the cursor
        if board.selected_piece:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            board.selected_piece.rect.center = (x_mouse, y_mouse)
                    

    if game_active:
        board.init_board(screen)
        board.all_pieces.draw(screen)
        board.all_pieces.update()

    else:
        screen.fill((118,150,86))
        screen.blit(surface,(150,400))


    pygame.display.update()
    clock.tick(60)

