from ctypes import cast
import random
import math
from math import acos

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
        self.nbDeaths = 0
        self.gold = 100

        # Obj
        self.castle = Castle(10,0)
        self.cave = Castle(10, 128-16)
        self.objWithProgBar = [self.castle, self.cave]
        self.posTextMessage  = 128

        # Entity
        self.enemy_list = []
        self.tower_list = []
        self.bullet_list = []

        # Run
        pyxel.run(self.update, self.draw)


    def enemyCreation(self):
        if pyxel.frame_count % (60/self.lvl) == 0:
            self.enemy_list.append(Enemy(1, self.cave.x + 60, self.cave.y))

    def towerCreation(self):
        if pyxel.btnr(pyxel.KEY_UP) and self.gold >= Tower.cost:
            self.gold -= Tower.cost
            self.tower_list.append(Tower(1, pyxel.mouse_x, pyxel.mouse_y, 5, "0", "kjb"))

    def collisions(self):
        for enemy in self.enemy_list:
            for bullet in self.bullet_list:
                if bullet.x >= enemy.x and bullet.x <= enemy.x + enemy.width and bullet.y >= enemy.y and bullet.y <= enemy.y + enemy.height:
                    self.deadEnemy(enemy, bullet)

    def deadEnemy(self, enemy, bullet):
        self.bullet_list.remove(bullet)
        if enemy in self.enemy_list:
            self.enemy_list.remove(enemy)
        self.gold += enemy.loot
        self.nbDeaths += 1

    def levelUp(self):
        if (self.nbDeaths % 11 == 0) and self.nbDeaths > 0:
            self.lvl +=1
            self.nbDeaths += 1


    def update(self):
        self.enemyCreation()
        self.towerCreation()
        self.collisions()
        self.levelUp()
        for enemy in self.enemy_list:
            if enemy.move() == False:
                self.castle.pv -= enemy.damage
                self.enemy_list.remove(enemy)
        for tower in self.tower_list:
            if pyxel.frame_count % 45 == 0:
                self.bullet_list.append(tower.shoot(self.enemy_list))
        for bullet in self.bullet_list:
            bullet.move()
            if bullet.target not in self.enemy_list:
                self.bullet_list.remove(bullet)


    def draw(self):
        
        pyxel.cls(0)
        if self.castle.pv < 0:
            pyxel.bltm(0, 0, 0, 0, 16*8, 256, 256)
        else:
            pyxel.bltm(0, 0, 0, 0, 0, 256, 256)
            for enemy in self.enemy_list:
                if pyxel.frame_count % enemy.time_ani == 0:
                    enemy.animation = 8
                else:
                    enemy.animation = 0
                pyxel.blt(enemy.x, enemy.y, enemy.image, enemy.props[(self.lvl-1)%5][0] + enemy.animation, enemy.props[(self.lvl-1)%5][1], 8, 8, 15, 0, enemy.scale)
            for bullet in self.bullet_list:
                pyxel.blt(bullet.x, bullet.y, 0, 16, 104, 1, 5, 0, bullet.rotation)
            for tower in self.tower_list:
                pyxel.blt(tower.x, tower.y, 0, 25, 112, 6, 8, 5)

            pyxel.rect(5, 5, 5, 5, 10)
            pyxel.text(12, 5, str(self.gold), 0)
            if self.posTextMessage > -330:
                self.start_message()
            else:
                self.progression_bare()


    def progression_bare(self):
        i = 1
        deplacement = 0
        for obj in self.objWithProgBar:
            if i == 2:
                deplacement = 7
            i+=1
            pyxel.rect(obj.x+(128/30)*10, obj.y+3+deplacement, obj.pv/100 * (128/30*10), 4, 11)
            pyxel.rectb(obj.x+(128/30)*10-1, obj.y+3+deplacement, (128/30*10)+2, 4, 0)


    def start_message(self):
        pyxel.text(self.posTextMessage, 121, "Appuyez sur la touche 'fleche du haut' pour poser des tourelles. Cout : 10 gold", 7)
        self.posTextMessage -= 1


        



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
        self.pv = 6
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
    cost = 15
    def __init__(self, lvl, x, y, damages, prop, proj):
        self.lvl = lvl
        self.damage = damages * lvl
        self.prop = prop
        self.proj = proj
        self.x = x
        self.y = y

    def shoot(self, enemy):
        bullet = Proj(self.x, self.y, self.damage)
        bullet.findCloseEnemy(enemy)
        return bullet



class Proj:
    def __init__(self, x, y, damage):
        self.x = x
        self.y = y
        self.damage = damage
        self.target = None
        self.rotation = 0

    def findCloseEnemy(self, enemys):
        dist = 1000
        for enemy in enemys:
            if (self.x - enemy.x)**2 + (self.y - enemy.y)**2 < dist:
                dist = (self.x - enemy.x)**2 + (self.y - enemy.y)**2
                self.target = enemy

    def move(self):
        if self.target != None:
            try:
                dx = (self.target.x - self.x) / math.sqrt((self.target.x - self.x) ** 2 + (self.target.y - self.y) ** 2)
            except ZeroDivisionError:
                dx = 0
            try:
                dy = (self.target.y - self.y) / math.sqrt((self.target.x - self.x) ** 2 + (self.target.y - self.y) ** 2)
            except ZeroDivisionError:
                dy = 0
            self.x += dx
            self.y += dy
            try:
                r = 1/math.sqrt(dx**2 + dy**2)
            except ZeroDivisionError :
                r = 1
            # We want to calcukate the angle made by dx and dy:
            costheta = dx/r
            sintheta = dy/r
            if costheta >= 0 and sintheta >= 0:
                theta = -acos(dx/r)+math.pi
            elif costheta >= 0 and sintheta <= 0:
                theta = acos(dx/r)
            elif costheta <= 0 and sintheta >= 0:
                theta = -acos(dx/r)
            elif costheta <= 0 and sintheta <= 0:
                theta = -acos(dx/r)+math.pi/2
            theta = theta%(2*math.pi)
            self.rotation = (theta*360)/(2*math.pi)



Main()
