from Grid import ColumnGrid
import random


def acceptHumanMove(grid):
	inp = input("Available columns: " + str([x+1 for x in grid.getFreeColumns()])+"\n")
	if inp is 'q':
		raise NotImplementedError()
	column = int(inp)-1
	while not grid.isColumnFree(column):
		inp = input("Available columns: " + str([x+1 for x in grid.getFreeColumns()])+"\n")
		if inp is 'q':
			raise NotImplementedError()
		column = int(inp)-1
	return column

def chooseRobotMove(grid):
	return random.choice(grid.getFreeColumns())

def start():
	humanPlayerId = 'X'
	robotPlayerId = 'O'
	grid = ColumnGrid()

	print("\nWelcome to a new game of Connect 4\n")
	print("This game is against an opponent playing randomly\n")
	print("To exit the game press Q + ENTER\n")
	print("Please do the first move")
	grid.printGrid()
	
	while not grid.gameOver():
		column = acceptHumanMove(grid)
		grid.addPawn(column, humanPlayerId)

		column = chooseRobotMove(grid)
		grid.addPawn(column, robotPlayerId)
		grid.printGrid()
	
	print("Player " + humanPlayerId + " won, congrats!\n")
	
start()