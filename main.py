from Computer import Computer
from Human import Human
from Player import Player

import tkinter as tk

import pygame
import pygame_menu
import time
import colors
import Connect4 as cFour


def load_screen():
    """
    This initializes the window for pygame to use
    """
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Connect4")
    return screen

def get_players():
    """
    Creates a tkinter object that gets players names
    """
    root = tk.Tk()
    root.title("Names")

    tk.Label(root, text="Player One", fg="blue").grid(row=0)
    tk.Label(root, text="Player Two", fg="red").grid(row=1)

    p1 = tk.Entry(root, font=(None, 15))
    p2 = tk.Entry(root, font=(None, 15))

    p1.grid(row=0, column=1)
    p2.grid(row=1, column=1)

    tk.Button(root, text='Play!', command= lambda: play_game(p1.get(),p2.get(), root) ).grid(row=10, column=1, sticky=tk.W)
    tk.mainloop()
    
def play_game(p1Name, p2Name, root):
    """
    Calling the connect4 object that enables 1v1 play
    """
    root.destroy()
    game = cFour.Connect4(Human(p1Name.strip()), Human(p2Name.strip())).play()
    
# def playAI(colorChoice, userName, master):
#     """
#     Calling the connect4 object that enables 1vAI play: 
#     """
#     master.destroy()

#     if colorChoice == "BLUE(Player 1)":
#         cFour.Connect4(userName, "Ed", True).playAi()
#     else:
#         cFour.Connect4("Ed", userName, True).playAi()

# def displayAIPanel():
#     """
#     Creating the panel to allow the user to select a color and go against the AI
#     """
#     master = tk.Tk()

#     colorChoice= tk.StringVar(master)
#     colorChoice.set("Color to play as")

#     tk.OptionMenu(master, colorChoice, "BLUE(Player 1)", "RED(Player 2)").grid()

#     tk.Label(text="Name").grid(row=3)
#     p1 = tk.Entry(master, font=(None, 15))
#     p1.grid(row=3, column=1)

#     tk.Button(master, text="PLAY COMPUTER!!!!", command=lambda: playAI(colorChoice.get(), p1.get(), master)).grid(row=4, column=1)
    
#     tk.mainloop()

if __name__ == "__main__":

    pygame.init()
    screen = load_screen()

    theme = pygame_menu.themes.Theme(
        title_font_shadow=True,
        widget_padding=25,
        title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE,
        widget_font=pygame_menu.font.FONT_FRANCHISE,
        title_background_color = (255, 255, 0),
        title_font_color = (0, 0, 255),
        title_font_shadow_color = (255, 0, 0),
        title_font_size = 80,
        background_color = (135,206,250),
        widget_font_color = (0, 0, 255),
        widget_font_size = 80
    )

    menu = pygame_menu.Menu('Connect4',600, 600, theme=theme)
                        
    menu.add.button('Human v Human', get_players, selection_color=(255, 255, 0))
    # menu.add.button('Human v AI', get_users, selection_color=(255,0,0))
    menu.add.button('Quit', pygame_menu.events.EXIT, selection_color=(128,128,128))
    menu.mainloop(screen)
