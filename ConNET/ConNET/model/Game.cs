using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConNET.model {
        
    public class Game {

        private int[,] disks; // disks[turn,0] = x; disks[turn,1] = y; player = turn / 2;

        public CellState[,] Grid {
            get {
                return toGrid(disks);
            }
        }

        public Game() {
            disks = createDisks(null);
        }

        public Game(int[] drops) {
            disks = createDisks(drops);
        }

        public void dropDisk(int x) {
            int turn = 0;
            while(disks[turn,0] != -1) {
                turn++;
            }
            setTurn(turn, x, getNewY(disks, x));
        }

        public bool isWon() {
            return false; //TODO
        }

        public bool columnFull(int x) {
            return getNewY(disks, x) == 6;
        }

        #region utils

        private void setTurn(int turn, int x, int y) {
            disks[turn, 0] = x;
            disks[turn, 1] = y;
        }

        private static int[,] createDisks(int[] drops) {
            int[,] disks = new int[6 * 7, 2];
            for (int turn = 0; turn < 6 * 7; turn++) {
                if (drops != null && turn < drops.Length) {
                    disks[turn, 0] = drops[turn];
                    disks[turn, 1] = getNewY(disks, drops[turn]);
                } else {
                    disks[turn, 0] = disks[turn, 1] = -1;
                }
            }
            return disks;
        }

        private static int getNewY(int[,] disks, int x) {
            int nbDropsInColumn = 0;
            int turn = 0;
            while (disks[turn, 0] != -1) {
                if (disks[turn, 0] == x) {
                    nbDropsInColumn++;
                }
                turn++;
            }
            return nbDropsInColumn;
        }

        private static CellState[,] toGrid(int[,] disks) {
            CellState[,] grid = new CellState[7, 6];
            int turn = 0;
            while (disks[turn, 0] != -1) {
                int x = disks[turn, 0];
                int y = disks[turn, 1];
                if(turn % 2 == 0) { // even
                    grid[x, y] = CellState.EvenDisk;
                } else { // uneven
                    grid[x, y] = CellState.UnevenDisk;
                }
                turn++;
            }
            return grid;
        }

        #endregion

    }
}
