import unittest, grid, player, options, strutils, random

proc add_one(v: var int) =
    v += 1

suite "Nim":
    test "test":
        check bool(0) == false
        check bool(1) == true
        check pred(2) == 1
        check succ(3) == 4
    
    test "echo":
        echo "hey"
        echo("hey")
    
    test "sequence":
        var sequ = @[9, 9, 9]
        for i in sequ:
            echo i

    test "add to variable argument in proc":
        var i = 1
        add_one(i)
        check i == 2

    test "same but with new var":
        var 
            i = 1
            j = i
        add_one(i)
        check j == 1
        doAssert i == 2

    test "strutils.DIGITS":
        check strutils.isDigit("2")
        doAssert (not(strutils.isDigit("k")))
    
    test "boolean expression":
        var x = 5
        check 0 < x and x <= 6

    test "random.random":
        random.randomize(92)
        for x in 0..<20:
            echo $random.random(7)
        check true
    