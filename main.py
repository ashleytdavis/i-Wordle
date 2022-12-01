import random, pygame, sys
from pygame.locals import *

# COLORS
GREEN = (60, 158, 91)
YELLOW = (255, 244, 63)
GREY = (161, 161, 161)
DARKGREY = (91, 91, 91)
WHITE = (255, 255, 255)
OFFWHITE = (249, 249, 249)
RED = (255, 0, 10)
BLACK = (0, 0, 0)

# OUR LIST OF WORDS TO PICK FROM
WORDLIST = []

# Wordlist retrieved from https://github.com/lor-ethan/Word-Game/blob/master/routes/wordlist.txt

# -----------------------------------------------------------------------

# Retrieves a random word of length n from the wordlist
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
    destination.fill(OFFWHITE)
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

# Draws the board and updates each square with a letter if typed
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

# Draws the keyboard and updates each key with a color depending on the secret word
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
            # If the letter is in the guess...
            if letter in tiles:
                # If the letter is not in the secret word, make the key grey
                if letter not in word:
                    keyBoard[row][col][1] = DARKGREY
                # If the letter is in the secret word and guessed in the right position, make the key green
                elif letter in tiles and word.index(letter) == tiles.index(letter):
                    keyBoard[row][col][1] = GREEN
                # Else, make the key yellow
                else:
                    keyBoard[row][col][1] = YELLOW

# Draws the game over screen and changes whether the user wins
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

        secret_word = pygame.font.SysFont(pygame.font.get_fonts()[69], 25).render('SECRET WORD:', True, BLACK)
        word_text = pygame.font.SysFont(pygame.font.get_fonts()[69], 35).render(word.upper(), True, BLACK)
        word_text_rect = word_text.get_rect()
        word_text_rect.center = (window.get_width() / 2, (window.get_height() / 2) - 135)

        window.blit(secret_word, ((window.get_width() / 2) - 88, (window.get_height() / 2) - 190))
        window.blit(word_text, word_text_rect)

        guess = ""
        for i in range(len(tiles[0])):
            guess += tiles[turn - 1][i]

        if guess == word:
            winner_text = pygame.font.SysFont(pygame.font.get_fonts()[69], 50).render('YOU WIN!', True, BLACK)
            window.blit(winner_text, ((window.get_width() / 2) - 113, (window.get_height() / 2) - 250))
        if turn == 6 and guess != word:
            loser_text = pygame.font.SysFont(pygame.font.get_fonts()[69], 50).render('YOU LOSE!', True, BLACK)
            window.blit(loser_text, ((window.get_width() / 2) - 125, (window.get_height() / 2) - 250))

# Performs game actions
def game(N):
    # Each letter and its status (color_
    keyBoard = [[["Q", GREY], ["W", GREY], ["E", GREY], ["R", GREY], ["T", GREY], ["Y", GREY],
                 ["U", GREY], ["I", GREY], ["O", GREY], ["P", GREY]],
                [['A', GREY], ["S", GREY], ["D", GREY], ["F", GREY], ["G", GREY], ["H", GREY],
                 ["J", GREY], ["K", GREY], ["L", GREY]],
                [["Z", GREY], ["X", GREY], ["C", GREY], ["V", GREY], ["B", GREY], ["N", GREY],
                 ["M", GREY]]]
    # The letters that are allowed to be used (no special characters,symbols,etc.)
    allowedChars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                    'w', 'x', 'y', 'z']

    # remove all attributes from before
    pygame.display.quit()
    pygame.init()
    window = pygame.display.set_mode(((N * 75 + 110), 680))
    # Change the background to off-white
    window.fill(OFFWHITE)
    # Change the caption of the window
    pygame.display.set_caption('i-Wordle')
    # Get the secret word!
    SECRET_WORD = getRandomWord(N)
    # Create the board
    tiles = [[""] * N for i in range(6)]
    # Initialize game variables
    letters = 0
    gameOver = False
    turn = 0
    turnActive = True
    timer = pygame.time.Clock()

    while True:
        timer.tick(60)
        # Update the screen
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
                # If the user hits the space bar, don't do anything
                if event.key == pygame.K_SPACE:
                    continue
                if event.key == pygame.K_RETURN:
                    # If the user hits the return key before completing their guess, do not let them move on
                    if letters != N:
                        continue
                    elif not gameOver:
                        turn += 1
                        letters = 0
                # If the user hits the backspace key, remove the last entered letter
                if event.key == pygame.K_BACKSPACE and letters > 0:
                    tiles[turn][letters - 1] = ""
                    letters -= 1
            if event.type == pygame.TEXTINPUT and turnActive and not gameOver:
                entry = event.__getattribute__('text')
                # Ensures only letters are entered
                if entry not in allowedChars:
                    continue
                else:
                    tiles[turn][letters] = entry
                    letters += 1

        # Ensures the user cannot type more letters than allowed
        if letters == N:
            turnActive = False
        if letters < N:
            turnActive = True

        # Checks if the user's guess was the secret word
        guess = ""
        for i in range(N):
            guess += tiles[turn - 1][i].lower()
        if guess == SECRET_WORD:
            gameOver = True

        pygame.display.update()


# Builds the interactive intro screen
def intro():
    # NUMBER OF LETTERS IN THE SECRET WORD
    N = 4
    pygame.display.quit()
    pygame.init()

    # Set the window size to 600 by 600
    window = pygame.display.set_mode((1000, 500))

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

    while True:
        # Update Counter Text
        COUNTERTEXT = pygame.font.SysFont(pygame.font.get_fonts()[69], 75)
        COUNTERTEXTSurfaceObj = COUNTERTEXT.render(str(N), True, WHITE, DARKGREY)
        COUNTERTEXTRectObj = pygame.draw.rect(window, DARKGREY, (450, 245, 100, 100))
        COUNTERTEXTRectObj2 = COUNTERTEXTSurfaceObj.get_rect()
        COUNTERTEXTRectObj.center = (500, 295)
        COUNTERTEXTRectObj2.center = (498, 293)
        window.blit(COUNTERTEXTSurfaceObj, COUNTERTEXTRectObj2)

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
                    if N == 13:
                        N = 13
                    else:
                        N += 1
                # If the user hits the begin button, play the game
                if begin.collidepoint(pygame.mouse.get_pos()):
                    game(N)

        pygame.display.update()


def main():
    intro()


if __name__ == "__main__":
    main()
