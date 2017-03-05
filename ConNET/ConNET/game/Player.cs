using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConNET.game {

    public interface Player {

        bool Even {
            get;
        }

        void signalJoin(Game game, bool isEven);

        void signalTurn(CellState[,] grid);

    }

}
