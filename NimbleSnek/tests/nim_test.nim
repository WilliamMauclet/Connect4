import unittest, strutils, grid, player, options, random, sequtils

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
        check isDigit("2")
        doAssert (not(isDigit("k")))
    
    test "boolean expression":
        var x = 5
        check 0 < x and x <= 6

    test "random.random":
        random.randomize(92)
        for x in 0..<20:
            echo $random.random(7)
        check true
    
    test "count":
        let
            s = @[1, 2, 2, 3, 2, 4, 2]
            c = s.count(2)
        assert c == 4

    test "concat":
        let
            s1 = @[1, 2, 3]
            s2 = @[4, 5]
            s3 = @[6, 7]
            total = concat(s1, s2, s3)
        assert total == @[1, 2, 3, 4, 5, 6, 7]
    
    test "concat arrays":
        let 
            a = @[1, 2, 3]
            b = @[4, 5, 6]
        var c: seq[int]
        c = concat(a, b)

        assert c == @[1, 2, 3, 4, 5, 6]

    test "array indices":
        var arr:array[3,int]
        for i in 0..2:
            arr[i] = i + 3
        assert arr == [3, 4, 5]

    test "array to seq":
        var arr = [1, 2, 3]
        assert @arr == @[1, 2, 3]