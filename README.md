# reversi-uct-project

## Introduction
This a project I built in CMSC474, Computational Game Theory, at the University of Maryland. In this project, I implemented the UCT algorithm for [Reversi](https://www.mastersofgames.com/rules/reversi-othello-rules.htm). The code for the game was provided by the instructor, and I built the UCT algorithm to play it. players/ordinary.py contains the UCT algorithm, while players/improved.py contains my improved version of the UCT algorithm, which was tested against the ordinary UCT algorithm under various constraints and consistently outperformed it (approximately 60% of the time, according to experiment data). The improved algorithm placed third in a competition with improved algorithms from other classmates; the class size was about 30 students.

## The UCT algorithm
At a high level, this algorithm works as follows: the algorithm takes as input the current state of the board, the player whose turn it is, all possible moves for that player, how many times it has simulated each of these moves, and how often each simulation results in a win. For any unsimulated move, the algorithm explores that move, applying itself recursively to the resulting board with the other player to move. Once each possible move has been simulated, the algorithm attempts to balance exploration with exploitation, calculating a "utility" value for each move it could simulate based on how strong the move seems and how many times it has been tried and simulating the move with the highest utility. The more times the move has resulted in a win for the current player, the higher its utility, and the less a move has been simulated, the higher the utility of simulating it again. When the alloted time to select a move runs out, the move with the highest win rate is selected, and returned by the get_move function to the game supervisor. 

To be more precise regarding the selection of which move is simulated next, this is managed by the UCB-choose algorithm. If a move has not yet been simulated, UCB-choose will select that move to be simulated next; otherwise, UCB choose calculates the following value, Q(a), for each possible move a:

Q(a) = r(a) + sqrt(2(ln t)/n(a))

Where:

- r(a) is the win rate of the move a in previous simulations
- t is the total number of simulations run from all possible moves given this board
- n(a) is the total number of simulations run using move a

And the a which results in the highest Q(a) is selected.

For more information, an explanation of this algorithm in the context of chess is provided [here](https://www.chessprogramming.org/UCT#:~:text=UCT%20(Upper%20Confidence%20bounds%20applied,score%20than%20other%2C%20better%20moves).

## Game Files
The following files are used either for the Reversi logic or for playing the Reversi game. I will note which files were provided by the instructor. 

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
This file contains the code for the improved UCT algorithm; this utilizes ordinary UCT, but with the following possible changes:

1. Until a certain turn, specified by the parameter, CORNER_TURN, set to 40, the algorithm will always take a corner, if it is available, assuming that this is the best possible move.

2. In the calculation for Q at each step, there is a constant in the square root which by default is 2. This can now be changed via the internal parameter Q_CONSTANT (though I left this unchanged by default); if Q_CONSTANT is greater, then exploration is prioritized more relative to exploitation.

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

### Multiple Games
To run two programs against each other for multiple games, cd to reversi-uct-project and put the following line of code into the terminal:

```bash
python3 test.py num_games prog1 prog2 timeout_limit verbose
```

This works as with the single game above, but with the following additions: 

- num_games sets the number of games for which the programs will run against each other.
- Between games, the system will print the total number of x wins thus far, as well as how many games have been played.

Example: to test the ordinary UCT algorithm against the improved UCT algorithm, with ordinary moving first, for 25 games; not showing the board between moves and alloting each player 0,5 seconds to move, we would say:

```bash
python3 25 test.py players.ordinary players.improved 0.5 0
```
