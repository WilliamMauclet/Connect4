using System;
using System.Text;
using System.Collections.Generic;
using Microsoft.VisualStudio.TestTools.UnitTesting;

using ConNET.game;

namespace ConNETTest {

    [TestClass]
    public class PatternTest {

        [TestMethod]
        public void testFromString() {
            Pattern testPattern = new Pattern(new TestPlayer(true),
                                                "I?_",
                                                "XOI");
            Assert.AreEqual(CellState.EvenDisk, testPattern.Grid[0, 1]);
            Assert.AreEqual(CellState.DontCare, testPattern.Grid[1, 1]);
            Assert.AreEqual(CellState.Empty, testPattern.Grid[2, 1]);

            Assert.AreEqual(CellState.Filled, testPattern.Grid[0, 0]);
            Assert.AreEqual(CellState.UnevenDisk, testPattern.Grid[1, 0]);
            Assert.AreEqual(CellState.EvenDisk, testPattern.Grid[2, 0]);
        }
    }

}
