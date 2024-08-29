import pygame

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
