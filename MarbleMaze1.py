# MarbleMaze1.py
import socket                   # Import socket module
import time
import pygame
import Adafruit_ADXL345
import sys
import random
import os
import webbrowser
import os.path
import re
import urllib
from bs4 import BeautifulSoup

######## Web Page ###########################
#Scoreboard

scoresAndRanks = []	#array alternating with rank & corresponding scores
highScores = []		#array of just the high scores
highScorers = []	#array of names of the high scorers

#helper function to remove tags
TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

#Maps the line numbers where each winner is stored in the HTML file (minus one)
firstLN = 19
secondLN = 25
thirdLN = 30
fourthLN = 35
fifthLN = 40

#Find and open highScores.html 
#Website: http://131.128.49.34/highScores.html	
save_path = '/var/www/'
name_of_file = 'scoreboard'
completeName = os.path.join(save_path, name_of_file+".html") 
f = open(completeName, "r")

url = completeName
html = urllib.urlopen(url).read()
soup = BeautifulSoup(html)

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get all of the ranks and scores
text = soup.get_text()
scoresAndRanks = re.findall('\d+', text)
print(scoresAndRanks)

#print out all ranks and scores for debugging
i = 0
while i < len(scoresAndRanks):
    print(scoresAndRanks[i])
    i += 1

#make a seperate array for just the high scores
i = 1
print('The high Scores you need to beat are:')
while i < len(scoresAndRanks):
    rawScore = int(scoresAndRanks[i])
    highScores.append(rawScore)
    i += 2
print(highScores)

#Extract the names of the high scorers from the HTML doc, save them in highScorers[]
for i, line in enumerate(f):

   if i == firstLN:
      firstplace = remove_tags(line)
      firstplace = firstplace.rstrip("\n")	#remove all newline tags
      firstplace = firstplace.strip()		#remove all trailing spaces
      highScorers.append(firstplace)
   elif i == secondLN:
      secondplace = remove_tags(line)
      secondplace = secondplace.rstrip("\n")
      secondplace = secondplace.strip()
      highScorers.append(secondplace)
   elif i == thirdLN:
      thirdplace = remove_tags(line)
      thirdplace = thirdplace.rstrip("\n")
      thirdplace = thirdplace.strip()
      highScorers.append(thirdplace)
   elif i == fourthLN:
      fourthplace = remove_tags(line)
      fourthplace = fourthplace.rstrip("\n")
      fourthplace = fourthplace.strip()
      highScorers.append(fourthplace)
   elif i == fifthLN:
      fifthplace = remove_tags(line)
      fifthplace = fifthplace.rstrip("\n")
      fifthplace = fifthplace.strip()
      highScorers.append(fifthplace)
   elif i > 42:
      break
print('the high scorers are:')
print(highScorers)
#print(text)

f.close()

############################################################
#Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
#Sizes
size = width, height = 800, 480

class Player(object):
 def __init__(self):
   self.rect = pygame.Rect((50,50,12,12))
 def move(self, dx, dy):
   if dx !=0:
     self.move_single_axis(dx,0)
   if dy !=0:
     self.move_single_axis(0,dy)
 
 def move_single_axis(self, dx, dy):
   self.rect.x += dx
   self.rect.y += dy
   
   for wall in walls:
     if self.rect.colliderect(wall.rect):
        if dx > 0: # Moving right; Hit the left side of the wall
          self.rect.right = wall.rect.left
        if dx < 0: # Moving left; Hit the right side of the wall
          self.rect.left = wall.rect.right
        if dy > 0: # Moving down; Hit the top side of the wall
          self.rect.bottom = wall.rect.top
        if dy < 0: # Moving up; Hit the bottom side of the wall
          self.rect.top = wall.rect.bottom

class Wall(object):
  def __init__(self, pos):
    walls.append(self)
    self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
    
#############Functions###############
running = True
def white_text(text, font):
    textSurface = font.render(text, True, (255,255,255))
    return textSurface, textSurface.get_rect()
    
def black_text(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()
    
def red_text(text, font):
    textSurface = font.render(text, True, (252,0,0))
    return textSurface, textSurface.get_rect()
    
def pink_text(text, font):
    textSurface = font.render(text, True, (241,140,142))
    return textSurface, textSurface.get_rect()
    
def Score(Points):
  largeText = pygame.font.Font('freesansbold.ttf',15)
  TextSurf, TextRect = black_text("Score =" +str(Points), largeText)
  TextRect.center = ( ((width/2)-60),(460))
  screen.blit(TextSurf, TextRect)

def Wait(counter):
  wait_text = ["Get Ready!", "3","2","1","GO"]
  largeText = pygame.font.Font('freesansbold.ttf',30)
  TextSurf, TextRect = white_text(wait_text[counter], largeText)
  TextRect.center = ( ((width/2)),(height/2))
  screen.blit(TextSurf, TextRect)
  pygame.display.update()
  
def Display_timer(timer):
  largeText = pygame.font.Font('freesansbold.ttf',15)
  TextSurf, TextRect = black_text("Timer =" +str(timer), largeText)
  TextRect.center = ( ((width/2)+60),(460))
  screen.blit(TextSurf, TextRect)

def Display_lvl(Level):
  largeText = pygame.font.Font('freesansbold.ttf',30)
  TextSurf, TextRect = white_text("Level " +str(Level), largeText)
  TextRect.center = ((width/2),200)
  screen.blit(TextSurf, TextRect)
  
def game_intro():

    Play = False
    Info = False
    Intro = True
    
    move = 0
    move1 = width
    while Intro:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()   
                start_click = Start_button.collidepoint(pos)
                info_click = Info_button.collidepoint(pos)
                if start_click:    
                    Intro = False
                    Play = True
                if info_click:    
                    Intro = False
                    Info = True   
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
               
        screen.fill(BLACK)

        largeText = pygame.font.Font('freesansbold.ttf',120)
        smallText = pygame.font.Font("freesansbold.ttf",20)
        
        TextSurf, TextRect = white_text("Marble Maze", largeText)
        TextRect.center = ((width/2),(height/4))
        screen.blit(TextSurf, TextRect)
        
        mouse = pygame.mouse.get_pos() 
        if 200+100 > mouse[0] > 200 and 320+40 > mouse[1] > 320:
            Start_button = pygame.draw.rect(screen, (241, 228, 228), (200,320,100,40))
        else:
            Start_button = pygame.draw.rect(screen, (151, 100, 199),(200,320,100,40))
        
        if 500+100 > mouse[0] > 500 and 320+40 > mouse[1] > 320:
            Info_button = pygame.draw.rect(screen,(21, 205, 168), (500,320,100,40)) 
        else:
            Info_button = pygame.draw.rect(screen, (9, 154, 151),(500,320,100,40))
        menu_words = ["Start", "Info"]
        menu_placement = [(250,340), (550,340)]
        
        textSurf, textRect = white_text(menu_words[0], smallText)
        textRect.center = menu_placement[0]
        screen.blit(textSurf, textRect) 
        textSurf, textRect = white_text(menu_words[1], smallText)
        textRect.center = menu_placement[1]
        screen.blit(textSurf, textRect)
        
        if move > width:
          move = 0
        else:
          move +=10
        if move1 < 0:
          move1 = width
        else:
          move1 -=10
        pygame.draw.circle(screen,(241, 228, 228),(move,270), 12)
        pygame.draw.circle(screen,(21, 205, 168),(move1,210), 12)
        pygame.draw.circle(screen,(151, 100, 199),(move,420), 12)
        pygame.draw.circle(screen,(9, 154, 151),(move1,400), 12)

        pygame.display.update()
        clock.tick(15)
    return Play,Info,Intro

def info_screen():

    Play = False
    Info = True
    Intro = False
    
    
    while Info:
        screen.fill((54,98,43))
        mouse = pygame.mouse.get_pos() 
        if 200+100 > mouse[0] > 200 and 320+40 > mouse[1] > 320:
            Start_button = pygame.draw.rect(screen, (198,227,119), (200,320,100,40))
        else:
            Start_button = pygame.draw.rect(screen, (114, 157, 57),(200,320,100,40))
        if 500+100 > mouse[0] > 500 and 320+40 > mouse[1] > 320:
            Back_button = pygame.draw.rect(screen,(198,227,119), (500,320,100,40)) 
        else:
            Back_button = pygame.draw.rect(screen, (114, 157, 57),(500,320,100,40))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()   
                start_click = Start_button.collidepoint(pos)
                back_click = Back_button.collidepoint(pos)
                if start_click:    
                    Play = True
                    Info = False  
                if back_click:    
                    Info = False
                    Intro = True   
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        info_words = ["Start", "Back", "Game Directions & Info", 
        "Lift the Board and tilt to move the marble.",
        "Avoid touching the wall! Beat the timer to win!", "Game by Corinne Ajemian and Keara Cole", "University of Rhode Island ELE409 2019"]
        info_placement = [(250,340), (550,340), ((width/2), 50), ((width/2), 125), ((width/2), 175), ((width/2), 225), ((width/2), 275)]       
        #Start
        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = white_text(info_words[0], smallText)
        textRect.center = info_placement[0]
        screen.blit(textSurf, textRect)
        #Back
        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = white_text(info_words[1], smallText)
        textRect.center = info_placement[1]
        screen.blit(textSurf, textRect)
        #Game Directions & Info
        largeText = pygame.font.Font('freesansbold.ttf',60)
        TextSurf, TextRect = white_text(info_words[2], largeText)
        TextRect.center = info_placement[2]
        screen.blit(TextSurf, TextRect)
        #Lift the Board and tilt to move the marble.
        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = white_text(info_words[3], smallText)
        textRect.center = info_placement[3]
        screen.blit(textSurf, textRect)
        #Avoid touching the wall! Beat the timer to win!.
        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = white_text(info_words[4], smallText)
        textRect.center = info_placement[4]
        screen.blit(textSurf, textRect)
        #Game by Corinne Ajemian and Keara Cole
        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = white_text(info_words[5], smallText)
        textRect.center = info_placement[5]
        screen.blit(textSurf, textRect)
        #URI ELE409 2019
        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = white_text(info_words[6], smallText)
        textRect.center = info_placement[6]
        screen.blit(textSurf, textRect)
         
        pygame.display.update()
        clock.tick(15)
    return Play,Info,Intro

def write_score(Points):
        print('points', Points)
	#test to see if it's a high score	
	newScore = Points
	isHighScore = 0		#Assume False
	place = 0		#Which place the user came in	
	i = 0			#loop count
	while i < len(highScores):
		highscore = highScores[i]
                print('highscore:', highscore)
                print('NEW SCORE:', newScore)
    		if newScore >= highscore:
                  print(isHighScore)
		  isHighScore = 1	#Make True
	          place = i		#User placed in this iteration
	          break
    		i += 1

	#If User has a high score
	if isHighScore != 0: 
		print('Congratulations! You have a high score!')
		replacementName = highScorers[place]
		print('you are replacing the name', replacementName)
		replacementScore = str(highScores[place])
		print('you are replacing the score', replacementScore)
		toFile = raw_input("What is your name?")
		print('Great job,', toFile, '!')

	#Update the high score array
		decrementer = 4	#loop backwards so you don't overwrite
		count = 4 - place
		
		while(count != 0):
			print(decrementer)
			highScores[decrementer] = highScores[decrementer-1]
			count -= 1
			decrementer -= 1
		highScores[place] = Points
		print(highScores)

	#Update the names of high scorers array
		decrementer = 4	#loop backwards so you don't overwrite
		count = 4 - place
		
		while(count != 0):
			print(decrementer)
			highScorers[decrementer] = highScorers[decrementer-1]
			count -= 1
			decrementer -= 1
		highScorers[place] = toFile
		print(highScorers)

		updatesRequired = 5-place
	#open the file and update the new high score
		count = updatesRequired
		placeCopy = place
		
		while(count > 0):
			print('loop taken')
			print('placeCopy =', placeCopy)
			with open(completeName,'r+') as myFile:
    				#convert to string:
    				data = myFile.read()
    				myFile.seek(0)
				replacementScore = str(highScores[placeCopy])
				print(replacementScore)
				newScore = str(highScores[placeCopy-1])
				print(newScore)
				myFile.write(re.sub(replacementScore,newScore,data,1))
                        	myFile.truncate()
			placeCopy += 1
			count -= 1
         #open the file and update the new high scorer's name
		count = updatesRequired
		placeCopy = place
		while(count > 0):
			print('loop taken')
			print('placeCopy =', placeCopy)
			with open(completeName,'r+') as myFile:
    				#convert to string:
    				data = myFile.read()
    				myFile.seek(0)
				replacementName = str(highScorers[placeCopy])
				print(replacementName)
				toFile = str(highScorers[placeCopy-1])
				print(toFile)
				myFile.write(re.sub(replacementName,toFile,data,1))
                        	myFile.truncate()
			placeCopy += 1
			count -= 1


	#Read the names from lines 21, 27, 32, 37, 42



def game_win(Points):
    
    Intro = False
    Win = True
    
    while Win:
        screen.fill((7,13,89))
        mouse = pygame.mouse.get_pos() 
        if 3600+100 > mouse[0] > 360 and 320+40 > mouse[1] > 320:
            Restart_button = pygame.draw.rect(screen, (206,221,239), (350,320,100,40))
        else:
            Restart_button = pygame.draw.rect(screen, (88, 147, 212),(350,320,100,40))
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()   
                is_inside = Restart_button.collidepoint(pos)
                if is_inside:    
                    Win = False
                    Intro = True
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
               
        win_words = ["Restart"]
        win_placement = [(400,340)]       
        #Start
        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = black_text(win_words[0], smallText)
        textRect.center = win_placement[0]
        screen.blit(textSurf, textRect)
        
        largeText = pygame.font.Font('freesansbold.ttf',120)
        TextSurf, TextRect = white_text("YOU WIN", largeText)
        TextRect.center = ((width/2),(height/4))
        screen.blit(TextSurf, TextRect)
        
        largeText = pygame.font.Font('freesansbold.ttf',50)
        TextSurf, TextRect = white_text("Score = " +str(Points), largeText)
        TextRect.center = ( ((width/2)),200)
        screen.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(15)
    return Intro, Win
           
def game_over():
    
    Intro = False
    Lose = True
    
    while Lose:
        screen.fill((95,0,0))
        mouse = pygame.mouse.get_pos() 
        if 3600+100 > mouse[0] > 360 and 320+40 > mouse[1] > 320:
            Restart_button = pygame.draw.rect(screen, (221,0,0), (350,320,100,40))
        else:
            Restart_button = pygame.draw.rect(screen, (189, 0, 0),(350,320,100,40))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()   
                is_inside = Restart_button.collidepoint(pos) 
                if is_inside:    
                    Lose = False
                    Intro = True
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
               
        largeText = pygame.font.Font('freesansbold.ttf',120)
        TextSurf, TextRect = red_text("Game Over!", largeText)
        TextRect.center = ((width/2),(height/4))
        screen.blit(TextSurf, TextRect)

        lose_words = ["Restart"]
        lose_placement = [(400,340)]       
        #Restart
        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = red_text(lose_words[0], smallText)
        textRect.center = lose_placement[0]
        screen.blit(textSurf, textRect)
        
        pygame.display.update()
        clock.tick(15)
    return Intro, Lose
            
def updatePoints():
  a, b, c = accel.read()
  float(a)
  float(b)
  if a > 2:
    RIGHT = 1
    Rratio = abs((a/255.0) * 10.0) * 2.0
  else: 
    RIGHT = Rratio = 0
  if a < -12:
    LEFT = 1
    Lratio = abs((a/270.0) * 10.0) * 2.0
  else: 
    LEFT = Lratio = 0
  if b < -15:
    DOWN = 1
    Dratio = abs((b/262.0) * 10.0) * 2.0
  else:
    DOWN = Dratio = 0
  if b > -7:
    UP = 1
    Uratio = abs((b/252.0) * 10.0) * 2.0
  else:
    UP = Uratio = 0
  return DOWN, Dratio, LEFT, Lratio, RIGHT, Rratio, UP, Uratio
  
def game(player, end_rect): 
  Play = True
  Win = False
  Lose = False
  #Set Colors
  Wall_color = (127, 71, 130)
  Player_color = (253, 208, 67)
  Background_color = (226, 89,139)
  Goal_color = (170, 92, 159)
  #Directions
  DOWN = LEFT = RIGHT = UP = 0
  #Set levels to begin and end with
  Level = 1
  Final_Level = 1
  Points = 100
  lvls_winpoints = [100, 200, 300, 400, 500]
  #Timer values, add extra 5 for the count down
  lvls_timer = [35, 35, 15, 35, 35]
  lvl_counter = 0
  timer = lvls_timer[lvl_counter]
  minutes = 0
  time_start = time.time()
  while Play:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit(); sys.exit();
    #start game timer for points
    seconds = int(time.time() - time_start) - minutes * 60
    #Reset Screen
    screen.fill(Background_color)
    if seconds < 5:
      for wall in walls:
      	pygame.draw.rect(screen, Wall_color, wall.rect)
      Display_lvl(Level)
      Wait(seconds)
    else:
      print("Level = ", Level) 
      #Update movement
      if DOWN == 1:
        player.move(0, Dratio)
      if UP == 1:
        Uratio = Uratio * -1
        player.move(0, Uratio)
      if RIGHT == 1:
        player.move(Rratio, 0)
      if LEFT == 1:
        Lratio = Lratio * -1
        player.move(Lratio, 0)
      DOWN, Dratio, LEFT, Lratio, RIGHT, Rratio, UP, Uratio = updatePoints()
      # Draw marble over Rect
      (x,y,a,b)=player.rect
      x= x+6
      y= y+6
      marble=pygame.draw.circle(screen,Player_color,(x,y), 12)
      # Time Count Down
      if timer > 0:
        timer = lvls_timer[lvl_counter] - seconds
      else:
        Play = False
        Win = False
        Lose = True 
      #Lose points for colliding with wall         
      for wall in walls:
        if  marble.colliderect(wall.rect):
          Points = Points - 1
          if Points <= 0:
            Points = 0         
      #New Level when reaching goal
      if player.rect.colliderect(end_rect):
        time_start = time.time()
        Points += lvls_winpoints[lvl_counter]
        lvl_counter +=1
        Points += timer
        timer = 60   
        if Level == Final_Level:
          Play = False
          Win = True
          Lose = False
        elif Level == 4:
          Level = 5
          del walls[:]
          Wall_color = (227, 227, 227)
          Player_color = (203, 55, 55)
          Background_color = (238, 111, 87)
          Goal_color = (250, 250, 250)
          Start_place = (400,32, 12, 12)
          player.rect = pygame.Rect(Start_place)
          x = y = 0
          for row in level5:
              for col in row:
                  if col == "W":
                      Wall((x, y))
                  if col == "E":
                      end_rect = pygame.Rect(x, y, 80, 16)
                  x += 16
              y += 16
              x = 0
        elif Level == 3:
          print("Level = ", Level)
          Level = 4
          del walls[:]
          Wall_color = (227, 227, 227)
          Player_color = (203, 55, 55)
          Background_color = (238, 111, 87)
          Goal_color = (250, 250, 250)
          Start_place = (400,32, 12, 12)
          player.rect = pygame.Rect(Start_place)
          x = y = 0
          for row in level4:
              for col in row:
                  if col == "W":
                      Wall((x, y))
                  if col == "E":
                      end_rect = pygame.Rect(x, y, 80, 16)
                  x += 16
              y += 16
              x = 0
        elif Level == 2:
          Level = 3
          del walls[:]
          Wall_color = (227, 227, 227)
          Player_color = (203, 55, 55)
          Background_color = (238, 111, 87)
          Goal_color = (250, 250, 250)
          Start_place = (400,32, 12, 12)
          player.rect = pygame.Rect(Start_place)
          x = y = 0
          for row in level3:
              for col in row:
                  if col == "W":
                      Wall((x, y))
                  if col == "E":
                      end_rect = pygame.Rect(x, y, 80, 16)
                  x += 16
              y += 16
              x = 0
        elif Level == 1:
          Level = 2
          del walls[:]
          Wall_color = (205, 69, 69)
          Player_color = (241, 104, 33)
          Background_color = (243, 163, 51)
          Goal_color = (255, 254, 154)
          Start_place = (750,32, 12, 12)
          player.rect = pygame.Rect(Start_place)
          x = y = 0
          for row in level2:
              for col in row:
                  if col == "W":
                      Wall((x, y))
                  if col == "E":
                      end_rect = pygame.Rect(x, y, 16, 80)
                  x += 16
              y += 16
              x = 0
      #Draw screen
      for wall in walls:
      	pygame.draw.rect(screen, Wall_color, wall.rect)
      Score(Points)
      Display_timer(timer)
      pygame.draw.rect(screen, Goal_color, end_rect)
      pygame.draw.rect(screen, Player_color, player.rect)
      pygame.display.flip()
      time.sleep(0.05)
  return Play, Win, Lose, Points 

Game = True
Intro = True
Lose = False
Win = False
while Game:      
  walls = []
  player = Player() # Create the player
  level1 = [         #50 by 30
  "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
  "W     WW                                          ",
  "W     WW                                          ",
  "W     WW                                          ",
  "W     EWW      WWWWWWWWWWWWWWWWWWWWWWWWWWWWW     W",
  "W     WW       WWWWWWWWWWWWWWWWWWWWWWWWWWWWW     W",
  "W     WW                                  WW     W",
  "W     WW                                  WW     W",
  "W     WW                                  WW     W",
  "W     WWWWWWWWWWWWW       WWWWWWW         WW     W",
  "W     WWWWWWWWWWWWW       WWWWWWW         WW     W",
  "W                WW                       WW     W",
  "W                WW                       WW     W",
  "W                WW                       WW     W",
  "W     WW         WWWWWWWWWWWWWWWW         WW     W",
  "W     WW         WWWWWWWWWWWWWWWW         WW     W",
  "W     WW         WW                       WW     W",
  "W     WW         WW                       WW     W",
  "W     WW         WW               WWWWWWWWWWWWWWWW",
  "W     WW         WW               WWWWWWWWWWWWWWWW",
  "W     WW                                         W",
  "W     WW                                         W",
  "W     WW                                         W",
  "W     WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW      W",
  "W     WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW      W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
  "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
  ]
  level2 = [         #50 by 30
  "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
  "E     WW                                         W",
  "      WW                                         W",
  "      WW                                         W",
  "W     WW       WWWWWWWWWWWWWWWWWWWWWWWWWWWWW     W",
  "W     WW       WWWWWWWWWWWWWWWWWWWWWWWWWWWWW     W",
  "W     WW                                  WW     W",
  "W     WW                                  WW     W",
  "W     WW                                  WW     W",
  "W     WWWWWWWWWWWWW       WWWWWWW         WW     W",
  "W     WWWWWWWWWWWWW       WWWWWWW         WW     W",
  "W                WW                       WW     W",
  "W                WW                       WW     W",
  "W                WW                       WW     W",
  "W     WW         WWWWWWWWWWWWWWWW         WW     W",
  "W     WW         WWWWWWWWWWWWWWWW         WW     W",
  "W     WW         WW                       WW     W",
  "W     WW         WW                       WW     W",
  "W     WW         WW               WWWWWWWWWWWWWWWW",
  "W     WW         WW               WWWWWWWWWWWWWWWW",
  "W     WW                                         W",
  "W     WW                                         W",
  "W     WW                                         W",
  "W     WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW      W",
  "W     WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW      W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
  "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
  ]
  level3 = [         #50 by 30
  "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
  "W   E               WW      WW     E             W",
  "W                   WW      WW                   W",
  "W                   WW      WW                   W",
  "W                   WW      WW                   W",
  "W         WW        WW      WW        WW         W",
  "W         WW        WW      WW        WW         W",
  "W         WW        WW      WW        WW         W",
  "W         WW        WW      WW        WW         W",
  "W         WWWWWWWWWWWW      WWWWWWWWWWWW         W",
  "W         WWWWWWWWWWWW      WWWWWWWWWWWW         W",
  "W                   WW      WW                   W",
  "W                   WW      WW                   W",
  "W                   WW      WW                   W",
  "W     WW            WW      WW            WW     W",
  "W     WW            WW      WW            WW     W",
  "W     WW            WW      WW            WW     W",
  "W     WW            WW      WW            WW     W",
  "W     WW            WW      WW            WW     W",
  "W     WW            WW      WW            WW     W",
  "W     WW            WW      WW            WW     W",
  "W     WW            WW      WW            WW     W",
  "W     WW            WW      WW            WW     W",
  "W     WWWWWWWWWWWWWWWW      WWWWWWWWWWWWWWWW     W",
  "W     WWWWWWWWWWWWWWWW      WWWWWWWWWWWWWWWW     W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
  "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
  ]
  level4 = [         #50 by 30
  "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                E                               W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
  ]
  level5 = [         #50 by 30
   "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                E                               W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "W                                                W",
  "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
  ]
  x = y = 0
  for row in level1:
      for col in row:
          if col == "W":
              Wall((x, y))
          if col == "E":
              end_rect = pygame.Rect(x, y, 16, 80)
          x += 16
      y += 16
      x = 0
  count = 0
  #Initialize screen, clock, G-Senosr, Game
  screen = pygame.display.set_mode(size)
  clock = pygame.time.Clock()
  accel = Adafruit_ADXL345.ADXL345(address=0x53, busnum=0)     
  pygame.init()
  #Functions for different screens
  if Intro:
    Play,Info,Intro = game_intro()
  elif Info:
    Play,Info,Intro = info_screen()
  elif Play:
    Play, Win, Lose, Points = game(player, end_rect)
  elif Lose:
    Intro, Lose = game_over()
  elif Win:
    write_score(Points)
    Intro, Win = game_win(Points)
