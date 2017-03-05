using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConNET.game {

    public interface Game {

        void start();

        void putDisk(Player player, int x);

    }

}
