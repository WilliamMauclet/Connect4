using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConNET.game {

    public enum CellState {
        Empty = ' ',
        EvenDisk = 'E',
        UnevenDisk = 'U',
        Filled = 'X',
        DontCare = '?'
    }

    public static class CellStateMethods {

        public static char getChar(this CellState state) {
            return Char.ConvertFromUtf32((int) state)[0];
        }

    }

}
