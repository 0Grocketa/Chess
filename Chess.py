from BoardClass import *
from sys import exit


# Display gameover screen
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
        
        # If player lets go of piece
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if board.selectedPiece:

                # Get placement position and valid moves of the piece
                targetPos = board.get_square_from_mouse()
                validMoves = board.get_valid_moves(board.selectedPiece)
                
                # If the piece is pinned restrict its movement
                if board.is_pinned(board.selectedPiece, targetPos):
                    validMoves = []
                    
                # If king seleceted remove squares which are under attack
                if isinstance(board.selectedPiece,King):
                    safe_moves = []
                    for move in validMoves:
                        if not board.is_square_under_attack(board.selectedPiece.color,targetPos):
                            safe_moves.append(move)
                    validMoves = safe_moves

                # Move the piece if placement position is legal
                if  targetPos in validMoves:
                    board.move_piece(board.selectedPiece, targetPos)

                    #If checkmate end game
                    if board.is_checkmate():
                        board.gameActive = False
                
                # Move is not legal move the piece to original spot 
                else:
                    board.selectedPiece.rect.center = board.squaresRect[board.originalPos[0]][board.originalPos[1]][0].center
                    board.originalPos = None
                    board.selectedPiece = None

        #Piece moving after the cursor
        if board.selectedPiece:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            board.selectedPiece.rect.center = (x_mouse, y_mouse)

    # Game screen
    if gameActive and not board.gameOver:
        board.init_board(screen)
        board.allPieces.draw(screen)
        board.allPieces.update()

    # Game over screen
    elif board.gameOver:
        game_over(board.playerActive)
    
    # Welcome screen
    else:
        screen.fill((118,150,86))
        screen.blit(surfaceGameStart,(150,400))


    pygame.display.update()
    clock.tick(60)