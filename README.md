# Min-Max implementation for tic-tac-toe based game "n-k-coh-coh"

# Running the code: 
	python nkcohcoh.py n k board time-limit
It takes following command-line arguments:
1. n: the size of the board
2. k: the number of consecutive pieces that are not allowed
3. board: n*n in the form of row-major order:  ".w......b"
time-limit: time is secs left to make the next move
		 
# Description: 
n-k-coh-coh is a popular game in which we are given n*n board and there are two
players, one will be placing white marbles on the board and the other one will
place black marbles. The player wins if he can avoid placing k consecutive marbles
along same row, column or diagonal.

Our aim in the code is to suggest the best next move within specified time-limit
for the player whose turn is next, given the current state of the board in the 
form of row major order ".w......b" which is equivalent to,

| 0   | 1   | 2   |
| --- | --- | --- |
|  .  |  w  |  .  |
|  .  |  .  |  .  |
|  .  |  .  |  b  |

# State space: 
State of the game contains the following attributes:
* board: current board eg, "..w....b."
* succ: best next move for the player whose turn is next.
* alpha: alpha value is set if the player is max (i.e. the player that has to play the next move)
* beta: beta value is set if the player is min (the opponent player)
* depth: current depth in the tree used for completing the search within given time limit
* secs: the time taken to reach the current state used for completing the search within given time limit

# Successor function: 
Computes the successors of the current board by placing the marble (black or white) at each of the unique locations only by not considering the positions at which a piece can be placed by rotating the existing successors so that duplicate states are not generated since all of them will evaluate to same result.
Example, successors of the board given above can be computed as,

| 0   | 1   | 2   |
| --- | --- | --- |
|  w  |  w  |  .  |
|  .  |  .  |  .  |
|  .  |  .  |  b  |

| 0   | 1   | 2   |
| --- | --- | --- |
|  .  |  w  |  .  |
|  w  |  .  |  .  |
|  .  |  .  |  b  |

| 0   | 1   | 2   |
| --- | --- | --- |
|  .  |  w  |  .  |
|  .  |  w  |  .  |
|  .  |  .  |  b  |

The "w" marble needs to be placed at only 3 locations as shown above and the rest all can be obtained by rotating these 3 successors.

# Evaluation function:
Estimates the possibilities for the max player (i.e. the player that has to play the next move) whether the player will win, lose or it will be a draw depending on the current state. This is done as follows: first we count the number of times max player has chance of losing by checking if k marbles can be placed consecutively along the same row, column or diagonal given the current board state. Same is done for the other player. Then since we want best move for the max player we would want him to win so we subtract the count where the max loses from the count where min loses. If it is positive then max will win, if it is 0 then it is draw, otherwise min will win.
Example, evaluation function for the state,

| 0   | 1   | 2   |
| --- | --- | --- |
|  w  |  w  |  .  |
|  .  |  .  |  .  |
|  .  |  .  |  b  |

and k=3 can be computed as: b: 4 losses w: 5 losses so it will be (4-5)=-1 so our max player,in this case, w will lose if he made this move.

# Terminal states:	
The case for terminal states is also handled in similar way if encountered by checking, if k pieces of a marble (white or black) are present along same row or column or diagonal. Also the case for a draw is checked in which the board is completely filled and neither player has won or lost.

# Time-Limit:
It will determine the depth (d) upto which we need to explore which is handled as follows:

	Time remaining is computed by: timeRem = (timeLimit-time_taken_so_far) where
	 
	 time_taken_so_far: (currentTime-startTime)
The number of states that need to be explored at a depth d are: (b^d) where b is the branching factor which is computed by counting the number of maximum successors that can be generated (eg, if the board was empty).
The time (t) to explore each state will be computed when the successor function is called on that state and stored.
Then we will check if,
	`timeRem < t*(b^d)`
and there will not be sufficient time to explore all the states at depth d further, so it will stop and move on with computation of evaluation function.

# Algorithm:
	Input: n, k, board, time-limit

	Assumption: White marble player makes the first move in case the board is empty or it contains equal number of black and white marbles.
1. First, we determine which player needs to make the next move. This is done by counting the number of black and white marbles on the given board. If it is equal, we assume that white player will always start the game first so white player will play next and if number of white marbles is 1 greater than black marbles then black player will play next. It will also give error if the difference in their counts is greater than 1 since both players play alternatively. We will call the player whose turn is next as "MAX" and the other will be "MIN"
2. Implemented Alpha-Beta pruning algorithm which works as follows: We will generate successor states for max player and min player alternatively starting with max upto certain depth (d) which is determined depending on the time-limit that it is specified.
3. After reaching the states at depth (d), we will compute the evaluation function for each of these states and send the results up one level until we reach back to the initial board state. This will be done as follows: The board states in which MAX has to be make the next move will be called MAX nodes and the other as MIN nodes. If the state one above, is MAX node then we will take the maximum value of the evaluation function among all its successors. Similarly, for MIN nodes we will take the minimum value.   
4. For each state, we will also be saving the board with the best move having the best evaluation function for the MAX player. So, at the end, we will get the next best move for the MAX player.