from Grid import ColumnGrid
from MinusFirstOrderRobot import MinusFirstOrderRobot
from ZeroOrderRobot import ZeroOrderRobot
from FirstOrderRobot import FirstOrderRobot
import random

def acceptHumanMove(grid):
	inp = input("Available columns: " + str([x+1 for x in grid.getFreeColumns()])+"\n")
	acceptedInputs = ['q','Q'] + [ str(x+1) for x in grid.getFreeColumns()]
	while inp not in acceptedInputs:
		inp = input("Please give one of the following values: " + str(acceptedInputs) + "\n")
	
	if inp == 'q' or inp == 'Q':
		raise Exception("Game finished by player")
	else:
		return int(inp)-1
		
def acceptHumanMovePrev(grid):
	inp = input("Available columns: " + str([x+1 for x in grid.getFreeColumns()])+"\n")
	if inp is 'q':
		raise Exception("Game aborted")
	column = int(inp)-1
	while not grid.isColumnFree(column):
		inp = input("Available columns: " + str([x+1 for x in grid.getFreeColumns()])+"\n")
		if inp is 'q':
			raise Exception ("Game aborted")
		column = int(inp)-1
	return column
	
def chooseOpponent():
	print("Choose an opponent against whom to play:\n")
	inp = None
	acceptedInputs= ['','-1','0','1']
	while inp not in acceptedInputs:
		inp = input("-1 for MinusOneOrderRobot, 0 for ZeroOrderRobot and 1 for FirstOrderRobot (last=default): ")
	if inp is "":
		inp = acceptedInputs[-1]
	if inp is '-1':
		print("\nThis game is against an opponent playing randomly.\n")
		return MinusOneOrderRobot()
	elif inp is '0':
		print("\nThis game is against an opponent playing randomly but avoiding simple traps.\n")
		return ZeroOrderRobot()
	elif inp is '1':
		print("\nThis game is against an opponen playing randomly but avoiding (/to make) simple traps.\n")
		return FirstOrderRobot()
	else:
		raise Exception("Did not recognise robot id: '" + inp + "'")

def start():
	humanPlayerId = 'X'
	robotPlayerId = 'O'
	grid = ColumnGrid()

	print("\nWelcome to a new game of Connect 4\n")
	
	robot = chooseOpponent()
	
	print("To exit the game press Q + ENTER\n")
	print("Please do the first move")
	
	#try:
	while grid.gameOver() == -1:
		grid.printGrid()
		column = acceptHumanMove(grid)
		grid.addPawn(column, humanPlayerId)
		
		if grid.gameOver() != -1:
			break

		column = robot.chooseMove(grid)
		grid.addPawn(column, robotPlayerId)
		
	grid.printGrid()
	print("\nPlayer " + str(grid.gameOver()) + " won, congrats!\n")
	#except Exception as exc:
		#print(exc.__str__())
start()