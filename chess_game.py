try:
    import Tkinter as tk
    from Tkinter import *
except:
    import tkinter as tk
    from tkinter import *
from math import atan2
from copy import deepcopy
import pygame

pygame.init()

DIRECTIONS = [(1, 0), (1, 1), (0, 1), (-1, 1),  # straight lines
              (-1, 0), (-1, -1), (0, -1), (1, -1),
              (2, 1), (1, 2), (-1, 2), (-2, 1),  # knights
              (-2, -1), (-1, -2), (1, -2), (2, -1),
              ]
RAYS = [atan2(d[1], d[0]) for d in DIRECTIONS]
PIECES = {'k': lambda y, dx, dy: abs(dx) <= 1 and abs(dy) <= 1,
          'q': lambda y, dx, dy: dx == 0 or dy == 0 or abs(dx) == abs(dy),
          'n1': lambda y, dx, dy: (abs(dx) >= 1 and abs(dy) >= 1 and abs(dx) + abs(dy) == 3),
          'n2': lambda y, dx, dy: (abs(dx) >= 1 and abs(dy) >= 1 and abs(dx) + abs(dy) == 3),
          'b1': lambda y, dx, dy: abs(dx) == abs(dy),
          'b2': lambda y, dx, dy: abs(dx) == abs(dy),
          'r1': lambda y, dx, dy: dx == 0 or dy == 0,
          'r2': lambda y, dx, dy: dx == 0 or dy == 0,
          'p1': lambda y, dx, dy: (y < 8 and abs(dx) <= 1 and dy == -1),
          'p2': lambda y, dx, dy: (y < 8 and abs(dx) <= 1 and dy == -1),
          'p3': lambda y, dx, dy: (y < 8 and abs(dx) <= 1 and dy == -1),
          'p4': lambda y, dx, dy: (y < 8 and abs(dx) <= 1 and dy == -1),
          'p5': lambda y, dx, dy: (y < 8 and abs(dx) <= 1 and dy == -1),
          'p6': lambda y, dx, dy: (y < 8 and abs(dx) <= 1 and dy == -1),
          'p7': lambda y, dx, dy: (y < 8 and abs(dx) <= 1 and dy == -1),
          'p8': lambda y, dx, dy: (y < 8 and abs(dx) <= 1 and dy == -1),

          'P1': lambda y, dx, dy: (y > 1 and abs(dx) <= 1 and dy == 1),
          'P2': lambda y, dx, dy: (y > 1 and abs(dx) <= 1 and dy == 1),
          'P3': lambda y, dx, dy: (y > 1 and abs(dx) <= 1 and dy == 1),
          'P4': lambda y, dx, dy: (y > 1 and abs(dx) <= 1 and dy == 1),
          'P5': lambda y, dx, dy: (y > 1 and abs(dx) <= 1 and dy == 1),
          'P6': lambda y, dx, dy: (y > 1 and abs(dx) <= 1 and dy == 1),
          'P7': lambda y, dx, dy: (y > 1 and abs(dx) <= 1 and dy == 1),
          'P8': lambda y, dx, dy: (y > 1 and abs(dx) <= 1 and dy == 1),
          }

MOVES = dict()

for sym, is_legal in PIECES.items():
    MOVES[sym] = list()
    for idx in range(64):
        MOVES[sym].append([list() for _ in range(8)])
        for end in sorted(range(64), key=lambda x: abs(x - idx)):
            y = 8 - idx // 8
            dx = (end % 8) - (idx % 8)
            dy = (8 - end // 8) - y

            if idx == end or not is_legal(y, dx, dy):
                continue

            angle = atan2(dy, dx)
            if angle in RAYS:
                ray_num = RAYS.index(angle) % 8
                MOVES[sym][idx][ray_num].append(end)

        MOVES[sym][idx] = [r for r in MOVES[sym][idx] if r]
for sym in ['K', 'Q', 'N1','N2', 'B1', 'B2', 'R1', 'R2']:
    MOVES[sym] = deepcopy(MOVES[sym.lower()])
MOVES['k'][4][0].append(6)
MOVES['k'][4][1].append(2)
MOVES['K'][60][0].append(62)
MOVES['K'][60][4].append(58)
IDX = 0
for i in range(8):
    MOVES['p1'][8 + i][IDX].append(24 + i)
    MOVES['p2'][8 + i][IDX].append(24 + i)
    MOVES['p3'][8 + i][IDX].append(24 + i)
    MOVES['p4'][8 + i][IDX].append(24 + i)
    MOVES['p5'][8 + i][IDX].append(24 + i)
    MOVES['p6'][8 + i][IDX].append(24 + i)
    MOVES['p7'][8 + i][IDX].append(24 + i)
    MOVES['p8'][8 + i][IDX].append(24 + i)
    MOVES['P1'][55 - i][IDX].append(39 - i)
    MOVES['P2'][55 - i][IDX].append(39 - i)
    MOVES['P3'][55 - i][IDX].append(39 - i)
    MOVES['P4'][55 - i][IDX].append(39 - i)
    MOVES['P5'][55 - i][IDX].append(39 - i)
    MOVES['P6'][55 - i][IDX].append(39 - i)
    MOVES['P7'][55 - i][IDX].append(39 - i)
    MOVES['P8'][55 - i][IDX].append(39 - i)
    IDX = 1
state=list()
for i in range(64):
    state.append('null')
imagestack=dict()

class GameBoard(tk.Frame):
    def __init__(self, parent, rows=8, columns=8, size=85, color1="white", color2="black"):
        '''size is the size of a square, in pixels'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.pieces = {}
        self.selected_piece='P4'
        self.count=0
        self.selection_square1=0
        self.selection_square2=0
        self.selection_row=0
        self.selection_col=0
        self.move_number=1
        canvas_width = columns * size+20
        canvas_height = rows * size+20

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=5,
                                width=canvas_width, height=canvas_height, background="bisque",cursor="fleur")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)
        self.canvas.bind("<Button-1>", self.highlighter)

    def transmission(self):
        x1=self.selection_square1%8
        y1=self.selection_square1//8
        x2=self.selection_square2%8
        y2=self.selection_square2//8
        if (state[self.selection_square1] in {'n1','n2','N1','N2'}):
            if(state[self.selection_square2]!='null'):
                pygame.mixer.music.load("capture1.ogg")
                pygame.mixer.music.play()
                self.deletepiece()
            else:
                pygame.mixer.music.load("move1.ogg")
                pygame.mixer.music.play()
            return('success')
        else:
            diff=self.selection_square2-self.selection_square1
            if(x1==x2):
                if(y2>y1):
                    facter=8
                else:
                    facter=-8
            elif(y1==y2):
                if(x2>x1):
                    facter=1
                else:
                    facter=-1
            elif(diff%7==0):
                if(y2>y1):
                    facter=7
                else:
                    facter=-7
            else:
                if(x2>x1):
                    facter=9
                else:
                    facter=-9
            i=self.selection_square1+facter
            while(i!=self.selection_square2):
                if(state[i]!='null'):
                    return('failure')
                i=i+facter
            if(state[self.selection_square2]!='null'):
                for k in state[self.selection_square1]:
                    if((k=='p' or k=='P') and (facter==8 or facter==-8)):
                        return('failure')
                if state[self.selection_square2]=='k':
                    print "White Won The match!!"
                elif state[self.selection_square2]=='K':
                    print "Black Won The match!!"
                self.deletepiece()
                pygame.mixer.music.load("capture1.ogg")
                pygame.mixer.music.play()
            else:
                for k in state[self.selection_square1]:
                    if((k=='p' or k=='P') and (facter in {7,9,-7,-9})):
                        return('failure')
                pygame.mixer.music.load("move1.ogg")
                pygame.mixer.music.play()
            return('success')


    def move_legality(self):
        if(state[self.selection_square2]!='null'):
            for i in state[self.selection_square2]:
                if (i.islower() and self.selected_piece[0].islower()) or (i.isupper() and self.selected_piece[0].isupper()):
                    return('failure')
                else:
                    return(self.transmission())
        else:
            return(self.transmission())
            

    def move_validation(self):
        for i in MOVES[self.selected_piece][self.selection_square1]:
            for j in i:
                if(self.selection_square2==j):
                    if(self.move_legality()=='success'):
                        self.placepiece(self.selected_piece,self.selection_square2//8,self.selection_square2%8)
                        state[self.selection_square2]=self.selected_piece
                        state[self.selection_square1]='null'
                        self.move_number=self.move_number+1
                        return 'task_completed'
                    
        pygame.mixer.music.load("invalid.ogg")
        pygame.mixer.music.play()


    def highlighter(self, event):
        if(self.count%2==0):
            x0=event.x
            y0=event.y
            self.selection_col=int(x0/self.size)
            self.selection_row=int(y0/self.size)
            self.selection_square1=self.selection_row*8+self.selection_col
            for name in self.pieces:
                if(self.pieces[name][0]==self.selection_row and self.pieces[name][1]==self.selection_col):
                    if((name.islower() and self.move_number%2==0) or (name.isupper() and self.move_number%2==1)):
                        self.selected_piece=name
                        x1 = (self.selection_col * self.size)
                        y1 = (self.selection_row * self.size)
                        x2 = x1 + self.size
                        y2 = y1 + self.size
                        self.canvas.create_rectangle(x1+5, y1+5, x2+5, y2+5, fill="red", tags="square")
                        self.canvas.tag_lower("square")
                        self.count=self.count+1

        else:
            if((self.selection_row+self.selection_col)%2==0):
                color=self.color1
            else:
                color=self.color2
            x1 = (self.selection_col * self.size)
            y1 = (self.selection_row * self.size)
            x2 = x1 + self.size
            y2 = y1 + self.size
            self.canvas.create_rectangle(x1+5, y1+5, x2+5, y2+5, fill=color, tags="square")
            self.canvas.tag_lower("square")
            self.count=self.count+1
            self.selection_col=int(event.x/self.size)
            self.selection_row=int(event.y/self.size)
            self.selection_square2=self.selection_row*8+self.selection_col
            if (self.selection_square1!=self.selection_square2):
                self.move_validation()

    def deletepiece(self):
        del self.pieces[state[self.selection_square2]]
        self.canvas.delete(imagestack[state[self.selection_square2]][0])

    def addpiece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        IMAGE=self.canvas.create_image(10,10, image=image, tags=(name, "piece"), anchor="c")
        imagestack[name]=list()
        imagestack[name].append(IMAGE)
        self.placepiece(name, row, column)

    def placepiece(self, name, row, column):
        '''Place a piece at the given row/column'''
        state[(row*8)+column]=name
        self.pieces[name] = (row,column)
        x0 = (column * self.size) + int(self.size/2)+5
        y0 = (row * self.size) + int(self.size/2)+5
        self.canvas.coords(name, x0, y0)

    def refresh(self, event):
        '''Redraw the board, possibly in response to window being resized'''
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1+5, y1+5, x2+5, y2+5, outline="black",width=0, fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        for name in self.pieces:
            self.placepiece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

if __name__ == "__main__":
    root = Tk()
    # root.wm_iconbitmap(r'/home/harnish/Desktop/ChessPro0/chessicons_small/index.ico')
    root.wm_title('ChessPro0')
    labelframe = LabelFrame(root,text="Do Your Best to beat Jarvis!!",foreground="red",font="papyrus",relief="sunken")
    labelframe.pack(fill="both", expand="yes")
    left = Label(labelframe, text="Try Your Best to Defeat Jarvis!!")
    board = GameBoard(left)
    board.pack(side="top", fill="both", expand="true", padx=2, pady=2)
    left.pack()
    pygame.mixer.music.load("start1.ogg")
    pygame.mixer.music.play()
    #Initialisation of pieces...
    #for black pieces
    k = tk.PhotoImage(file="bk.png")
    b = tk.PhotoImage(file="bb.png")
    n = tk.PhotoImage(file="bn.png")
    q = tk.PhotoImage(file="bq.png")
    p = tk.PhotoImage(file="bp.png")
    r = tk.PhotoImage(file="br.png")
    #for white pieces
    K = tk.PhotoImage(file="wk.png")
    B = tk.PhotoImage(file="wb.png")
    N = tk.PhotoImage(file="wn.png")
    Q = tk.PhotoImage(file="wq.png")
    P = tk.PhotoImage(file="wp.png")
    R = tk.PhotoImage(file="wr.png")

    board.addpiece("r1", r, 0,0)
    board.addpiece("n1", n, 0,1)
    board.addpiece("b1", b, 0,2)
    board.addpiece("q", q, 0,3)
    board.addpiece("k", k, 0,4)
    board.addpiece("b2", b, 0,5)
    board.addpiece("n2", n, 0,6)
    board.addpiece("r2", r, 0,7)

    board.addpiece("R1", R, 7,0)
    board.addpiece("N1", N, 7,1)
    board.addpiece("B1", B, 7,2)
    board.addpiece("Q", Q, 7,3)
    board.addpiece("K", K, 7,4)
    board.addpiece("B2", B, 7,5)
    board.addpiece("N2", N, 7,6)
    board.addpiece("R2", R, 7,7)

    board.addpiece("p2", p, 1,1)
    board.addpiece("p3", p, 1,2)
    board.addpiece("p1", p, 1,0)
    board.addpiece("p4", p, 1,3)
    board.addpiece("p5", p, 1,4)
    board.addpiece("p6", p, 1,5)
    board.addpiece("p7", p, 1,6)
    board.addpiece("p8", p, 1,7)

    board.addpiece("P1", P, 6,0)
    board.addpiece("P2", P, 6,1)
    board.addpiece("P3", P, 6,2)
    board.addpiece("P4", P, 6,3)
    board.addpiece("P5", P, 6,4)
    board.addpiece("P6", P, 6,5)
    board.addpiece("P7", P, 6,6)
    board.addpiece("P8", P, 6,7)
    root.mainloop()
