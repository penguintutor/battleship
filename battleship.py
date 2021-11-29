import pygame
import pgzrun
from fleet import Fleet
from grid import Grid
from playerai import PlayerAi
from playerhuman import PlayerHuman
from controller import Controller

# Default screen size - can be changed by config
WIDTH = 1280
HEIGHT  = 720
TITLE = "Battleships"

# Set SIZE_SML to True for small size (800 x 480)
SIZE_SML = True

# Set fullscreen
FULLSCREEN = False

GRID_SIZE = (38,38)

# suffix for image
img_txt = ""

# Track if fullscreen
fullscreen_status = False

player = "player1setup"

grid_img_1 = Actor ("grid", topleft=(50,150))
grid_img_2 = Actor ("grid", topleft=(500,150))

# Uses start of grid (after grid labels)
own_fleet = Fleet((94,179), GRID_SIZE)
enemy_fleet = Fleet((544,179), GRID_SIZE)

player1=PlayerHuman()
# Player 2 represents the AI player
player2=PlayerAi()

mouse_position = (0,0)         

key_position = (1000, 150)

your_fleet_txt_pos = (100,100)
enemy_fleet_txt_pos = (550,100)

# list of different ship types
ship_list = [
    Actor("carrier", topleft=(key_position[0], key_position[1]+70)),
    Actor("battleship", topleft=(key_position[0], key_position[1]+150)),
    Actor("submarine", topleft=(key_position[0], key_position[1]+230)),
    Actor("cruiser", topleft=(key_position[0], key_position[1]+310)),
    Actor("destroyer", topleft=(key_position[0], key_position[1]+390))
    ]

ship_list_text = [
    ("Carrier (5)", (key_position[0], key_position[1]+40)),
    ("Battleship (4)", (key_position[0], key_position[1]+120)),
    ("Submarine (3)", (key_position[0], key_position[1]+200)),
    ("Cruiser (3)", (key_position[0], key_position[1]+280)),
    ("Destroyer (2)", (key_position[0], key_position[1]+360))
     ]

joypad = Controller()
print (joypad.get_controllers())


def setup ():
    global player_ships, placing_ship, placing_ship_direction
    # configure is used to read config 
    # after this will know screen size 
    configure()
    
    # Add Ai ships - start with largest
    # position ship takes ship size and returns direction, position
    hide_ship = True
    this_ship = player2.position_ship(5)
    enemy_fleet.add_ship("carrier",this_ship[1],this_ship[0], img_txt, GRID_SIZE, hide_ship)
    this_ship = player2.position_ship(4)
    enemy_fleet.add_ship("battleship",this_ship[1],this_ship[0], img_txt, GRID_SIZE, hide_ship)
    this_ship = player2.position_ship(3)
    enemy_fleet.add_ship("submarine",this_ship[1],this_ship[0], img_txt, GRID_SIZE, hide_ship)
    this_ship = player2.position_ship(3)
    enemy_fleet.add_ship("cruiser",this_ship[1],this_ship[0], img_txt, GRID_SIZE, hide_ship)
    this_ship = player2.position_ship(2)
    enemy_fleet.add_ship("destroyer",this_ship[1],this_ship[0], img_txt, GRID_SIZE, hide_ship)

    player_ships = {
        "carrier" : 5,
        "battleship" : 4,
        "cruiser" : 3,
        "submarine" : 3,
        "destroyer": 2 }
    placing_ship = "carrier"
    placing_ship_direction = "horizontal"


def configure():
    global WIDTH, HEIGHT, GRID_SIZE, img_txt, grid_img_1, grid_img_2, your_fleet_txt_pos, enemy_fleet_txt_pos
    if (SIZE_SML == False):
        return
    WIDTH=800
    HEIGHT=480
    GRID_SIZE=(25,25)
    img_txt = "_sml"
    
    grid_img_1.image = "grid"+img_txt
    grid_img_2.image = "grid"+img_txt
    grid_img_1.topleft = (60, 140)
    grid_img_2.topleft = (420, 140)
    
    your_fleet_txt_pos = (80, 90)
    enemy_fleet_txt_pos = (440, 90)
    
    own_fleet.change_grid((91, 163), GRID_SIZE, img_txt)
    enemy_fleet.change_grid((451, 163), GRID_SIZE, img_txt)

def draw():
    global fullscreen_status
    if (FULLSCREEN == True and fullscreen_status == False):
        screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        fullscreen_status = True
    screen.fill((192,192,192))
    grid_img_1.draw()
    grid_img_2.draw()
    screen.draw.text("Battleships", fontsize=60, center=(WIDTH/2,50), shadow=(1,1), color=(255,255,255), scolor=(32,32,32))
    screen.draw.text("Your fleet", fontsize=40, topleft=your_fleet_txt_pos, color=(255,255,255))
    screen.draw.text("The enemy fleet", fontsize=40, topleft=enemy_fleet_txt_pos, color=(255,255,255))
    own_fleet.draw()
    enemy_fleet.draw()
    if (player == "gameover1"):
        screen.draw.text("Game Over\nYou won", fontsize=60, center=(WIDTH/2,HEIGHT/2), shadow=(1,1), color=(255,255,255), scolor=(32,32,32))
    elif (player == "gameover2"):
        screen.draw.text("Game Over\nYou lost!", fontsize=60, center=(WIDTH/2,HEIGHT/2), shadow=(1,1), color=(255,255,255), scolor=(32,32,32))
    elif (player == "player1setup"):
        screen.draw.text("Place your ships", fontsize=40, center=(WIDTH/2,650), color=(255,255,255))
        if (own_fleet.grid.check_in_grid(mouse_position)):
            if (placing_ship_direction == "horizontal"):
                preview_width = (GRID_SIZE[0] * player_ships[placing_ship]) - 4
                preview_height = GRID_SIZE[1] - 4
            else:
                preview_width = GRID_SIZE[0] - 4
                preview_height = (GRID_SIZE[1] * player_ships[placing_ship]) - 4
            # Show approx position of ship (slightly offset to top left)
            screen.draw.rect(Rect((mouse_position[0]-2, mouse_position[1]-2),(preview_width,preview_height)), (128,128,128))
    else:
        screen.draw.text("Aim and fire", fontsize=40, center=(WIDTH/2,650), color=(255,255,255))
    # Only show key if screen is wider than 1200
    if (WIDTH >= 1200):
        for ship_key_img in ship_list:
            ship_key_img.draw()
        screen.draw.text("Ships", topleft=key_position, fontsize=38)
        for ship_text in ship_list_text:
            screen.draw.text(ship_text[0], topleft=ship_text[1])

def update():
    global player
    if keyboard.q:
        exit()
    if (player == "player1setup"):
        pass

    if (player == "player2"):
        grid_pos = player2.fire_shot()
        # Ai uses list position - but grid uses grid
        result = own_fleet.fire(grid_pos)
        player2.fire_result (grid_pos, result)
        # If ship sunk then inform Ai player
        if (result == True):
            if (own_fleet.is_ship_sunk_grid_pos(grid_pos)):
                player2.ship_sunk(grid_pos)
                # As a ship is sunk - check to see if all ships are sunk
                if own_fleet.all_sunk():
                    player = "gameover2"
                    return

        # If reach here then not gameover, so switch back to main player
        player = "player1"

# Track position of mouse, needed during ship placement
def on_mouse_move(pos):
        global mouse_position
        mouse_position = (pos)

def on_mouse_down(pos, button):
    global player, player_ships, placing_ship, placing_ship_direction
    if (player == "player1setup"):
        if (button == mouse.RIGHT):
            if (placing_ship_direction == "horizontal"):
                placing_ship_direction = "vertical"
            else:
                placing_ship_direction = "horizontal"
        elif (button == mouse.LEFT):
            # Click to place_ship
            # Check if no grid
            if (own_fleet.grid.check_in_grid(mouse_position)):
                # convert to grid position
                grid_pos = own_fleet.grid.get_grid_pos(mouse_position)
                # check it fits and reserve space
                if (player1.check_ship_fit(player_ships[placing_ship], placing_ship_direction, grid_pos)):
                    player1.place_ship(player_ships[placing_ship], placing_ship_direction, grid_pos)
                    # Create the ship object
                    own_fleet.add_ship(placing_ship,grid_pos,placing_ship_direction, img_txt, GRID_SIZE)
                    # Remove from list of ships to add_ship
                    player_ships.pop(placing_ship)
                    # If more ships to place_ship
                    if (len (player_ships) > 0):
                        # Get next ship to add
                        placing_ship = next(iter(player_ships))
                        placing_ship_direction = "horizontal"
                    else:
                        # When completed adding ships switch to play
                        player="player1"

    if (button != mouse.LEFT):
        return
    if (player == "player1"):
        if (enemy_fleet.grid.check_in_grid(pos)):
            grid_location = enemy_fleet.grid.get_grid_pos(pos)
            enemy_fleet.fire(grid_location)
            if enemy_fleet.all_sunk():
                player = "gameover1"
            else:
                # switch to player 2
                player = "player2"
    elif (player == "gameover1" or player == "gameover2"):
        own_fleet.reset()
        enemy_fleet.reset()
        player1.reset()
        player2.reset()
        setup()
        player = "player1setup"
   
setup()
pgzrun.go()
