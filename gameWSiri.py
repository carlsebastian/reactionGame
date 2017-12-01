#!/usr/bin/env python
# -*- coding: utf-8 -*-
from graphics import *
from random import randint
from math import sqrt
from client import *
import time

nrplayers = 2
points = 0
player_name = ""
server= ""

def insideCircle(circle, click):
    center = circle.getCenter()
    distance = sqrt(((click.x - center.x) ** 2) +
                    ((click.y - center.y) ** 2))
    return distance < circle.radius

def insideRectangle(left_pt, right_pt, click):
    leftX = left_pt.getX()
    leftY = left_pt.getY()
    rightX = right_pt.getX()
    rightY = right_pt.getY()

    if (leftX <= click.x <= rightX and leftY <= click.y <= rightY):
        return True
    else:
        return False

def areaOfTraingle(lx,ly,rx,ry,tx,ty):
    return abs(((1.0/2.0)*(lx*(ry-ty) + rx*(ty-ly) + tx*(ly-ry))))

def insideTriangle(left_pt, right_pt, top_pt, click):
    leftX = left_pt.getX()
    leftY = left_pt.getY()
    rightX = right_pt.getX()
    rightY = right_pt.getY()
    topX = top_pt.getX()
    topY = top_pt.getY()

    A  = areaOfTraingle(leftX, leftY, rightX, rightY, topX, topY)
    A1 = areaOfTraingle(click.x, click.y, rightX, rightY, topX, topY)
    A2 = areaOfTraingle(leftX, leftY, click.x, click.y, topX, topY)
    A3 = areaOfTraingle(leftX, leftY, rightX, rightY, click.x, click.y)
    return (A == (A1 + A2 + A3))

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
    boo = False
    if form_id == 0:
        left_pt = calc_left_point(position)
        right_pt = calc_right_point(position)
        R = Rectangle(left_pt, right_pt)
        R.setFill(color[k])
        R.draw(win)
        while(not(boo)):
            click = win.getMouse() # pause for click in window
            if(insideRectangle(left_pt, right_pt,click)):
                boo = True
            else:
                print(insideRectangle(left_pt, right_pt, click))
        R.undraw()

    elif form_id == 1:
        C = Circle(position, 100)
        C.setFill(color[k])
        C.draw(win)
        while(not(boo)):
            click = win.getMouse() # pause for click in window
            if(insideCircle(C,click)):
                boo = True
            else:
                print(insideCircle(C,click))
        C.undraw()

    else:
        rand = randint(1, 300)
        leftX = position.getX() - rand
        rightX = position.getX() + rand
        topY = position.getY() - rand

        left_pt = Point(leftX, position.getY())
        right_pt = Point(rightX, position.getY())
        top_pt = Point(position.getX(),topY)

        T = Polygon(top_pt, right_pt, left_pt)
        T.setFill(color[k])
        T.draw(win)
        while(not(boo)):
            click = win.getMouse() # pause for click in window
            if(insideTriangle(left_pt, right_pt, top_pt, click)):
                boo = True
            else:
                print(insideTriangle(left_pt, right_pt, top_pt, click))
        T.undraw()


def init(nrplayers, points):
    win = GraphWin("Game", 1000, 500)
    global playerBox
    heightbox = 20 * nrplayers
    playerBox = Rectangle(Point(0,0), Point(300,heightbox))
    playerBox.setFill('white')
    i = 0
    height = 10
    playerBox.draw(win)

    players, score = score_user_receive()


    while i < nrplayers:
        Text(Point(100,height), players[i] + " have: " + str(points) + " points").draw(win)
        i += 1
        height += 20
    return win

def make_intro_win():
    global player_name, server
    win = GraphWin("start", 1000, 500)

    Text(Point((win.getWidth())/6,win.getHeight()/10), "Player name: ").draw(win)
    name_entry = Entry(Point(win.getWidth()/2,win.getHeight()/10), 50)
    Text(Point((win.getWidth())/6,9*win.getHeight()/10), "Which server?").draw(win)
    server_entry = Entry(Point(win.getWidth()/2,9*win.getHeight()/10), 50)
    name_entry.draw(win)
    server_entry.draw(win)

    win.getMouse()
    win.close()
    player_name = name_entry.getText()
    server = server_entry.getText()
    return

def main():
    global nrplayers, points, player_name, server
    make_intro_win()
    tell_server_of_connection(player_name, server)
    win = init(nrplayers, points)
    i = 0
    while(i < 5):
        obj, coord = recieve_position_and_object_from_server()
        pt = Point(int(coord[0]), int(coord[1]))
        #obj = randint(0,2) #För att testa utan server
        #pt = Point(500,500) #För att testa utan server
        drawObject(pt, int(obj), win)
        send_timestamp()
        #time.sleep(1)#För att testa utan server
        i += 1

if __name__ == "__main__":
    main()
