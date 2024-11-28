#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import threading
import time



# Create your objects here.
ev3 = EV3Brick()
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
r = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)
Uss = UltrasonicSensor(Port.S4)
Cs = ColorSensor(Port.S3)
pas = Motor(Port.A, positive_direction=Direction.COUNTERCLOCKWISE)
Touch1 = TouchSensor(Port.S1)
Touch2 = TouchSensor(Port.S2)


DriveSpeedCalc = 300
DriveSpeed = DriveSpeedCalc
DriveSpeedNegated = DriveSpeed * (-1)
Zluta = 60

r.settings(-100000, 1000, 300, 400)


#=====FUNKCE===========================================================================================
def End():
    wait(90*1000)


def Wait(cas):
    wait(cas)


def Nabirani():
    global DriveSpeedNegated
    global DriveSpeed
    global DriveSpeedCalc
    global Aktivovano
    Aktivovano = True
    DriveSpeed = DriveSpeedCalc / 2.5
    DriveSpeedNegated = DriveSpeed * (-1)
    pas.run_until_stalled(10000, Stop.COAST,100)
    pas.run_until_stalled(-10000, Stop.HOLD, 100)
    DriveSpeed = DriveSpeedCalc
    DriveSpeedNegated = DriveSpeed * (-1)
    Aktivovano = False


def Wfollow(Distance):
    global DriveSpeedNegated
    global DriveSpeed
    global DriveSpeedCalc
    DriveSpeedNegated = DriveSpeed * (-1)
    while Touch1.pressed() == False:

        while 60 <= Cs.reflection():
            if Touch1.pressed():
                break

            if (Distance - 70) < Uss.distance() < Distance:
                r.drive(DriveSpeedNegated, -20)
                ev3.speaker.beep(100, 10)
            else:
                r.drive(DriveSpeedNegated, 15)
                wait(10)
               
        thread = threading.Thread(target=Nabirani)
        thread.start()
        while 60 <= Cs.reflection():
            wait(1)
    r.stop()
    r.straight(-20)



def WfollowCount(Distance):
    wait(200)
    global DriveSpeedNegated
    global DriveSpeed
    global DriveSpeedCalc
    DriveSpeed = 230

    DriveSpeedNegated = DriveSpeed * (-1)

    for i in range(3):
        
        while 20 <= Cs.reflection():
            if Touch1.pressed():
                return

            if (Distance - 70) < Uss.distance() < Distance:
                r.drive(DriveSpeedNegated, -15)
                ev3.speaker.beep(100, 10)
            else:
                r.drive(DriveSpeedNegated, 7)

        
        thread = threading.Thread(target=Nabirani)
        thread.start()
        ev3.speaker.beep(1000,200)
        wait(50)


CaryCount = 0

def isYellow(rgb):
    return Zluta > rgb[2]

def ThirdRun():
    global DriveSpeedNegated
    global DriveSpeed
    global DriveSpeedCalc
    global CaryCount
    global Aktivovano
    while CaryCount < 3:
        if Aktivovano == False:
            DriveSpeedNegated = DriveSpeed * (-1)


        if 30 >= Cs.reflection():
            DriveSpeedNegated = DriveSpeed / (-5)
            r.drive(DriveSpeedNegated, -5)
            thread = threading.Thread(target = Nabirani)
            thread.start()
            CaryCount = CaryCount + 1
            wait(500)



        if Touch2.pressed() == True:
            r.drive(-80, 60)
            ev3.speaker.beep(800,1)
        else:
            r.drive(-250, -20)
            wait(1)




def RunToBall(Distance):
    global DriveSpeedNegated
    global DriveSpeed
    global DriveSpeedCalc
    global deviation
    DriveSpeed = 160
    PROPORTIONAL_GAIN = 1
    DriveSpeedNegated = DriveSpeed * (-1)
    deviation = 0
    for i in range(2):
        while not isYellow(Cs.rgb()):
            while Zluta < Cs.rgb()[2]:
                if Touch1.pressed():
                    return
                if (Distance - 50) < Uss.distance() and (Distance + 50) > Uss.distance():              
                    deviation = Uss.distance() - Distance
                    TurnRate = PROPORTIONAL_GAIN * deviation
                    ev3.screen.clear()
                    ev3.screen.print(deviation)
                    r.drive(DriveSpeedNegated, TurnRate)
                ev3.speaker.beep(100,100)
                TurnRate = PROPORTIONAL_GAIN * deviation
                r.drive(DriveSpeedNegated, TurnRate)

def PasDolu():
    pas.run_until_stalled(10000, Stop.COAST,100)
  
def PasNahoru():
    pas.run_until_stalled(-10000, Stop.COAST,100)

#======CODE========================================================================================

'''

while True:
    ev3.screen.print(Cs.rgb()[2])

'''
'''r.drive
for i in range(2):
    while Cs.reflection() > 50:
        r.drive(-80, 0)
    thread = threading.Thread(target = Nabirani)
    thread.start()
    ev3.speaker.beep(100,50)

'''
while not Touch2.pressed():
    wait(10)


pas.run_until_stalled(-1000000, Stop.HOLD, 150)
thread = threading.Thread(target = Nabirani)
thread.start()

r.drive(-130, 0)
wait(50)

ev3.speaker.play_notes(['C4/4', 'E4/4', 'G4/4'], 300)

WfollowCount(444)
wait(150)
r.stop()


#---------------------------------------------------PRVNI RADA HOTOVA---

r.straight(-60)
r.turn(-140)
pas.run_until_stalled(-10000, Stop.HOLD, 90)
r.straight(250)

r.drive(-100,0)
while True:
    count=0
    while (Cs.rgb()[2]) < Zluta and count <2 :
        print("Zluta")
        count = count + 1
    # wait(3)
    # if (Cs.rgb()[2]) < Zluta:
    #     break
    if count == 2:
        break

r.stop(Stop.HOLD)
thread = threading.Thread(target=Nabirani)
thread.start()
r.turn(-160)

ev3.speaker.beep(100, 100)
while not (330 <= Uss.distance()):
    r.turn(-3)
r.stop()

WfollowCount(325)
#-------------------------------------------------DRUHA RADA HOTOVA---
while Touch1.pressed == False:
    r.drive(100,0)
r.stop()
r.straight(-40)
r.turn(155)
ev3.speaker.beep(1000,5)
if Touch2.pressed():
    r.turn(-20)
r.straight(100)
while True:
    while (Cs.rgb()[2]) > Zluta:
        r.drive(-300,-12)
        if Touch2.pressed():
            r.drive(-40, 40)
            ev3.speaker.beep(300, 2)

        
    wait(3)
    if (Cs.rgb()[2]) < Zluta:
        break

r.straight(20)
thread = threading.Thread(target=Nabirani)
thread.start()

r.turn(155)
ev3.speaker.beep(100,100)

ThirdRun()
r.stop()
#------------------------------------------------------------TRETI RADA HOTOVA
r.turn(-40)
r.straight(30)
ev3.speaker.beep(300,2000)
#----------------------------------------------------prvni zasobnik vysypany

r.straight(-100)


r.turn(220)
r.drive(400,0)
thread = threading.Thread(target=PasDolu)
thread.start()
wait(1200)           #zacouva ke stene

r.drive(-300,0)         #jede az na cernou
while Cs.reflection() > 50:
    wait(2)
r.stop(Stop.COAST)
r.straight(190)

pas.run_until_stalled(-10000, Stop.COAST, 100)
pas.run_until_stalled(-10000, Stop.COAST, 100)
r.straight(-100)
r.turn(260)
r.drive(-300,0)
"""
while Uss.distance() > 40:
    wait(10)
while Uss.distance() < 40:
    r.turn(-10)

while  50 < Cs.reflection():
    if Touch2.pressed() == True:
            r.drive(-250, 60)
            ev3.speaker.beep(800,1)
    else:
        r.drive(-500, -15)

r.turn(170)
r.drive(300,0)
wait(1500)
r.stop()

ev3.speaker.beep(300,300)
r.straight(50)
CaryCount = 0
while not CaryCount == 2:
    r.drive(-300, 12)
    
    if 300 > Uss.distance():
        r.drive(-120, -40)
        ev3.speaker.beep(300, 2)
    
    if Zluta > Cs.rgb()[2]:
        r.straight(10)
        CaryCount = CaryCount + 1

pas.run_until_stalled(10000, Stop.COAST, 90)
r.straight(50)
RunToBall(615)
r.straight(190)

pas.run_until_stalled(-10000, Stop.COAST, 100)
pas.run_until_stalled(-10000, Stop.COAST, 100)
#-----------------------------------------------Nabrany basketbl
r.straight(-30)
r.turn(175)
r.straight(100)
while True:
    while (Cs.rgb()[2]) > Zluta:
        r.drive(-300, -15)
        if 40 > Uss.distance():
            r.drive(-160, 20)
            ev3.speaker.beep(300, 100)
    wait(3)
    if (Cs.rgb()[2]) < Zluta:
        if Cs.reflection() > 30:
            break


wait(400)
r.stop()

thread = threading.Thread(target=Nabirani)
thread.start()
r.turn(-230)
"""

ev3.speaker.beep(1000, 1000)
r.straight(300)
r.reset()
while Uss.distance() > 170 and r.distance() > (-300):
    r.drive(-1000, 0)

    ev3.speaker.beep(1000, 10)
r.stop()
r.drive(-300, 20)
    
ev3.speaker.beep(500, 5000) 