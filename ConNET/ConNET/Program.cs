using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using ConNET.model;

namespace ConNET
{
    public class Connect4
    {
        public static void Main(string[] args)
        {
            System.Console.WriteLine("Start game");
            Game game = new Game();
            while(! game.isWon()) {
                System.Console.WriteLine("Type number to drop disk in column.");
                char inp = (char)System.Console.Read();
                double inpD = Char.GetNumericValue(inp);
                if(inpD > -1
                    && inpD < 7
                    && (inpD % 1) == 0) {
                    game.dropDisk((int)inpD);
                }
                printGrid(game.Grid);
            }
        }

        private static void printGrid(CellState[,] grid) {
            for(int y = 5; y > -1; y--) {
                string rowString = " |";
                for (int x = 0; x < 7; x++) {
                    rowString += " " + grid[x, y].getChar() + " |";
                }
                System.Console.WriteLine(rowString);
            }
        }

    }
}
