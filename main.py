import pygame, sys
import box

# Määritä kenttä (0 = tyhjä, 1 = seinä, 2 = maali, 3 = laatikko, 5 = laatikko maalissa)
MAP = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 3, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 2, 0, 0, 1, 0, 0, 2, 1],
        [1, 0, 3, 0, 2, 1, 0, 3, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        ]

FLOOR_TYPE = 0
WALL_TYPE = 1
GOAL_TYPE = 2
BOX_TYPE = 3
BOX_IN_GOAL_TYPE = 5

# Määritä ruudun koko ja kentän leveys ja korkeus
BLOCK_SIZE = 75
MAP_WIDTH = len(MAP[0])
MAP_HEIGHT = len(MAP)

# Määritä pelinäkymän koko
SCREEN_WIDTH = MAP_WIDTH * BLOCK_SIZE
SCREEN_HEIGHT = MAP_HEIGHT * BLOCK_SIZE

# Alusta Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sokoban peli")

# Lataa kuvat
kodarit_voitto_img = pygame.image.load("voittoruutu.png")
kodarit_voitto_img = pygame.transform.scale(kodarit_voitto_img, (BLOCK_SIZE * 10, BLOCK_SIZE * 7))

box_img = pygame.image.load("box.png")
box_img = pygame.transform.scale(box_img, (BLOCK_SIZE, BLOCK_SIZE))

player_img = pygame.image.load("bird.png")
player_img = pygame.transform.scale(player_img, (BLOCK_SIZE, BLOCK_SIZE))

goal_img = pygame.image.load("goal.png")
goal_img = pygame.transform.scale(goal_img, (BLOCK_SIZE, BLOCK_SIZE))

wall_img = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
wall_img.fill("#00556f")

#Tähän kerätään kentällä olevien laatikoiden tiedot
boxes = []
#Tähän kerätään kentällä olevien maalien tiedot
goals = []

# Piirrä kenttä
def draw_floor_and_walls():
    screen.fill("#a6c6d5")
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if MAP[y][x] == 1:
                screen.blit(wall_img, (x * BLOCK_SIZE, y * BLOCK_SIZE))

#Luodaan maali Rectejä MAP-pelialuemäärityksen mukaan
def create_goals():
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if MAP[y][x] == GOAL_TYPE:
                goal_obj = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                goals.append(goal_obj)

#Piirretään maalit kentälle
def draw_goals():
    for goal in goals:
        screen.blit(goal_img, goal)

#Luodaan laatikko-Rectejä MAP-pelialuemäärityksen mukaan
def create_boxes():
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if MAP[y][x] == BOX_TYPE:
                box_obj = box.Box(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE)
                boxes.append(box_obj)

#Piirretään laatikot kentälle
def draw_boxes():
    for box in boxes:
        screen.blit(box_img, box)

#Tarkistetaan ovatko kaikki laatikot maalien päällä
def are_all_boxes_in_goal():
    all_goals = len(goals)
    boxes_in_goal = 0
    for box in boxes:
        for goal in goals:
            if (box.y == goal.y and box.x == goal.x):
                boxes_in_goal += 1
                print("laatikko maalissa")
    if boxes_in_goal == all_goals:
        print("Voitto!")
        return True

#Saadaan sijaintin tyypi
def get_cell_type(position):
    return MAP[position[1]][position[0]]

#Saadaan uuden sijaintin suuntauksesta riippuen
def get_new_position(old_pos, direction):
    new_pos = old_pos.copy()
    if direction == "left":
        new_pos[0] -= 1
    elif direction == "right":
        new_pos[0] += 1
    elif direction == "up":
        new_pos[1] -= 1
    elif direction == "down":
        new_pos[1] += 1
    print("get_new_position(): ", old_pos, " -> ", new_pos)
    return new_pos

#Tarkistetaan osuiko pelihahmo laatikkoon ja 
#riippuen mistä suunnasta hahmo siihen osui 
#siirretään laatikkoa, jos mahdollista
def move_box(position, direction):
    new_pos = get_new_position(position, direction)
    new_cell_type = get_cell_type(new_pos)
    print("move_box(): current position = ", position, " new_position = ", new_pos, " new cell type = ", new_cell_type)
    #siirretään laatikkon vain jos uuden sijaintin on tyhjä tai maali
    if new_cell_type == FLOOR_TYPE or new_cell_type == GOAL_TYPE:
        for box in boxes:
            if box.get_position() == position:
                box.move((new_pos[0] - position[0]) * BLOCK_SIZE, (new_pos[1] - position[1]) * BLOCK_SIZE)
                MAP[new_pos[1]][new_pos[0]] += BOX_TYPE
                MAP[position[1]][position[0]] -= BOX_TYPE
                return True
    return False

#Tarkistetaan, että pelaaja pystyy siirtää uuteen sijaintiin
def can_move_player(new_position, direction):
    new_cell_type = get_cell_type(new_position)
    print("move_player(): new position = ", new_position, " new cell type ", new_cell_type)
    if new_cell_type == FLOOR_TYPE or new_cell_type == GOAL_TYPE:
        return True
    if new_cell_type == WALL_TYPE:
        return False
    if new_cell_type == BOX_TYPE or new_cell_type == BOX_IN_GOAL_TYPE:
        #Pelaaja pystyy siirtää vain jos laatikon myös siirtää etenpäin
        if move_box(new_position, direction):
            return True
    return False

# Pääohjelma
def main():
    player_pos = [1, 1] # Alusta pelaajan sijainti
    player = pygame.Rect(player_pos[0] * BLOCK_SIZE, player_pos[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    kodarit_voitto = pygame.Rect(0, 0, BLOCK_SIZE * 10, BLOCK_SIZE * 7)
    create_goals()
    create_boxes()
    running = True
    kew_pressed = ""
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                new_position = player_pos.copy() #Copioi pelaajan sijainti ja muuta sen, jos nuoli on painettu
                if event.key == pygame.K_LEFT:
                    key_pressed = "left"
                    new_position[0] -= 1 
                elif event.key == pygame.K_RIGHT:
                    key_pressed = "right"
                    new_position[0] += 1
                elif event.key == pygame.K_UP:
                    key_pressed = "up"
                    new_position[1] -= 1
                elif event.key == pygame.K_DOWN:
                    key_pressed = "down"
                    new_position[1] += 1

                #Ennen kuin pelihahmon sijaintia päivitetään, tarkistetaan,
                #ettei kohdesolussa ole estettä
                #Tämä estää pelihahmoa liikkumasta
                #seinien tai muiden esteiden läpi.
                if can_move_player(new_position, key_pressed):
                    #Tehdään player rect uuteen positioon
                    player_pos = new_position.copy()
                    player = pygame.Rect(player_pos[0] * BLOCK_SIZE, player_pos[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)

                #Tsekataan ovatko kaikki laatikot maaleissa ja jos niin näytetään voittoruutua
                if are_all_boxes_in_goal() == True:
                    screen.blit(kodarit_voitto_img, kodarit_voitto)
                    #Tämä käsky päivittää näytön
                    pygame.display.flip()
                    #Odotetaan 4 sekuntia, että näyttö päivittyy
                    pygame.time.wait(4000)
                    running = False

        # Piiretään kenttä ja pelaaja
        draw_floor_and_walls()
        draw_goals()
        draw_boxes()
        screen.blit(player_img, player)
        #Tämä käsky päivittää näytön
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
