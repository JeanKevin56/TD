from ctypes import cast
import random

import pyxel

class Main:
    def __init__(self):
        self.lvl = 1
        pyxel.init(128,128,title="Tower Defence, protect your gold")
        self.castle = Castle(self.lvl,0)
        self.cave = Castle(self.lvl, 128-16)
        self.objToDraw = [self.castle, self.cave]
        self.enemy_list = []
        pyxel.run(self.update, self.draw)

    def enemyCreation(self):
        if pyxel.frame_count % 30 == 0:
            self.enemy_list.append(Enemy(1, self.cave.x, self.cave.y))
            print("isbgfr")


    def update(self):
        self.enemyCreation()
        for enemy in self.enemy_list:
            enemy.move()

    def draw(self):
        pyxel.cls(0)
        for obj in self.objToDraw:
            pyxel.rect(obj.x, obj.y, obj.height, obj.width, 9)
        for enemy in self.enemy_list:
            pyxel.rect(enemy.x, enemy.y, enemy.height, enemy.width, 9)



class Entity:
    def __init__(self, lvl, x, y):
        self.pv = 5 * lvl
        self.damage = 5 * lvl
        self.x = x
        self.y = y
        self.height = 4
        self.width = 4

class Enemy(Entity):
    def __init__(self, lvl, x, y):
        super().__init__(lvl, x, y)
        self.loot = 1 * lvl

    def move(self):
        if (random.randint(0, 100) < 20):
            deplacement = random.randint(2, 4)
            if (self.x + 4 + deplacement > 128):
                self.x -= deplacement
            elif (self.x - deplacement < 0):
                self.x += deplacement
            elif (random.randint(1, 2) == 1):
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


