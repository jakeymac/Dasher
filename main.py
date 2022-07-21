import pygame
import pygame_menu
import game_window

class Main_Menu():
    def __init__(self):
        self.set_color_choice((255,0,0))

    def open_menu(self):

        self.main_surface = pygame.display.set_mode((500,500))
        

        self.menu = pygame_menu.Menu("Welcome to Dasher",500,500,theme=pygame_menu.themes.THEME_GREEN)
        
        self.menu.add.button("Play",self.start_game)
        self.menu.add.button("Instructions",self.show_information)
        self.menu.add.button("Options",self.open_options)
        self.menu.add.button("Exit",pygame_menu.events.EXIT)

        self.menu.mainloop(self.main_surface)
        
    def start_game(self):
        new_game = game_window.Game_Window((self.color_choice))
        self.open_menu()

    def show_information(self):
        self.information_surface = pygame.display.set_mode((500,500))
        self.information_menu = pygame_menu.Menu("Information",500,500,onclose=self.open_menu)
        self.information_menu.add.label("""Welcome to Dasher!\nYour objective is to make \nit as far as you can\nwithout hitting any obstacles! \nUse the up arrow key to jump!\nGood luck!""")
        self.information_menu.add.button("Exit",self.open_menu)
        self.information_menu.mainloop(self.information_surface)
        
    def open_options(self):
        self.option_surface = pygame.display.set_mode((500,500))
        self.option_menu = pygame_menu.Menu("Options",500,500,onclose=self.open_menu)
        
        self.option_menu.add.label("Welcome to the options menu")
        self.option_menu.add.label("Select your player's color below:")
        self.option_menu.add.button("Green",lambda:self.set_color_choice((0,125,0)))
        self.option_menu.add.button("Red",lambda:self.set_color_choice((255,0,0)))
        self.option_menu.add.button("Blue",lambda:self.set_color_choice((0,0,255)))
        self.option_menu.add.button("Orange",lambda:self.set_color_choice((255,125,0)))
        self.option_menu.add.button("Exit",self.open_menu)
        self.option_menu.mainloop(self.option_surface)

    def set_color_choice(self,color_choice):
        self.color_choice = color_choice

#pygame.init()
main = Main_Menu()
main.open_menu()