import copy
import math
import turtle
import random
n=8
t=turtle.Turtle()
s=turtle.Screen()
boardSize=90
s.bgcolor("forest green")
s.tracer(0,0)
t.speed(10)
s.setup(n*120,n*120)
gameboard=[]
player1="black"
player2="white"

def drawSquare(height):
	for i in range(4):
		t.pendown()
		t.forward(height)
		t.right(90)
	t.penup()

def drawColumn(n,height):
	start=t.xcor(),t.ycor()
	for i in range(n):
		t.pendown()
		drawSquare(height)
		t.forward(height)
	t.penup()
	t.goto(start)

def drawBoard(n):
	height=boardSize
	t.penup()
	t.goto((-n)/2*height,(n)/2*height)
	for i in range(n):
		drawColumn(n,height)
		t.right(90)
		t.forward(height)
		t.left(90)

def whichRow(y):
	return math.floor(((-y)+boardSize*n/2)/boardSize)

def whichColumn(x):
	return math.floor(((x)+boardSize*n/2)/boardSize)

def xFromColumn(column):
	return (column*boardSize)-boardSize*n/2+50

def yFromRow(row):
	return (-1)*((row*boardSize)-boardSize*n/2)-50

def stampPlayer(row,column,player):
	t.penup()
	t.pencolor(player)
	t.fillcolor(player)
	t.goto(xFromColumn(column),yFromRow(row))
	t.shape('circle')
	t.shapesize(2.5,2.5,2.5)
	t.stamp()

def updateBoard(board,player,row,column):
	board[row][column]=player
	
def returnUpdatedBoard(board,player,move):
	board[move[0]][move[1]]=player
	return board
	#variation on updated board that returns the board

def drawPieces():
	for i in range(len(gameboard)):
		for j in range(len(gameboard[i])):
			if gameboard[i][j]!=0:
				stampPlayer(i,j,gameboard[i][j])
			

def calculateScore(board,player):
	score=0
	for i in range(len(board)):
		for j in range(len(board[i])):
			if player==board[i][j]:
				score+=1
	return score

def updateScore():
	t.penup()
	t.pencolor(player2)
	valW=calculateScore(gameboard,player2)
	t.goto((-200),410)
	t.write(f"{player2} = {valW}")
	t.penup()
	t.goto((200),410)
	valB=calculateScore(gameboard,player1)
	t.write(f"{player1} = {valB}")	

def redraw():
	t.reset()
	drawBoard(8)
	drawPieces()
	updateScore()
	#rewdraws the gameboard after the board has been changed

def initialize():
	global gameboard
	t.reset()
	gameboard=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
	updateBoard(gameboard,"black",3,4)
	updateBoard(gameboard,"black",4,3)
	updateBoard(gameboard,"white",3,3)
	updateBoard(gameboard,"white",4,4)
	redraw()


def oppositePlayer(player):
	if player == player1:
		return player2
	return player1

def validMove(board, player, row, column):
	if 0<=(row)<=7 and 0<=(column)<=7:
		if board[row][column]!=0:
			return False
		for i in [-1,0,1]:
			for j in [-1,0,1]:
				if 0<=(row+i)<=7 and 0<=(column+j)<=7:
					if board[row+i][column+j]==oppositePlayer(player):
						opponentSquareRow=row+i
						opponentSquareColumn=column+j
						while board[opponentSquareRow][opponentSquareColumn]==oppositePlayer(player) and 0<=(opponentSquareRow+i)<=7 and 0<=(opponentSquareColumn+j)<=7:
							opponentSquareRow+=i
							opponentSquareColumn+=j
							if board[opponentSquareRow][opponentSquareColumn] == player:
								return True
	return False

def allMoves(board, player):
	movelist=[]
	for i in range(len(board)):
		for j in range(len(board)):
			if validMove(board,player,i,j):
				movelist+=[[i,j]]
	return(movelist)



def boardFlip(board, player, row, column):
	for i in [-1,0,1]:
		for j in [-1,0,1]:
			if 0<=(row+i)<=7 and 0<=(column+j)<=7:
				if board[row+i][column+j]==oppositePlayer(player):
					opponentSquareRow=row+i
					opponentSquareColumn=column+j
					board[row][column]=player
					playerFound=False
					while board[opponentSquareRow][opponentSquareColumn]==oppositePlayer(player) and 0<=(opponentSquareRow+i)<=7 and 0<=(opponentSquareColumn+j)<=7:
						opponentSquareRow+=i
						opponentSquareColumn+=j
						if board[opponentSquareRow][opponentSquareColumn] == player:
							playerFound=True
					if playerFound==True:
						opponentSquareRow=row+i
						opponentSquareColumn=column+j
						while board[opponentSquareRow][opponentSquareColumn]==oppositePlayer(player) and 0<=(opponentSquareRow+i)<=7 and 0<=(opponentSquareColumn+j)<=7:
							updateBoard(board, player, opponentSquareRow, opponentSquareColumn)
							opponentSquareRow+=i
							opponentSquareColumn+=j
						
	#figures out which tiles to flip for a given move


def endGame():
	if calculateScore(gameboard,player1)+calculateScore(gameboard, player2)==64:
		if calculateScore(gameboard,player1)> calculateScore(gameboard,player2):
			t.penup()
			t.pencolor(player1)
			t.goto(0,410)
			t.write(f"{player1} wins")
			return
		if calculateScore(gameboard,player1)< calculateScore(gameboard,player2):
			t.penup()
			t.pencolor(player2)
			t.goto(0,410)
			t.write(f"{player2} wins")
		else:
			t.penup()
			t.pencolor("red")
			t.goto(0,410)
			t.write("draw")
		return True
#figures out if the game is over and updates the board accordingly

def nextBoard(board, player, move):
	if validMove(board, player, move[0],move[1]):	
		boardFlip(board, player, move[0], move[1])
	redraw()
	endGame()


def passTurn(board, player):
	if allMoves(board, player) == []:
		return True
	return False
#determines if there are no moves a player can make

def evaluate(board, player):
	return(calculateScore(board, player))


def miniMax(board, player, depth, A, B):
	if depth==0 or endGame():
		return([evaluate(board, player),[-1,-1]])
	if player==player2:
		bestVal= -math.inf
		bestMove= [-1,-1]
		for move in allMoves(board, player):
			value=miniMax(returnUpdatedBoard(copy.deepcopy(board),player2,move),player1,depth-1,A,B)[0]
			bestVal=max(bestVal, value)
			if bestVal==value:
				bestMove=move
			A=max(A, bestVal)
			if B <= A:
				break
		return([bestVal,bestMove])
	else:
		bestVal= math.inf
		bestMove= [-1,-1]
		for move in allMoves(board, player):
			value=miniMax(returnUpdatedBoard(copy.deepcopy(board),player1,move),player2,depth-1,A,B)[0]
			bestVal=min(bestVal, value)
			if bestVal==value:
				bestMove=move
			B=min(B, bestVal)
			if B <= A:
				break
		return([bestVal,bestMove])
			

def computerMove():
	if not(passTurn(gameboard, player2)):
		nextBoard(gameboard,player2, miniMax(gameboard,player2,8,-math.inf,math.inf)[1])
	#comnputer response
	#computer is always white

def handleClick(x,y):
	if validMove(gameboard, player1, whichRow(y),whichColumn(x)):
		nextBoard(gameboard, player1, [whichRow(y),whichColumn(x)])
		computerMove()
	if passTurn(gameboard,player1):
		computerMove()
	#handles click from player
	#player is always black
		


initialize()

s.onclick(handleClick)
turtle.mainloop()