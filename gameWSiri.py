#!/usr/bin/env python
# -*- coding: utf-8 -*-
from graphics import *
from random import randint
from math import sqrt
from client import *
import time

nrplayers = 2
player_name = ""
server = ""
score = []
players = []

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

def calc_left_point(position, width, height):
    xpos = position.getX()
    ypos = position.getY()
    return Point(xpos - width,ypos - height)

def calc_right_point(position, width, height):
    xpos = position.getX()
    ypos = position.getY()
    return Point(xpos + width,ypos + height)

def drawButton(position, win, text, color):
    left_pt = calc_left_point(position, 150, 50)
    right_pt = calc_right_point(position, 150, 50)
    R = Rectangle(left_pt, right_pt)
    R.setFill(color)
    R.draw(win)
    Text(position, text).draw(win)
    boo = False
    while(not(boo)):
        click = win.getMouse() # pause for click in window
        if(insideRectangle(left_pt, right_pt,click)):
            boo = True
        else:
            print(insideRectangle(left_pt, right_pt, click))
    R.undraw()


def drawObject(position, form_id, win):
    color = ["green", "red", "grey", "white", "black", "orange", "purple"]
    k = randint(1,len(color)-1)
    boo = False
    if form_id == 0:
        left_pt = calc_left_point(position, 100,100)
        right_pt = calc_right_point(position, 100, 100)
        R = Rectangle(left_pt, right_pt)
        R.setFill(color[k])
        R.draw(win)
        boo = False
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
        rand = 150
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


def init():
    global win
    win = GraphWin("Game", 1000, 500)

def redraw_scorebox(nrplayers):
    global playerBox, score, players
    heightbox = 20 * nrplayers
    playerBox = Rectangle(Point(0,0), Point(300,heightbox))
    playerBox.setFill('white')
    i = 0
    height = 10
    playerBox.draw(win)
    players, score = score_user_receive()
    while i < nrplayers:
        Text(Point(100,height), players[i] + " have: " + str(score[i]) + " points").draw(win)
        i += 1
        height += 20

def make_intro_win():
    global player_name, server
    win = GraphWin("start", 1000, 500)

    Text(Point((win.getWidth())/6,win.getHeight()/10), "Player name: ").draw(win)
    name_entry = Entry(Point(win.getWidth()/2,win.getHeight()/10), 50)
    Text(Point((win.getWidth())/6,2*win.getHeight()/10), "Which server?").draw(win)
    server_entry = Entry(Point(win.getWidth()/2,2*win.getHeight()/10), 50)
    name_entry.draw(win)
    server_entry.draw(win)

    drawButton(Point(win.getWidth()/2,6*win.getHeight()/10), win, "Press here to play our awesome game", "green" )

    player_name = name_entry.getText()
    server = server_entry.getText()

    win.close()
    return
#creates the goodbye window
def goodbye_win(nrplayers):
    players, score = score_user_receive()
    count = 0
    scoore = score[0]
    winner = players[0]
    while count < (nrplayers - 1):
        if score[count] < score[count + 1]:
            winner = players[count+1]
            scoore = score[count+1]
        else:
            pass
        count = count + 1
    goodbye_win = GraphWin("start", 1000, 500)
    txt = Text(Point(goodbye_win.getWidth()/2, goodbye_win.getHeight()/4), str(winner) + ' is the winner with ' + str(scoore) + ' points!!')
    txt.draw(goodbye_win)
    drawButton(Point(goodbye_win.getWidth()/2,6*goodbye_win.getHeight()/10), goodbye_win, "finnish", "green" )



def main():
    global nrplayers, player_name
    make_intro_win()
    tell_server_of_connection(player_name, server)
    init()
    i = 0
    while(i < 5):
        redraw_scorebox(nrplayers)
        obj, coord = recieve_position_and_object_from_server()
        pt = Point(int(coord[0]), int(coord[1]))
        #obj = randint(0,2) #För att testa utan server
        #pt = Point(500,500) #För att testa utan server
        drawObject(pt, int(obj), win)
        send_timestamp()
        #time.sleep(1)#För att testa utan server
        i += 1
    win.close() # optional if we want game windw to close immediatly
    goodbye_win(nrplayers)


if __name__ == "__main__":
    main()
