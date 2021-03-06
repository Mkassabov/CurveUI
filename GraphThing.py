import json
import sys
import tkinter as tk

#set to false if >2 intersection per point is okay 
onlyTwoLoops = True

isValid = True
isClosed = False
pointSize = 25
pointNum = 0
points = {}
black, white, red = '#000000', '#FFFFFF', '#FF0000'

def line():
	if pointNum >= 1:
		x0, y0 = points['p' + str(pointNum - 1)]['x'], points['p' + str(pointNum - 1)]['y']
		x1, y1 = points['p' + str(pointNum)]['x'], points['p' + str(pointNum)]['y']
		canvas.create_line(x0, y0, x1, y1, width = 3)

def placePoint(event):
	x, y = event.x, event.y
	global isClosed
	
	nearestPoint = pointNearPoint(x, y)
	
	if nearestPoint == None:
		canvas.create_oval(x - (pointSize / 2), y - (pointSize / 2), x + (pointSize / 2), y + (pointSize / 2), outline = black, fill = white, width = 2)
		points['p' + str(pointNum)] = {'x':x, 'y':y, 'used':0, 'index':pointNum}
		isClosed = False
	else:
		if onlyTwoLoops:		
			if (points[nearestPoint]['used'] == 1) and (points[nearestPoint]['index'] != 0):
				isValid = False
		if (pointNum - points[nearestPoint]['index']) == 2:
				isValid = False
		x = points[nearestPoint]['x']
		y = points[nearestPoint]['y']
		points['p' + str(pointNum)] = {'x':x, 'y':y, 'used':1, 'index':pointNum, 'otherpoint':points[nearestPoint]['index']}
		points[nearestPoint]['used'] = 1
		points[nearestPoint]['otherpoint'] = pointNum
		canvas.create_oval(x - (pointSize / 2), y - (pointSize / 2), x + (pointSize / 2), y + (pointSize / 2), outline = red, fill = white, width = 2)
		if points[nearestPoint]['index'] == 0:
			isClosed = True
		else:
			isClosed = False
	
	line()
	incrementPointNum()
	
def incrementPointNum():
	global pointNum
	pointNum += 1

def pointNearPoint(x, y):
	for point in points:
		dist = (x - points[point]['x']) ** 2 + (y - points[point]['y']) ** 2
		if dist < (pointSize) ** 2:
			return point
	return None

def output():
	print()
	if isValid and isClosed:
		print('points:')
		print(json.dumps(points))
	else:
		print("invalid graph")

def restart():
	global points, pointNum, isValid, isClosed
	points = {}
	pointNum = 0
	isValid = True
	isClosed = False
	canvas.delete('all')
	

root = tk.Tk()
root.title("Knot Generator")

outputButton = tk.Button(text='output', command=output)
outputButton.pack(side=tk.TOP, anchor=tk.W)

restartButton = tk.Button(text='restart ', command=restart)
restartButton.pack(side=tk.TOP, anchor=tk.W)

canvas = tk.Canvas(bg=white, width=800, height=800)
canvas.pack()

canvas.bind('<ButtonPress-1>', placePoint)
root.mainloop()