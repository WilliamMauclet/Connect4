# Connect4
This project is about facing off two AI approaches to the Connect 4 game. 

On the one hand, the Hispida project (<Atheris Hispida) uses a min-max algorithm.

On the other, the ConNET project uses a pattern-matching algorithm.

The shape of the grid is as following:

> ![The grid coordinates.](https://raw.githubusercontent.com/WilliamMauclet/Connect4/master/grid.png)

The first player listens on port 9998, the other on port 9999. The first player is listens for connections, 
the other player connects and the first player makes the first move.