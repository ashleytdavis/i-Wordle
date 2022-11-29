import random, pygame, sys, os
from pygame.locals import *

# Global Variables

# COLORS
GREEN = (60, 158, 91)
YELLOW = (255, 244, 63)
GREY = (161, 161, 161)
DARKGREY = (91, 91, 91)
WHITE = (255, 255, 255)
OFFWHITE = (249, 249, 249)
RED = (255, 0, 10)
BLACK = (0, 0, 0)

# WINDOW DIMENSIONS
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500

# OUR LIST OF WORDS TO PICK FROM
WORDLIST = []


# Wordlist retrieved from https://github.com/lor-ethan/Word-Game/blob/master/routes/wordlist.txt

# -----------------------------------------------------------------------

# Retrieves a random word of length n from the wordlist
# Input: int ranging from 1 to 29
# Output: string
def getRandomWord(n):
    file = open("wordlist.txt", 'r')
    for row in file:
        if len(row) == n + 1:
            WORDLIST.append(row.strip('\n'))
    return WORDLIST[random.randint(0, len(WORDLIST) - 1)]


# Abstracted button method that creates a button with a given position and characteristics
def button(screen, position, text, color, fontsize):
    font = pygame.font.SysFont(pygame.font.get_fonts()[69], fontsize)
    text_render = font.render(text, True, (255, 255, 255))
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
                pygame.draw.rect(destination, GREY, (row * 75 + 68, col * 75 + 85, 50, 50), 0, 5)


def drawBoard(destination, tiles):
    # Title text at the top of the screen
    WORDLETEXT = pygame.font.SysFont(pygame.font.get_fonts()[69], 45)
    WORDLETEXTSurfaceObj = WORDLETEXT.render('i-WORDLE', True, GREEN)
    WORDLETEXTRectObj = WORDLETEXTSurfaceObj.get_rect()
    WORDLETEXTRectObj.center = (destination.get_width() / 2, 30)
    destination.blit(WORDLETEXTSurfaceObj, WORDLETEXTRectObj)

    for row in range(0, len(tiles[0])):
        for col in range(0, len(tiles)):
            pygame.draw.rect(destination, DARKGREY, ((row * 75) + 68, (col * 75) + 85, 50, 50), 3, 5)
            text = pygame.font.SysFont(pygame.font.get_fonts()[69], 25).render(tiles[col][row], True, BLACK)
            destination.blit(text, (row * 75 + 85, col * 75 + 92))


def drawKeyBoard(word, tiles, destination, keyBoard):
    for index in range(0, len(keyBoard[0])):
        pygame.draw.rect(destination, keyBoard[0][index][1],
                         ((index * 35) + (destination.get_width() / 2) - 170, 550, 25, 25))
        pygame.draw.rect(destination, BLACK, ((index * 35) + (destination.get_width() / 2) - 170, 550, 25, 25), 1)
        text = pygame.font.SysFont(pygame.font.get_fonts()[69], 16).render(keyBoard[0][index][0], True, (0, 0, 0))
        destination.blit(text, ((index * 35) + (destination.get_width() / 2) - 164, 551))

    for index in range(0, len(keyBoard[1])):
        pygame.draw.rect(destination, keyBoard[1][index][1],
                         ((index * 35) + (destination.get_width() / 2) - 147, 590, 25, 25))
        pygame.draw.rect(destination, BLACK, ((index * 35) + (destination.get_width() / 2) - 147, 590, 25, 25), 1)
        text = pygame.font.SysFont(pygame.font.get_fonts()[69], 16).render(keyBoard[1][index][0], True, (0, 0, 0))
        destination.blit(text, ((index * 35) + (destination.get_width() / 2) - 141, 591))

    for index in range(0, len(keyBoard[2])):
        pygame.draw.rect(destination, keyBoard[2][index][1],
                         ((index * 35) + (destination.get_width() / 2) - 112, 630, 25, 25))
        pygame.draw.rect(destination, BLACK, ((index * 35) + (destination.get_width() / 2) - 112, 630, 25, 25), 1)
        text = pygame.font.SysFont(pygame.font.get_fonts()[69], 16).render(keyBoard[2][index][0], True, (0, 0, 0))
        destination.blit(text, ((index * 35) + (destination.get_width() / 2) - 106, 631))

    for row in range(3):
        for col in range(len(keyBoard[row])):
            letter = keyBoard[row][col][0].lower()
            if letter in tiles:
                if letter not in word:
                    keyBoard[row][col][1] = DARKGREY
                elif letter in tiles and word.index(letter) == tiles.index(letter):
                    keyBoard[row][col][1] = GREEN
                else:
                    keyBoard[row][col][1] = YELLOW


def gameover(turn, gameOver, window, tiles, word):
    if turn == 6 or gameOver:
        pygame.draw.rect(window, BLACK,
                                (int((window.get_width() / 2) - 150), int((window.get_height() / 2) - 250), 300, 200))
        pygame.draw.rect(window, WHITE,
                                (int((window.get_width() / 2) - 148), int((window.get_height() / 2) - 248), 296, 196))
        playAgain = button(window, ((window.get_width() / 2) - 85, (window.get_height() / 2) - 100), 'PLAY AGAIN?', GREEN, 30)

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if playAgain.collidepoint(pygame.mouse.get_pos()):
                    intro()
            if event.type == pygame.KEYDOWN:
                # If the user hits the escape button, quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        guess = ""
        for i in range(len(tiles[0])):
            guess += tiles[5][i]
        if turn == 6 and guess != word:
            loser_text = pygame.font.SysFont(pygame.font.get_fonts()[69], 50).render('YOU LOSE!', True, BLACK)
            secret_word = pygame.font.SysFont(pygame.font.get_fonts()[69], 25).render('SECRET WORD:', True, BLACK)
            word_text = pygame.font.SysFont(pygame.font.get_fonts()[69], 35).render(word.upper(), True, BLACK)

            window.blit(loser_text, ((window.get_width() / 2) - 125, (window.get_height() / 2) - 250))
            window.blit(secret_word, ((window.get_width() / 2) - 88, (window.get_height() / 2) - 190))
            window.blit(word_text, ((window.get_width() / 2) - 42, (window.get_height() / 2) - 160))
            return

        return #You win!


def game(N):
    keyBoard = [[["Q", GREY], ["W", GREY], ["E", GREY], ["R", GREY], ["T", GREY], ["Y", GREY],
                 ["U", GREY], ["I", GREY], ["O", GREY], ["P", GREY]],
                [['A', GREY], ["S", GREY], ["D", GREY], ["F", GREY], ["G", GREY], ["H", GREY],
                 ["J", GREY], ["K", GREY], ["L", GREY]],
                [["Z", GREY], ["X", GREY], ["C", GREY], ["V", GREY], ["B", GREY], ["N", GREY],
                 ["M", GREY]]]
    allowedChars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                    'w', 'x', 'y', 'z']

    # remove all attributes from before
    pygame.display.quit()
    pygame.init()
    window = pygame.display.set_mode(((N * 75 + 110), 680))
    # Change the background to off-white
    window.fill((249, 249, 249))

    # Change the caption of the window
    pygame.display.set_caption('i-Wordle')

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
        drawKeyBoard(SECRET_WORD, tiles[turn - 1], window, keyBoard)
        gameover(turn, gameOver, window, tiles, SECRET_WORD)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # If the user hits the escape button, quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    tiles[turn][letters - 1] = ""
                    letters -= 1
                if event.key == pygame.K_RETURN:
                    if letters != N:
                        continue
                    elif not gameOver:
                        turn += 1
                        letters = 0
                if event.key == pygame.K_BACKSPACE and letters > 0:
                    tiles[turn][letters - 1] = ""
                    letters -= 1
            if event.type == pygame.TEXTINPUT and turnActive and not gameOver:
                entry = event.__getattribute__('text')
                if entry not in allowedChars:
                    continue
                else:
                    tiles[turn][letters] = entry
                    letters += 1

        if letters == N:
            turnActive = False
        if letters < N:
            turnActive = True

        guess = ""
        for i in range(N):
            guess += tiles[turn - 1][i].lower()
        if guess == SECRET_WORD:
            gameOver = True
            winner = pygame.font.SysFont(pygame.font.get_fonts()[69], 50).render('Winner', True, (255, 0, 0))
            window.blit(winner, (window.get_width() / 2, window.get_height() / 2))

        pygame.display.flip()


# Builds the interactive intro screen
def intro():
    # NUMBER OF LETTERS IN THE SECRET WORD
    N = 4
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
        # Update Counter Text
        COUNTERTEXTSurfaceObj = COUNTERTEXT.render(str(N), True, WHITE, DARKGREY)
        COUNTERTEXTRectObj = COUNTERTEXTSurfaceObj.get_rect()
        COUNTERTEXTRectObj.center = (500, 295)
        window.blit(COUNTERTEXTSurfaceObj, COUNTERTEXTRectObj)

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
                    if N == 4:
                        N = 4
                    else:
                        N -= 1

                if plus.collidepoint(pygame.mouse.get_pos()):
                    # Clamping Values
                    if N == 23:
                        N = 23
                    else:
                        N += 1
                if begin.collidepoint(pygame.mouse.get_pos()):
                    game(N)

        pygame.display.flip()


def main():
    intro()


if __name__ == "__main__":
    main()
