import tkinter as tk
p1_amount = 18000
p1_networth = p1_amount
p2_amount = 18000
p2_networth = p2_amount
counter = 0
player_1_turn = True


# creating welcome screen
window = tk.Tk()
frame1 = tk.Frame(width=50, height=25, bg="yellow")
frame1.pack(fill=tk.BOTH)

# creating welcome text
label_greeting = tk.Label(text="Welcome to Warriors Monopoly!",
                          bg="black",
                          fg="yellow",
                          width=25,
                          height=10)
label_greeting.pack(fill=tk.BOTH, expand=True)

# creating instructions for entering name of p1
label_name_p1 = tk.Label(text="Enter Player 1 Name: ")
label_name_p1.pack(fill=tk.BOTH)
# creating textbox to enter name
box_for_p1 = tk.Entry()
box_for_p1.pack()

# creating instructions for entering name of p2
label_name_p2 = tk.Label(text="Enter Player 2 Name: ")
label_name_p2.pack()
# creating textbox to enter name
box_for_p2 = tk.Entry()
box_for_p2.pack()


# when players press start_game button game_window_init is run
def game_window_init():
    global p2_amount, player_1_turn
    global p1_amount
    global p1_networth
    global p2_networth
    global counter
    import pygame
    import random

    pygame.init()
    screen_width = 1300
    screen_height = 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    screen.fill((0, 0, 0))
    is_running = True
    # IMPORTANT INFO: THE GAP BETWEEN ANY CORRESPONDING BETWEEN 2 TILES IS 92
    # storing fonts (p1 and p2 text font, amount font, Waterloo Monopoly font, and button fonts)
    p1_font = pygame.font.SysFont("Times New Roman", 30)
    p2_font = pygame.font.SysFont("Times New Roman", 30)
    amount_p1_font = pygame.font.SysFont("Times New Roman", 30)
    amount_p2_font = pygame.font.SysFont("Times New Roman", 30)
    waterloo_mono_font = pygame.font.SysFont("Times New Roman", 50)
    a_button_font = pygame.font.SysFont("Times New Roman", 20)

    # storing images (Monopoly board and sample money)
    moola = pygame.image.load("stackofmoney.jpg").convert()
    sketchup_board = pygame.image.load("Monopolyboard.jpg").convert()
    rev_virtual_rect = pygame.Rect(485, 577, 92, 92)

    # functions to displays text/image
    def blit_text(text, font, text_colour, x, y):
        screen.blit((font.render(text, True, text_colour)), (x, y))

    def blit_image(image, width, height, x, y):
        image = pygame.transform.scale(image, (width, height))
        screen.blit(image, (x, y))

    # move_p1(x, y, n, amt, networth) takes in the x and y coordinates, the dice number, the amount and networth of
    # player 1, changes the x and y coordinates based on the dice and returns a list of each of those parameters in order.
    # if player has passed go, amount and networth get incremented by 2000
    # move_p1: int int int int int -> [int, int, int, int, int]
    # requires: n <= 6
    def move_p1(x, y, n, amt, networth):
        if n == 0:
            return [x, y, amt, networth]
        # corners
        elif x == 600 and y == 630:
            return move_p1(x - 92, y, n - 1, amt + 2000, networth + 2000)
        elif x == 48 and y == 630:
            return move_p1(x, y - 92, n - 1, amt, networth)
        elif x == 48 and y == 78:
            return move_p1(x + 92, y, n - 1, amt, networth)
        elif x == 600 and y == 78:
            return move_p1(x, y + 92, n - 1, amt, networth)
        # determining which row/columns
        elif 140 <= x <= 508 and y == 630:
            return move_p1(x - 92, y, n - 1, amt, networth)
        elif x == 48 and 170 <= y <= 538:
            return move_p1(x, y - 92, n - 1, amt, networth)
        elif 140 <= x <= 508 and y == 78:
            return move_p1(x + 92, y, n - 1, amt, networth)
        elif x == 600 and 170 <= y <= 578:
            return move_p1(x, y + 92, n - 1, amt, networth)

    # movement for p2 (same as p1)
    def move_p2(x, y, n, amt, networth):
        if n == 0:
            return [x, y, amt, networth]
        # corners
        elif x == 640 and y == 630:
            return move_p2(x - 92, y, n - 1, amt + 2000, networth + 2000)
        elif x == 88 and y == 630:
            return move_p2(x, y - 92, n - 1, amt, networth)
        elif x == 88 and y == 78:
            return move_p2(x + 92, y, n - 1, amt, networth)
        elif x == 640 and y == 78:
            return move_p2(x, y + 92, n - 1, amt, networth)
        # determining which row/columns
        elif 180 <= x <= 548 and y == 630:
            return move_p2(x - 92, y, n - 1, amt, networth)
        elif x == 88 and 170 <= y <= 538:
            return move_p2(x, y - 92, n - 1, amt, networth)
        elif 180 <= x <= 548 and y == 78:
            return move_p2(x + 92, y, n - 1, amt, networth)
        elif x == 640 and 170 <= y <= 578:
            return move_p2(x, y + 92, n - 1, amt, networth)

    # is_member(lst_of_lst, property_name) takes in a list of property name-price pairs, as well as a property name
    # and returns true if the property name is present in the list, and false otherwise
    # is_member: list of [string, int], string -> Bool
    def is_member(lst_of_lst, property_name):
        if len(lst_of_lst) == 0:
            return False
        elif property_name == lst_of_lst[0][0]:
            return True
        else:
            return is_member(lst_of_lst[1: len(lst_of_lst) + 1], property_name)

    # defining class for a button
    class Button:
        def __init__(self, surface, rect_colour, x, y, width, height, text_to_display, font, text_colour, border_colour, border_rect):
            self.surface = surface  # initialising button surface (usually screen)
            self.rect_colour = rect_colour  # initialising the rectangle colour for the button (inner rectangle)
            self.x = x  # x coordinate of the top left of the inner rectangle
            self.y = y  # y coordinate of the top left of the inner rectangle
            self.width = width  # width of the inner rectangle
            self.height = height  # height of the inner rectangle
            self.text_to_display = text_to_display  # a string displaying text on the button
            self.font = font  # button font (the sys_font stuff)
            self.text_colour = text_colour  # text colour, which is passed as a string
            self.border_colour = border_colour  # the outer border colour, passed as a string
            self.border_rect = border_rect  # the (x, y, width, height) of the border
            border_drawn = pygame.draw.rect(self.surface, self.border_colour, border_rect)  # drawing the rectangle border
            button_drawn = pygame.draw.rect(self.surface, self.rect_colour, (self.x, self.y, self.width, self.height))  # drawing the button rect
            blit_text(self.text_to_display, self.font, self.text_colour, self.x, self.y)  # displaying button text

        # returns the virtual rectangle used to identify mouse clicks (makes it so the button is clickable)
        def return_virtual_rect(self):
            return pygame.Rect(self.x, self.y, self.width, self.height)

    # updating the display with everything above before game-board is displayed
    pygame.display.update()

    # displaying buttons/text and storing/initializing variables
    blit_image(sketchup_board, 644, 644, 25, 25)

    # initialising variables for player coordinates, amount and networth
    p1_x = 600
    p1_y = 630
    p2_x = 640
    p2_y = 630

    # making player tokens drawn as circles on the board
    p1_token = pygame.draw.circle(screen, "red", (p1_x, p1_y), 10)
    p2_token = pygame.draw.circle(screen, "blue", (p2_x, p2_y), 10)

    # blitting all the text on the board and outside of it
    blit_text("Player 1: " + box_for_p1.get(), p1_font, "Red", 900, 50)
    blit_text("Player 2: " + box_for_p2.get(), p2_font, "Blue", 900, 550)
    blit_text("Amount: ", amount_p1_font, "Red", 800, 100)
    blit_text("Amount: ", amount_p2_font, "Blue", 800, 600)
    blit_text("Net worth: ", amount_p1_font, "Red", 1005, 100)
    blit_text("Net worth: ", amount_p2_font, "Blue", 1005, 600)
    blit_text("Waterloo Monopoly!", waterloo_mono_font, (255, 215, 0), 150, 325)

    # making buttons on the board for buying, renting and rolling dice
    roll_dice_button = Button(screen, "red", 200, 200, 85, 25, "Roll Dice!", a_button_font, "yellow", "white", (195, 195, 95, 35))
    roll_dice_button_2 = Button(screen, "red", 400, 200, 85, 25, "2 Roll Dice!", a_button_font, "yellow", "white", (395, 195, 95, 35))
    hide_info_button = Button(screen, "red", 200, 150, 85, 25, "Hide info", a_button_font, "yellow", "white", (195, 145, 95, 35))
    buy_button = Button(screen, "red", 200, 250, 85, 25, "Buy now!", a_button_font, "yellow", "white", (195, 245, 95, 35))
    dont_buy_button = Button(screen, "red", 400, 250, 85, 25, "Don't Buy", a_button_font, "yellow", "white", (395, 245, 95, 35))
    pay_rent_button = Button(screen, "red", 400, 150, 85, 25, "Pay Rent", a_button_font, "yellow", "white", (395, 145, 95, 35))

    # blitting text for the amounts and net_worth(s) outside the board
    blit_text(str(p1_amount), amount_p1_font, "Red", 910, 100)
    blit_text(str(p2_amount), amount_p2_font, "Blue", 910, 600)
    blit_text(str(p1_networth), amount_p1_font, "Red", 1140, 100)
    blit_text(str(p2_networth), amount_p2_font, "Blue", 1140, 600)

    # initializing lists of properties owned and unowned
    properties_unowned = [["REV", 1000], ["MKV", 1200], ["M3", 2000], ["MC", 2200], ["Mudie's", 3000], ["V1", 3200],
                          ["UWP", 4000], ["CMH", 4200], ["DC Bytes", 5000], ["DC", 5200], ["PAC", 6000], ["SLC", 6200],
                          ["STC", 7000], ["DP", 7200], ["Tim Hortons", 8000], ["QNC", 8200]]
    p1_owned = []
    p2_owned = []

    # initializing variables to control the flow of the game (whose turn it is/endgame status)

    endgame = 0

    # function to do after a player lands on property and wants to buy
    def player1_turn(property_name, property_price, indicator_rect):
        global p1_amount
        global p1_networth
        global p2_amount
        global p2_networth
        global counter

        # if the property is unowned and the player wants to buy the property
        if is_member(properties_unowned, property_name) and event.type == pygame.MOUSEBUTTONDOWN and buy_button.return_virtual_rect().collidepoint(event.pos):
            pygame.draw.rect(screen, "red", indicator_rect)  # indicator gets blit onto board
            p1_owned.append([property_name, property_price])  # adds the property to the list of p1 owned properties
            # drawing rect over old amount
            pygame.draw.rect(screen, (0, 0, 0), (910, 100, 90, 50))
            # drawing new amount (with the deducted price)
            blit_text(str(p1_amount - property_price), amount_p1_font, "red", 910, 100)
            p1_amount -= property_price
            pygame.draw.rect(screen, 'black', (1140, 100, 90, 50))  # drawing the black rect over the old networth
            blit_text(str(p1_networth), p1_font, 'red', 1140, 100)
            # blit_text(str(p2_networth), p2_font, 'blue', 1140, 600)
            properties_unowned.remove([property_name, property_price])
            counter = 2

        elif is_member(properties_unowned,
                       property_name) and event.type == pygame.MOUSEBUTTONDOWN and dont_buy_button.return_virtual_rect().collidepoint(
                event.pos):
            counter = 2
        elif is_member(p1_owned, property_name):
            counter = 2
        elif is_member(p2_owned,
                       property_name) and event.type == pygame.MOUSEBUTTONDOWN and pay_rent_button.return_virtual_rect().collidepoint(
                event.pos):
            # drawing rect over old p1 amount and blitting the new p1 amounts and net_worth
            pygame.draw.rect(screen, 'black', (910, 100, 90, 50))
            blit_text(str(int(p1_amount - (property_price / 2))), amount_p1_font, 'red', 910, 100)
            pygame.draw.rect(screen, 'black', (1140, 100, 90, 50))
            blit_text(str(int(p1_networth - (property_price / 2))), p1_font, 'red', 1140, 100)

            # drawing rect over old p2 amount and blitting the new p1 amounts and net_worth
            pygame.draw.rect(screen, 'black', (910, 600, 90, 50))
            blit_text(str(int(p2_amount + (property_price / 2))), amount_p2_font, 'blue', 910, 600)
            pygame.draw.rect(screen, 'black', (1140, 600, 90, 50))
            blit_text(str(int(p2_networth + (property_price / 2))), p2_font, 'blue', 1140, 600)

            # changing values of things
            p1_amount = int(p1_amount - (property_price / 2))
            p1_networth = int(p1_networth - (property_price / 2))
            p2_amount = int(p2_amount + (property_price / 2))
            p2_networth = int(p2_networth + (property_price / 2))
            counter = 2

    def player2_turn(property_name, property_price, indicator_rect):
        global p1_amount
        global p1_networth
        global p2_amount
        global p2_networth
        global counter

        # if the property is unowned and the player wants to buy the property
        if is_member(properties_unowned, property_name) and event.type == pygame.MOUSEBUTTONDOWN and buy_button.return_virtual_rect().collidepoint(event.pos):
            pygame.draw.rect(screen, "blue", indicator_rect)  # indicator gets blit onto board
            p2_owned.append([property_name, property_price])  # adds the property to the list of p1 owned properties
            # drawing rect over old amount
            pygame.draw.rect(screen, (0, 0, 0), (910, 600, 90, 50))
            # drawing new amount (with the deducted price)

            blit_text(str(p2_amount - property_price), amount_p2_font, "blue", 910, 600)
            p2_amount -= property_price
            pygame.draw.rect(screen, 'black', (1140, 600, 90, 50))  # drawing the black rect over the old networth
            blit_text(str(p1_networth), p1_font, 'red', 1140, 100)
            blit_text(str(p2_networth), p2_font, 'blue', 1140, 600)
            properties_unowned.remove([property_name, property_price])
            counter = 1

        elif is_member(properties_unowned,
                       property_name) and event.type == pygame.MOUSEBUTTONDOWN and dont_buy_button.return_virtual_rect().collidepoint(event.pos):
            counter = 1
        elif is_member(p2_owned, property_name):
            counter = 1
        elif is_member(p1_owned,
                       property_name) and event.type == pygame.MOUSEBUTTONDOWN and pay_rent_button.return_virtual_rect().collidepoint(event.pos):
            # drawing rect over old p1 amount and blitting the new p1 amounts and net_worth
            pygame.draw.rect(screen, 'black', (910, 100, 90, 50))
            blit_text(str(int(p1_amount + (property_price / 2))), amount_p1_font, 'red', 910, 100)
            pygame.draw.rect(screen, 'black', (1140, 100, 90, 50))
            blit_text(str(int(p1_networth + (property_price / 2))), p1_font, 'red', 1140, 100)

            # drawing rect over old p2 amount and blitting the new p1 amounts and net_worth
            pygame.draw.rect(screen, 'black', (910, 600, 90, 50))
            blit_text(str(int(p2_amount - (property_price / 2))), amount_p2_font, 'blue', 910, 600)
            pygame.draw.rect(screen, 'black', (1140, 600, 90, 50))
            blit_text(str(int(p2_networth - (property_price / 2))), p2_font, 'blue', 1140, 600)

            # changing values of things
            p1_amount += int(property_price / 2)
            p1_networth += int(property_price / 2)
            p2_amount -= int(property_price / 2)
            p2_networth -= int(property_price / 2)
            counter = 1

    # below code is executed while win conditions have not been met
    while is_running:
        for event in pygame.event.get():
            # checks if user closes window
            if event.type == pygame.QUIT:
                is_running = False

            # win conditions
            if p1_amount <= 0:
                blit_text("player 2 won", p1_font, "Blue", 1000, 300)
                endgame = 1
            if p2_amount <= 0:
                blit_text("player 1 won", p1_font, "Red", 1000, 300)
                endgame = 1

            if len(properties_unowned) == 0:
                if p1_networth > p2_networth:
                    blit_text("Player 1 won!", p1_font, "Red", 1000, 300)
                    endgame = 1
                elif p1_networth < p2_networth:
                    blit_text("Player 2 won!", p1_font, "Blue", 1000, 300)
                    endgame = 1
                else:
                    blit_text("Players tied!", p1_font, "Yellow", 1000, 300)
                    endgame = 1

            # when win conditions have not been met
            if endgame == 0:
                # if player 1 rolls
                if event.type == pygame.MOUSEBUTTONDOWN and roll_dice_button.return_virtual_rect().collidepoint(event.pos) and player_1_turn:
                    number_rolled = (random.randrange(1, 7))
                    blit_text(("Player 1 rolled: " + str(number_rolled) + "!"), p1_font, "Red", 200, 500)
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    pygame.draw.rect(screen, (0, 0, 0), (400, 400, 200, 50))
                    list_p1_cords = move_p1(p1_x, p1_y, number_rolled, p1_amount, p1_networth)
                    p1_x = list_p1_cords[0]
                    p1_y = list_p1_cords[1]
                    p1_amount = list_p1_cords[2]
                    p1_networth = list_p1_cords[3]

                    # after movement immediately re-blit board/buttons
                    blit_image(sketchup_board, 644, 644, 25, 25)
                    blit_text("Waterloo Monopoly!", waterloo_mono_font, (255, 215, 0), 150, 325)
                    roll_dice_button = Button(screen, "red", 200, 200, 85, 25, "Roll Dice!", a_button_font, "yellow", "white", (195, 195, 95, 35))
                    roll_dice_button_2 = Button(screen, "red", 400, 200, 85, 25, "2 Roll Dice!", a_button_font, "yellow", "white", (395, 195, 95, 35))
                    hide_info_button = Button(screen, "red", 200, 150, 85, 25, "Hide info", a_button_font, "yellow", "white", (195, 145, 95, 35))
                    buy_button = Button(screen, "red", 200, 250, 85, 25, "Buy now!", a_button_font, "yellow", "white", (195, 245, 95, 35))
                    dont_buy_button = Button(screen, "red", 400, 250, 85, 25, "Don't Buy", a_button_font, "yellow", "white", (395, 245, 95, 35))
                    pay_rent_button = Button(screen, "red", 400, 150, 85, 25, "Pay Rent", a_button_font, "yellow", "white", (395, 145, 95, 35))
                    pygame.draw.rect(screen, "black", (910, 100, 80, 40))
                    blit_text(str(p1_amount), amount_p1_font, "red", 910, 100)
                    pygame.draw.rect(screen, 'black', (1140, 100, 90, 50))
                    blit_text(str(p1_networth), p1_font, 'red', 1140, 100)
                    blit_text(str(p2_networth), p2_font, 'blue', 1140, 600)
                    p1_token = pygame.draw.circle(screen, "red", (p1_x, p1_y), 10)
                    p2_token = pygame.draw.circle(screen, "blue", (p2_x, p2_y), 10)
                    counter = 1
                    player_1_turn = False

                # if player 2 rolls
                elif event.type == pygame.MOUSEBUTTONDOWN and roll_dice_button_2.return_virtual_rect().collidepoint(event.pos) and not player_1_turn:
                    number_rolled = (random.randrange(1, 7))
                    blit_text(("Player 2 rolled: " + str(number_rolled) + "!"), p2_font, "Blue", 200, 500)
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    pygame.draw.rect(screen, (0, 0, 0), (400, 400, 200, 50))
                    list_p2_cords = move_p2(p2_x, p2_y, number_rolled, p2_amount, p2_networth)
                    p2_x = list_p2_cords[0]
                    p2_y = list_p2_cords[1]
                    p2_amount = list_p2_cords[2]
                    p2_networth = list_p2_cords[3]

                    # after movement immediately re-blit the board and buttons
                    blit_image(sketchup_board, 644, 644, 25, 25)
                    blit_text("Waterloo Monopoly!", waterloo_mono_font, (255, 215, 0), 150, 325)
                    roll_dice_button = Button(screen, "red", 200, 200, 85, 25, "Roll Dice!", a_button_font, "yellow", "white", (195, 195, 95, 35))
                    roll_dice_button_2 = Button(screen, "red", 400, 200, 85, 25, "2 Roll Dice!", a_button_font, "yellow", "white", (395, 195, 95, 35))
                    hide_info_button = Button(screen, "red", 200, 150, 85, 25, "Hide info", a_button_font, "yellow", "white", (195, 145, 95, 35))
                    buy_button = Button(screen, "red", 200, 250, 85, 25, "Buy now!", a_button_font, "yellow", "white", (195, 245, 95, 35))
                    dont_buy_button = Button(screen, "red", 400, 250, 85, 25, "Don't Buy", a_button_font, "yellow", "white", (395, 245, 95, 35))
                    pay_rent_button = Button(screen, "red", 400, 150, 85, 25, "Pay Rent", a_button_font, "yellow", "white", (395, 145, 95, 35))
                    pygame.draw.rect(screen, "black", (910, 600, 80, 40))
                    blit_text(str(p2_amount), amount_p2_font, "blue", 910, 600)
                    pygame.draw.rect(screen, 'black', (1140, 600, 90, 50))
                    blit_text(str(p2_networth), p2_font, 'blue', 1140, 600)
                    blit_text(str(p1_networth), p1_font, 'red', 1140, 100)
                    p1_token = pygame.draw.circle(screen, "red", (p1_x, p1_y), 10)
                    p2_token = pygame.draw.circle(screen, "blue", (p2_x, p2_y), 10)
                    counter = 2
                    player_1_turn = True

                if counter == 1:

                    # p1 lands on REV
                    if p1_x == 508 and p1_y == 630:
                        player1_turn("REV", 1000, (485, 669, 90, 10))

                    # p1 lands on MKV
                    if p1_x == 416 and p1_y == 630:
                        player1_turn("MKV", 1200, (393, 669, 92, 10))

                    # p1 lands on M3
                    if p1_x == 232 and p1_y == 630:
                        player1_turn("M3", 2000, (209, 669, 92, 10))

                    # p1 lands on MC
                    if p1_x == 140 and p1_y == 630:
                        player1_turn("MC", 2200, (117, 669, 92, 10))

                    # p1 lands on Mudie's
                    if p1_x == 48 and p1_y == 538:
                        player1_turn("Mudie's", 3000, (15, 485, 10, 92))

                    # if p1 lands on V1
                    if p1_x == 48 and p1_y == 446:
                        player1_turn("V1", 3200, (15, 393, 10, 92))

                    # if p1 lands on UWP
                    if p1_x == 48 and p1_y == 262:
                        player1_turn("UWP", 4000, (15, 209, 10, 92))

                    # if p1 lands on CMH
                    if p1_x == 48 and p1_y == 170:
                        player1_turn("CMH", 4200, (15, 117, 10, 92))

                    # if p1 lands on DC Bytes
                    if p1_x == 140 and p1_y == 78:
                        player1_turn("DC Bytes", 5000, (117, 15, 92, 10))

                    # if p1 lands on DC
                    if p1_x == 232 and p1_y == 78:
                        player1_turn("DC", 5200, (209, 15, 92, 10))

                    # if p1 lands on PAC
                    if p1_x == 416 and p1_y == 78:
                        player1_turn("PAC", 6000, (393, 15, 92, 10))

                    # if p1 lands on SLC
                    if p1_x == 508 and p1_y == 78:
                        player1_turn("SLC", 6200, (485, 15, 92, 10))

                    # if p1 lands on STC
                    if p1_x == 600 and p1_y == 170:
                        player1_turn("STC", 7000, (669, 117, 10, 92))

                    # if p1 lands on DP
                    if p1_x == 600 and p1_y == 262:
                        player1_turn("DP", 7200, (669, 209, 10, 92))

                    # if p1 lands on Tim Hortons
                    if p1_x == 600 and p1_y == 446:
                        player1_turn("Tim Hortons", 8000, (669, 393, 10, 92))

                    # if p1 lands on QNC
                    if p1_x == 600 and p1_y == 538:
                        player1_turn("QNC", 8200, (669, 485, 10, 92))

                    # p1 lands on Ion rail
                    if p1_x == 48 and p1_y == 630:
                        counter = 2

                # if it is player 2s turn
                else:

                    # p2 lands on REV
                    if p2_x == 548 and p2_y == 630:
                        player2_turn("REV", 1000, (485, 669, 90, 10))

                    # p2 lands of MKV
                    if p2_x == 456 and p2_y == 630:
                        player2_turn("MKV", 1200, (393, 669, 92, 10))

                    # p2 lands on M3
                    if p2_x == 272 and p2_y == 630:
                        player2_turn("M3", 2000, (209, 669, 92, 10))

                    # p2 lands on MC
                    if p2_x == 180 and p2_y == 630:
                        player2_turn("MC", 2200, (117, 669, 92, 10))

                    # p2 lands on Mudie's
                    if p2_x == 88 and p2_y == 538:
                        player2_turn("Mudie's", 3000, (15, 485, 10, 92))

                    # p2 lands on V1
                    if p2_x == 88 and p2_y == 446:
                        player2_turn("V1", 3200, (15, 393, 10, 92))

                    # p2 lands on UWP
                    if p2_x == 88 and p2_y == 262:
                        player2_turn("UWP", 4000, (15, 209, 10, 92))

                    # p2 lands on CMH
                    if p2_x == 88 and p2_y == 170:
                        player2_turn("CMH", 4200, (15, 117, 10, 92))

                    # p2 lands on DC Bytes
                    if p2_x == 180 and p2_y == 78:
                        player2_turn("DC Bytes", 5000, (117, 15, 92, 10))

                    # p2 lands on DC
                    if p2_x == 272 and p2_y == 78:
                        player2_turn("DC", 5200, (209, 15, 92, 10))

                    # p2 lands on PAC
                    if p2_x == 456 and p2_y == 78:
                        player2_turn("PAC", 6000, (393, 15, 92, 10))

                    # p2 lands on SLC
                    if p2_x == 548 and p2_y == 78:
                        player2_turn("SLC", 6200, (485, 15, 92, 10))

                    # p2 lands on STC
                    if p2_x == 640 and p2_y == 170:
                        player2_turn("STC", 7000, (669, 117, 10, 92))

                    # p2 lands on DP
                    if p2_x == 640 and p2_y == 262:
                        player2_turn("DP", 7200, (669, 209, 10, 92))

                    # p2 lands on Tim hortons
                    if p2_x == 640 and p2_y == 446:
                        player2_turn("Tim Hortons", 8000, (669, 393, 10, 92))

                    # p2 lands on QNC
                    if p2_x == 640 and p2_y == 538:
                        player2_turn("QNC", 8200, (669, 485, 10, 92))

                # clicking the hide info button
                if event.type == pygame.MOUSEBUTTONDOWN and hide_info_button.return_virtual_rect().collidepoint(event.pos):
                    pygame.draw.rect(screen, (0, 0, 0), (735, 175, 500, 300))

                # displaying placeholder property card
                if event.type == pygame.MOUSEBUTTONDOWN and rev_virtual_rect.collidepoint(event.pos):
                    blit_image(moola, 500, 300, 735, 175)

            pygame.display.flip()

    pygame.quit()


# creating start game button
start_button = tk.Button(text="Start Game!",
                         fg="purple",
                         command=game_window_init)
start_button.pack()

window.mainloop()
