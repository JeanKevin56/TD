from ctypes import cast

import pyxel

class Main:
    def __init__(self):
        pyxel.init(128,128,title="Tower Defence, protect your gold")
        self.castle = Castle(100, 0,64,0, 8, 8)
        self.cave = Castle(100, 0, 64, 128-8, 8, 8)
        self.objToDraw = [self.castle, self.cave]
        self.enemy_list = []
        pyxel.run(self.update, self.draw)

    def enemyCreation(self):
        if (pyxel.frame_count % 30 == 0):
            self.enemy_list.append(Enemy(25, 10, self.cave.x, self.cave.y, 8, 8))


    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)
        for obj in self.objToDraw:
            pyxel.rect(obj.x, obj.y, obj.height, obj.width, 9)
        for enemy in self.enemy_list:
            pyxel.rect(enemy.x, enemy.y, enemy.height, enemy.width, 9)



class Entity:
    def __init__(self, pv, damage, x, y, height, width):
        self.pv = pv
        self.damage = damage
        self.x = x
        self.y = y
        self.height = height
        self.width = width

class Enemy(Entity):
    def __init__(self, pv, damage, x, y, height, width):
        super().__init__(pv, damage, x, y, height, width)


class Ally(Entity):
    def __init__(self, pv, damage, x, y, height, width):
        super().__init__(pv, damage, x, y, height, width)

class Castle(Entity):
    def __init__(self, pv, damage, x, y, height, width):
        super().__init__(pv, damage, x, y, height, width)




Main()


