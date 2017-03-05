using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using ConNET.game;

namespace ConNETTest {

    public class TestPlayer : Player {

        private bool even;
        public bool Even {
            get {
                return even;
            }
        }

        public TestPlayer(bool even) {
            this.even = even;
        }

        public void signalJoin(Game game, bool isEven) {
            // do nothing
        }

        public void signalTurn(CellState[,] grid) {
            // do nothing
        }
    }

}
