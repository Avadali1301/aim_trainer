import time
import pygame
from Cursor import Cursor
from Target import Target
import math
import random
from sklearn.metrics import mean_squared_error
import numpy as np
from matplotlib import pyplot as plt

class Session:
	# len(deadTargets) = number of targets clicked
	def getTargetData(self):
		return self.targetData
	def getLossList(self):
		return self.lossList
######################################################
	def __init__(self, target_radius, simLen, numTargets):
		self.simLen = simLen
		self.radius = target_radius
		self.numTargets = numTargets
		pygame.init()
		self.width = 1300
		self.height = 800
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.background_color = (255, 255, 255)
		self.screen.fill(self.background_color)

		self.targetList = []

		self.initialX, self.initialY = pygame.mouse.get_pos()

		self.mouse = Cursor(self.initialX, self.initialY)
		self.running = True
		self.targetData = []
		self.pathList = []
		self.currentPath = []
		self.lossList = []
		self.timeList = []
		self.pointTimes = []
		self.spawnedTargets = []
		self.point_times_list = []
		self.totalClicks = 0
		self.t_final = 0
		self.xValues = []
		self.deadTargets = []
		self.flicks = []
		# self.spawnDelay = spawnDelay
######################################################
	def spawnTarget(self, xPos, yPos):
		self.targetList.append(Target(self.radius, self.screen, xPos, yPos))

	def spawnPoint(self, x, y):
		pygame.draw.circle(self.screen, self.BLUE, (x, y), 1)
		pygame.display.update()
######################################################
# IMPORTANT: CHANGE THIS LOSS METRIC TO RMSE
# For all points in the path, we have to compute the RMSE, then to keep it standardized depending on the number of points, we compute standard deviation of those points from the line of best fit.
	def RMSE(self, t1, t2, points):
		# right here solve the system for the equation of the lines between t1 and t2
		# Yt1 = Xt1*m + b
		# Yt2 = Xt2 * m + b
		# m = (Yt2 - Yt1) / (Xt2 - Xt1)
		X1 = t1.getXPos()
		Y1 = t1.getYPos()
		X2 = t2.getXPos()
		Y2 = t2.getYPos()
		m = (Y2 - Y1) / (X2 - X1)
		b = Y1 - m * X1
		# linear equation: y = mx + b (best fit between t1 and t2)
		total = 0
		for p in points:
			# compute residuals
			yAct = p[0]*m + b
			yPred = p[1]
			val = (yPred - yAct) ** 2
			total += val
		if(len(points) == 0):
			mse = 0
		else:
			mse = total / len(points)
		rmse = math.sqrt(mse)
		# in theory max rmse is 800 so we scale it down
		nrmse = rmse / 800
		return nrmse

# 	def computeLoss(self, t1, t2, points):
# 		# compute the distance between both Targets then compare that distance to the approximated curve
# 		part1 = (t1.getXPos() - t2.getXPos()) ** 2
# 		part2 = (t1.getYPos() - t2.getYPos()) ** 2
# 		distance = math.sqrt((part1 + part2))
# 		# the real shortest distance between two Targets; start on the edge of both circles
# 		distance -= 2 * self.radius
# 		curve = 0
# 		# points is a list of tuples of the path between the Targets
# 		# take the distance between each point anad approximate a curve for the path
# 		for p in range(len(points) - 1):
# 			# compute the distance between points on the path
# 			p1 = (points[p + 1][0] - points[p][0]) ** 2
# 			p2 = (points[p + 1][1] - points[p][1]) ** 2
# 			curve += math.sqrt((p1 + p2))
# 		return curve - distance
# # 24 June, build the Target data (this is completed)
# # 25 June, build the Path data and the loss function (this is completed)

# IMPORTANT: FIX POINT SAMPLING. Right now, if the user goes too quickly, not enough points are samples so the curve ends up being shorter than the line, which isn't possible
# maks it so that the curve approximation is always accurate
	def runSession(self):
		for i in range(self.numTargets):
			# for every Target, start the loop at the beginning of the list. once you reset the coords, set the inc back to 0
			# ensures that Targets do not overlap
			j = 0
			xPos = random.randint(self.radius, self.screen.get_width() + 1 - self.radius)
			yPos = random.randint(self.radius, self.screen.get_height() + 1 - self.radius)
			while(j < len(self.targetList)):
				if(0 <= ((self.targetList[j].getXPos() - xPos)**2 + (self.targetList[j].getYPos() - yPos)**2) and ((self.targetList[j].getXPos() - xPos)**2 + (self.targetList[j].getYPos() - yPos)**2) <= (2 * self.radius)**2):
					xPos = random.randint(self.radius, screen.get_width() + 1 - self.radius)
					yPos = random.randint(self.radius, screen.get_height() + 1 - self.radius)
					j = 0
				else:
					j += 1
			t = Target(self.radius, self.screen, xPos, yPos)
			self.targetList.append(t)
			self.spawnedTargets.append(t)
		self.t_final = time.time() + self.simLen # the value you are adding is the length of the session in seconds
		while (time.time() < self.t_final):
			# getting the mouse coordinates, updating the Cursor, and adding the coordinates to the path
			mouseX, mouseY = pygame.mouse.get_pos()
			self.currentPath.append((mouseX, mouseY))
			self.mouse.updateCoords(mouseX, mouseY)
			self.pointTimes.append(self.simLen - (self.t_final - time.time()))
			for event in pygame.event.get():
				# checks if the mouse is being clicked
				if event.type == pygame.MOUSEBUTTONUP:
					self.totalClicks += 1
					for target in self.targetList:
						# checks if the cursor is in or on any of the Targets and if the Target is active
						if((self.mouse.getXPosition() - target.getXPos())**2 + (self.mouse.getYPosition() - target.getYPos())**2 <= self.radius**2 and target.getActive()):
							# if the cursor is in/on a Target, it executes the protocal for onHit() and stores the data
							self.targetData.append(target.onHit())
							# makes it so that I'm not looping through dead Targets
							self.targetList.remove(target)
							# kill the current Target
							self.deadTargets.append(target)
							# add the currentPath to the list of paths taken
							self.pathList.append(tuple(self.currentPath))
							# clear out the current path
							self.currentPath.clear()
							self.point_times_list.append(tuple(self.pointTimes))
							self.pointTimes.clear()
							self.timeList.append(self.simLen - (self.t_final - time.time()))
							# wait the dely to spawn a new Target
							# time.sleep(self.spawnDelay)
							# spawn a new Target
							# figure out how to fix this preferabaly without using multithreading

							# this block of code ensures that none of my Targets ever overlap
							j = 0
							xPos = random.randint(self.radius, self.screen.get_width() + 1 - self.radius)
							yPos = random.randint(self.radius, self.screen.get_height() + 1 - self.radius)
							while(j < len(self.targetList)):
								if(0 <= ((self.targetList[j].getXPos() - xPos)**2 + (self.targetList[j].getYPos() - yPos)**2) and ((self.targetList[j].getXPos() - xPos)**2 + (self.targetList[j].getYPos() - yPos)**2) <= (2 * self.radius)**2):
									xPos = random.randint(self.radius, self.screen.get_width() + 1 - self.radius)
									yPos = random.randint(self.radius, self.screen.get_height() + 1 - self.radius)
									j = 0
								else:
									j += 1
							t = Target(self.radius, self.screen, xPos, yPos)
							self.targetList.append(t)
							self.spawnedTargets.append(t)
							# print out the loss for debugging
							# print(lossList)
							# print(targetList)
							pygame.display.update()
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
		# gotta copy the list (there is a much better way to do this, but this works for now)
		if(len(self.pathList) > 0):
			self.pathList.pop(0)
	# compute the loss and store the value in the list
		for i in range(len(self.deadTargets) - 1):
			t = self.deadTargets[i]
			t_connect = self.deadTargets[i + 1]
			# have to get pathList[i + 1] because pathList stores first path and we want to skip that value
			self.lossList.append(self.RMSE(t, t_connect, self.pathList[i]))

		# self.flicking(self.deadTargets[0], self.deadTargets[1], self.pathList[1])
		for target in self.targetList:
			target.deactivate()
# in terms of data displaying, you could use a few different graphs to show a few different things
	def getAccuracy(self):
		# total user's accuracy
		if(self.totalClicks > 0):
			accuracy = len(self.deadTargets) / self.totalClicks
		else:
			accuracy = 0
		return str(accuracy * 100) + '%'
	def getMeanLoss(self):
		# user's mean loss between Targets
		summ = 0
		for l in self.lossList:
			summ += l

		if(len(self.lossList) > 0):
			meanLoss = summ / len(self.lossList)
		else:
			meanLoss = 1

		return str(meanLoss * 100) + '%'
	# plot RMSE discrete time series
	def plotRMSE(self):
		if(len(self.timeList) > 0):
			self.timeList.pop(0)
		plt.scatter(self.timeList, self.lossList)
		plt.xlabel('Time (seconds)')
		plt.ylabel('RMSE')
		plt.yticks(np.arange(0, 1, 0.05))
		plt.xticks(np.arange(0, self.simLen, self.simLen / 20))
		plt.xlim(0, self.simLen)
		plt.ylim(0, 1)
		plt.show()

	# implement distance formula
	def distance(self, x1, y1, x2, y2):
		term1 = (x1 - x2) ** 2
		term2 = (y1 - y2) ** 2
		d = math.sqrt(term1 + term2)
		return d
# determine if, when going to the target, the user over or under flicked the cursor
# overflicking is functional now
# overflicking: compute the tangent line of the circle perpendicular to the segment from the cursor to the edge of the circle that goes through the center of the circle
# overflicking; check if any points in the path are past this line
	def flicking(self, t2, path, times):
		x1 = path[0][0]
		y1 = path[0][1]
		h = t2.getXPos()
		k = t2.getYPos()
		m = float(k - y1) / float(h - x1)
		b = y1 - m * x1
		# print((h, k))
		# print((x1, y1))
		# print((m, b))
		# y = mx + b is the equation of the line from the Cursor to the center of the target

		# compute the points where the perp intersects the circle
		# use this point to compute the tangent
		radius = t2.getRadius()
		# equation of circle: (x - h)^2 + (y - k)^2 = radius^2
		# (x - h)^2 + (mx + b - k)^2 = radius^2
		# x^2 - 2hx + h^2 + (mx)^2 + 2bmx + b^2 - 2kmx - 2bk + k^2 = radius^2
		# x^2 + m^2 * x^2 - 2hx + 2bmx - 2kmx + h^2 + b^2 - 2bk + k^2 = radius^2
		# x^2 (m^2 + 1) - x(2h - 2bm + 2km) + h^2 + b^2 + k^2 - 2bk - radius^2 = 0
		a = float(m ** 2) + 1
		b1 = (float(2*b*m) - float(2*h) - float(2*k*m))
		c = float(h ** 2) + float(b ** 2) + float(k ** 2) - float(2*b*k) - float(radius ** 2)
		# now we implement a quadratic solver
		# since the perp goes through the center, there will always be two positive solutions
		discrim = float(b1 ** 2) - float(4 * a * c)
		root1 = -b1 + (float(math.sqrt(discrim)) / float(2 * a))
		root2 = -b1 - (float(math.sqrt(discrim)) / float(2 * a))
		# compute the two points of intersection between the target and the perp here
		sol1 = float(root1 * m) + b
		sol2 = float(root2 * m) + b
		farRoot = None
		farSol = None
		# take the far point of intersection, bc line will be tangent at that point
		if(self.distance(x1, y1, root1, sol1) > self.distance(x1, y1, root2, sol2)):
			farRoot = root1
			farSol = sol1
		else:
			farRoot = root2
			farSol = sol2

		# dy / dx [(x - h)^2 + (y - k)^2 = radius^2] = (h - x) / (y - k)
		slope = float(h - farRoot) / float(farSol - k)
		y_intercept = farSol - float(slope * farRoot)
		# print((slope, y_intercept))
		# equation of tangent: y = slope * x + y_intercept
		# determine whether the center of the circle is above or below the tangent
		sol_circ = float(h * slope) + y_intercept
		great = True
		if(k < sol_circ):
			great = False

		# print(great)
		overflicking = False
		# this is right
		# now loop through all points in the path and make sure that, if great = True, they are above the tangent, and if great = False, they are below the tangent
		for point in path:
			point_y = float(point[0] * slope) + y_intercept
			if(great):
				if(point[1] < point_y):
					overflicking = True
			elif(not(great)):
				if(point[1] > point_y):
					overflicking = True

		# start computing underflicking
		# for underflicking, we essentially want to check if there is a period of acceleration then rapid deceleration all under the tangent line
		# between points compute the velocity
		# then we have to measure the Δv. If the Δv is positive, that means that the velocity increasing, but if it's negative, we know that the velocity is decreasing
		# if the velocity is not increasing or remaining constant, it must be decreasing, thus the cursor must be slowing down.
		# since this is all taking place below the tangent, the user must be underflicking their cursor if it is slowing down before the tangent
		# since the user will, statistically speaking, never perfectly flick, we can sort of ignore that case
		slow = False
		# pixels / second
		vPrev = 0
		underflicking = False
		if(not(overflicking)):
			for i in range(len(path) - 1):
				x_cur = path[i][0]
				y_cur = path[i][1]
				x_nxt = path[i + 1][0]
				y_nxt = path[i + 1][1]
				cur_sol_y = float(x_cur * slope) + y_intercept
				nxt_sol_y = float(x_nxt * slope) + y_intercept
				cur_time = times[i]
				nxt_time = times[i + 1]
				d = self.distance(x_cur, y_cur, x_nxt, y_nxt)
				t_del = nxt_time - cur_time
				v = float(d / t_del)
				if(great):
					if(y_cur > cur_sol_y and y_nxt > nxt_sol_y):
						if(v < vPrev):
							underflicking = True
				elif(not(great)):
					if(y_cur < cur_sol_y and y_nxt < nxt_sol_y):
						if(v < vPrev):
							underflicking = True
				vPrev = v
		if(underflicking):
			return 'underflicking'
		elif(overflicking):
			return 'overflicking'
		else:
			return 'perfect flick'
	def computeFlickings(self):
		if(len(self.point_times_list) > 0):
			self.point_times_list.pop(0)
		flickingList = []
		for i in range(len(self.pathList)):
			# top of pathList has already been popped off
			t2 = self.deadTargets[i + 1]
			flickingList.append(self.flicking(t2, self.pathList[i], self.point_times_list[i]))

		self.flicks = flickingList.copy()


# relay the user's cursor movement back to them sort of like a replay
# add a speed parameter: that would be pretty sick

	def plotReplay(self, pathx, pathy, title, flick):
		# respawn the initial Targets
		# for i in range(self.numTargets):
		# 	self.spawnedTargets[i].activate()
		plt.xlabel('x')
		plt.ylabel('y')
		plt.suptitle(title, fontsize=10)
		plt.yticks(np.arange(0, 800, 100))
		plt.xticks(np.arange(0, 1300, 150))
		plt.xlim(0, 1300)
		plt.ylim(0, 800)
		plt.scatter(pathx, pathy)
		plt.plot((pathx[0], pathx[-1]), (pathy[0], pathy[-1]), 'k-')
		plt.text(400, 820, flick)
		# now I execute a replay such that it looks like I'm just running the same session again
		plt.show()
			# iterate through the replay_t_points and essentially wait that much time before spawning the corresponding point (a circle with 0 < radius < 1)
			# between spawning points, check if the time is past a certain benchmark that indicates if a Target hit
			# if aa Target was hit, spawn it
			# make the points a very different color than red so that the user doesn't confuse them for targets

	def replays(self):
		for i in range(len(self.pathList)):
			pathy = []
			pathx = []
			title = 'Plot of path between target ' + str(i + 1) + ' and target ' + str(i + 2)
			for j in self.pathList[i]:
				pathy.append(j[1])
				pathx.append(j[0])
			self.plotReplay(pathx, pathy, title, self.flicks[i])
