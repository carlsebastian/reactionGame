#!/usr/bin/env python
# -*- coding: utf-8 -*-
from graphics import *
from random import randint
from math import sqrt
from client import *
import time

def insideCircle(circle, click):
    center = circle.getCenter()
    distance = sqrt(((click.x - center.x) ** 2) +
                    ((click.y - center.y) ** 2))
    return distance < circle.radius

def calc_left_point(position):
    randX = randint(1,500)
    randY = randint(1,500)
    xpos = position.getX()
    ypos = position.getY()
    return Point(xpos - randX,ypos - randY)

def calc_right_point(position):
    randX = randint(1,500)
    randY = randint(1,500)
    xpos = position.getX()
    ypos = position.getY()
    return Point(xpos + randX,ypos + randY)

def drawObject(position, form_id, win):
    color = ["green", "red", "grey", "white", "black", "orange", "purple"]
    k = randint(1,len(color)-1)
    if form_id == 0:
        left_pt = calc_left_point(position)
        right_pt = calc_right_point(position)
        R = Rectangle(left_pt, right_pt)
        R.setFill(color[k])
        R.draw(win)
        click = win.getMouse() # pause for click in window

        R.undraw()

    elif form_id == 1:
        C = Circle(position, 100)
        C.setFill(color[k])
        C.draw(win)
        boo = False
        while(not(boo)):
            click = win.getMouse() # pause for click in window
            if(insideCircle(C,click)):
                boo = True
            else:
                print(insideCircle(C,click))
        C.undraw()

    elif form_id == 2:
        left_pt = calc_left_point(position)
        right_pt = calc_right_point(position)
        O = Oval(left_pt, right_pt)
        O.setFill(color[k])
        O.draw(win)
        click = win.getMouse() # pause for click in window
        O.undraw()

    else:
        rand = randint(1, 300)
        leftX = position.getX() - rand
        rightX = position.getX() + rand
        topY = position.getY() - rand

        leftPt = Point(leftX, position.getY())
        rightPt = Point(rightX, position.getY())
        topPt = Point(position.getX(),topY)

        T = Polygon(topPt, rightPt, leftPt)
        T.setFill(color[k])
        T.draw(win)
        click = win.getMouse()
        T.undraw()


def init(nrplayers, points):
    win = GraphWin("Game", 1000, 1000)
    global playerBox
    heightbox = 20 * nrplayers
    playerBox = Rectangle(Point(0,0), Point(300,heightbox))
    playerBox.setFill('white')
    i = 0
    height = 10
    playerBox.draw(win)
    while i < nrplayers:
        Text(Point(100,height), "Player " + str(i+1) + " have: " + str(points) + " points").draw(win)
        i += 1
        height += 20
    return win

def main():
    nrplayers = 2
    points = 0
    tell_server_of_connection()
    win = init(nrplayers, points)
    i = 0
    while(i < 5):
        obj, coord = recieve_position_and_object_from_server()
        pt = Point(int(coord[0]), int(coord[1]))
        #obj = 1 För att testa utan server
        #pt = Point(500,500) För att testa utan server
        drawObject(pt, int(obj), win)
        send_timestamp()
        #time.sleep(4)
        i += 1

if __name__ == "__main__":
    main()
