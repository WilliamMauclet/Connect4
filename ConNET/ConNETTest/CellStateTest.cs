using System;
using System.Text;
using System.Collections.Generic;
using Microsoft.VisualStudio.TestTools.UnitTesting;

using static ConNET.game.CellState;

namespace ConNETTest {

    [TestClass]
    public class CellStateTest {

        [TestMethod]
        public void testCanBe() {
            Assert.IsTrue(DontCare.canBe(DontCare));
            Assert.IsTrue(DontCare.canBe(Filled));
            Assert.IsTrue(DontCare.canBe(Empty));
            Assert.IsTrue(DontCare.canBe(EvenDisk));
            Assert.IsTrue(DontCare.canBe(UnevenDisk));

            Assert.IsFalse(Filled.canBe(DontCare));
            Assert.IsTrue(Filled.canBe(Filled));
            Assert.IsFalse(Filled.canBe(Empty));
            Assert.IsTrue(Filled.canBe(EvenDisk));
            Assert.IsTrue(Filled.canBe(UnevenDisk));

            Assert.IsFalse(Empty.canBe(DontCare));
            Assert.IsFalse(Empty.canBe(Filled));
            Assert.IsTrue(Empty.canBe(Empty));
            Assert.IsFalse(Empty.canBe(EvenDisk));
            Assert.IsFalse(Empty.canBe(UnevenDisk));

            Assert.IsFalse(EvenDisk.canBe(DontCare));
            Assert.IsFalse(EvenDisk.canBe(Filled));
            Assert.IsFalse(EvenDisk.canBe(Empty));
            Assert.IsTrue(EvenDisk.canBe(EvenDisk));
            Assert.IsFalse(EvenDisk.canBe(UnevenDisk));

            Assert.IsFalse(UnevenDisk.canBe(DontCare));
            Assert.IsFalse(UnevenDisk.canBe(Filled));
            Assert.IsFalse(UnevenDisk.canBe(Empty));
            Assert.IsFalse(UnevenDisk.canBe(EvenDisk));
            Assert.IsTrue(UnevenDisk.canBe(UnevenDisk));
        }
    }
}
