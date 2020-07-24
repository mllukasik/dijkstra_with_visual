import pygame
from random import randint 
from time import sleep 
import math

class Screen():
	def __init__(self):
		#global variable
		#size
		self.width = 1280
		self.height = 720
		#colors
		self.white = pygame.Color(255, 255, 255)
		self.black = pygame.Color(0, 0, 0)
		self.red = pygame.Color(138, 14, 11)
		self.green = pygame.Color(13, 69, 50)
		self.orange = pygame.Color(255, 106, 0)
		#screen
		self.screen = pygame.display.set_mode((self.width, self.height))
		#font
		pygame.font.init() 
		self.fontSize = 35
		self.font = pygame.font.SysFont("Italic", self.fontSize)
		#traceList
		self.tracesList = []

	def drawBackground(self):
		self.screen.fill(self.white)

		backgroudPoints = []
		backgroudPoints.append([int(self.width * 0.05),int(self.height *0.05)]);#left-top
		backgroudPoints.append([int(self.width * 0.9),int(self.height *0.05)]);#right-top
		backgroudPoints.append([int(self.width * 0.9),int(self.height *0.9)]);#right-bottom
		backgroudPoints.append([int(self.width * 0.05),int(self.height *0.9)]);#left-bottom

		pygame.draw.lines(self.screen, self.black, True, backgroudPoints, 5)

	def drawHero(self, hero):
		pygame.draw.circle(self.screen, self.orange, hero, 7)

	def drawHouse(self, x, y):
		color = self.black
		#draw roof
		pygame.draw.rect(self.screen, color, (x - 30, y - 25, 60, 15))
		pygame.draw.polygon(self.screen, color, [(x - 40, y - 10), (x - 30, y - 10), (x - 30, y - 25)])
		pygame.draw.polygon(self.screen, color, [(x + 40, y - 10), (x + 30, y - 10), (x + 30, y - 25)])
		
		#draw house
		pygame.draw.rect(self.screen, color, (x - 30, y - 12, 60, 35))

	def cDrawHouse(self, x, y, color, number):
		#draw roof
		pygame.draw.rect(self.screen, color, (x - 30, y - 25, 60, 15))
		pygame.draw.polygon(self.screen, color, [(x - 40, y - 10), (x - 30, y - 10), (x - 30, y - 25)])
		pygame.draw.polygon(self.screen, color, [(x + 40, y - 10), (x + 30, y - 10), (x + 30, y - 25)])
		
		#draw house
		pygame.draw.rect(self.screen, color, (x - 30, y - 12, 60, 35))

		#render house number
		self.screen.blit(self.font.render(str(number), False, self.orange),(x - int(self.fontSize / 5),y - int(self.fontSize / 5)))

	def drawTrace(self, houses):
		#random color
		color = pygame.Color(randint(0,255), randint(0,255), randint(0,255));
		pygame.draw.lines(self.screen, color, False, houses, 3)
		if houses not in self.tracesList:
			self.tracesList.append(houses)

	def calcDistance(self, first, second):
		return math.sqrt(math.pow((first[0] - second[0]),2) + math.pow((first[1] - second[1]),2))

	def collcionTest(self, newHouse, houses):
		for house in houses:
			if house == None:
				continue
			if self.calcDistance(newHouse, house) < 150:
				return True
		return False

	def randomHouses(self, amount):
		minW = int(self.width * 0.05) + 50
		maxW = int(self.width * 0.9) - 50
		minH = int(self.height * 0.05)  + 50
		maxH = int(self.height * 0.9) - 50

		houses = [None] * amount
		distances = {}
		
		for i in range(amount):

			while True:
				x = randint(minW, maxW)
				y = randint(minH, maxH)
				if not self.collcionTest([x,y],houses):
					break

			#set random house to array[i]
			houses[i] = [x,y]
			
			#create distances set for house
			distances[str(i)] = {}
			if i > 1:
				#get 2 previous house distance to house[i]  
				distances[str(i-1)][str(i)] = self.calcDistance(houses[i-1], houses[i])
				self.drawTrace([houses[i-1], houses[i]])
				distances[str(i-2)][str(i)] = self.calcDistance(houses[i-2], houses[i])
				self.drawTrace([houses[i-2], houses[i]])
				#get distance from house[i] to 2 previous house
				distances[str(i)][str(i-2)] = self.calcDistance(houses[i], houses[i-2])
				distances[str(i)][str(i-1)] = self.calcDistance(houses[i], houses[i-1])

			if i == 1:
				#set distance to house[1] from house[0]
				distances["0"]["1"] = self.calcDistance(houses[0], houses[1])
				self.drawTrace([houses[0], houses[1]])
				#set distance to house[0] from house[1]
				distances["1"]["0"] = self.calcDistance(houses[1], houses[0])

		#draw all houses
		for i,house in enumerate(houses):
			self.drawHouse(house[0], house[1])
			#render house number
			self.screen.blit(self.font.render(str(i), False, self.orange),(house[0] - int(self.fontSize / 5),house[1] - int(self.fontSize / 5)))

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

#dijkstra variable
#infinity value
infinity = float("inf")

#start
screen = Screen()
screen.drawBackground()

#random houses
returned = screen.randomHouses(10)
houses = returned[0]
distances = returned[1]

#set start house and meta 
start = houses[0]
meta = houses[-1]

#color first and last house
screen.cDrawHouse(start[0],start[1], screen.green, 0)
screen.cDrawHouse(meta[0], meta[1], screen.red, len(houses)-1)

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
screen.drawHero(hero)

pygame.display.update()
#main loop
running = True
while running:
	if len(trace) > 0:
		if screen.calcDistance(hero,houses[int(trace[0])]) < 10:
			del trace[0]
	if len(trace) > 0:
			length=math.sqrt(math.pow(hero[0] - houses[int(trace[0])][0],2)+math.pow(hero[1] - houses[int(trace[0])][1],2))
			velocityX = (houses[int(trace[0])][0] - hero[0]) / length * 10
			velocityY = (houses[int(trace[0])][1] - hero[1]) / length * 10
			hero[0] +=  int(velocityX) 
			hero[1] +=  int(velocityY)
	screen.drawBackground()
	
	for traceHouse in screen.tracesList:
		screen.drawTrace(traceHouse)

	for i in range(1,len(houses) - 1):
		screen.drawHouse(houses[i][0], houses[i][1])
		screen.screen.blit(screen.font.render(str(i), False, screen.orange),(houses[i][0] - int(screen.fontSize / 5),houses[i][1] - int(screen.fontSize / 5)))

	screen.cDrawHouse(start[0],start[1], screen.green, 0)
	screen.cDrawHouse(meta[0], meta[1], screen.red, len(houses) - 1)
	screen.drawHero(hero)
	sleep(0.02)
	pygame.display.update()
	events = pygame.event.get()
	for event in events:
	    if event.type == pygame.QUIT:
	        pygame.quit()
	        exit()