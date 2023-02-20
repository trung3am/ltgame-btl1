import pygame
import time
import random


pygame.init()
X= 800
Y= 600
DEFAULT_WALL_SIZE = (800,600)
DEFAULT_ZOMBIE_SIZE = (80,150)
ZOMBIE_WIDTH_OFFSET = 40
INIT = "init"
HIT = 'hit'
WITHDRAW = 'withdraw'
HITWITHDRAW = 'hitwithdraw'
screen = pygame.display.set_mode((X,Y))
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
pygame.display.set_caption('Whack Zombie')
font = pygame.font.Font('freesansbold.ttf', 32)
wall = pygame.image.load('D:\\ltgame\\btl1\\wall2.png')
wall = pygame.transform.scale(wall, DEFAULT_WALL_SIZE)
zombie_img = pygame.image.load('D:\\ltgame\\btl1\\zb.png')
zombie_nohead_img = pygame.image.load('D:\\ltgame\\btl1\\zb-nohead.png')
zombie_hit_img = pygame.image.load('D:\\ltgame\\btl1\\zb-hit.png')
zombie_img = pygame.transform.scale(zombie_img,DEFAULT_ZOMBIE_SIZE)
zombie_nohead_img = pygame.transform.scale(zombie_nohead_img,DEFAULT_ZOMBIE_SIZE)
zombie_hit_img = pygame.transform.scale(zombie_hit_img,DEFAULT_ZOMBIE_SIZE)
zombie_offset = (40,150)
zombies = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
zombies_create_interval = [0]
score = [0]
class Zombie:
  def __init__(self, duration, pos) -> None:
    self.createdAt = time.time()
    self.duration = duration
    self.state = INIT
    self.height = 30
    self.pos = pos
    self.hitTimeStamp = 0

def randomPos():
  x = random.randint(0,5)
  y = random.randint(0,6)
  return (x,y)

def countAvailableSpawn():
  count = 0
  for x in zombies:
    for y in x:
      if y == 0:
        count+=1
  return count

def createSingleZombie():
  duration = random.uniform(2.0,4.0)
  pos = randomPos()

  while(zombies[pos[0]][pos[1]]!=0):
    pos = randomPos()

  zombie = Zombie(duration,pos)
  zombies[pos[0]][pos[1]] = zombie

  
  return

def removeZombie(pos):

  if zombies[pos[0]][pos[1]] !=0:
    x =  zombies[pos[0]][pos[1]]
    del x

    zombies[pos[0]][pos[1]] = 0

def generateZombies():
  if time.time() - zombies_create_interval[0] < 0:
    return
  count = countAvailableSpawn()
  if count > 3: count = 3
  if count > 0:
    n_zombie = random.randint(1,count)
    while(n_zombie!=0):
      n_zombie-=1
      createSingleZombie()
  zombies_create_interval[0] = time.time() + random.uniform(1,3)
  
def proceedZombies():
  for x in zombies:
    for y in x:
      if y ==0: continue
      if y.state == INIT:
        t = (time.time() - y.createdAt)*50
        print(t)
        if t >= 100: 
          y.height = 150
        else:
          y.height = int(t*15)
          if y.height > 150: y.height = 150
        if t > y.duration*50: 
          y.state = WITHDRAW
          print("true")
      if y.state == WITHDRAW or y.state == HITWITHDRAW:
        if y.height < 15:
          removeZombie(y.pos)
        else: 
          t = (time.time() - y.createdAt - y.duration)*50
          if t >= 100:
            y.height = 0
            removeZombie(y.pos)
          else: 
            y.height = y.height - int(t*15)
            if y.height < 0: y.height = 0
      if y.state == HIT and time.time() - y.hitTimeStamp > 0.5:
        y.state = HITWITHDRAW
        y.createdAt =time.time()
        y.duration = 0

# 75-150 ~ 700 500 0-8 0 6
def paintWall():
  text = font.render("score: "+str(score[0]), True, green, blue)
  screen.blit(wall, (0,0))
  screen.blit(text,(650,535))
def paintZombie(zombie:Zombie):
  print(zombie.pos)
  print((zombie.pos[0]*150-ZOMBIE_WIDTH_OFFSET,zombie.pos[1]*150-zombie.height))
  if zombie.state == INIT or zombie.state == WITHDRAW:
    img = zombie_img
  if zombie.state == HIT:
    img = zombie_hit_img
  if zombie.state == HITWITHDRAW:
    img = zombie_nohead_img
  z = img.subsurface(0,0,80,zombie.height)
  screen.blit(z,((zombie.pos[0]+2)*75-ZOMBIE_WIDTH_OFFSET,(zombie.pos[1]+2)*75-zombie.height))

def refresh():
  pygame.display.flip()

def updateScreen():
  paintWall()
  for x in zombies:
    for y in x:
      if y != 0:
        paintZombie(y)
  refresh()

def hitCheck(pos):
  for x in zombies:
    for y in x:
      if y != 0 and (y.state == INIT or y.state == WITHDRAW):
        spot = ((y.pos[0]+2)*75-ZOMBIE_WIDTH_OFFSET,(y.pos[1]+2)*75-y.height)
        if pos[0] - spot[0] > 0 and pos[0] - spot[0] < 60 and pos[1] - spot[1] > 0 and pos[1] - spot[1] < 50: 
          y.state = HIT
          y.hitTimeStamp = time.time()
          score[0] += 1
          return True
  return False




running = True

while(running):
  generateZombies()
  proceedZombies()
  updateScreen()
  for i in pygame.event.get():
    if i.type == pygame.MOUSEBUTTONDOWN:
      pos = pygame.mouse.get_pos()
      hitCheck(pos)
      print(pos)
    if i.type == pygame.QUIT:
      running = False
pygame.quit()