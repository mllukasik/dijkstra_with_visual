import pygame
import math
from time import time 
from random import randint  

class Screen():
	def __init__(self):
		#global variable
		#size
		self.width = 1280
		self.height = 720
		#colors
		self.white = pygame.Color(255, 255, 255)
		self.black = pygame.Color(0, 0, 0)
		self.green = pygame.Color(13, 225, 50)
		self.orange = pygame.Color(255, 106, 0)
		#screen
		self.screen = pygame.display.set_mode((self.width, self.height + 100))#extend height to display info Text under board
		#font
		pygame.font.init() 
		self.fontSize = 35
		self.font = pygame.font.SysFont("Ubuntu Mono", self.fontSize)
		#info
		self.infoText = None
		#traceList
		self.tracesList = []
		self.tracesColor = {}
		self.housesColor = {}

	#draw background color with border
	def drawBackground(self):
		self.screen.fill(self.white)

		backgroudPoints = []
		backgroudPoints.append([int(self.width * 0.05),int(self.height *0.05)]);#left-top
		backgroudPoints.append([int(self.width * 0.9),int(self.height *0.05)]);#right-top
		backgroudPoints.append([int(self.width * 0.9),int(self.height *0.9)]);#right-bottom
		backgroudPoints.append([int(self.width * 0.05),int(self.height *0.9)]);#left-bottom

		pygame.draw.lines(self.screen, self.black, True, backgroudPoints, 5)

	#draw hero on heros position
	def drawHero(self, hero):
		pygame.draw.circle(self.screen, self.orange, (hero.x,hero.y), 7)

	#draw all houses with their number
	def drawHouses(self, houses):
		for i in range(len(houses)):
			self.drawHouse(houses[i][0], houses[i][1], i)

	#draw all houses with their cost
	def drawHousesWithCosts(self, houses, costs):
		for i in range(len(houses)):
			cost = costs[str(i)]		
			if cost != float("inf"):
				cost = int(cost)
			self.drawHouse(houses[i][0], houses[i][1], cost)

	def drawHouse(self, x, y, number):
		if str([x,y]) not in self.housesColor:
			color = pygame.Color(randint(0, 225), randint(0, 225), randint(0, 225));
			self.housesColor[str([x,y])] = color
		else:
		 	color = self.housesColor[str([x,y])]
		#draw roof
		pygame.draw.rect(self.screen, color, (x - 30, y - 25, 60, 15))
		pygame.draw.polygon(self.screen, color, [(x - 40, y - 10), (x - 30, y - 10), (x - 30, y - 25)])
		pygame.draw.polygon(self.screen, color, [(x + 40, y - 10), (x + 30, y - 10), (x + 30, y - 25)])
		
		#draw house
		pygame.draw.rect(self.screen, color, (x - 30, y - 12, 60, 35))

		#render house number
		text = self.font.render(str(number), False, self.orange)
		center = x - (text.get_width() / 2)
		top = y - (text.get_height() / 2)
		self.screen.blit(text,(int(center), int(top)))

	def setHouseColorLikeParentColor(self, house, parent):
		color = self.housesColor[str(parent)]
		self.housesColor[str(house)] = color

	def setTrace(self, houses):
		self.tracesColor[str(self.tracesList.index(houses))] = self.green
	
	def drawAllTraces(self):
		for trace in self.tracesList:
			self.drawTrace(trace)

	def drawTrace(self, houses):
		size = 7 #draw size

		#create new trace if not in traceList
		if houses not in self.tracesList:
			color = pygame.Color(0,0,0);
			pygame.draw.lines(self.screen, color, False, houses, size)
			#add new trace in list and save new color. New trace index -> new color 
			self.tracesList.append(houses)
			self.tracesColor[str(len(self.tracesList) - 1)] = color
		else:
			#get color if trace already exist in list
			#trace index -> color
			color = self.tracesColor[str(self.tracesList.index(houses))]
			pygame.draw.lines(self.screen, color, False, houses, size)

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

		return [houses, distances]

	#draw expandable text
	def showText(self, message):
		#get all words in text
		text = message.split(' ')

		#render all words
		for i, word in enumerate(text):
			word += ' '#append white character, which was removed by split function
			text[i] = self.font.render(word, False, self.black) 
		
		drawText = []
		drawText.append([])#add row
		#last elem in row always is length of row
		length = 0
		
		#create rows from words
		for word in text:
			#if text overbound
			if length + word.get_width() > self.width * 0.9:
				#last elem in row always is length of row
				#put length of row in last elem of row table
				drawText[-1].append(length)

				#create new row
				drawText.append([])
				#append word to created row
				drawText[-1].append(word)
				#set lenght for new row
				length = word.get_width()
			else:
				#append word to last row
				drawText[-1].append(word)
				#set lenght for last row
				length += word.get_width()
		
		#put length of last row in last elem of row table
		drawText[-1].append(length)
		#draw all words on screeen
		top = int(self.height * 0.95)#margin to bottom border 5%
		for row in drawText:
			#create center point to draw text in center of screen
			start = int((self.width / 2) - (row[-1] / 2))			
			
			for word in row[:-1]:#skip last elem, is lenght of row
				#draw word
				self.screen.blit(word,(start,top))
				
				#add to start word width
				start += int(word.get_width())
			top += row[-2].get_height() #add to top height of last word in row

	def showAndWait(self, message):
		#render message 
		self.showText(message)
		self.updateScreen()

		running = True
		#endless loop waiting for any key
		while running:
			#check if exit button is pressed
			try:
				events = pygame.event.get()
				for event in events:
					if event.type == pygame.QUIT:
						pygame.quit()
						quit()
					elif event.type == pygame.KEYUP:
						running = False
			except pygame.error as error:
				pass

	def updateScreen(self):
		pygame.display.update()

	def renderCosts(self, houses, costs):
		self.drawBackground()
		self.drawAllTraces()
		self.drawHousesWithCosts(houses, costs)

		if self.infoText != None:
			self.showText(self.infoText)

	def isExit(self):
		try:
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:
					pygame.quit()
					return True
		except pygame.error as error:
			return False
		return False

	#sleep for x time but still checking, if exit button is pressed
	def sleep(self, x):
		startTime = time()
		while time() - startTime < x:
			if self.isExit():
				exit()