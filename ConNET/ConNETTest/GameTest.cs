using System;
using Microsoft.VisualStudio.TestTools.UnitTesting;

using ConNET.game;

namespace ConNETTest {
    [TestClass]
    public class GameTest {
        [TestMethod]
        public void testCreateDisks() {
            DefaultGame game = new DefaultGame(new TestPlayer(true), new TestPlayer(false),
                new int[12] { 0,1,2,3,4,5,6,5,4,3,2,1 });
            Assert.AreEqual(CellState.EvenDisk, game.Grid[0, 0]);
            Assert.AreEqual(CellState.UnevenDisk, game.Grid[1, 0]);
            Assert.AreEqual(CellState.EvenDisk, game.Grid[2, 0]);
            Assert.AreEqual(CellState.UnevenDisk, game.Grid[3, 0]);
            Assert.AreEqual(CellState.EvenDisk, game.Grid[4, 0]);
            Assert.AreEqual(CellState.UnevenDisk, game.Grid[5, 0]);
            Assert.AreEqual(CellState.EvenDisk, game.Grid[6, 0]);
            Assert.AreEqual(CellState.UnevenDisk, game.Grid[1, 1]);
            Assert.AreEqual(CellState.EvenDisk, game.Grid[2, 1]);
            Assert.AreEqual(CellState.UnevenDisk, game.Grid[3, 1]);
            Assert.AreEqual(CellState.EvenDisk, game.Grid[4, 1]);
            Assert.AreEqual(CellState.UnevenDisk, game.Grid[5, 1]);
        }
    }

}
