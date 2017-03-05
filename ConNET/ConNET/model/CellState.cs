using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConNET.model {

    public enum CellState {
        Empty = ' ',
        Filled = 'X',
        DontCare = '?',
        EvenDisk = 'E',
        UnevenDisk = 'U'
    }

    public static class CellStateMethods {

        public static char getChar(this CellState state) {
            return Char.ConvertFromUtf32((int) state)[0];
        }

    }

}
