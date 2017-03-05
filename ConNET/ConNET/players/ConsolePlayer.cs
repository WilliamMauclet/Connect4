using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using ConNET.game;
using ConNET.gui;

namespace ConNET.players {
    class ConsolePlayer : Player {

        private Game game;
        private bool even;
        public bool Even {
            get {
                return even;
            }
        }

        private string name;

        public ConsolePlayer(string name = "ConsolePlayer") {
            this.name = name;
        }

        public void signalJoin(Game game, bool even) {
            if(game == null) {
                this.game = game;
                this.even = even;
            }
        }

        public void signalTurn(CellState[,] grid) {
            System.Console.WriteLine(name + ", your turn. Type number to drop disk in column.");
            ConsoleTools.printGrid(grid);
            string inp = System.Console.ReadLine();
            double inpD = Char.GetNumericValue(inp, 0);
            if (inpD > -1
                && inpD < 7
                && (inpD % 1) == 0) {
                game.putDisk(this, (int)inpD);
            }
        }

    }
}
