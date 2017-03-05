using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using ConNET.model;

namespace ConNET.gui {
    public abstract class ConsoleTools {
      public static void printGrid(CellState[,] grid) {
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
