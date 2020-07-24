import math

class Hero:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	#move self to point by one step
	def moveTo(self, x, y, speed):
		length=math.sqrt(math.pow(self.x - x,2)+math.pow(self.y - y,2))
		velocityX = (x - self.x) / length * speed
		velocityY = (y - self.y) / length * speed
		self.x +=  int(velocityX) 
		self.y +=  int(velocityY)

		