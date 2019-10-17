from tkinter import *
from random import randrange as rnd, choice
import time
import math


root = Tk()
root.geometry('800x600')

canv = Canvas(root, bg='white')
canv.pack(fill=BOTH, expand=1)
pi = 3.1415926
colours = ["red", "green", "orange", "blue"]


class boll:
    """Шары, которые движутся по прямой, случайно отражаются от стенок и стоят одно очко"""
    x = 0
    y = 0
    r = 0
    d_boll = canv.create_oval(0, 0, 0, 0)    # Сокращение от Drawn Boll - вид объекта
    speed = 0.0
    destanation = 0.0   # Это угол, отложенный от Ox Canvas к Oy
    alive = 0
    def __init__(self, r, x, y, colour, speed, destanation):
        self.d_boll = canv.create_oval(x - r, y - r, x + r, y + r,fill=colour)
        self.r = r
        self.speed = speed
        self.destanation = destanation
        self.x = x
        self.y = y
        self.alive = 1
        self.moving()
         
    def moving(self):
        """Движение шара. Скорость и направление определены соответствующими полями класса"""
        canv.move(self.d_boll, self.speed*math.cos(self.destanation), self.speed*math.sin(self.destanation))
        self.x += self.speed*math.cos(self.destanation)
        self.y += self.speed*math.sin(self.destanation)
        if self.x + self.r > 800:
            self.rand_turn_back("vertical_right")      # случаи встречи со стенками
        if self.x - self.r < 0:
            self.rand_turn_back("vertical_left")
        if self.y + self.r > 600:
            self.rand_turn_back("horizontal_bottom")
        if self.y-self.r < 0:
            self.rand_turn_back("horizontal_top")
        if self.alive:
            root.after(10, self.moving)

    def rand_turn_back(self, stop):
        """Случайное отражение от стенки"""
        if stop == "vertical_right":
            self.destanation = choice([1, -1]) * rnd(650, 950) / 1000 * pi
        if stop == "vertical_left":
            self.destanation = choice([1, -1]) * rnd(50, 450) / 1000 * pi
        if stop == "horizontal_bottom":
                self.destanation = -rnd(100, 900) / 1000 * pi
        if stop == "horizontal_top":
                self.destanation = rnd(100, 900) / 1000 * pi

    def is_clicked(self,event):
        """Возвращает полученные очки при попадании мышкой на шар и прячет кликнутый шар"""
        if (self.x - event.x)**2 + (self.y - event.y)**2 <= self.r**2 and self.alive == 1:
            self.alive = 0
            canv.delete(self.d_boll)
            return(1)
        else:
            return(0)


class not_boll:
    """Квадраты, которые движутся по окружностям, отражаются зеркально, вращаются вокруг своей оси и постепенно уменьшают размер
       и стоимость с 6 до 0"""
    x = 0
    y = 0
    r = 0
    d_not_boll = canv.create_polygon(0,0)
    speed = 0.0
    destanation = 0.0
    alive = 0
    colour = ""
    rot = 0
    
    def __init__(self, r, x, y, colour, speed, destanation):
        self.colour = colour
        self.r = r
        self.speed = speed
        self.destanation = destanation
        self.x = x
        self.y = y
        r0 = r * 2**(-0.5)
        self.d_not_boll = canv.create_polygon(x - r0, y - r0, x + r0, y - r0, x + r0, y + r0, x - r0, y + r0, fill=colour)
        self.alive = 6
        self.rot = pi / 4
        self.moving()
        self.rotating()
        root.after(1000, self.melting)
        
    def moving(self):
        """Движение квадрата по дугам окружностей"""
        canv.move(self.d_not_boll, self.speed*math.cos(self.destanation), self.speed*math.sin(self.destanation))
        self.x += self.speed*math.cos(self.destanation)
        self.y += self.speed*math.sin(self.destanation)
        self.destanation += pi/200
        if self.x + self.r > 800 or self.x - self.r < 0:
            self.turn_back("vertical")
        if self.y + self.r > 600 or self.y - self.r < 0:
            self.turn_back("horizontal")
        if self.alive:
            root.after(10, self.moving)

    def rotating(self):
        """Вращение квадрата изменением атрибута поворота относительно оси симметрии и перерисовыванием"""
        if self.alive:
            self.rot += 2 * pi / 30
            r = self.r
            x = self.x
            y = self.y
            rcos = r * math.cos(self.rot)
            rsin = r * math.sin(self.rot)
            canv.delete(self.d_not_boll)
            self.d_not_boll = canv.create_polygon(x - rcos, y - rsin, x + rsin, y - rcos, x + rcos, y + rsin, x - rsin, y + rcos, fill=self.colour)
            root.after(100, self.rotating)
        
    def turn_back(self, stop):
        """Зеркальное отражение"""
        if stop == "vertical":
            self.destanation = pi - self.destanation
        if stop == "horizontal":
                self.destanation =- self.destanation

    def melting(self):
        """Уменьшение со временем квадрата и даваемых за него очков"""
        if self.alive:
            self.r /= 1.5
            self.alive -= 1
            root.after(1000, self.melting)

                
    def is_clicked(self,event):
        """Возвращает полученные очки при попадании мышкой на квадрат и прячет кликнутый квадрат"""
        if (self.x - event.x)**2 + (self.y - event.y)**2 <= 2 * self.r**2 and self.alive:
            cost = self.alive
            self.alive = 0
            canv.delete(self.d_not_boll)
            return(cost)
        else:
            return(0)


class bolls_and_not_union:
    """Класс, создающий и удаляющий мишени, обрабатывающий события мыши и считающий очки"""
    list_of_bolls = []
    list_of_not_bolls = []
    score = 0
    finished = 0
    def __init__(self):
        for i in range(5):
            self.list_of_bolls.append(boll(rnd(100, 400) / 10, rnd(100, 700), rnd(100, 500), choice(colours), rnd(1000, 7000) / 1000, rnd(0,1001) / 1000 * 2 * pi))
        for i in range(3):
            self.list_of_not_bolls.append(not_boll(rnd(400, 900) / 10, rnd(100, 700), rnd(100, 500), choice(colours), rnd(1000, 7000) / 1000, rnd(0, 1001) / 1000 * 2 * pi))
        self.score = 0
        self.change()

    def change(self):
        """Замена мишеней"""
        canv.delete(self.list_of_bolls[0].d_boll)
        self.list_of_bolls[0].alive = 0
        for i in range(4):
            self.list_of_bolls[i] = self.list_of_bolls[i+1]
        self.list_of_bolls[4] = boll(rnd(100, 400) / 10, rnd(100, 700), rnd(100, 500), choice(colours), rnd(1000, 7000) / 1000, rnd(0, 1001) / 1000 * 2 * pi)
        canv.delete(self.list_of_not_bolls[0].d_not_boll)
        self.list_of_not_bolls[0].alive = 0
        for i in range(2):
            self.list_of_not_bolls[i] = self.list_of_not_bolls[i+1]
        self.list_of_not_bolls[2] = not_boll(rnd(100, 400)/10, rnd(100, 700), rnd(100, 500), choice(colours), rnd(1000, 7000) / 1000, rnd(0, 1001) / 1000 * 2 * pi)
        if not self.finished:
            root.after(2000, self.change)
            
    def are_clicked(self, event):
        """Распределение события клика между мишенями и подсчёт очков"""
        for i in self.list_of_bolls:
            self.score += i.is_clicked(event)
        for i in self.list_of_not_bolls:
            self.score += i.is_clicked(event)
            self.score += i.is_clicked(event)
        print(self.score)
        
        
a = bolls_and_not_union()
canv.bind('<Button-1>', a.are_clicked)

mainloop()
