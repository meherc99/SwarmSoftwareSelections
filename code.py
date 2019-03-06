import sys
from api import *
from time import sleep
import numpy as np

#######    YOUR CODE FROM HERE #######################
grid =[]

class Node:
	def __init__(self,value,point):
		self.value = value  #0 for blocked,1 for unblocked
		self.point = point
		self.parent = None
		self.move=None
		self.H = 0
		self.G = 0
		
neigh=[[-1,-1],[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1]]

def isValid(pt):
	return pt[0]>=0 and pt[1]>=0 and pt[0]<200 and pt[1]<200

def neighbours(point):  #returns valid neighbours
	global grid,neigh
	x,y = point.point
	links=[]
	for i in range(len(neigh)):
		newX=x+neigh[i][0]
		newY=y+neigh[i][1]
		if not isValid((newX,newY)):
			continue
		links.append((i+1,grid[newX][newY]))
	return links
		
def diagonal(point,point2):
	return max(abs(point.point[0] - point2.point[0]),abs(point.point[1]-point2.point[1]))

def aStar(start, goal):
	#The open and closed sets
	openset = set()
	closedset = set()
	#Current point is the starting point
	current = start
	#Add the starting point to the open set
	openset.add(current)
	#While the open set is not empty
	while openset:
		#Find the item in the open set with the lowest G + H score
		current = min(openset, key=lambda o:o.G + o.H)
		#Remove the item from the open set
		openset.remove(current)
		#Add it to the closed set
		closedset.add(current)
		#If it is the item we want, retrace the path and return it
		if current == goal:
			path = []
			while current.parent:
				path.append(current)
				current = current.parent
			path.append(current)
			return path[::-1]
		#Loop through the node's children/siblings which are valid and not blocked
		for move,node in neighbours(current):
			#If it is already in the closed set, skip it
			if node in closedset:
				continue
			#if cell is blocked
			if node.value==0:
				continue
			#Otherwise if it is already in the open set
			if node in openset:
				#Check if we beat the G score 
				new_g = current.G + 1 #onl
				if node.G > new_g:
					#If so, update the node to have a new parent
					node.G = new_g
					node.parent = current
					node.move=move
			else:
				#If it isn't in the open set, calculate the G and H score for the node
				node.G = current.G + 1
				node.H = diagonal(node, goal)
				#Set the parent to our current item
				node.parent = current
				node.move=move
				#Add it to the set
				openset.add(node)
	#Throw an exception if there is no path
	raise ValueError('No Path Found')

def closestpt(pt, goals):
	nodes = np.asarray(goals)
	dist = np.sum((nodes - pt)**2, axis=1)
	dist2 = np.sum(dist,axis=1)
	closestgreen = np.argmin(dist2)
	green = nodes[closestgreen]
	closestpt = np.argmin(np.sum((green - pt)**2,axis=1))
	return closestgreen, closestpt

def shortpath(start,goals):
	steps=[]
	x=0
	min_step=5000

	for goal in goals:
		steps[x]=aStar(grid[start[0]][start[1]] , grid[int((goal[0][0]+goal[2][0])/2)][int((goal[0][1]+goal[2][1])/2)])
		if len(steps[x]) < min_step:
			min_step = len(steps[x])
			minx=x
		x=x+1

	x=0
	min_step=5000
	for x in range(0,4):
		corners[x]=astar(start, goals[minx][x])
		if len(corners[x])<min_step:
			min_step=len(corners[x])
			mincorn = x

	return corners[mincorn]



def level1(botId):
	global grid
	moveType = 5
	botsPose = get_botPose_list()
	obstaclePose = get_obstacles_list()
	greenZone = get_greenZone_list()
	redZone = get_redZone_list()
	originalGreenZone = get_original_greenZone_list()
	for i in range(200):
		grid.append([])
		for j in range(200):
			grid[i].append(Node(1,(i,j)))
	for pt in obstaclePose:
		for i in range(pt[0][0],pt[2][0]+1):
			for j in range(pt[0][1],pt[2][1]+1):
				grid[i][j]=Node(0,(i,j))

	closegreen, closecorner = closestpt(botsPose[0],greenZone)
	start=grid[botsPose[0][0]][botsPose[0][1]]
	goal=grid[greenZone[closegreen][closecorner][0]][greenZone[closegreen][closecorner][1]]
	path=aStar(start, goal)
	print(len(path))
	print("final pos:",greenZone[0][0])
	pos=get_botPose_list()
	print("initial pos:",pos[0])
	sleep(5)
	for i in range(1,len(path)):
		successful_move, mission_complete = send_command(botId,path[i].move)
		pos=get_botPose_list()
		if successful_move:
			print("YES")
		else:
			print("NO")
		if mission_complete:
			print("MISSION COMPLETE")
		pos=get_botPose_list()
		print(pos[0])

def level2(botId):
	global grid
	moveType = 5
	pos = get_botPose_list()
	obstaclePose = get_obstacles_list()
	greenZone = get_greenZone_list()
	redZone = get_redZone_list()
	originalGreenZone = get_original_greenZone_list()

	# for x in originalGreenZone:
	# 	grid=[]
	# 	# print(*greenZone)
	# 	for i in range(200):
	# 		grid.append([])
	# 		for j in range(200):
	# 			grid[i].append(Node(1,(i,j)))
	# 	for pt in obstaclePose:
	# 		for i in range(pt[0][0],pt[2][0]+1):
	# 			for j in range(pt[0][1],pt[2][1]+1):
	# 				grid[i][j]=Node(0,(i,j))

	# 	closegreen, closecorner = closestpt(pos[0],greenZone)
	# 	start=grid[pos[0][0]][pos[0][1]]
	# 	goal=grid[greenZone[closegreen][closecorner][0]][greenZone[closegreen][closecorner][1]]
	# 	print(start.point, goal.point)
	# 	path=aStar(start, goal)
	# 	print(len(path))
	# 	print("final pos:",greenZone[0][0])
	# 	pos=get_botPose_list()
	# 	print("initial pos:",pos[0])
	# 	sleep(2)
	# 	for i in range(1,len(path)):
	# 		successful_move, mission_complete = send_command(botId,path[i].move)
	# 		pos=get_botPose_list()
	# 		if successful_move:
	# 			print("YES")
	# 		else:
	# 			print("NO")
	# 		pos = get_botPose_list()
	# 		print(pos[0])
	# 	greenZone = get_greenZone_list()
	# 	print(*greenZone)
	# if mission_complete:
	# 	print("MISSION COMPLETE")
	# pos=get_botPose_list()
	# print(pos[0])

	# greenZone = originalGreenZone

	for x in originalGreenZone:
		grid=[]
		# print(*greenZone)
		for i in range(200):
			grid.append([])
			for j in range(200):
				grid[i].append(Node(1,(i,j)))
		for pt in obstaclePose:
			for i in range(pt[0][0],pt[2][0]+1):
				for j in range(pt[0][1],pt[2][1]+1):
					grid[i][j]=Node(0,(i,j))

		path = shortpath(pos[0],greenZone)
		print(len(path))
		print("final pos:",greenZone[0][0])
		pos=get_botPose_list()
		print("initial pos:",pos[0])
		sleep(2)
		for i in range(1,len(path)):
			successful_move, mission_complete = send_command(botId,path[i].move)
			pos=get_botPose_list()
			if successful_move:
				print("YES")
			else:
				print("NO")
			pos = get_botPose_list()
			print(pos[0])
		greenZone = get_greenZone_list()
		print(*greenZone)
	if mission_complete:
		print("MISSION COMPLETE")
	pos=get_botPose_list()
	print(pos[0])


def level3(botId):
	pass

def level4(botId):
	pass

def level5(botId):
	pass

def level6(botId):
	pass


#######    DON'T EDIT ANYTHING BELOW  #######################

if  __name__=="__main__":
	botId = int(sys.argv[1])
	level = get_level()
	if level == 1:
		level1(botId)
	elif level == 2:
		level2(botId)
	elif level == 3:
		level3(botId)
	elif level == 4:
		level4(botId)
	elif level == 5:
		level5(botId)
	elif level == 6:
		level6(botId)
	else:
		print("Wrong level! Please restart and select correct level")
