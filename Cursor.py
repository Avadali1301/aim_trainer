

class Cursor:
	__xPosition = 0
	__yPosition = 0

# the Cursor class doesn't really do much except help keep the code cleaner

	def __init__(self, x, y):
		self.__xPosition = x
		self.__yPosition = y

	def updateCoords(self, x, y):
		self.__xPosition = x
		self.__yPosition = y

	def getXPosition(self):
		return self.__xPosition

	def getYPosition(self):
		return self.__yPosition