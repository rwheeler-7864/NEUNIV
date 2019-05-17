#Josh Fish
#import all the libraries needed
#import RealTrafficArraycolM which does the wiring for you
from LightArray import *
from RealTrafficArraycolM import *
import random
import time
import pymsgbox as pymsgbox
import threading
import pygame
import pygame.camera
import httplib
import urllib
import base64
import operator
import requests
import json
import sys
from PIL import Image

headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '0bf3ef41437e4dbd8e170baa320287f2', #new key 5_16
    
    #'Ocp-Apim-Subscription-Key': '5ed07c17-0ddc-424b-be85-1502e4ed9f84', #new key 2_15
    #'Ocp-Apim-Subscription-Key': 'aa173f203feb4db8af7ac95d792f21d7', # new key 1 changed 3.19
    #'Ocp-Apim-Subscription-Key': '7ffa4f355bb8428183d2923e9c3642d3', # new key 2
}
params = urllib.urlencode({})
#NUMBER OF COLUMNS AND ROWS
NUMCOL=8
NUMROW=9

#turns off all the lights
def clearArray(array):
    w = array.getWidth()
    h = array.getHeight()
    for x in range(w):
        for y in range(h):
            array.turnOff(x, y)
# given an array, and a number for green,yellow, and red
# which is how many of that color you want to light up
# uses random so it doesn't light up the same spots everytime
def trafficSubset(array, green, yellow, red):
    w = array.getWidth()
    h = array.getHeight()
    color = green
    for y in range(h):
        if y % 3 == 0:
            color = green
        elif y % 3 == 1:
            color = yellow
        else:
            color = red
        for x in random.sample(range(w), color):
            array.turnOn(x, y)
#given an array and an emotion number, turns on the required lights
def setEmotion(a, e):
    clearArray(a)    
    if e == 1:
        trafficSubset(a, NUMCOL, 0, 0)# turns on all the red lights
        runPatterns(a,0);#run patterns for solid red rows
    elif e == 2:
        trafficSubset(a, NUMCOL, 1, 0)
        runPatterns(a,0);#run patterns for solid red rows
    elif e == 3:
        trafficSubset(a, 5, 3, 0)            
    elif e == 4:
        trafficSubset(a, 2, NUMCOL, 0)
        runPatterns(a,1);#run patterns for solid yellow rows
    elif e == 5:
        trafficSubset(a, 0, NUMCOL, 0)#turns on all the yellow lights
        runPatterns(a,1);#run patterns for solid yellow rows
    elif e == 6:
        trafficSubset(a, 0, NUMCOL, 2)
        runPatterns(a,1);#run patterns for solid yellow rows
    elif e == 7:
        trafficSubset(a, 0, 3, 5)            
    elif e == 8:
        trafficSubset(a, 0, 1, NUMCOL)
        runPatterns(a,2);#run patterns for solid green rows
    elif e == 9:
        trafficSubset(a, 0, 0, NUMCOL)#turns on all the green lights
        runPatterns(a,2);#run patterns for solid green rows
        
#uses pygame to get the image from the camera       
def getImage(cam):
        print "1"
        img = cam.get_image()
        print "2"
        pygame.image.save(img,"filename.jpg")
        print "3"
        return open('filename.jpg', 'r')
#uses microsoft api to get emotion, returns emotion in qoutes
def getEmotion(image):
        try:
            conn = httplib.HTTPSConnection('api.projectoxford.ai')
            print("[Connected to api]")
            conn.request("POST", "/emotion/v1.0/recognize?%s" % params, image, headers)
            print("[Sent request]")
            response = conn.getresponse()
            print("[Recieved response]")
            data = response.read()
            conn.close()
        except Exception as e:
            print("network error")
            exit(1)
        
        if len(json.loads(data)) > 0:
                #print(data)
                jdata = json.loads(data)[0]
                max_emotion = max(jdata['scores'].iteritems(), key=operator.itemgetter(1))[0]
                return max_emotion
        else:
                return 'neutral'
            
#4 behaviors to run when a full bar is lit up
def leftToRight(array, row):
    w = array.getWidth()
    for x in range(0,w):
        array.turnOff(x,row)
        time.sleep(0.2)
        array.turnOn(x,row)
def rightToLeft(array, row):
    w = array.getWidth()
    for x in range(w-1,-1,-1):
        array.turnOff(x,row)
        time.sleep(0.2)
        array.turnOn(x,row)

def middleOut(array, row):
    m = 3 #middle of the array
    for a in range(0,m+1):# need to change this due to the number of columns being 8 now instead of 7
        array.turnOff(m+a,row)
        array.turnOff(m-a,row)
        time.sleep(0.2)
        array.turnOn(m+a,row)
        array.turnOn(m-a,row)
def outMiddle(array, row):
    last = array.getWidth()-1
    for a in range(0,4): # 4 is the number of iterations required to reach the middle of the array
        array.turnOff(last-a,row)
        array.turnOff(0+a,row)
        time.sleep(0.2)
        array.turnOn(last-a,row)
        array.turnOn(0+a,row)
def fullBarPattern(array,row):
    #pick and run random behavior for a full bar of color
    rand = random.randint(1,4)
    if(rand==1):
        leftToRight(array,row)
    elif(rand==2):
        rightToLeft(array,row)
    elif(rand==3):
        middleOut(array,row)
    elif(rand==4):
        outMiddle(array,row)
def runPatterns(a,startRow):
    #run patterns for all 3 rows of lights of the same color
    fullBarPattern(a,startRow)
    time.sleep(1)
    fullBarPattern(a,startRow+3)
    time.sleep(1)
    fullBarPattern(a,startRow+6)
    time.sleep(1)

        
#5 behaviors
def randomLightOn(array):
    w = array.getWidth()
    h = array.getHeight()
    x =random.randint(0,w) #random number between 0 and the width of array
    y =random.randint(0,h) #random number between 0 and the height of array
    array.turnOn(x,y) #turn on light that is at rand x,y coord
    time.sleep(0.005) #delay for 0.015s
def cycleRow(array):
    w = array.getWidth()
    h = array.getHeight()
    for y in range(0,h):
        time.sleep(0.1)
        clearArray(array)
        for x in range(0,w):
            array.turnOn(x,y)
def cycleColumn(array):
    w = array.getWidth()
    h = array.getHeight()
    for x in range(0,w):
        time.sleep(0.1)
        clearArray(array)
        for y in range(0,h):
            array.turnOn(x,y)
def OneAtATime(array):
    w = array.getWidth()
    h = array.getHeight()
    clearArray(array)
    #randstart = random.randint(0,w)

    for x in range(0,w):
        for y in range(0,h):
            array.turnOn(x,y)
            time.sleep(0.03)
            array.turnOff(x,y)

#can be commented out if not fixed, was built with odd number of coloumns            
def boxPattern(array):
    for l in range (1,10):
        x = 3 #these values should be in the middle of the array
        y = 4
        change= l-1
        for a in range (y-change,y+change+1):
            for b in range(x-change,x+change+1):
                array.turnOn(b+1,a)
                array.turnOn(b,a)
        for a in range (y-change+1,y+change):
            for b in range(x-change+1,x+change):
                array.turnOff(b+1,a)
                array.turnOff(b,a)
        time.sleep(0.1)
        clearArray(array)
#lights up a random square burst       
def randomBurst(array):
    numBursts=10
    for num in range(0,numBursts):
        time.sleep(1)
        clearArray(array)
        w = array.getWidth()
        h = array.getHeight()
        x =random.randint(1,w-2)
        y =random.randint(1,h-2)
        array.turnOn(x,y)
        time.sleep(0.2)
        for a in range (y-1,y+2):
                for b in range(x-1,x+2):
                    array.turnOn(b,a)
                    array.turnOn(b,a)
        array.turnOff(x,y)

def processCam(cam, i):
    print("processing cam{}".format(i))
    img = getImage(cam)
    print "[got image]"
    emotion = getEmotion(img)
    return emotion
        
#Code starts running here

#NOTE: uncomment this and the code in the while loop to display images
#pygame.init()
#height = 480
#width = 640
#screen = pygame.display.set_mode((width, height))

pygame.camera.init()
camList = pygame.camera.list_cameras() #Cameras detected
print(camList)
CAMS = []
# Set up all of the available cameras
for cam in camList:
    CAMS.append(pygame.camera.Camera(cam, (640,480)))
for cam in CAMS:
    cam.start()

a = RealTrafficArray() # instantiate traffic light array
emo=5 # set the main emotion to neutral
e=5 #set the background emotion to neutral
TIMEDELAY=2*len(CAMS)#used below and explained
while True:
        # get the emotion here , set variable emotion = to it
        clearArray(a)
        timeOnEmotion= 4 #number of times the camera/microsoft gets an emotion
        #and updates the background state before changing the main state
        
        for t in range(timeOnEmotion/len(CAMS)):
                setEmotion(a,emo)#set emotion to the main state
                emotions = []
                for i, cam in enumerate(CAMS): # process each camera and add emotion to list
                    emotions.append(processCam(cam, i))
                
                #NOTE: uncomment this section and some code above to display the image in a window.
                #display_img = pygame.image.load('filename.jpg')
                #print(display_img)
                #screen.blit(display_img, (0, 0))
                #pygame.display.flip()

                for emotion in emotions:
                    #check what the new emotion if, and based on this change the background state of the emotion        
                    if emotion.strip() == 'happiness': 
                            e += 1
                    elif emotion.strip() != 'neutral':
                            e -= 1
                    if e < 1:#account for overflow
                       e = 1
                    elif e >= 9:
                        e = 9
                    print(emotion)
                    
                #print to the terminal the final emotion calculated, the main state being displayed, and the background state    
                print(emo)
                print(e)

                time.sleep(TIMEDELAY)# THIS VALUE OF TIMEDELAY IS WHAT DEALS WITH THE USAGE MICROSOFT CAN HANDLE
                #SO BASICALLY SINCE IT IS RUNNING 8 TIMES IT TAKES about 16 seconds between main emotion state switches

        #update the emoption to be displayed based on average of emotions over time    
        emo=e
       
        print("")
        print("a new emotion was set")
        print("")

        
        #pick and run random behavior for inbetween state
        rand = random.randint(1,5)
        if(rand==1):
                for x in range(400):#turns on all lights randomly
                        randomLightOn(a)
        elif(rand==2):
                cycleRow(a)
                cycleRow(a)
                clearArray(a)
        elif(rand==3):
                cycleColumn(a)
                cycleColumn(a)
                clearArray(a)
        elif(rand==4):
                OneAtATime(a)
                OneAtATime(a)
                clearArray(a)
        elif(rand==5):
                randomBurst(a)
                randomBurst(a)
                clearArray(a)
                



