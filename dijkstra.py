from screen import Screen
from hero import Hero

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

#random houses
returned = screen.randomHouses(10)
houses = returned[0]
distances = returned[1]

screen.drawBackground()
screen.drawAllTraces()
screen.drawHouses(houses)
screen.showAndWait("Houses was generate, any key to continue")
screen.updateScreen()

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

#set info text, which will display under board
screen.infoText = "Calculation distances(cost) house 0 -> any house for find shortest trace to last house"

while node != None:
	for key in distances[node]:
		new_cost = costs[node] + distances[node][key]
		if new_cost < costs[key]:
			costs[key] = new_cost
			parents[key] = node
			screen.setHouseColorLikeParentColor(houses[int(key)], houses[int(node)])
			screen.renderCosts(houses, costs)
			screen.updateScreen()
			screen.sleep(0.5)	
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


#set info text, which will display under board
screen.infoText = "Create shortest trace to last house"

#set green color for trace in trace
for i in range(1,len(trace)):
	index1 =  int(trace[i])
	index0 =  int(trace[i - 1])
	screen.setTrace([houses[index0],houses[index1]])
	screen.sleep(0.5)
	screen.renderCosts(houses, costs)
	screen.updateScreen()

#create hero on postion house[0]
hero = Hero(houses[0][0], houses[0][1])
screen.drawHero(hero)
screen.updateScreen()

#end

screen.infoText = None
screen.renderCosts(houses, costs)
screen.showAndWait("Shortest track to last house was found. Any key to continue")

#main loop
running = True
while running:
	if len(trace) > 0:
		if screen.calcDistance((hero.x, hero.y),houses[int(trace[0])]) < 10:
			del trace[0]
	if len(trace) > 0:
		house = houses[int(trace[0])]
		hero.moveTo(house[0],house[1],10)
	
	screen.renderCosts(houses, costs)
	screen.drawHero(hero)
	screen.updateScreen()
	
	screen.sleep(0.025)