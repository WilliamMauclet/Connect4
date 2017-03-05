using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConNET.game {
        
    public class DefaultGame : Game {

        private int[,] disks; // disks[turn,0] = x; disks[turn,1] = y; player = turn / 2;

        public CellState[,] Grid {
            get {
                return toGrid(disks);
            }
        }

        private Player evenPlayer;
        private Player unevenPlayer;

        private Player currentPlayer; // the player that can enter a disk now

        public DefaultGame(Player evenPlayer, Player unevenPlayer, int[] drops = null){
            this.evenPlayer = this.currentPlayer = evenPlayer;
            this.unevenPlayer = unevenPlayer;
            disks = createDisks(drops);
            evenPlayer.signalJoin(this, true);
            unevenPlayer.signalJoin(this, false);
        }

        public void start() {
            currentPlayer.signalTurn(this.Grid);
        }

        public void putDisk(Player player, int x) {
            dropDisk(x, disks);
            if(currentPlayer == evenPlayer) {
                currentPlayer = unevenPlayer;
            } else {
                currentPlayer = evenPlayer;
            }
            currentPlayer.signalTurn(this.Grid);
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
                disks[turn, 0] = -1;
                disks[turn, 1] = -1;
                if (drops != null && turn < drops.Length) {
                    disks[turn, 0] = drops[turn];
                    disks[turn, 1] = getNewY(disks, drops[turn]);
                }
            }
            return disks;
        }

        private static int getNewY(int[,] disks, int x) {
            int nbDropsInColumn = 0;
            int turn = 0;
            while (turn < 6*7 && disks[turn, 1] != -1) {
                if (disks[turn, 0] == x) {
                    nbDropsInColumn++;
                }
                turn++;
            }
            return nbDropsInColumn;
        }

        public static CellState[,] createEmptyGrid() {
            CellState[,] grid = new CellState[7, 6];
            for(int y = 0; y < 6; y++) {
                for(int x = 0; x < 7; x++) {
                    grid[x, y] = CellState.Empty;
                }
            }
            return grid;
        }

        private static CellState[,] toGrid(int[,] disks) {
            CellState[,] grid = createEmptyGrid();
            int turn = 0;
            while (turn < 6 * 7 && disks[turn, 0] != -1) {
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
        
        public static int[,] dropDisk(int x, int[,] disks) {
            int turn = 0;
            while (disks[turn, 0] != -1) {
                turn++;
            }
            disks[turn, 0] = x;
            disks[turn, 1] = getNewY(disks, x);
            return disks;
        }

        #endregion

    }
}
