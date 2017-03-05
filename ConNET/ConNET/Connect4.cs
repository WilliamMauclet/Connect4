using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using ConNET.model;
using ConNET.gui;

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
                string inp = System.Console.ReadLine();
                double inpD = Char.GetNumericValue(inp, 0);
                if(inpD > -1
                    && inpD < 7
                    && (inpD % 1) == 0) {
                    game.dropDisk((int)inpD);
                }
                ConsoleTools.printGrid(game.Grid);
            }
        }

    }
}
