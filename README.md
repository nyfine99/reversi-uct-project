# reversi-uct-project

## Introduction
This a project I built in CMSC474, Computational Game Theory, at the University of Maryland. In this project, I implemented the UCT algorithm for a (slightly modified) version of reversi. The code for the game was provided by the instructor, and I built the UCT algorithm to play it. players/ordinary.py contains the UCT algorithm, while players/improved.py contains my improved version of the UCT algorithm, which was tested against the ordinary UCT algorithm under various constraints and consistently outperformed it (approximately 60% of the time, according to experiment data). The improved algorithm placed third in a competition with improved algorithms from other classmates; the class size was about 30 students.

## The UCT algorithm
An explanation of this algorithm in the context of chess is provided here: https://www.chessprogramming.org/UCT#:~:text=UCT%20(Upper%20Confidence%20bounds%20applied,score%20than%20other%2C%20better%20moves.

## Game Files
The following files are used either for the reversi logic or for playing the reversi game. I will note which files were provided by the instructor. 

### reversi.py
This file contains the game's logic, as well as functions to obtain the move for a predefined computer player (which isn't very good at the game) and to obtain the move for a human player. Provided by the instructor.

### supervisor.py
This file allows for the user to pit two of the algorithms against each other, a human player against one of the algorithms, or two humans against each other for a single game. Usage details to follow. Provided by the instructor.

### test.py 
This file allows for the user to pit two of the algorithms against each other, a human player against one of the algorithms, or two humans against each other for several games, and to observe the results. Usage details to follow.

## Player Files
The following files are all contained within the "players" folder, and contain essential functions for both human and automated players. I will note which files were provided by the instructor.

### computer.py
This file simply contains the get_move function for the predefined computer player. Provided by the instructor.

### human.py
This file allows a human to play against any of the automated players, or against another human.

### improved.py 
This file contains the code for the improved UCT algorithm.

### ordinary.py
This file contains the code for the ordinary UCT algorithm.

### random_player.py
This file simply contains the get_move function for the predefined random player, which moves randomly. Provided by the instructor.

## Usage

### Single Game 
To run two programs against each other, to play against a program, or to play against another human, cd to reversi-uct-project and put the following line of code into the terminal:

```bash
python3 supervisor.py prog1 prog2 timeout_limit verbose
```

prog1: the name of the program which will go first, and play as X. Example: to assign a human player to be X, use "players.human" as prog1.

prog2: the name of the program which will go second, and play as O. Example: to assign a UCT (ordinary) player to be O, use "players.ordinary" as prog2.

timeout_limit (optional): the time alloted to any player using some form of UCT to make their move. By default, this is 1 second.

verbose (optional): determines whether or not to show the board before each move; 1 (True) to show the board, 0 (False) not to show the board. By default, this is True.

Example: to test the ordinary UCT algorithm against the improved UCT algorithm, with ordinary moving first, showing the board between moves, and alloting each player 2 seconds to move, we would say:

```bash
python3 supervisor.py players.ordinary players.improved 2.0 1
```
