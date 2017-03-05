using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConNET.game {

    public interface Player {

        void signalJoin(Game game);

        void signalTurn(CellState[,] grid);

    }

}
