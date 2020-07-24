import pygame
from random import randint 
from time import sleep 
import math

#global variable
(width, height) = (1280, 720)
white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)
red = pygame.Color(138, 14, 11)
green = pygame.Color(13, 69, 50)
orange = pygame.Color(255, 106, 0)
infinity = float("inf")

tracesList = []

pygame.font.init() 
fontSize = 35
font = pygame.font.SysFont("Italic", fontSize)

def createScreen():
	screen = pygame.display.set_mode((width, height))
	drawBackground(screen)
	return screen

def drawBackground(screen):
	screen.fill(white)

	backgroudPoints = []
	backgroudPoints.append([int(width * 0.05),int(height *0.05)]);#left-top
	backgroudPoints.append([int(width * 0.9),int(height *0.05)]);#right-top
	backgroudPoints.append([int(width * 0.9),int(height *0.9)]);#right-bottom
	backgroudPoints.append([int(width * 0.05),int(height *0.9)]);#left-bottom

	pygame.draw.lines(screen, black, True, backgroudPoints, 5)

def drawHero(screen, hero):
	pygame.draw.circle(screen, orange, hero, 7)

def drawHouse(screen, x, y):
	color = black
	#draw roof
	pygame.draw.rect(screen, color, (x - 30, y - 25, 60, 15))
	pygame.draw.polygon(screen, color, [(x - 40, y - 10), (x - 30, y - 10), (x - 30, y - 25)])
	pygame.draw.polygon(screen, color, [(x + 40, y - 10), (x + 30, y - 10), (x + 30, y - 25)])
	
	#draw house
	pygame.draw.rect(screen, color, (x - 30, y - 12, 60, 35))

def cDrawHouse(screen, x, y, color, number):
	#draw roof
	pygame.draw.rect(screen, color, (x - 30, y - 25, 60, 15))
	pygame.draw.polygon(screen, color, [(x - 40, y - 10), (x - 30, y - 10), (x - 30, y - 25)])
	pygame.draw.polygon(screen, color, [(x + 40, y - 10), (x + 30, y - 10), (x + 30, y - 25)])
	
	#draw house
	pygame.draw.rect(screen, color, (x - 30, y - 12, 60, 35))

	#render house number
	screen.blit(font.render(str(number), False, orange),(x - int(fontSize / 5),y - int(fontSize / 5)))

def drawTrace(screen, houses):
	#random color
	color = pygame.Color(randint(0,255), randint(0,255), randint(0,255));
	pygame.draw.lines(screen, color, False, houses, 3)
	if houses not in tracesList:
		tracesList.append(houses)

def calcDistance(first, second):
	return math.sqrt(math.pow((first[0] - second[0]),2) + math.pow((first[1] - second[1]),2))

def collcionTest(newHouse, houses):
	for house in houses:
		if house == None:
			continue
		if calcDistance(newHouse, house) < 150:
			return True
	return False

def randomHouses(screen, amount):
	minW = int(width * 0.05) + 50
	maxW = int(width * 0.9) - 50
	minH = int(height * 0.05)  + 50
	maxH = int(height * 0.9) - 50

	houses = [None] * amount
	distances = {}
	
	for i in range(amount):

		while True:
			x = randint(minW, maxW)
			y = randint(minH, maxH)
			if not collcionTest([x,y],houses):
				break

		#set random house to array[i]
		houses[i] = [x,y]
		
		#create distances set for house
		distances[str(i)] = {}
		if i > 1:
			#get 2 previous house distance to house[i]  
			distances[str(i-1)][str(i)] = calcDistance(houses[i-1], houses[i])
			drawTrace(screen, [houses[i-1], houses[i]])
			distances[str(i-2)][str(i)] = calcDistance(houses[i-2], houses[i])
			drawTrace(screen, [houses[i-2], houses[i]])
			#get distance from house[i] to 2 previous house
			distances[str(i)][str(i-2)] = calcDistance(houses[i], houses[i-2])
			distances[str(i)][str(i-1)] = calcDistance(houses[i], houses[i-1])

		if i == 1:
			#get distance to house[1] from house[0]
			distances["0"]["1"] = calcDistance(houses[0], houses[1])
			drawTrace(screen, [houses[0], houses[1]])
			#get distance to house[0] from house[1]
			distances["1"]["0"] = calcDistance(houses[1], houses[0])

	#draw all houses
	for i,house in enumerate(houses):
		drawHouse(screen, house[0], house[1])
		#render house number
		screen.blit(font.render(str(i), False, orange),(house[0] - int(fontSize / 5),house[1] - int(fontSize / 5)))

	return [houses, distances]

def getShortest(costs, processed):
	min = infinity
	index = None
	for key in costs:
		if key in processed:
			continue
		if costs[key] < min:
			min = costs[key]
			index = key
	return index

#start
screen = createScreen()

#random houses
returned = randomHouses(screen, 10)
houses = returned[0]
distances = returned[1]

#set start house and meta 
start = houses[0]
meta = houses[-1]

#color first and last house
cDrawHouse(screen, start[0],start[1], green, 0)
cDrawHouse(screen, meta[0], meta[1], red, len(houses)-1)

#algorithms implementations
#processed
processed = []

#create parents set
parents = {}
#create costs set
costs = {}
#put values in costs and parents sets
for i in range(1, len(houses)):
	parents[str(i)] = i - 1
	costs[str(i)] = infinity

#cost, parent for 0 
costs["0"] = 0
parents["0"] = 0

#set costs 0->1 and 0->2
costs["1"] = distances["0"]["1"]
costs["2"] = distances["0"]["2"]
parents["2"] = 0

processed.append("0")

node = getShortest(costs, processed)
while node != None:
	for key in distances[node]:
		new_cost = costs[node] + distances[node][key]
		if new_cost < costs[key]:
			costs[key] = new_cost
			parents[key] = node
		processed.append(node)
	node = getShortest(costs, processed)

trace = []
#add meta 
trace.append(len(houses)-1)
parent = parents[str(len(houses)-1)]
while parent != 0:
	trace.append(parent)
	parent = parents[str(parent)]

#add start
trace.append(0)

#reverse and print trace
trace.reverse()
print(trace)

#create hero
hero = [houses[0][0], houses[0][1]]
drawHero(screen, hero)

pygame.display.update()
#main loop
running = True
while running:
	if len(trace) > 0:
		if calcDistance(hero,houses[int(trace[0])]) < 10:
			del trace[0]
	if len(trace) > 0:
			length=math.sqrt(math.pow(hero[0] - houses[int(trace[0])][0],2)+math.pow(hero[1] - houses[int(trace[0])][1],2))
			velocityX = (houses[int(trace[0])][0] - hero[0]) / length * 10
			velocityY = (houses[int(trace[0])][1] - hero[1]) / length * 10
			hero[0] +=  int(velocityX) 
			hero[1] +=  int(velocityY)
	drawBackground(screen)
	
	for traceHouse in tracesList:
		drawTrace(screen, traceHouse)

	for i in range(1,len(houses) - 1):
		drawHouse(screen,houses[i][0], houses[i][1])
		screen.blit(font.render(str(i), False, orange),(houses[i][0] - int(fontSize / 5),houses[i][1] - int(fontSize / 5)))

	cDrawHouse(screen, start[0],start[1], green, 0)
	cDrawHouse(screen, meta[0], meta[1], red, len(houses) - 1)
	drawHero(screen,hero)
	sleep(0.02)
	pygame.display.update()
	events = pygame.event.get()
	for event in events:
	    if event.type == pygame.QUIT:
	        pygame.quit()
	        exit()