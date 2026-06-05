from ctypes import cast
import random

import pyxel
from pyxel.pyxel_binding import mouse

class Main:
    def __init__(self):
        # Pyxel
        pyxel.init(128,128,title="Tower Defence, protect your gold")
        pyxel.load("U4.pyxres")
        pyxel.mouse(True)

        # Jeu
        self.lvl = 1
        self.gold = 100

        # Obj
        self.castle = Castle(10,0)
        self.cave = Castle(10, 128-16)
        self.objToDraw = [self.cave]
        self.objWithProgBar = [self.castle, self.cave]

        # Entity
        self.enemy_list = []
        self.tower_list = []
        self.bullet_list = []

        # Run
        pyxel.run(self.update, self.draw)

    def enemyCreation(self):
        if pyxel.frame_count % 75 == 0:
            self.enemy_list.append(Enemy(1, self.cave.x+(self.cave.height/2), self.cave.y-7))

    def towerCreation(self):
        if pyxel.btnr(pyxel.KEY_UP) and self.gold >= Tower.cost:
            self.gold -= Tower.cost
            self.tower_list.append(Tower(1, pyxel.mouse_x, pyxel.mouse_y, 5, "0", "kjb"))

 



    def update(self):
        self.enemyCreation()
        self.towerCreation()
        for enemy in self.enemy_list:
            if enemy.move() == False:
                self.castle.pv -= enemy.damage
                if self.castle.pv < 0:
                    self.CastleDectruction()
                self.enemy_list.remove(enemy)
        for tower in self.tower_list:
            shoot = tower.shoot()
            if shoot != None:
                self.bullet_list.append(shoot)
        for bullet in self.bullet_list:
            bullet.move()


    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 0, 256, 256)
        for obj in self.objToDraw:
            pyxel.rect(obj.x, obj.y, obj.height, obj.width, 9)
        self.progression_bare()
        for enemy in self.enemy_list:
            if pyxel.frame_count % enemy.time_ani == 0:
                enemy.animation = 8
            else:
                enemy.animation = 0
            pyxel.blt(enemy.x, enemy.y, enemy.image, enemy.props[self.lvl-1][0] + enemy.animation, enemy.props[self.lvl-1][1], 8, 8, 15, 0, enemy.scale)
        for tower in self.tower_list:
            pyxel.rect(tower.x, tower.y, 8, 8, 9)
        for bullet in self.bullet_list:
            pyxel.rect(bullet.x, bullet.y, 1, 5, 9)
        pyxel.blt(0, 32, 0, 0, 104, 8, 8)

        pyxel.rect(5, 5, 5, 5, 10)
        pyxel.text(12, 5, str(self.gold), 0)






    def progression_bare(self):
        for obj in self.objWithProgBar:
            pyxel.rect(obj.x+(128/30)*10, obj.y+3, obj.pv/100 * (128/30*10), 4, 11)
            pyxel.rectb(obj.x+(128/30)*10-1, obj.y+3, (128/30*10)+2, 4, 0)

        



class Entity:
    def __init__(self, lvl, x, y):
        self.pv = 10 * lvl
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
        right_or_left = random.randint(1, 4)
        if right_or_left == 1:
            self.direction = 80
        elif right_or_left == 2:
            self.direction = 56
        elif right_or_left == 3:
            self.direction = 44
        else:
            self.direction = 20

    def move(self):
        if pyxel.frame_count % 5 == 0:
            if (random.randint(0, 100) < 75):
                deplacement = random.randint(2, 4)
                if (self.x + 8 + deplacement > 128):
                    self.x -= (deplacement + 10)
                elif (self.x - deplacement < 0):
                    self.x += (deplacement + 10)
                elif (random.randint(0, 100) < self.direction):
                    self.x += deplacement
                else:
                    self.x -= deplacement
            else:
                deplacement = random.randint(2, 3)
                if (self.y - deplacement <= 16):
                    return False
                else:
                    self.y -= deplacement

class Ally(Entity):
    def __init__(self, lvl, x, y):
        super().__init__(lvl, x, y)

class Castle(Entity):
    def __init__(self, lvl, y):
        super().__init__(lvl, 0, y)
        self.height = 128
        self.width = 16

class Tower:
    cost = 10
    def __init__(self, lvl, x, y, damages, prop, proj):
        self.lvl = lvl
        self.damage = damages * lvl
        self.prop = prop
        self.proj = proj
        self.x = x
        self.y = y

    def shoot(self):
        if pyxel.frame_count % 30 == 0:
            return Proj(self.x, self.y, self.damage)

class Proj:
    def __init__(self, x, y, damage):
        self.x = x
        self.y = y
        self.damage = damage

    def move(self):
        self.y += 1



Main()
