import pygame
import time
import random
import os
print(os.path.abspath(os.getcwd()))
path = os.path.abspath(os.getcwd())
pygame.init()
X= 800
Y= 600
DEFAULT_WALL_SIZE = (X,Y)
DEFAULT_ZOMBIE_SIZE = (80,150)
ZOMBIE_WIDTH_OFFSET = 40
pygame.mixer.music.load(path + "\\bgmusic.mp3")
pygame.mixer.music.set_volume(.3)
pygame.mixer.music.play(-1)
ding = pygame.mixer.Sound(path+"\\ding.mp3")
ding.set_volume(.5)
INIT = "init"
HIT = 'hit'
WITHDRAW = 'withdraw'
HITWITHDRAW = 'hitwithdraw'
screen = pygame.display.set_mode((X,Y))
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
GRAVE_SPOT = [(406,147),(554,147),(318,249),(475,249),(638,249),(480,357),(643,357),(400,451),(483,562)]
pygame.display.set_caption('Whack Zombie')
font = pygame.font.Font('freesansbold.ttf', 32)
wall = pygame.image.load(path+'\\wall2.png')
wall = pygame.transform.scale(wall, DEFAULT_WALL_SIZE)
zombie_img = pygame.image.load(path+'\\zb.png')
zombie_nohead_img = pygame.image.load(path+'\\zb-nohead.png')
zombie_hit_img = pygame.image.load(path+'\\zb-hit.png')

cursor_basic = pygame.image.load("cursor-basic.png")
cursor_basic = pygame.transform.scale(cursor_basic, (90,90))
cursor_hit = pygame.image.load("cursor-hit.png")
cursor_hit = pygame.transform.scale(cursor_hit,(90,90))
cursor = cursor_basic
press_time=time.time()

zombie_img = pygame.transform.scale(zombie_img,DEFAULT_ZOMBIE_SIZE)
zombie_nohead_img = pygame.transform.scale(zombie_nohead_img,DEFAULT_ZOMBIE_SIZE)
zombie_hit_img = pygame.transform.scale(zombie_hit_img,DEFAULT_ZOMBIE_SIZE)
zombie_offset = (40,150)
zombies = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
grave_zombies = [0,1,2,3,4,5,6,7,8]
zombies_create_interval = [0]
score = [0]
miss = [0]
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
  Gcount = 0
  for x in grave_zombies:
      if type(x) == int:
        Gcount+=1
  return (count,Gcount)



def createSingleZombie():
  duration = random.uniform(2.5,6.0)
  pos = randomPos()

  while(zombies[pos[0]][pos[1]]!=0):
    pos = randomPos()

  zombie = Zombie(duration,pos)
  zombies[pos[0]][pos[1]] = zombie
  return

def randomGravePos():
  pos = random.choice(grave_zombies)
  while(type(pos)!= int): pos = random.choice(grave_zombies)
  return pos

def createSingleGraveZombie():
  duration = random.uniform(2.5,6.0)
  pos = randomGravePos()
  zombie = Zombie(duration, pos)
  grave_zombies[pos] = zombie


def removeZombie(pos):
  if type(pos) == tuple:
    if zombies[pos[0]][pos[1]] !=0:
      x =  zombies[pos[0]][pos[1]]
      zombies[pos[0]][pos[1]] = 0
      if x.state == WITHDRAW:
        miss[0]+=1
      del x
      return
  if type(pos) == int:
    if grave_zombies[pos]:
      x = grave_zombies[pos]
      grave_zombies[pos] = pos
      if x.state == WITHDRAW:
        miss[0]+=1
      del x

def generateZombies():
  if time.time() - zombies_create_interval[0] < 0:
    return
  count = countAvailableSpawn()
  Gcount = count[1]
  count = count[0]
  if count > 3: count = 3
  if Gcount > 3: Gcount = 3
  # if count > 0:
  #   n_zombie = random.randint(1,count)
  #   while(n_zombie!=0):
  #     n_zombie-=1
  #     createSingleZombie()
  if Gcount > 0:
    n_zombieG = random.randint(1,Gcount)
    while(n_zombieG!=0):
      n_zombieG-=1
      createSingleGraveZombie()
  zombies_create_interval[0] = time.time() + random.uniform(1,3)
  
def proceedZombies():
  for x in zombies:
    for y in x:
      if y ==0: continue
      if y.state == INIT:
        t = (time.time() - y.createdAt)*50
        # print(t)
        if t >= 100: 
          y.height = 150
        else:
          y.height = int(t*15)
          if y.height > 150: y.height = 150
        if t > y.duration*50: 
          y.state = WITHDRAW
          # print("true")
      if y.state == WITHDRAW or y.state == HITWITHDRAW:
        if y.height < 15:
          removeZombie(y.pos)
        else: 
          t = (time.time() - y.createdAt - y.duration)*50
          if t >= 100:
            y.height = 0
            removeZombie(y.pos)
          else: 
            y.height = y.height - int(t*8)
            if y.height < 0: y.height = 0
      if y.state == HIT and time.time() - y.hitTimeStamp > 0.5:
        y.state = HITWITHDRAW
        y.createdAt =time.time()
        y.duration = 0

def proceedGraveZombie():
  for y in grave_zombies:
    if type(y) ==int: continue
    if y.state == INIT:
      t = (time.time() - y.createdAt)*50
      # print(t)
      if t >= 100: 
        y.height = 150
      else:
        y.height = int(t*15)
        if y.height > 150: y.height = 150
      if t > y.duration*50: 
        y.state = WITHDRAW
        # print("true")
    if y.state == WITHDRAW or y.state == HITWITHDRAW:
      if y.height < 15:
        removeZombie(y.pos)
      else: 
        t = (time.time() - y.createdAt - y.duration)*50
        if t >= 100:
          y.height = 0
          removeZombie(y.pos)
        else: 
          y.height = y.height - int(t*8)
          if y.height < 0: y.height = 0
    if y.state == HIT and time.time() - y.hitTimeStamp > 0.5:
      y.state = HITWITHDRAW
      y.createdAt =time.time()
      y.duration = 0

# 75-150 ~ 700 500 0-8 0 6
def paintWall():
  text = font.render("hit/miss: "+str(score[0]) + '/' + str(miss[0]), True, green, blue)
  screen.blit(wall, (0,0))
  screen.blit(text,(10,10))
def paintZombie(zombie:Zombie):
  # print(zombie.pos)
  # print((zombie.pos[0]*150-ZOMBIE_WIDTH_OFFSET,zombie.pos[1]*150-zombie.height))
  if zombie.state == INIT or zombie.state == WITHDRAW:
    img = zombie_img
  if zombie.state == HIT:
    img = zombie_hit_img
  if zombie.state == HITWITHDRAW:
    img = zombie_nohead_img
  z = img.subsurface(0,0,80,zombie.height)
  if type(zombie.pos) == tuple: screen.blit(z,((zombie.pos[0]+2)*75-ZOMBIE_WIDTH_OFFSET,(zombie.pos[1]+2)*75-zombie.height))
  if type(zombie.pos) == int: screen.blit(z,(GRAVE_SPOT[zombie.pos][0]-ZOMBIE_WIDTH_OFFSET,GRAVE_SPOT[zombie.pos][1]-zombie.height))

def refresh():
  pygame.mouse.set_visible(False)
  x,y = pygame.mouse.get_pos()
  if cursor==cursor_basic:
    screen.blit(cursor, (x-18,y-28))
  else:
    screen.blit(cursor, (x-30,y-50))
  pygame.display.flip()
  
def updateScreen():
  paintWall()
  for x in zombies:
    for y in x:
      if y != 0:
        paintZombie(y)
  for z in grave_zombies:
    if type(z) != int:
      paintZombie(z)
  refresh()

def hitCheck(pos):
  for x in zombies:
    for y in x:
      if y != 0 and (y.state == INIT or y.state == WITHDRAW):
        if type(y.pos) == tuple: spot = ((y.pos[0]+2)*75-ZOMBIE_WIDTH_OFFSET,(y.pos[1]+2)*75-y.height)
        if pos[0] - spot[0] > 0 and pos[0] - spot[0] < 60 and pos[1] - spot[1] > 0 and pos[1] - spot[1] < 50: 
          y.state = HIT
          y.hitTimeStamp = time.time()
          score[0] += 1
          ding.play()
          return True
  for y in grave_zombies:
    if type(y) != int  and (y.state == INIT or y.state == WITHDRAW):
      if type(y.pos) == int: spot = (GRAVE_SPOT[y.pos][0]-ZOMBIE_WIDTH_OFFSET,GRAVE_SPOT[y.pos][1]-y.height)
      if pos[0] - spot[0] > 0 and pos[0] - spot[0] < 60 and pos[1] - spot[1] > 0 and pos[1] - spot[1] < 50: 
        y.state = HIT
        y.hitTimeStamp = time.time()
        score[0] += 1
        ding.play()
        return True
  
  # miss[0] +=1
  return False


# updateScreen()

running = True

while(running):
  generateZombies()
  # proceedZombies()
  proceedGraveZombie()
  updateScreen()
  for i in pygame.event.get():
    if i.type == pygame.MOUSEBUTTONDOWN:
      pos = pygame.mouse.get_pos()
      hitCheck(pos)
      cursor = cursor_hit
      press_time=time.time()
      print(pos)
    if i.type == pygame.QUIT:
      running = False
  if time.time()-press_time > .2:
    cursor = cursor_basic
pygame.quit()