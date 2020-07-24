from screen import Screen
import math
from time import time 

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

#draw all houses
screen.drawHouses(houses)

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

#create hero
hero = [houses[0][0], houses[0][1]]
screen.drawHero(hero)
screen.updateScreen()


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
	screen.drawAllTraces()
	screen.drawHouses(houses)
	screen.drawHero(hero)
	screen.updateScreen()
	
	#sleep for x time but still checking, if exit button is pressed
	startTime = time()
	while time() - startTime < 0.025:
		if screen.isExit():
			running = False
