import random, pygame, sys, os
from pygame.locals import *

# Global Variables

# COLORS
GREEN = (60, 158, 91)
YELLOW = (255, 244, 63)
GREY = (161, 161, 161)
DARKGREY = (122, 122, 122)
WHITE = (255, 255, 255)
OFFWHITE = (249, 249, 249)
RED = (255, 0, 10)

# WINDOW DIMENSIONS
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500

# Wordlist retrieved from https://github.com/lor-ethan/Word-Game/blob/master/routes/wordlist.txt

# -----------------------------------------------------------------------

# Retrieves a random word of length n from the wordlist
# Input: int ranging from 1 to 29
# Output: string
def getRandomWord(n):
    WORDLIST = []
    file = open("wordlist.txt", 'r')
    for row in file:
        if len(row) == n + 1:
            WORDLIST.append(row.strip())
    return WORDLIST[random.randint(0, len(WORDLIST) - 1)]

# Abstracted button method that creates a button with a given position and characteristics
def button(screen, position, text, color, fontsize):
    font = pygame.font.SysFont(pygame.font.get_fonts()[69], fontsize)
    text_render = font.render(text, 1, (255, 255, 255))
    x, y, w, h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w, y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x + w, y + h), [x + w, y], 5)
    pygame.draw.rect(screen, color, (x, y, w, h))
    return screen.blit(text_render, (x, y))

# Updates the window as to how the users guess matches up with the secret word
def check_word(destination, word, tiles, turn):
    for row in range(0, len(tiles[0])):
        for col in range(0, len(tiles)):
            # If letter is in the right spot, make it green!
            if word[row] == tiles[col][row] and turn > col:
                pygame.draw.rect(destination, GREEN, (row * 75 + 68, col * 75 + 85, 50, 50), 0, 5)
            # If the letter is in the wrong spot, make it yellow!
            elif tiles[col][row] in word and turn > col:
                pygame.draw.rect(destination, YELLOW, (row * 75 + 68, col * 75 + 85, 50, 50), 0, 5)
            # If the letter is not in this word, make it grey!
            elif tiles[col][row] not in word and turn > col:
                pygame.draw.rect(destination, DARKGREY, (row * 75 + 68, col * 75 + 85, 50, 50), 0, 5)

def drawBoard(destination, tiles):

    # Title text at the top of the screen
    WORDLETEXT = pygame.font.SysFont(pygame.font.get_fonts()[69], 45)
    WORDLETEXTSurfaceObj = WORDLETEXT.render('i-WORDLE', True, GREEN)
    WORDLETEXTRectObj = WORDLETEXTSurfaceObj.get_rect()
    WORDLETEXTRectObj.center = (destination.get_size()[0] / 2, 30)
    destination.blit(WORDLETEXTSurfaceObj, WORDLETEXTRectObj)


    for row in range(0, len(tiles[0])):
        for col in range(0, len(tiles)):
            pygame.draw.rect(destination, DARKGREY, ((row * 75) + 68, (col * 75) + 85, 50, 50), 3, 5)
            text = pygame.font.SysFont(pygame.font.get_fonts()[69], 25).render(tiles[col][row], True, (0, 0, 0))
            destination.blit(text, (row * 75 + 85, col * 75 + 92))

def game(N):
    #remove all attributes from before
    pygame.display.quit()
    pygame.init()
    window = pygame.display.set_mode(((N * 75 + 110), 700))    # Change the background to off-white
    window.fill((249, 249, 249))

    # Get the secret word!
    SECRET_WORD = getRandomWord(N)

    tiles = [[""] * N for i in range(6)]


    letters = 0
    gameOver = False
    turn = 0
    turnActive = True
    timer = pygame.time.Clock()


    while True:
        timer.tick(60)
        check_word(window, SECRET_WORD, tiles, turn)
        drawBoard(window, tiles)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.TEXTINPUT and turnActive and not gameOver:
                entry = event.__getattribute__('text')
                tiles[turn][letters] = entry
                letters += 1
            if event.type == pygame.KEYDOWN:
                # If the user hits the escape button, quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_BACKSPACE and letters > 0:
                    tiles[turn][letters-1] = ""
                    letters -= 1
                if event.key == pygame.K_RETURN:
                    if turn == 6:
                        intro()
                    elif letters != N:
                        continue
                    elif not gameOver:
                        turn += 1
                        letters = 0


        guess = ""
        for row in range(0, 6):
            for i in range(0, N - 1):
                guess += tiles[row][i]
            if guess == SECRET_WORD and row < turn:
                gameOver = True

        if letters == N:
            turnActive = False
        if letters < N:
            turnActive = True

        if gameOver or turn == 6:
            gameOver = True
            playAgain = button(window, (window.get_size()[0] / 3, 600), 'PLAY AGAIN?', GREEN, 30)
            playAgain.center = (window.get_size()[0] / 2, 600)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playAgain.collidepoint(pygame.mouse.get_pos()):
                    intro()
            if turn < 6:
                Winner_text = pygame.font.SysFont(pygame.font.get_fonts()[69], 50).render('Winner', True, GREEN)
                window.blit(Winner_text, (40, 550))
            else:
              loser_text = pygame.font.SysFont(pygame.font.get_fonts()[69], 35).render('You lose!', True, RED)
              window.blit(loser_text, (40, 510))


        pygame.display.flip()




# Builds the interactive intro screen
def intro():

    # NUMBER OF LETTERS IN THE SECRET WORD
    N = 3
    pygame.display.quit()
    pygame.init()

    # Set the window size to 600 by 600
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Change the caption of the window
    pygame.display.set_caption('i-Wordle')

    # Change the background to off-white
    window.fill(OFFWHITE)

    # Title at the top of the game
    WORDLETEXT = pygame.font.SysFont(pygame.font.get_fonts()[69], 170)
    WORDLETEXTSurfaceObj = WORDLETEXT.render('i-WORDLE', True, GREEN)
    WORDLETEXTRectObj = WORDLETEXTSurfaceObj.get_rect()
    WORDLETEXTRectObj.center = (500, 125)
    window.blit(WORDLETEXTSurfaceObj, WORDLETEXTRectObj)

    # Begin Button
    begin = button(window, (450, 415), 'BEGIN', GREEN, 40)

    # - Button
    minus = button(window, (410, 270), '-', GREY, 50)

    # + Button
    plus = button(window, (570, 270), '+', GREY, 50)

    # Counter Box
    pygame.draw.rect(window, DARKGREY, (450, 250, 100, 100))
    COUNTERTEXT = pygame.font.SysFont(pygame.font.get_fonts()[69], 75)
    COUNTERTEXTSurfaceObj = COUNTERTEXT.render(str(N), True, WHITE, DARKGREY)
    COUNTERTEXTRectObj = COUNTERTEXTSurfaceObj.get_rect()
    COUNTERTEXTRectObj.center = (500, 295)
    window.blit(COUNTERTEXTSurfaceObj, COUNTERTEXTRectObj)

    while True:
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # If the user hits the escape button, quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if minus.collidepoint(pygame.mouse.get_pos()):
                    # Clamping Values
                    if N == 3:
                        N = 3
                    else:
                        N -= 1
                    # Update Counter Text
                    COUNTERTEXTSurfaceObj = COUNTERTEXT.render(str(N), True, WHITE, DARKGREY)
                    COUNTERTEXTRectObj = COUNTERTEXTSurfaceObj.get_rect()
                    COUNTERTEXTRectObj.center = (500, 295)
                    window.blit(COUNTERTEXTSurfaceObj, COUNTERTEXTRectObj)
                if plus.collidepoint(pygame.mouse.get_pos()):
                    # Clamping Values
                    if N == 29:
                        N = 29
                    else:
                        N += 1
                    # Update Counter Text
                    COUNTERTEXTSurfaceObj = COUNTERTEXT.render(str(N), True, WHITE, DARKGREY)
                    COUNTERTEXTRectObj = COUNTERTEXTSurfaceObj.get_rect()
                    COUNTERTEXTRectObj.center = (500, 295)
                    window.blit(COUNTERTEXTSurfaceObj, COUNTERTEXTRectObj)
                if begin.collidepoint(pygame.mouse.get_pos()):
                    game(N)

        pygame.display.flip()


def main():
    intro()


if __name__ == "__main__":
    main()
