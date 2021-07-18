import time
import pygame
import random

class Target():
	__radius = 1 #radius of Target
	__xPos = 0
	__yPos = 0
	__timeElapsed = 0 # time elapsed in seconds
	__active = True # keeps track of if the Target is alive or dead
	__surface = None
	def __init__(self, radius, blank_surface, xPos, yPos):
		self.RED = (255, 0, 0)
		self.__radius = radius
		self.__surface = blank_surface
		# initialize x and y to values that are between the bounds
		# show a Target with center (x, y) and radius = __radius
		# when a Target object is created, start the countdown
		self.__xPos = xPos
		self.__yPos = yPos
		pygame.draw.circle(blank_surface, self.RED, (self.__xPos, self.__yPos), self.__radius)
		pygame.display.update()
		self.startCountdown()

	def startCountdown(self):
		# start a running count of the time elapsed between the calling of _init_ and deactivate()
		self.__timeElapsed = time.time()

	def stopCountdown(self):
		# stop the running count of the time elapsed
		self.__timeElapsed = time.time() - self.__timeElapsed
	def onHit(self):
		# plug in Cursor's coordinates into the circle equation and make sure that it is less than or equal to the __radius^2 
		if(self.__active):
			self.stopCountdown()
			self.deactivate()
			targetData = (self.__xPos, self.__yPos, self.__timeElapsed)
			return targetData
			# pass targetData
		# when a Target is hit, the countdown should stop, the Target should deactivate, and the Target's information should be passed as a tuple to the Session
	
	def deactivate(self):
		# A Target should be permanently 'hit' and it should disappear from the canvas
		# since we can't change a varibale to a constant in Python, we can just set the Target to 'inactive'
		# we just draw over the Target and make it inactive
		pygame.draw.circle(self.__surface, (255, 255, 255), (self.__xPos, self.__yPos), self.__radius)
		pygame.display.update()
		self.__active = False

	def activate(self):
		# we use this method in the replay
		# we want to display this Target, but we can keep active is False so that the on-hit events don't trigger
		pygame.draw.circle(self.__surface, self.RED, (self.__xPos, self.__yPos), self.__radius)
		pygame.display.update()
		self.__active = False
	def getXPos(self):
		return self.__xPos
	def getActive(self):
		return self.__active
	def getYPos(self):
		return self.__yPos
	def getTimeElapsed(self):
		return self.__timeElapsed
	def getRadius(self):
		return self.__radius

		



