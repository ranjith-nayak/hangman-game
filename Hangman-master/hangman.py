#########################################################
## File Name: hangman.py                               ##
## Description: Starter for Hangman project - ICS3U    ##
#########################################################
import pygame
import random


pygame.init()
winHeight = 700
winWidth = 1500

win = pygame.display.set_mode((winWidth, winHeight))

# Load and play background music
#pygame.mixer.music.load('full1.mp3')
#pygame.mixer.music.play(-1)  # Loop the music indefinitely

# Load sound effects
click_sound = pygame.mixer.Sound('click.mp3')
win_sound = pygame.mixer.Sound('win1.mp3')
lose_sound = pygame.mixer.Sound('lose.mp3')

#---------------------------------------#
# initialize global variables/constants #
#---------------------------------------#
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (102, 255, 255)
GRAY = (238, 238, 238)
CGRAY= (147, 168, 172)

btn_font = pygame.font.SysFont("Noto Serif", 30)
guess_font = pygame.font.SysFont("Bona Nova SC", 50)
lost_font = pygame.font.SysFont('Ga Maamli', 65)
word = ''
hint = ''
buttons = []
guessed = []
hangmanPics = [pygame.image.load('hangman0.png'), pygame.image.load('hangman1.png'), pygame.image.load('hangman2.png'), pygame.image.load('hangman3.png'), pygame.image.load('hangman4.png'), pygame.image.load('hangman5.png'), pygame.image.load('hangman6.png')]

limbs = 0


def redraw_game_window():
    global guessed
    global hangmanPics
    global limbs
    global hint
    
    win.fill(CGRAY)
    
    # Draw Buttons with hover effect
    mouse_pos = pygame.mouse.get_pos()
    for i in range(len(buttons)):
        if buttons[i][4]:
            color = LIGHT_BLUE if (buttons[i][1] - 20 < mouse_pos[0] < buttons[i][1] + 20 and
                                   buttons[i][2] - 20 < mouse_pos[1] < buttons[i][2] + 20) else buttons[i][0]
            pygame.draw.circle(win, BLACK, (buttons[i][1], buttons[i][2]), buttons[i][3])
            pygame.draw.circle(win, color, (buttons[i][1], buttons[i][2]), buttons[i][3] - 2)
            label = btn_font.render(chr(buttons[i][5]), 1, BLACK)
            win.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))

    spaced = spacedOut(word, guessed)
    label1 = guess_font.render(spaced, 1, BLACK)
    rect = label1.get_rect()
    length = rect[2]
    
    win.blit(label1, (winWidth/2 - length/2, 400))

    pic = hangmanPics[limbs]
    win.blit(pic, (winWidth/2 - pic.get_width()/2 + 20, 150))
    
    # Display the hint
    display_hint(hint)
    
    pygame.display.update()


def randomWord():
    file = open('words.txt')
    f = file.readlines()
    i = random.randrange(0, len(f) - 1)
    word, hint = f[i].strip().split(',')
    return word, hint


def display_hint(hint):
    hint_label = guess_font.render('Hint: ' + hint, 1, BLACK)
    win.blit(hint_label, (winWidth / 2 - hint_label.get_width() / 2, 500))


def hang(guess):
    global word
    if guess.lower() not in word.lower():
        return True
    else:
        return False


def spacedOut(word, guessed=[]):
    spacedWord = ''
    guessedLetters = guessed
    for x in range(len(word)):
        if word[x] != ' ':
            spacedWord += '_ '
            for i in range(len(guessedLetters)):
                if word[x].upper() == guessedLetters[i]:
                    spacedWord = spacedWord[:-2]
                    spacedWord += word[x].upper() + ' '
        elif word[x] == ' ':
            spacedWord += ' '
    return spacedWord
            

def buttonHit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]
    return None


def end(winner=False):
    global limbs
    lostTxt = 'YOU LOST, press any key to play again...'
    winTxt = 'WINNER!, press any key to play again...'
    redraw_game_window()
    pygame.time.delay(1000)
    win.fill(GRAY)

    if winner:
        pygame.mixer.Sound.play(win_sound)
        label = lost_font.render(winTxt, 1, BLACK)
    else:
        pygame.mixer.Sound.play(lose_sound)
        label = lost_font.render(lostTxt, 1, BLACK)

    wordTxt = lost_font.render(word.upper(), 1, BLACK)
    wordWas = lost_font.render('The phrase was: ', 1, BLACK)

    win.blit(wordTxt, (winWidth/2 - wordTxt.get_width()/2, 295))
    win.blit(wordWas, (winWidth/2 - wordWas.get_width()/2, 245))
    win.blit(label, (winWidth / 2 - label.get_width() / 2, 140))
    pygame.display.update()
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                again = False
    reset()


def reset():
    global limbs
    global guessed
    global buttons
    global word
    global hint
    for i in range(len(buttons)):
        buttons[i][4] = True

    limbs = 0
    guessed = []
    word, hint = randomWord()

#MAINLINE


# Setup buttons
increase = round(winWidth / 13)
for i in range(26):
    if i < 13:
        y = 40
        x = 25 + (increase * i)
    else:
        x = 25 + (increase * (i - 13))
        y = 85
    buttons.append([GRAY, x, y, 20, True, 65 + i])
    # buttons.append([color, x_pos, y_pos, radius, visible, char])

word, hint = randomWord()
inPlay = True

while inPlay:
    redraw_game_window()
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inPlay = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()
            letter = buttonHit(clickPos[0], clickPos[1])
            if letter is not None:
                pygame.mixer.Sound.play(click_sound)
                guessed.append(chr(letter))
                buttons[letter - 65][4] = False
                if hang(chr(letter)):
                    if limbs != 6:
                        limbs += 1
                    else:
                        end()
                else:
                    print(spacedOut(word, guessed))
                    if spacedOut(word, guessed).count('_') == 0:
                        end(True)

pygame.quit()
