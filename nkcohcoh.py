import sys
import time
import re
import json

'''
Implementation of min-max algorithm with alpha beta pruning for a tic-tac-toe based game
called "n-k-coh-coh"
@author Shruti Rachh
'''
start=time.time()
n=int(sys.argv[1])
k=int(sys.argv[2])
timeLimit=sys.argv[4]
try:
	with open("states.txt","r+") as fr:
		savedStates=json.load(fr)
except IOError:
	savedStates={}

class State(object):
	board=""
	succ=""
	alpha=0
	beta=0
	depth=0
	secs=0
	def __init__(self,board,depth=0,secs=0,alpha=-sys.maxint,beta=sys.maxint):
		self.board=board
		self.depth=depth
		self.secs=secs
		self.alpha=alpha
		self.beta=beta
'''
Finds which player needs to play next given the current board
Input:
	board: current board eg, "..w....b."
Output:
	returns "b" for black marble player, "w" for white marble player and ".", if the input 
	board is invalid  
'''
def whichPlayer(board):
	blackCnt=board.count("b")
	whiteCnt=board.count("w")
	if blackCnt==whiteCnt or blackCnt-whiteCnt==1:
		return "w"
	elif blackCnt-whiteCnt==-1:
		return "b"
	else:
		return "."

'''
Checks whether the player has won or lost
Input:
	board: current board eg, "..w....b."
	exp: regular expression to match for k w's or b's along same row,column or diagonal
Output:
	returns 1 if the player has lost, 0 otherwise  
'''
def check(board,exp):
	if re.match(exp,board):
		return 1
	return 0

'''
Heuristic applied along the row to count the number of possibilities where a player loses
Input:
	board: current board eg, "..w....b."
	exp: regular expression to match for k w's or b's along same row,column or diagonal
Output:
	returns the number of losses  
'''
def countRow(board,exp):
	count=0
	for r in range(0,len(board),n):
		count+=check(board[r:r+n],exp)
	return count

'''
Heuristic applied along the column to count the number of possibilities where a player loses
Input:
	board: current board eg, "..w....b."
	exp: regular expression to match for k w's or b's along same row,column or diagonal
Output:
	the number of losses  
'''
def countCol(board,exp):
	count=0
	for r in range(0,n):
		count+=check(board[r::n],exp)
	return count

'''
Gets list of all the diagonals of length k on the board
Input:
	board: current board eg, "..w....b."
Output:
	list of diagonals 
'''
def getDiags(board):
	diags=[]
	for r in range(0,(n-k+1)):
		diags.append([board[(i*n)+i+r] for i in range(n-r)]) 	
		diags.append([board[(i*n)+n-1-i-r]for i in range(n-r)])
		if r!=0:
			diags.append([board[(i*n)+i-r] for i in range(r,n)])
			diags.append([board[(i*n)+n-1-i+r] for i in range(r,n)])
	return diags

'''
Heuristic applied along the diagonal to count the number of possibilities where a player loses
Input:
	board: current board eg, "..w....b."
	exp: regular expression to match for k w's or b's along same row,column or diagonal
Output:
	returns the number of losses  
'''
def countDiag(board,exp):
	count=0
	diags=getDiags(board)
	for d in diags:
		count+=check(''.join(d),exp)
	return count

'''
Checks for teminal state whether the player has won or lost or it is a draw
Input:
	board: current board eg, "..w....b."
	player: b for black marble player, w for white marble player
Output:
	returns true if it is a terminal state, false otherwise
'''
def isTerminal(board,player):
	exp=player*k
	return countRow(board,exp)==1 or countCol(board,exp)==1 or countDiag(board,exp)==1 or board.find(".")==-1

'''
Estimates the possibilities for the max player (i.e. the player that has to play the next move)
whether the player will win, lose or it will be a draw depending on the current state.
Input:
	board: current board eg, "..w....b."
	player: b for black marble player, w for white marble player
Output:
	returns true if it is a terminal state, false otherwise
'''
def evaluate(board,player):
	wPlayer="[w.]{"+str(k)+"}"
	bPlayer="[b.]{"+str(k)+"}"
	w=countRow(board,wPlayer)+countCol(board,wPlayer)+countDiag(board,wPlayer)
	b=countRow(board,bPlayer)+countCol(board,bPlayer)+countDiag(board,bPlayer)
	if player=="w":
		return (b-w)
	return (w-b)

'''
Groups the indices such that if we place a marble (white or black) on one of them, 
we would effectively be placing on all of them by rotating the board clockwise 
or anti-clockwise multiple times.
Output:
	2D list containing the groups of indices
'''
def computeInd():
	ind=[]
	for i in range(n/2):
		for j in range(i,n-i-1):
			ind.append([((i*n)+j),(n-1-j)*n+i,(n-i)*n-1-j,(j*n)+(n-i-1)])
	if n%2!=0:
		ind.append([(n*n)/2])
	return ind

'''
Computes the successors of the current board by placing the marble (black or white) 
at each of the unique locations only by not considering the positions at which
a piece can be placed by rotating the existing successors so that duplicate states
are not generated since all of them will evaluate to same result.  
Input:
	board: current board eg, "..w....b."
	player: b for black marble player, w for white marble player
	ind: contains the groups of indices that are treated same (by rotations of existing boards)
Output:
	list of successor states 
'''
def successor(board,player,ind):
	succ=[]
	tmp=board
	for i in ind:
		for j in i:
			if board[j]==".":
				tmp=board[:j]+player+board[(j+1):] #http://stackoverflow.com/questions/1228299/change-one-character-in-a-string-in-python/1228327#1228327
				succ.append(tmp)
				break
	return succ

'''
Changes the player from b to w or vice versa depending on whose turn is next.
Input:
	player: b for black marble player, w for white marble player
Output:
	returns b if the current player is w, otherwise w
'''
def switchPlayer(player):
	if player=="b":
		return "w"
	else:
		return "b"

'''
Checks whether there is sufficient time to predict the outcome of next move played by
a player by expanding the nodes further. This is done by comparing the time that is 
left to guess the next move computed by subtracting the timeLimit and time taken so 
far and estimated time that is required to expanding all the states onto next move.
Example, if state is ".w.w.b.b." for n=3,k=3 and depth=1 and t=time to expand the current 
state that is pre-computed for each state. At any depth d, we need to expand b^d nodes each 
will take time t, then it checks,
	if (timeLimit-time_taken_so_far)<t*(b^d), then it will not have sufficient time to expand
		all nodes further. 
Input:
	state: current state of the board
	bfactor: the max branching factor for a state
Output:
	returns true if there is no sufficient time to expand onto next depth,otherwise false
'''
def isTimeout(state,bfactor):
	return float(timeLimit)-(time.time()-start)<state.secs*(bfactor**state.depth)

'''
Performs the computations for the max player (the player whose turn is next to whom the best
move will be suggested) 
Input:
	state: current state of the board
	player: b for black marble player, w for white marble player
	ind: contains the groups of indices that are treated same (by rotations of existing boards)
Output:
	returns the state containing the best move
'''
def maxValue(state,player,ind):
	if isTerminal(state.board,switchPlayer(player)):
		state.alpha=1
		return state
	if isTimeout(state,len(ind)):
		state.alpha=evaluate(state.board,player)
		return state
	succ=successor(state.board,player,ind)
	secs=time.time()-start
	for s in succ:
		succState=State(s,(state.depth+1),secs,state.alpha)
		sc=minValue(succState,switchPlayer(player),ind).beta
		if state.alpha<sc:
			state.succ=succState.board
			state.alpha=sc
		if state.alpha>=state.beta:
			return state
		savedStates[state.board]=state.succ
	return state

'''
Performs the computations for the min player (the opponent player),
assuming that the player will always make his best move.
Input:
	state: current state of the board
	player: b for black marble player, w for white marble player
	ind: contains the groups of indices that are treated same (by rotations of existing boards)
Output:
	returns state containing the best move
'''
def minValue(state,player,ind):
	if isTerminal(state.board,switchPlayer(player)):
		state.beta=-1
		return state
	if isTimeout(state,len(ind)):
		state.beta=evaluate(state.board,switchPlayer(player))
		return state
	succ=successor(state.board,player,ind)
	secs=time.time()-start
	for s in succ:
		succState=State(s,(state.depth+1),secs,-sys.maxint,state.beta)
		sc=maxValue(succState,switchPlayer(player),ind).alpha
		if state.beta>sc:
			state.succ=succState.board
			state.beta=sc
		if state.alpha>=state.beta:
			return state
		savedStates[state.board]=state.succ
	return state

'''
Returns the position of the best move by comparing the board containing the
best move and the original board given in the input 
Input:
	orig: original board given in the input 
	new: board containing the suggested best move 
Output:
	position of the best move
'''
def getPos(orig,new):
	for pos in range(len(orig)):
		if orig[pos]!=new[pos]:
			return pos
	return -1

board=sys.argv[3]
player=whichPlayer(board)

'''
 Handles the invalid input case if the board does not contain n*n characters
 or if the player whose next turn is to be played is neither black or white
 in case when input is of the form "w..w.w.b." which could never happen
 since black and white marble player are playing alternatively.
'''
if len(board)!=(n*n) or player=="." or k>n:
	print "Invalid input for state of board!"
elif savedStates and board in savedStates:
	print "Trying to find best move from the database.."
	pos=getPos(board,savedStates[board])
	if pos!=-1:
		print "Hmm. I would recommend putting your marble at row "+str(pos/n)+" and column "+str(pos%n)
	print "New board:"
	print savedStates[board]
else:
	print "Thinking! Please wait.."
	state=State(board)
	ind=computeInd()
	bestState=maxValue(state,player,ind)
	pos=getPos(board,bestState.succ)
	if pos!=-1:
		print "Hmm. I would recommend putting your marble at row "+str(pos/n)+" and column "+str(pos%n)
	print "New board:"
	print bestState.succ
	with open("states.txt","wb") as fw:
		json.dump(savedStates,fw)