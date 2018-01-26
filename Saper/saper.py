import re
import numpy
import random

excludedLocation = []

def getNeighbours(location):
    i = location[0]
    j = location[1]
    neighboursPattern = [(i - 1, j - 1),
                  (i - 1, j),
                  (i - 1, j + 1),
                  (i, j - 1),
                  (i, j + 1),
                  (i + 1, j - 1),
                  (i + 1, j),
                  (i + 1, j + 1)]
    neighbours = []
    for i in range(8):
        if checkSize(neighboursPattern[i][0], int(numpy.sqrt(map.size))) \
                and checkSize(neighboursPattern[i][1], int(numpy.sqrt(map.size)))\
                and neighboursPattern[i] not in excludedLocation:
            neighbours.append(neighboursPattern[i])

    return neighbours

# =============================================================================


def mark(i, j):  # mark field as potential bomb so it can't be reveal
    if fog[i][j] == "!":
        print("Field already marked, take another action")
    elif fog[i][j] == "-":
        fog[i][j] = "!"
        print("Field marked")
    else:
        print("Field already revealed, take another action")

# =============================================================================


def unmark(i, j):  # unmark field so it can be reveal
    if fog[i][j] == "-":
        print("Field already unmarked, take another action")
    elif fog[i][j] == "!":
        fog[i][j] = "-"
        print("Field unmarked")
    else:
        print("Field already revealed, take another action")
# =============================================================================


def reveal(i, j):  # reveal field
    global excludedLocation
    excludedLocation = []

    if fog[i][j] == "!":
        print("Cannot reveal marked field - there can be a bomb!")
    elif fog[i][j] == "-":
        if map[i][j] == -1:
            fog[i][j] = "#"
        else:
            revealInternal((i, j))


def revealInternal(location):
    global excludedLocation
    if location not in excludedLocation:
        excludedLocation.append(location)

    fog[location[0]][location[1]] = "_"
    if map[location] == 0:
        neighbours = getNeighbours(location)
        # print(neighbours)
        for neighbour in neighbours:
            # print(neighbour)
            revealInternal(neighbour)
# =============================================================================

# dictionary for available game actions
actions = ["r", "m", "u"]
actionsDictionary = {
    actions[0]: reveal,
    actions[1]: mark,
    actions[2]: unmark,
}

# fog values
fogValues = ["-", "!", "#"]

# fireworks for console
consoleEffects = {
    0: '\033[97m',
    1: '\033[1m',
    2: '\033[92m',
    3: '\033[93m',
    4: '\033[95m',
    5: '\033[91m',
    6: '\033[96m',
    7: '\033[94m',
    8: '\033[90m',
    "END": '\033[0m',
}

# =============================================================================


def checkSize(value, size): # check if given value fits with size
    return value >= 0 and value < size
# =============================================================================


def buildMap(size): # prepare map matrix and fog
    global map
    global fog
    map = numpy.zeros((size, size)).astype(int)
    fog = [["-" for x in range(size)] for y in range(size)]

    k = 0
    for i in range(size):
        for j in range(size):
            k += 1
            map[i][j] = k
# =============================================================================


def plantBombs(): # place bomb in random place on map
    global map
    size = int(numpy.sqrt(map.size))
    global bombs
    bombs = int(round(size * (1 + (size - 5)/15)))
    draw = random.sample(list(map.flat), bombs)

    for field in draw:
        map[tuple(*zip(*numpy.where(map == field)))] = -1
# =============================================================================


def fillField(i, j): # fill plac without bomb with proper values
    if map[i][j] != -1:
        k = 0
        neighbours = getNeighbours((i, j))
        for neighbour in neighbours:
            try:
                if map[neighbour] == -1 :
                    k += 1
                else:
                    k
            except IndexError:
                k += 0
        map[i][j] = k
# =============================================================================


def fillMap(): # set all map fields
    global map
    for i in range(int(numpy.sqrt(map.size))):
        for j in range(int(numpy.sqrt(map.size))):
                fillField(i, j)
# =============================================================================


def generateMap(size):  # generate game map
    buildMap(size)
    plantBombs()
    fillMap()
# =============================================================================


def printMap(): # print current map state
    size = int(numpy.sqrt(map.size))
    loose = None

    print("\\   ", end='')
    for i in range((size)):
        if i < 10:
            print(" {} ".format(i), end='')
        else:
            print(" {}".format(i), end='')

    print()
    print("  ====", end='')
    for i in range((size) * 3):
        print("=", end='')
    print()
    for i in range(size):

        if i < 10:
            print("{} ||".format(i), end='')
        else:
            print("{}||".format(i), end='')
        for j in range(size):
            if fog[i][j] in fogValues:
                print(" {} ".format(fog[i][j]), end='')
                if fog[i][j] == "#":
                    loose = True
            else:
                consolePrint = consoleEffects[map[i][j]] + " {} " + consoleEffects["END"]
                print(consolePrint.format(map[i][j]), end='')
        print("||")
    print("  ====", end='')
    for i in range((size) * 3):
        print("=", end='')
    print()

    return loose
# =============================================================================


def winCheck():
    loose = None

    global bombs
    knownFog = 0
    unknownFog = 0
    for row in fog:
        knownFog += row.count("_")
    for row in fog:
        unknownFog += row.count("-")
        unknownFog += row.count("!")

    # print("fog known {}".format(knownFog))
    # print("fog unknown {}".format(unknownFog))
    # print("bombs {}".format(bombs))
    # print("not bombs {}".format(map.size - bombs))
    if unknownFog == bombs and knownFog == map.size - bombs:
        loose = False

    return loose
# =============================================================================

# welcoming and instructions
print("Hello there, in console Saper v0.1.")
print("============================")
print("Some instructions:")
print("Identify field through columns X and rows Y")
print("To reveal field type 'r X Y', eg.: r 5 3")
print("To mark field as potential bomb type 'm X Y' - you cannot reveal marked field")
print("To unmark field type 'u X Y' - then you can reveal it again")
print("Type 'exit', to exit game")
print("============================")
# =============================================================================
while True:
    # setting game map size and start game
    sizeInput = input("Please type map size, between 5 and 20\n")
    if sizeInput == "exit":
        break

    while True:
        try:
            if int(sizeInput) < 5 or int(sizeInput) > 20:
                sizeInput = input("Wrong size entered, please type correct size\n")
            else:
                break
        except ValueError:
            sizeInput = input("Wrong size entered, please type correct size\n")

    size = int(sizeInput)
    generateMap(size)
    print("LET THE GAME BEGIN:")
    print("============================")
    # =============================================================================

    # main game loop
    printMap()
    while True:
        loose = None
        actionInput = input("What to do?\n")
        if re.match("^[rmu] \d?\d \d?\d$", actionInput):
            action = actionInput.split(' ')
            if (action[0] in actions) and checkSize(int(action[1]), size) and checkSize(int(action[2]), size):
                actionsDictionary[action[0]]\
                    (int(action[2]), int(action[1]))
                loose = printMap()
                if loose:
                    print("Sadly, you just exploded")
                    break

                loose = winCheck()
                if loose == False:
                    print("You win!")
                    break
            else:
                print("Invalid command - check instruction and type again")

        elif actionInput == "exit":
            break
        else:
            print("Invalid command - check instruction and type again")