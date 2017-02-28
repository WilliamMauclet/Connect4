import random

class AvoidingAndMoveEvaluatingRobot():
	"""This robot DOES NOT LEARN. 
	It applies simple algorithms to see if it can avoid a four in a row.
	In addition, it looks to see if the move it wants to make does create an immediate win possibility for the opponent.
	Except for that, it just plays randomly."""
	
	def chooseMove(self, grid):
		raise NotImplementedError("Not implemented yet!")