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
        self.scale = 1
        self.loot = 1 * lvl
        self.image = 0
        self.props = [(0, 64), (0, 72), (16, 64), (16, 72), (32, 64), (32, 72)]
        self.animation = 0
        self.time_ani = random.randint(1, 30)

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


