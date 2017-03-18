using System;
using System.Text;
using System.Collections.Generic;
using Microsoft.VisualStudio.TestTools.UnitTesting;

using ConNET.game;

namespace ConNETTest {

    [TestClass]
    public class PatternTest {

        /*
         * 5 
         * 4 
         * 3 
         * 2    U           U
         * 1    U        U  E
         * 0 E  U  E  U  E  E  E
         *   0  1  2  3  4  5  6
         */
        private static readonly int[] TURNS = new int[12] { 0, 1, 2, 3, 4, 1, 5, 1, 6, 4, 5, 5 };
        
        [TestMethod]
        public void testFromString() {
            Pattern testPattern = new Pattern(new string[2] { "I?_",
                                                              "XOI" });
            CellState[,] grid = testPattern.toGrid(new TestPlayer(true));

            Assert.AreEqual(CellState.EvenDisk, grid[0, 1]);
            Assert.AreEqual(CellState.DontCare, grid[1, 1]);
            Assert.AreEqual(CellState.Empty, grid[2, 1]);

            Assert.AreEqual(CellState.Filled, grid[0, 0]);
            Assert.AreEqual(CellState.UnevenDisk, grid[1, 0]);
            Assert.AreEqual(CellState.EvenDisk, grid[2, 0]);
        }

        [TestMethod]
        public void testMatches() {
            Player evenPlayer = new TestPlayer(true);
            Player unevenPlayer = new TestPlayer(false);
            DefaultGame game = new DefaultGame(evenPlayer, unevenPlayer, TURNS);
            // vertical pattern
            Pattern testPattern1 = new Pattern(new string[1] { "III" });
            int[,] matches1_e = testPattern1.getMatches(evenPlayer, game.Grid);
            Assert.AreEqual(1, matches1_e.GetLength(0));
            Assert.AreEqual(4, matches1_e[0, 0]);
            Assert.AreEqual(0, matches1_e[0, 1]);

            int[,] matches1_u = testPattern1.getMatches(unevenPlayer, game.Grid);
            Assert.AreEqual(0, matches1_u.GetLength(0));
            // horizontal pattern
            Pattern testPattern2 = new Pattern(new string[3] { "O", "O", "O" });
            int[,] matches2_e = testPattern2.getMatches(evenPlayer, game.Grid);
            Assert.AreEqual(1, matches2_e.GetLength(0));
            Assert.AreEqual(1, matches2_e[0, 0]);
            Assert.AreEqual(0, matches2_e[0, 1]);

            int[,] matches2_u = testPattern2.getMatches(unevenPlayer, game.Grid);
            Assert.AreEqual(0, matches2_u.GetLength(0));
            // diagonal pattern
            Pattern testPattern3 = new Pattern(new string[3] { "??O",
                                                               "?OX",
                                                               "OXX" });
            int[,] matches3_e = testPattern3.getMatches(evenPlayer, game.Grid);
            Assert.AreEqual(1, matches3_e.GetLength(0));
            Assert.AreEqual(3, matches3_e[0, 0]);
            Assert.AreEqual(0, matches3_e[0, 1]);

            int[,] matches3_u = testPattern3.getMatches(unevenPlayer, game.Grid);
            Assert.AreEqual(0, matches3_u.GetLength(0));
        }
    }

}
