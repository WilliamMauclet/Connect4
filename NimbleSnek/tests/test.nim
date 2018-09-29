import unittest
from strutils import nil

suite "Testing stuff":
  test "strutils.DIGITS":
    check strutils.isDigit("2")
    check (not(strutils.isDigit("k")))

  test "boolean expression":
    var x = 5
    check 0 < x and x <= 6