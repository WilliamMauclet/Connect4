using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConNET.game {

    public class Pattern {

        private readonly CellState[,] grid;
        public CellState[,] Grid {
            get {
                return grid;
            }
        }

        /*
         * ? <=> DontCare
         * X <=> Filled
         * _ <=> Empty
         * I <=> me
         * O <=> the other player
         */
        public Pattern(Player me, params string[] rowStrings) {
            this.grid = toGrid(me, rowStrings);
        }

        private static CellState[,] toGrid(Player me, params string[] rowStrings) {
            int nbRows = rowStrings.Length;
            int nbColumns = rowStrings[0].Length;
            CellState[,] grid = new CellState[nbColumns, nbRows];
            for(int y = 0; y < nbRows; y++) {
                string rowString = rowStrings[nbRows - 1 - y];
                for(int x = 0; x < nbColumns; x++) {
                    grid[x, y] = toCellState(me, rowString[x]);
                }
            }
            return grid;
        }

        private static CellState toCellState(Player player, char symbol) {
            if(symbol == '?') return CellState.DontCare;
            if(symbol == 'X') return CellState.Filled;
            if(symbol == '_') return CellState.Empty;
            if(symbol == 'I') {
                if (player.Even) return CellState.EvenDisk;
                else return CellState.UnevenDisk;
            } else { // symbol == 'O'
                if (player.Even) return CellState.UnevenDisk;
                else return CellState.EvenDisk;
            }
        }

    }

}
