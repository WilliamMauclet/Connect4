using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using System.Drawing;

namespace ConNET.game {

    public class Pattern {

        private string[] rowStrings;

        /*
         * ? <=> DontCare
         * X <=> Filled
         * _ <=> Empty
         * I <=> me
         * O <=> the other player
         */
        public Pattern(string[] rowStrings) {
            this.rowStrings = rowStrings;
        }

        public int[,] getMatches(Player me, CellState[,] gameGrid) {
            CellState[,] patternGrid = toGrid(me, rowStrings);
            List<Point> points = new List<Point>();
            int width = patternGrid.GetLength(0);
            int height = patternGrid.GetLength(1);
            // (t_x,t_y) is the translation
            for (int t_x=0;t_x<=7-width;t_x++) {
                for (int t_y=0;t_y<=6-height;t_y++) {
                    if(matches(gameGrid, patternGrid, t_x, t_y)) {
                        points.Add(new Point(t_x, t_y));
                    }
                }
            }
            return toArray(points);
        }

        private bool matches(CellState[,] gameGrid, CellState[,] patternGrid, int t_x, int t_y) {
            int patternWidth = patternGrid.GetLength(0);
            int patternHeight = patternGrid.GetLength(1);
            for (int x=t_x; x<t_x+patternWidth; x++) {
                for(int y=t_y; y<t_y+patternHeight; y++) {
                    CellState patternCellState = patternGrid[x - t_x, y - t_y];
                    CellState gameCellState = gameGrid[x, y];
                    if(! patternCellState.canBe(gameCellState)) {
                        return false;
                    }
                }
            }
            return true;
        }

        public CellState[,] toGrid(Player me) {
            return toGrid(me, rowStrings);
        }

        private static CellState[,] toGrid(Player me, string[] rowStrings) {
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

        private static int[,] toArray(List<Point> points) {
            int[,] array = new int[points.Count, 2];
            for(int y = 0; y < points.Count; y++) {
                array[y, 0] = points.ElementAt(y).X;
                array[y, 1] = points.ElementAt(y).Y;
            }
            return array;
        }

    }

}
