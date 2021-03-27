from Player import Player

import tkinter as tk
import pygame
import pygame_menu
import time
import colors
import Connect4 as cFour
import Minimax as mx


def text_format(option, textSize, textColor):
    """
    Creates a text object to show in the main menu
    """
    newFont = pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, textSize)
    newText = newFont.render(option, 0, textColor)
    return newText

def load_screen():
    """
    This initializes the window for pygame to use
    """
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Connect4")
    return screen

def get_player_details(screen):
    """
    Creates a tkinter object(button) that gets players names
    """
    root = tk.Tk()
    root.title("Player Names!")

    tk.Label(root, text="Player One", fg="blue").grid(row=0)
    tk.Label(root, text="Player Two", fg="red").grid(row=1)

    p1 = tk.Entry(root, font=(None, 15))
    p2 = tk.Entry(root, font=(None, 15))

    p1.grid(row=0, column=1)
    p2.grid(row=1, column=1)

    tk.Button(root, text='Play!', command= lambda: play_game(p1.get(),p2.get(), root, screen)).grid(row=10, column=1, sticky=tk.W)
    tk.mainloop()
    
def get_player_ai_details(screen):
    """
    Creating the panel to allow the user to select a color and go against the AI
    """
    options = ["Player 1", "Player 2"]
    root = tk.Tk()
    root.title("Player 1(Blue) or 2(Red)?")

    colorChoice= tk.StringVar(root)
    colorChoice.set(options[0])

    tk.OptionMenu(root, colorChoice, *options).grid(row=3)

    p1 = tk.Entry(root, font=(None, 15))
    p1.grid(row=3, column=1)

    tk.Button(root, text="Play Computer!", command=lambda: play_computer(colorChoice.get(), p1.get(), root, screen)).grid(row=10, column=1)
    
    tk.mainloop()

def play_computer(colorChoice, playerName, root, screen):
    """
    Connect4 play function (human v computer)
    """
    root.destroy()

    if colorChoice == "Player 1":
        mx.Minimax(Player(playerName), Player("Ed"), screen).play_computer()
    else:
        mx.Minimax(Player("Ed"), Player(playerName), screen).play_computer()
    
def play_game(p1Name, p2Name, root, screen):
    """
    Connect4 play function (human v human)
    """
    root.destroy()
    game = cFour.Connect4(Player(p1Name.strip()), Player(p2Name.strip()), screen).play()

if __name__ == "__main__":
    pygame.init()
    screen = load_screen()

    features = [
        ("Player Vs Player", colors.yellow),
        ("Player Vs AI", colors.red),
        ("Quit", colors.gray)
    ]

    iterator = 0
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            #This if block makes it where the user doesnt have to click arrow key up/down if they have exhausted the possible options, it will loop you throughout options
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    iterator += 1
                    if iterator == len(features):
                        iterator = 0

                if event.key == pygame.K_UP:
                    iterator -= 1
                    if iterator < 0:
                        iterator = len(features) - 1

                if event.key == pygame.K_RETURN:
                    if selected == "Player Vs Player":
                        get_player_details(screen)
                    if selected == "Player Vs AI":
                        get_player_ai_details(screen)
                    if selected == "Quit":
                        pygame.quit()
                        quit()
            selected = features[iterator][0]
                
        screen.fill(colors.blue)
        screen_rect = screen.get_rect()
        for i in range(0, len(features)):
            counter = -50 + (i * 90) # Equation that sets distance between each choice in main menu
            if i == iterator:
                text = text_format(features[i][0], 80, features[i][1])
            else:
                text = text_format(features[i][0], 80, colors.black)
            player_rect = text.get_rect(center=screen_rect.center)
            player_rect[1] = player_rect[1] + counter
            screen.blit(text, player_rect)    
        pygame.display.update()
