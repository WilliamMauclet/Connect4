using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using ConNET.game;

namespace ConNET.gui {

    public class ConsoleTools {

        public static readonly Dictionary<CellState, char> toChar = new Dictionary<CellState, char>();

        static ConsoleTools() {
            toChar.Add(CellState.DontCare, '?');
            toChar.Add(CellState.Filled, 'X');
            toChar.Add(CellState.Empty, ' ');
            toChar.Add(CellState.EvenDisk, 'E');
            toChar.Add(CellState.UnevenDisk, 'U');
        }

        public static void printGrid(CellState[,] grid) {
            for (int y = 5; y > -1; y--) {
                string rowString = " |";
                for (int x = 0; x < 7; x++) {
                    rowString += " " + toChar[grid[x, y]] + " |";
                }
                System.Console.WriteLine(rowString);
            }
        }
    }

}
