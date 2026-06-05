from ctypes import cast
import random

import pyxel

class Main:
    def __init__(self):
        # Pyxel
        pyxel.init(128,128,title="Tower Defence, protect your gold")
        pyxel.load("U4.pyxres")

        # Jeu
        self.lvl = 1
        self.gold = 0

        # Obj
        self.castle = Castle(self.lvl,0)
        self.cave = Castle(self.lvl, 128-16)
        self.objToDraw = [self.castle, self.cave]

        # Entity
        self.enemy_list = []

        # Run
        pyxel.run(self.update, self.draw)

    def enemyCreation(self):
        if pyxel.frame_count % 30 == 0:
            self.enemy_list.append(Enemy(1, self.cave.x, self.cave.y))
            print("isbgfr")

    def update(self):
        if pyxel.frame_count % 5 == 0:
            if pyxel.frame_count % 8 == 0:
                self.enemyCreation()
            for enemy in self.enemy_list:
                enemy.move()

    def draw(self):
        pyxel.cls(0)
        for obj in self.objToDraw:
            pyxel.rect(obj.x, obj.y, obj.height, obj.width, 9)
        for enemy in self.enemy_list:
            if pyxel.frame_count % enemy.time_ani == 0:
                enemy.animation = 8
            else:
                enemy.animation = 0
            print(enemy.x, enemy.y, enemy.image, enemy.props[self.lvl-1][0] + enemy.animation, enemy.props[self.lvl-1][1], enemy.height, enemy.width, 15)
            pyxel.blt(enemy.x, enemy.y, enemy.image, enemy.props[self.lvl-1][0] + enemy.animation, enemy.props[self.lvl-1][1], 8, 8, 15, 0, enemy.scale)



class Entity:
    def __init__(self, lvl, x, y):
        self.pv = 5 * lvl
        self.damage = 5 * lvl
        self.x = x
        self.y = y
        self.height = 8
        self.width = 8

class Enemy(Entity):
    def __init__(self, lvl, x, y):
        super().__init__(lvl, x, y)
        self.loot = 1 * lvl
        right_or_left = random.randint(1,4)
        if right_or_left == 1:
            self.direction = 80
        elif right_or_left == 2:
            self.direction = 56
        elif right_or_left == 3:
            self.direction = 44
        else:
            self.direction = 20


    def move(self):
        if (random.randint(0, 100) < 65):
            deplacement = random.randint(1, 3)
            if (self.x + 8 + deplacement > 128):
                self.x -= (deplacement+10)
            elif (self.x - deplacement < 0):
                self.x += (deplacement+10)
            elif (random.randint(0, 100) < self.direction):
                self.x += deplacement
            else:
                self.x -= deplacement
        else:
            deplacement = random.randint(1, 2)
            if (self.y - deplacement <= 16):
                return "caboom"
            else:
                self.y -= deplacement

class Ally(Entity):
    def __init__(self, lvl, x, y):
        super().__init__(lvl, x, y)

class Castle(Entity):
    def __init__(self, lvl, y):
        super().__init__(lvl, 64, y)
        self.height = 16
        self.width = 16




Main()


