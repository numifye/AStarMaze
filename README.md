# AStarMaze
A* Search (AI)

Purpose: Gain experience with problem solving agents and the A* algorithm


When presented a n x m, text-based maze, the game character strives to climb to the top floor using the A*-algorithm.



Character = @

Goal is always in top left (#)

An obstacle is represented by =

All other squares in the n x m board have a '.'


@ can move one square to the left, right or up of current location; off the edge of board to the left or right & will wrap-around to other side of board provided there are no obstacles in destination square

Input boards will always place @ somewhere on bottom row of the board

If there’s no path to the #, output NO PATH.
Algorithm uses heuristic specified by the command-line argument (e.g. manhattan).
Program is run from command line: python nario.py file_name heuristic
