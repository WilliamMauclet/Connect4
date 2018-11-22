import unittest, grid, player, options, strutils

proc fill_columns(grid:var Grid, player:Player, columns:varargs[int]) =
  for column in columns:
    for i in 0..<HEIGHT:
      grid.add_pawn(column, player)

suite "Grid":
  var 
    grid: Grid

  setup:
    grid = new_grid()

  test "get_empty_top_index":
    check new_grid().get_empty_top_index(4).get() == 0

  # TODO
  # test "get_empty_top_index with full column":
  #   check new_grid().get_empty_top_index(4).get() == 5

  test "check initialization":
    check grid[4][2] == ZERO
  
  test "check column getter":
    check new_grid()[4][3] == ZERO

  test "add_pawn":
    grid.add_pawn(2, X)
    check grid[2][0] == X

  test "add_pawn twice":
    grid.add_pawn(2, Y)
    grid.add_pawn(2, X)
    check grid[2][0] == Y
    check grid[2][1] == X

  test "get_state_string_representation":
    grid.add_pawn(2, X)
    check "x" in grid.get_state_string_representation()
    check (not("y" in grid.get_state_string_representation()))

  test "has_four_in_a_column #none":
    check grid.has_winner().isNone()

  test "has_four_in_a_column #not_enough":
    for i in 0..2:
      grid.add_pawn(2, X)
    check grid.has_winner().isNone()

  test "has_four_in_a_column #enough":
    for i in 0..3:
      grid.add_pawn(2, X)
    check grid.has_winner().isSome()
    check grid.has_winner().get() == X

  test "has_four_in_a_row #none":
    check grid.has_winner().isNone()

    test "has_four_in_a_row #interleave":
      grid.add_pawn(3, Y)
      grid.add_pawn(3, X)
      grid.add_pawn(3, Y)
      grid.add_pawn(3, Y)
      grid.add_pawn(3, Y)
      check grid.has_winner().isNone()
      
  test "has_four_in_a_row #not_enough":
    for x in 2..4:
      grid.add_pawn(x, Y)
    check grid.has_winner().isNone()
  
  test "has_four_in_a_row #enough":
    for x in 2..5:
      grid.add_pawn(x, Y)
    check grid.has_winner().isSome()
    check grid.has_winner().get() == Y
  
  test "get_diagonal_down":
    grid.add_pawn(5, X)
    check grid.get_diagonal_down(0, 5) == @[ZERO, ZERO, ZERO, ZERO, ZERO, X]

  test "get_diagonal_up #complex":
    grid.add_pawn(0, Y)
    grid.add_pawn(1, Y)
    grid.add_pawn(1, X)
    check grid.get_diagonal_up(0, 0) == @[Y, X, ZERO, ZERO, ZERO, ZERO]

  test "has_winner (no)":
    grid.add_pawn(0, X)
    grid.add_pawn(4, Y)
    grid.add_pawn(4, Y)
    grid.add_pawn(4, Y)
    check grid.has_winner().isNone()
  
  test "has_winner (Y,up)":
    grid.add_pawn(4, Y)
    grid.add_pawn(4, Y)
    grid.add_pawn(4, Y)
    grid.add_pawn(4, Y)
    check grid.has_winner().get() == Y

  test "has_winner (X,right)":
    grid.add_pawn(2, X)
    grid.add_pawn(3, X)
    grid.add_pawn(4, X)
    grid.add_pawn(5, X)
    check grid.has_winner().get() == X

  test "has_winner (X,diagonal up)":
    grid.add_pawn(1, X)
    grid.add_pawn(2, Y)
    grid.add_pawn(2, X)
    grid.add_pawn(3, Y)
    grid.add_pawn(3, Y)
    grid.add_pawn(3, X)
    grid.add_pawn(4, X)
    grid.add_pawn(4, Y)
    grid.add_pawn(4, X)
    grid.add_pawn(4, X)
    check grid.has_winner().get() == X

  test "has_winner (X,diagonal down)":
    grid.add_pawn(1, X)
    grid.add_pawn(1, Y)
    grid.add_pawn(1, X)
    grid.add_pawn(1, X)
    grid.add_pawn(2, Y)
    grid.add_pawn(2, Y)
    grid.add_pawn(2, X)
    grid.add_pawn(3, Y)
    grid.add_pawn(3, X)
    grid.add_pawn(4, X)
    check grid.has_winner().get() == X
        
  test "game_over":
    check new_grid().game_over() == false
  
  test "get_open_column_indices":
    fill_columns(grid, X, 0, 1, 4, 5)

    check grid.get_open_column_indices() == @[2, 3, 6]

  test "is_full":
    fill_columns(grid, X, 0, 1, 2, 3, 4, 5, 6)

    check grid.is_full()
    
  test "clone_for_move":
    var grid_clone = grid.clone_for_move(3, X)

    check grid[3][0] == ZERO
    check grid_clone[3][0] == X