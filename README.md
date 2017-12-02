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
