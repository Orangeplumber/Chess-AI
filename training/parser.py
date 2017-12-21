import numpy as np
import piece_valid_moves
from datetime import datetime
startTime = datetime.now()
# function to understand the position
error_count=0
def position_converter(position):
	x=ord(position[0])-97
	y=56-ord(position[1])
	return((8*y)+x)

space_count=0
target_pos=0
num_index=1	
# Initialising the 12*64 vector
# pairing of 12 one dimensional vector--> (0,1,2,3,4,5,6,7,8,9,10,11)~(k,q,n,r,b,p,K,Q,N,R,B,P)
features=['k','q','n','r','b','p','K','Q','N','R','B','P']
def Initial_State():
	a=np.zeros((12,64),dtype=np.int)
	a[0][4]=1
	a[1][3]=1
	a[2][1]=1
	a[2][6]=1
	a[3][0]=1
	a[3][7]=1
	a[4][2]=1
	a[4][5]=1
	for i in range(8,16):
		a[5][i]=1

	a[6][60]=1
	a[7][59]=1
	a[8][62]=1
	a[8][57]=1
	a[9][63]=1
	a[9][56]=1
	a[10][58]=1
	a[10][61]=1
	for i in range(48,56):
		a[11][i]=1
	return(a)

def king_killing(state,i,target_pos,turn):
	State=state
	State[target_pos]=State[i]
	State[i]='null'
	if(turn==0):
		l=State.index('K')
		for j in range(64):
			if(State[j][0] in {'q','r','b'}):
				if(piece_valid_moves.valid_moves(State,j,l)=='success'):
					return 1
		return 0
	else:
		l=State.index('k')
		for j in range(64):
			if(State[j][0] in {'Q','R','B'}):
				if(piece_valid_moves.valid_moves(State,j,l)=='success'):
					return 1
		return 0

def matrix_manipulation(move):
	# global validity
	global error_count
	global game
	# print move
	global output_vector
	global input_vector
	global state
	global space_count
	global promoted_piece_count
	turn=space_count%3-1
	# turn=0(black turn) turn=1(white) 
	check=0
	kill=0
	targeting_piece="null"
	promoted_piece='none'
	killer_piece="P"
	active_file="none"
	active_rank="none"
	killer_pos=-1
	# move can be "e4","de4","Ne4","Nd5e4","N5e4s","Nde4","dxe4","Nxe4","Ndxe4","O-O","O-O-O" and x can be added to any of them.
	if(move[len(move)-1]=="+"):
		check=1
		move=move.translate(None, '+')
	elif(move[len(move)-1]=="#"):
		# checkmate, game over
		move=move.translate(None, '#')
	if(move=="O-O-O"):
		# chessling on left side
		if(turn==0):
			state[58]='K'
			state[60]='null'
			state[59]='R1'
			state[56]='null'
			input_vector[6][58]=1
			input_vector[6][60]=0
			input_vector[9][59]=1
			input_vector[9][56]=0
		else:
			state[2]='k'
			state[4]='null'
			state[3]='r1'
			state[0]='null'
			input_vector[0][2]=1
			input_vector[0][4]=0
			input_vector[3][3]=1
			input_vector[3][0]=0
	elif(move=="O-O"):
		# chessling on right side
		if(turn==0):
			state[62]='K'
			state[60]='null'
			state[61]='R2'
			state[63]='null'
			input_vector[6][62]=1
			input_vector[6][60]=0
			input_vector[9][61]=1
			input_vector[9][63]=0
		else:
			state[6]='k'
			state[4]='null'
			state[5]='r2'
			state[7]='null'
			input_vector[0][6]=1
			input_vector[0][4]=0
			input_vector[3][5]=1
			input_vector[3][7]=0
	else:
		for i in move:
			if(i in {'1','2','3','4','5','6','7','8'}):
				num_index=move.index(i)
			elif(i=="x"):
				kill=1
				move=move.translate(None,"x")
		pos_str=move[num_index-1]+move[num_index]
		target_pos=position_converter(pos_str)
		if(len(move)!=num_index+1):
			if(move[num_index+1]=="="):
				# pawn promotion
				promoted_piece=move[num_index+2]
				promoted_piece_count+=1
				move=move.translate(None,"=")
				move=move.translate(None,promoted_piece)
		if(num_index==2):
			# de4,Ne4
			if(move[0].islower()):
				active_file=move[0]
			else:
				killer_piece=move[0]
		elif(num_index==3):
			# Nde4, N5e4
			killer_piece=move[0]
			if(move[1] in {'1','2','3','4','5','6','7','8'}):
				active_rank=move[1]
			else:
				active_file=move[1]
		elif(num_index==4):
			# Nd5e4
			killer_piece=move[0]
			pos_str=move[1]+move[2]
			killer_pos=position_converter(pos_str)
		if(turn==0):
			if(active_file=='none' and active_rank=="none"):
				if(killer_piece=='P'):
					if(state[target_pos]!='null'):
						if(state[target_pos+7][0]=='P'):
							killer_pos=target_pos+7
						else:
							killer_pos=target_pos+9
					elif(state[target_pos]=='null' and kill==1):
						# en_passant
						if(state[target_pos+9][0]=='P'):
							killer_pos=target_pos+9
						else:
							killer_pos=target_pos+7
						input_vector[features.index('p')][target_pos+8]=0
						state[target_pos+8]='null'
						kill=0
					else:
						if(state[target_pos+8][0]=='P'):
							killer_pos=target_pos+8
						else:
							killer_pos=target_pos+16
				else:
					for i in range(64):
						if(state[i][0]==killer_piece and i!=target_pos):
							if(piece_valid_moves.valid_moves(state,i,target_pos)=='success'):
								killer_pos=i
								break


			elif(active_file!='none' and active_rank=='none'):
				column=ord(active_file)-97
				for i in range(8):
					if(state[column][0]==killer_piece):
						if(piece_valid_moves.valid_moves(state,column,target_pos)=='success'):
							killer_pos=column
							break
					column=column+8
				if(state[target_pos]=='null' and kill==1):
					# en_passant
					if((target_pos+9)%8==ord(active_file)-97):
						killer_pos=target_pos+9
					else:
						killer_pos=target_pos+7
					input_vector[features.index('p')][target_pos+8]=0
					state[target_pos+8]='null'
					kill=0
			elif(active_file=='none' and active_rank!='none'):
				row=(56-ord(active_rank))*8
				for i in range(8):
					if(state[row][0]==killer_piece):
						if(piece_valid_moves.valid_moves(state,row,target_pos)=='success'):
							killer_pos=row
							break
					row=row+1
		else:
			promoted_piece=promoted_piece.lower()
			killer_piece=killer_piece.lower()
			if(active_file=='none' and active_rank=="none"):
				if(killer_piece=='p'):
					if(state[target_pos]!='null'):
						if(state[target_pos-7][0]=='p'):
							killer_pos=target_pos-7
						else:
							killer_pos=target_pos-9
					elif(state[target_pos]=='null' and kill==1):
						# en_passant
						if(state[target_pos-9][0]=='p'):
							killer_pos=target_pos-9
						else:
							killer_pos=target_pos-7
						input_vector[features.index(state[target_pos-8][0])][target_pos-8]=0
						state[target_pos-8]='null'
						kill=0
					else:
						if(state[target_pos-8][0]=='p'):
							killer_pos=target_pos-8
						else:
							killer_pos=target_pos-16
				else:
					for i in range(64):
						if(state[i][0]==killer_piece and i!=target_pos and state[i]!='null'):
							if(piece_valid_moves.valid_moves(state,i,target_pos)=='success'):
								killer_pos=i
								break

			elif(active_file!='none' and active_rank=='none'):
				column=ord(active_file)-97
				for i in range(8):
					if(state[column][0]==killer_piece and state[column]!='null'):
						if(piece_valid_moves.valid_moves(state,column,target_pos)=='success'):
							killer_pos=column
							break
					column=column+8
				if(state[target_pos]=='null' and kill==1):
					# en_passant
					if((target_pos-9)%8==ord(active_file)-97):
						killer_pos=target_pos-9
					else:
						killer_pos=target_pos-7
					input_vector[features.index('P')][target_pos-8]=0
					state[target_pos-8]='null'
					kill=0
			elif(active_file=='none' and active_rank!='none'):
				row=(56-ord(active_rank))*8
				for i in range(8):
					if(state[row][0]==killer_piece and state[row]!='null'):
						if(piece_valid_moves.valid_moves(state,row,target_pos)=='success'):
							killer_pos=row
							break
					row=row+1

		
		input_vector[features.index(killer_piece)][killer_pos]=0
		if(kill==1):
			input_vector[features.index(state[target_pos][0])][target_pos]=0
		input_vector[features.index(killer_piece)][target_pos]=1
		state[target_pos]=state[killer_pos]
		state[killer_pos]='null'
		if(promoted_piece!='none'):
			state[target_pos]=promoted_piece+chr(96+promoted_piece_count)
			input_vector[features.index(killer_piece)][target_pos]=0
			input_vector[features.index(promoted_piece)][target_pos]=1
		# print state
		# print killer_pos
		# print '~'
		# if(game==766):
			# print state
		# try:
			# king_pos=state.index('k')
			# king_pos=state.index('K')
		# except:
			# validity=0

		
	# print input_vector



		



move_no=0
total_move=0
f = open("good_new.txt","r")
lines = f.readlines()
f.close()
game=0
with open("input_vector1.csv","w") as a, open("output_vector1.csv","w") as b:
	for line in lines:
		total_move+=move_no
		game+=1
		if(game==1002):
			break
		print game
		if(game not in {766,2227,3031,3056,4352,5006,5737,7835,10411,11383,11437,13190,14745,15130,16213,18593,21087,26964,27165,28125,28563,29905,30332,32980,33737,34463,34844,40566,40995,42497,43505,46945,48195,48899}):
			# en_passant validation left
			output_vector=np.zeros((1,3),dtype=np.int)
			end_index=line.index("}")
			if(line[end_index+2]=='1'):
				if(line[end_index+3]=='/'):
					# draw
					output_vector[0][1]=1
				else:
					# white wins
					output_vector[0][0]=1
			else:
				# black wins
				output_vector[0][2]=1
			# print output_vector
			# print game
			move_no=0
			space_count=0
			# validity=1
			promoted_piece_count=0
			j=-1
			# Intialise the input vector as the initial chess state.
			state=['r1', 'n1', 'b1', 'q', 'k', 'b2', 'n2', 'r2', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'R1', 'N1', 'B1', 'Q', 'K', 'B2', 'N2', 'R2']
			input_vector=Initial_State()

			for i in line:
				j=j+1
				if(i=='{'):
					break
				elif(i=='.'):
					move_no=move_no+1
				elif(i==' '):
					space_count=space_count+1
					if(space_count%3!=0):
						k=j+1
						move=""
						if(line[k]!='{'):
							while(line[k]!=' '):
								move=move+line[k]
								k=k+1
							# print game
							# print move
							matrix_manipulation(move)
	    					b.write(" ".join("".join(map(str,output_vector.flatten()))))
	    					b.write("\n")
	    					a.write(" ".join("".join(map(str,input_vector.flatten()))))
	    					a.write("\n")
							# function call for training
	a.close()
	b.close()
print "end"
print datetime.now() - startTime
