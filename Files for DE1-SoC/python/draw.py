# draw.py
# # apt-get install python-pygame  or pip install pygame
import socket                   # Import socket module
import time
import pygame
import Adafruit_ADXL345
pygame.init()
accel = Adafruit_ADXL345.ADXL345(address=0x53, busnum=0)

WHITE = (255,255,255)
RED = (255, 0, 0)
BLACK = (0,0,0)
size = width, height = 800, 480
screen = pygame.display.set_mode(size)
LEFT = 1
RIGHT = 3
MID = 2
theDrawing = []
Drawings = []
down = 0
level = 1	#start at level 1
xc = 50		#x-coordinate (starting position)
yc = 50		#y-coordinate (starting position)
debugCount = 30
print('Printing X, Y, Z axis values, press Ctrl-C to quit...')
while True:
    # Read the X, Y, Z axis acceleration values and print them.
    x, y, z = accel.read()
    print('X={0}, Y={1}, Z={2}'.format(x, y, z))
    # Wait half a second and repeat.
    time.sleep(0.5)
    for event in pygame.event.get():
        screen.fill(WHITE)
        x,y = pygame.mouse.get_pos()
	pygame.draw.circle(screen,BLACK,(xc,yc), 15)
	#xc = xc + 20
	#yc = yc + 20
	#if x > tempx+5
	    #pygame.draw.circle(screen,BLACK,(x+100,y), 20)

	###### maps gyro x to coordinate x ###############

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
            Drawings = []
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:	#tapping board
            down = 1
	    x, y, z = accel.read()
            x,y = pygame.mouse.get_pos()
	    pygame.draw.circle(screen,BLACK,(x,y), 20)
	    debugCount = debugCount + 10
	    print('debug count =', debugCount)
        if down == 1:
            theDrawing.append([x,y])
	    pygame.draw.circle(screen,BLACK,(x,y), 20)
            try:
                pygame.draw.lines(screen,RED,False,theDrawing,15)
            except:
                donothing = "do nothing"
        if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
            down = 0
            Drawings.append(theDrawing)
            theDrawing = []
	#if level==1:
		#print('Level 1')
	#if level==2:
		#print('Level 2')
      #  try:
         #   for drawing in Drawings:
          #      pygame.draw.lines(screen,BLACK,False,drawing,15)
	#	theDrawing.append([x,y])
       # except:
       #     donothing = "do nothing"
        pygame.display.flip()
		
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == MID:
            pygame.image.save(screen, "screenshot.png")

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
