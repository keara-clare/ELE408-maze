# draw.py
# # apt-get install python-pygame  or pip install pygame
import socket                   # Import socket module
import time
import pygame
import Adafruit_ADXL345
import sys
pygame.init()
accel = Adafruit_ADXL345.ADXL345(address=0x53, busnum=0)

#Variables
#Colors
WHITE = (255,255,255)
RED = (255, 0, 0)
BLACK = (0,0,0)
GREEN = (30, 105, 53)
GOLD = (255, 215, 0)
#Sizes
size = width, height = 800, 480
screen = pygame.display.set_mode(size)
#Directions
DOWN = 0
LEFT = 0
RIGHT = 0
UP = 0
#Drawings
theDrawing = []
Drawings = []
#Levels
Level = 1	#start at level 1
#coordinates
xc = 50		#x-coordinate (starting position)
yc = 50		#y-coordinate (starting position)
color = RED
clock = pygame.time.Clock()
#Create a timer
seconds = 0
minutes = 0
#Counter
count = 0
#goal coordinates
goal = (0,0)
#Points
Points = 75

def updatePoints():
  a, b, c = accel.read()
  #print('X={0}, Y={1}'.format(a, b))
  if a > 2:
    RIGHT = 1
  else: 
    RIGHT = 0
  if a < -3:
    LEFT = 1
  else: 
    LEFT = 0
  if b < -10:
    DOWN = 1
  else:
    DOWN = 0
  if b > -4:
    UP = 1
  else:
    UP = 0
  return DOWN, LEFT, RIGHT, UP

def arithmetic(x,y):
  x = abs(x)
  x = x * 3.2
  x = round(x,0)
  x = int(x)
  y = abs(y)
  y = y * 1.75
  y = round(y,0)
  y = int(y)
  return x,y

def drawBorder():
    lineThickness = 20
    #m, n = 800, 480
    #for i in range(m):
      #for j in range(n):
    points = [(1,1), (1,479), (799,479), (799,1), (1,1)]
    pygame.draw.lines(screen, BLACK, False, points, lineThickness)
def Lvl1Maze(): 
    lineThickness = 20
    #m, n = 800, 480
    #for i in range(m):
      #for j in range(n):
    points = [(80,1), (80,380), (160,380), (160,80), (200,80)]
    pygame.draw.lines(screen, GREEN, False, points, lineThickness)
def Goal():
    goal = (120,350)
    pygame.draw.circle(screen, GOLD, goal, 15)
    
while (True):
  time_start = time.time()
  sys.stdout.write("\r{minutes} Minutes {seconds} Seconds".format(minutes=minutes, seconds=seconds))
  sys.stdout.flush()
  time.sleep(1)
  seconds = int(time.time() - time_start) - minutes * 60
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit(); sys.exit();

    constant = 1
    time_start = time.time()
    #Start position of Marble
    x = 15
    y = 15
    while constant %1==0:
        #start game timer for points
        seconds = int(time.time() - time_start) - minutes * 60
        #Reset Screen
        screen.fill(WHITE)
        drawBorder()
        Lvl1Maze()
        Goal()
        #update circle
        print('X={0}, Y={1}'.format(x, y))
        if DOWN == 1:
          y += 5
        if UP == 1:
          y -= 5
        if RIGHT == 1:
          x += 5
        if LEFT == 1:
          x-= 5
        
        pygame.draw.circle(screen,color,(x,y), 15)
        DOWN, LEFT, RIGHT, UP = updatePoints()
        print(DOWN)

        #x,y = arithmetic(x,y)
        print("Points =",Points)
        print("Seconds =", seconds)
        if seconds%10 == 0:
          Points += 1
        pygame.display.flip()
        time_elapsed = (time.time() - time_start)
        print(time_elapsed)
        #time.sleep(0.20)
        time.sleep(0.1)

#######SOCKET Portion###############   	
s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
port = 40000                    # Reserve a port for your service.

s.connect(('131.128.49.109', port))
# Try get some sleep
time.sleep(3)
filename='screenshot.png'
f = open(filename,'rb')
l = f.read(1024)
while (l):
  s.send(l)
  l = f.read(1024)
f.close()

print('Done sending')
s.close()
print('connection closed')
