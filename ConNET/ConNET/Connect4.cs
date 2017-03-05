using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using ConNET.game;
using ConNET.gui;
using ConNET.players;

namespace ConNET
{
    public class Connect4
    {
        public static void Main(string[] args)
        {
            System.Console.WriteLine("Start game");
            Player evenPlayer = new ConsolePlayer("Player 1");
            Player unevenPlayer = new ConsolePlayer("Player 2");
            DefaultGame game = new DefaultGame(evenPlayer, unevenPlayer);
            game.start();
        }

    }
}
