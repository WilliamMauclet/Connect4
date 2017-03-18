using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConNET.game {

    public class CellState {

        public static readonly CellState DontCare = new CellState(null, "DontCare");
        public static readonly CellState Filled = new CellState(DontCare, "Filled");
        public static readonly CellState Empty = new CellState(DontCare, "Empty");
        public static readonly CellState EvenDisk = new CellState(Filled, "EvenDisk");
        public static readonly CellState UnevenDisk = new CellState(Filled, "UnevenDisk");

        private readonly CellState superState; // this relation defines a tree on the CellStates
        public CellState SuperState {
            get {
                return superState;
            }
        }

        private string stringRep;

        public CellState(CellState superState, string stringRep) {
            this.superState = superState;
            this.stringRep = stringRep;
        }

        public bool hasSuperState() {
            return superState != null;
        }

        /**
         * Returns true if and only if te other CellState is a more specific description than this description.
         * E.g.:
         *     Filled.canBe(EvenDisk) == true;
         *     UnevenDisk.canBe(Filled) == false;
         */
        public bool canBe(CellState other) {
            if(other.Equals(this)) {
                return true;
            }
            if (! other.hasSuperState()) {
                return false;
            }
            if(other.SuperState.Equals(this)) {
                return true;
            }
            if(other.SuperState.SuperState == null) {
                return false;
            }
            if(other.SuperState.SuperState.Equals(this)) {
                return true;
            }
            return false;
        }

        public override string ToString() {
            return stringRep;
        }

    }

}
