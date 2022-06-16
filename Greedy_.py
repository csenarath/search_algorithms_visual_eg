# created by chandima
# This to visualize the Enemy , Hero , kids and walls with Greedy Search algorithm
# Enemy is moving on constant  path as predefine by user ( Killer_Movement_())
# Ones kid engage with enemy , kid will die

# limits : on each search node , only consider corresponding left, up, right and down  as child nodes.(no diagonal support)
# limits : if node is already searched it will not consider again.
#
#           at each search node he will calculate straight line distance (euclidean distance) to enemy at that time.
#           Unlike cost search he will not going back on nodes

import pygame as pygame
import time
from pygame.locals import *
from datetime import datetime, timedelta
import numpy as np

pygame.display.set_mode()
WAIT_BEFORE_START = 5  # waiting time before start
SPEED_UP = 10  # to Speed Up

# by changing  these time will get get different out comes
MOVING_TIME_TICK = 2 / SPEED_UP  # enemy moving speed
SEARCH_NODE_TIME = 0.26 / SPEED_UP  # time spend on each search node
ISMOVE = False  # to enable movement on Enemy character

if ISMOVE:  # set Enemy Start Position if he move
    E_ROW = 13
    E_COL = 5
else:  # set Enemy Start Position if he not move
    E_ROW = 19
    E_COL = 18

flags_s = DOUBLEBUF

pygame.init()  # start  pygame
clock = pygame.time.Clock()

Done = False  # variable to keep track if window is open
MapSize = 25  # how many tiles in either direction of grid

# pixel sizes for grid squares
TileWidth = 30
TileHeight = 30
TileMargin = 2

# Colors
RED_2 = pygame.image.load('img/thif2.png').convert_alpha()
RED_2 = pygame.transform.scale(RED_2, (TileWidth, TileHeight))

PINK = pygame.image.load('img/coin.png').convert_alpha()
PINK = pygame.transform.scale(PINK, (TileWidth, TileHeight))

BLACK_3 = pygame.image.load('img/tree2.png').convert_alpha()
BLACK_3 = pygame.transform.scale(BLACK_3, (TileWidth, TileHeight))

BLUE_2 = pygame.image.load('img/p2.png').convert_alpha()
BLUE_2 = pygame.transform.scale(BLUE_2, (TileWidth, TileHeight))


YELLOW = pygame.image.load('img/caught2.png').convert_alpha()
YELLOW = pygame.transform.scale(YELLOW, (TileWidth, TileHeight))

#BROWN = pygame.image.load('img/b2.png').convert_alpha()
#BROWN = pygame.transform.scale(BROWN, (TileWidth, TileHeight))

RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREEN2 = (154, 205, 50)
BLUE = (0, 0, 255)
#BLUE_2 = (18, 133, 150)
#YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
OFF_WHITE = (176, 174, 169)
BLACK= (0,0,0)
BLACK_2 = (36, 35, 35)
#BLACK_3 = (22, 10, 48)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
BROWN = (248, 240, 164)
GREEN_3 = (16, 107, 77)
GREEN_4 = (175, 179, 73)

# create Screen
Screen = pygame.display.set_mode([(MapSize * (TileWidth + TileMargin)) + TileMargin,
                                  (MapSize * (TileHeight + TileMargin)) + TileMargin], flags_s)

pygame.display.set_caption("Greedy Algorithm")
Screen.fill(BLACK_2)  # margin color between tiles
pygame.display.flip()

BG_Color = BROWN  # Tiles Color


# draw Tiles
def drawTile(row, column, color):
    try:
        tile = pygame.draw.rect(Screen, color, [(TileMargin + TileWidth) * column + TileMargin,
                                                (TileMargin + TileHeight) * row + TileMargin,
                                                TileWidth,
                                                TileHeight])
    except:
        rect = color.get_rect()
        rect.topleft = (TileMargin + TileWidth) * column + TileMargin,  (TileMargin + TileHeight) * row + TileMargin

        Screen.blit(color, [(TileMargin + TileWidth) * column + TileMargin,
                                                (TileMargin + TileHeight) * row + TileMargin,
                                              TileWidth,
                                                TileHeight])

        tile = pygame.draw.rect(Screen, BLACK_2, rect,1,0)

    pygame.display.update(tile)


# draw initial space
def initial_screen():
    for Row in range(MapSize):  # Drawing grid
        for Column in range(MapSize):
            drawTile(Row, Column, BROWN)


# object class
class Objects(object):

    def __init__(self, type, name, row, column, color, status, rigit):
        self.Name = name
        self.Color = color
        self.Column = column
        self.Row = row
        self.Column_old = column
        self.Row_old = row
        self.Is_Status = status
        self.Rigit = rigit
        self.Type = type
        self.search_parent_node = None
        self.Distance = 0

    def draw(self):
        drawTile(self.Row, self.Column, self.Color)

    # make object dead
    def Dead(self):
        self.Color = GREY
        self.Is_Status = 0
        print("{} is Dead ".format(self.Name))

    # make object Move
    def Move(self, row, column):
        if (self.Column + column) < MapSize:
            self.Column_old = self.Column
            self.Column = self.Column + column
            print("{} move from : Column {} to {}".format(self.Name, self.Column_old, self.Column))
        else:
            print("{} unable to move on Columns  : Limit ".format(self.Name))
            self.Column_old = self.Column

        if (self.Row + row) < MapSize:
            self.Row_old = self.Row
            self.Row = self.Row + row
            print("{} move from : Row {} to {}".format(self.Name, self.Row_old, self.Row))
        else:
            print("{} unable to move on Rows : Limit ".format(self.Name))
            self.Row_old = self.Row

    # get Near by coordination
    def get_Neighbors(self):
        up = None
        down = None
        left = None
        right = None

        if self.Row - 1 >= 0:
            up = (self.Row - 1, self.Column)

        if self.Row + 1 < MapSize:
            down = (self.Row + 1, self.Column)

        if self.Column - 1 >= 0:
            left = (self.Row, self.Column - 1)

        if self.Column + 1 < MapSize:
            right = (self.Row, self.Column + 1)
        return [left, up, right, down]

    # coordination comparison
    def compare_coordination(self, raw, column):
        if self.Row == raw and self.Column == column:
            return True
        else:
            return False

    # Searched check function
    def Checked(self):
        if self.Type != "Hero":
            self.Color = GREEN2
        self.Rigit = 1
        print("{} is Checked ".format(self.Name))

    # add parent node for backtracking
    def Add_Search_Parent_node(self, objects):
        self.search_parent_node = objects

    # when object (enemy) get caught
    def Caught(self):
        self.Color = YELLOW

    def Get_Distance(self, Object):
        # Euclidean distance
        point1 = np.array((self.Row, self.Column))
        point2 = np.array((Object.Row, Object.Column))
        sum_sq = np.sum(np.square(point1 - point2))
        self.Distance = np.sqrt(sum_sq)

        # Map class

# Map Class
class Map(object):
    global MapSize

    Grid = [[]]

    for Row in range(MapSize):  # Creating grid
        Grid.append([])
        for Column in range(MapSize):
            Grid[Row].append([])

    # create main character  objects

    Hero = Objects("Hero", "Hero", 5, 5, BLUE_2, 1, 0)
    Enemy = Objects("Enemy", "Enemy", E_ROW, E_COL, RED_2, 1, 0)
    kid1 = Objects("Kid", "kid1", 13, 15, PINK, 1, 0)
    kid2 = Objects("Kid", "kid2", 5, 22, PINK, 1, 0)
    kid3 = Objects("Kid", "kid3", 22, 4, PINK, 1, 0)

    Object_list = [Hero, Enemy, kid1, kid2, kid3]

    for Object_ in Object_list:
        Grid[Object_.Row][Object_.Column].append(Object_)
        Object_.draw()

    def Update(self):
        for Object_ in self.Object_list:
            if (Object_.Column != Object_.Column_old) or (Object_.Row != Object_.Row_old):
                self.Grid[Object_.Row_old][Object_.Column_old].remove(Object_)
                self.Grid[Object_.Row][Object_.Column].append(Object_)

        print("Updated")

    # add walls
    Object_Wall = []
    for raw in range(0, 3):
        wall = Objects("Wall", "Wall", raw, 8, BLACK_3, 1, 2)
        Object_Wall.append(wall)
        Grid[wall.Row][wall.Column].append(wall)
    for raw in range(0, 3):
        wall = Objects("Wall", "Wall", raw, 18, BLACK_3, 1, 2)
        Object_Wall.append(wall)
        Grid[wall.Row][wall.Column].append(wall)
    for raw in range(3, 9):
        wall = Objects("Wall", "Wall", raw, 11, BLACK_3, 1, 2)
        Object_Wall.append(wall)
        Grid[wall.Row][wall.Column].append(wall)
    for raw in range(10, 12):
        wall = Objects("Wall", "Wall", raw, 11, BLACK_3, 1, 2)
        Object_Wall.append(wall)
        Grid[wall.Row][wall.Column].append(wall)
    for raw in range(16, 21):
        wall = Objects("Wall", "Wall", raw, 8, BLACK_3, 1, 2)
        Object_Wall.append(wall)
        Grid[wall.Row][wall.Column].append(wall)
    for raw in range(15, 21):
        wall = Objects("Wall", "Wall", raw, 2, BLACK_3, 1, 2)
        Object_Wall.append(wall)
        Grid[wall.Row][wall.Column].append(wall)
    for raw in range(8, 12):
        wall = Objects("Wall", "Wall", raw, 9, BLACK_3, 1, 2)
        Object_Wall.append(wall)
        Grid[wall.Row][wall.Column].append(wall)
    for raw in range(4, 8):
        wall = Objects("Wall", "Wall", raw, 2, BLACK_3, 1, 2)
        Object_Wall.append(wall)
        Grid[wall.Row][wall.Column].append(wall)
    for raw in range(6, 14):
        wall = Objects("Wall", "Wall", raw, 19, BLACK_3, 1, 2)
        Object_Wall.append(wall)
        Grid[wall.Row][wall.Column].append(wall)
    for raw in range(9, 18):
        wall = Objects("Wall", "Wall", raw, 23, BLACK_3, 1, 2)
        Object_Wall.append(wall)
        Grid[wall.Row][wall.Column].append(wall)
    for raw in range(15, 23):
        wall = Objects("Wall", "Wall", raw, 15, BLACK_3, 1, 2)
        Object_Wall.append(wall)
        Grid[wall.Row][wall.Column].append(wall)
    for raw in range(12, 21):
        wall = Objects("Wall", "Wall", raw, 21, BLACK_3, 1, 2)
        Object_Wall.append(wall)
        Grid[wall.Row][wall.Column].append(wall)
    for column in range(2, 5):
        wall = Objects("Wall", "Wall", 8, column, BLACK_3, 1, 2)
        Object_Wall.append(wall)
        Grid[wall.Row][wall.Column].append(wall)
    for column in range(6, 9):
        wall = Objects("Wall", "Wall", 8, column, BLACK_3, 1, 2)
        Object_Wall.append(wall)
        Grid[wall.Row][wall.Column].append(wall)
    for column in range(20, 24):
        wall = Objects("Wall", "Wall", 7, column, BLACK_3, 1, 2)
        Object_Wall.append(wall)
        Grid[wall.Row][wall.Column].append(wall)
    for column in range(6, 11):
        wall = Objects("Wall", "Wall", 15, column, BLACK_3, 1, 2)
        Object_Wall.append(wall)
        Grid[wall.Row][wall.Column].append(wall)
    for column in range(2, 12):
        wall = Objects("Wall", "Wall", 20, column, BLACK_3, 1, 2)
        Object_Wall.append(wall)
        Grid[wall.Row][wall.Column].append(wall)
    for column in range(6, 12):
        wall = Objects("Wall", "Wall", 12, column, BLACK_3, 1, 2)
        Object_Wall.append(wall)
        Grid[wall.Row][wall.Column].append(wall)
    for column in range(2, 7):
        wall = Objects("Wall", "Wall", 1, column, BLACK_3, 1, 2)
        Object_Wall.append(wall)
        Grid[wall.Row][wall.Column].append(wall)
    for column in range(15, 24):
        wall = Objects("Wall", "Wall", 3, column, BLACK_3, 1, 2)
        Object_Wall.append(wall)
        Grid[wall.Row][wall.Column].append(wall)
    for column in range(1, 7):
        wall = Objects("Wall", "Wall", 11, column, BLACK_3, 1, 2)
        Object_Wall.append(wall)
        Grid[wall.Row][wall.Column].append(wall)
    for column in range(16, 22):
        wall = Objects("Wall", "Wall", 20, column, BLACK_3, 1, 2)
        Object_Wall.append(wall)
        Grid[wall.Row][wall.Column].append(wall)


# Enemy move class
class EnemyMove(object):
    Enemy_step = 0


# killer movement : constant path
def Killer_Movement_():
    # as path design it took 60 steps to enemy to kill all
    pos_r = Map.Enemy.Row
    pos_c = Map.Enemy.Column
    moved = False
    if enemy_move.Enemy_step < 10:
        Map.Enemy.Move(0, 1)
        enemy_move.Enemy_step = enemy_move.Enemy_step + 1
        Map.Enemy.draw()
        Map.Update()
        moved = True
    elif enemy_move.Enemy_step < 18:
        Map.Enemy.Move(-1, 0)
        enemy_move.Enemy_step = enemy_move.Enemy_step + 1
        Map.Enemy.draw()
        Map.Update()
        moved = True
    elif enemy_move.Enemy_step < 25:
        Map.Enemy.Move(0, 1)
        enemy_move.Enemy_step = enemy_move.Enemy_step + 1
        Map.Enemy.draw()
        Map.Update()
        moved = True

    elif enemy_move.Enemy_step < 34:
        Map.Enemy.Move(0, -1)
        enemy_move.Enemy_step = enemy_move.Enemy_step + 1
        Map.Enemy.draw()
        Map.Update()
        moved = True

    elif enemy_move.Enemy_step < 51:
        Map.Enemy.Move(1, 0)
        enemy_move.Enemy_step = enemy_move.Enemy_step + 1
        Map.Enemy.draw()
        Map.Update()
        moved = True

    elif enemy_move.Enemy_step < 60:
        Map.Enemy.Move(0, -1)
        enemy_move.Enemy_step = enemy_move.Enemy_step + 1
        Map.Enemy.draw()
        Map.Update()
        moved = True

    if moved:
        if len(Map.Grid[pos_r][pos_c]) > 0:
            if len(Map.Grid[pos_r][pos_c]) == 1:
                Map.Grid[pos_r][pos_c][0].draw()
            else:
                Map.Grid[pos_r][pos_c][0].draw()
        else:
            drawTile(pos_r, pos_c, BG_Color)

    for obj_ in Map.Grid[pos_r][pos_c]:
        if obj_.Type == "Kid":
            obj_.Dead()
            for characters in Map.Object_list:
                characters.draw()
            print("{} is dead".format(obj_.Name))


def Killer_Movement():
    if ISMOVE:
        Killer_Movement_()


# check node is valid for move
# objects cant go through / access rigid body's (objects)

def Valid_Node(row, column):
    if len(Map.Grid[row][column]) == 0:
        return True
    else:
        if len(Map.Grid[row][column]) == 1:
            if Map.Grid[row][column][0].Rigit > 0:
                return False
        else:
            for obj_ in Map.Grid[row][column]:
                if obj_.Rigit > 0:
                    return False

    return True

def Algo_Greed():
    start_time = datetime.now()

    # set start position / node by Hero
    if len(Open_list) == 0:
        Open_list.append(Map.Hero)

    done = False

    while not done:

        # move Killer every 1 sec
        if datetime.now() > start_time + timedelta(seconds=MOVING_TIME_TICK):
            Killer_Movement()
            start_time = datetime.now()

        # update distance to enemy
        # sort list according to distance
        for item_ in Open_list:
            item_.Get_Distance(Map.Enemy)
        Open_list.sort(key=lambda x: x.Distance)

        # Get a node
        current_Node = Open_list[0]
        current_Node.Checked()
        current_Node.draw()

        neighbor_list = current_Node.get_Neighbors()

        if Map.Enemy.compare_coordination(current_Node.Row, current_Node.Column):
            current_Node.Color = ORANGE
            done = True
            Map.Enemy.Caught()
        current_Node.draw()

        if not done:
            stage_child_list = []
            for neighbor_ in neighbor_list:

                if neighbor_ is not None:

                    if Valid_Node(neighbor_[0], neighbor_[1]):
                        name = "Search " + str(neighbor_[0]) + " " + str(neighbor_[1])

                        # time on each node since execution times are faster , for smooth visualization
                        time.sleep(SEARCH_NODE_TIME)

                        # add child nodes

                        search_node = Objects("Search", name, neighbor_[0], neighbor_[1], GREEN_4, 1, 1)
                        search_node.draw()
                        search_node.Add_Search_Parent_node(current_Node)

                        Map.Grid[neighbor_[0]][neighbor_[1]].append(search_node)
                        stage_child_list.append(search_node)
            for item_ in stage_child_list:
                item_.Get_Distance(Map.Enemy)
            stage_child_list.sort(key=lambda x: x.Distance)
            if len(stage_child_list) > 0:
                Open_list.append(stage_child_list[0])

        # for stopping characters disappearing
        for characters_ in Map.Object_list:
            characters_.draw()

        Closed_list.append(current_Node)
        del Open_list[0]

        print("Open_list:{}".format(len(Open_list)))
        print("closed_list:{}".format(len(Closed_list)))

        # if found Enemy get path
        if done:
            path_node = Closed_list[-1]
            path_node_list = []
            get_path_complete = False
            while not get_path_complete:
                path_node_list.append(path_node)
                if path_node.Type == "Hero":
                    get_path_complete = True
                else:
                    path_node = path_node.search_parent_node

            for path_node_ in path_node_list[1:]:
                if path_node_.Type != "Hero" and path_node_.Type != "Enemy":
                    drawTile(path_node_.Row, path_node_.Column, PURPLE)
            print("path: size  {}".format(len(path_node_list)))
        # end if State space is completed
        if len(Open_list) < 1:
            done = True



initial_screen()  # draw grid

Map = Map()  # set map

# draw walls
for wall_ in Map.Object_Wall:
    wall_.draw()

# draw characters
for characters in Map.Object_list:
    characters.draw()

enemy_move = EnemyMove()

Game_start_time = datetime.now()

Open_list = []
Closed_list = []


time.sleep(WAIT_BEFORE_START)


Algo_Greed()

Game_end_time = datetime.now()
print("---End---")
print("Game Stared at : {}".format(Game_start_time))
print("Game Stared at : {}".format(Game_end_time))
print("Game took  : {}".format(Game_end_time - Game_start_time))

print("Open_list:{}".format(len(Open_list)))
print("closed_list:{}".format(len(Closed_list)))

time.sleep(10)
pygame.quit()
