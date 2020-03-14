import random
from tkinter import *

class board:
    ALLATOMS=8
    SIZE=14
    atomslist=[]
    
    def __init__(self):
        self.board=[[0 for i in range(self.SIZE)] for j in range(self.SIZE)]
        self.board1=[[0 for i in range(self.SIZE)] for j in range(self.SIZE)]
        atoms=0
        while atoms!=self.ALLATOMS:
            x=random.randint(2,self.SIZE-3)
            y=random.randint(2,self.SIZE-3)
            if self.board[y][x]==0:
                self.atomslist.append([x,y])
                self.board[y][x]=1
                self.board[y-1][x-1]=2
                self.board[y-1][x+1]=2
                self.board[y+1][x+1]=2
                self.board[y+1][x-1]=2
                self.board[y-1][x]=2
                self.board[y][x+1]=2
                self.board[y+1][x]=2
                self.board[y][x-1]=2
                atoms+=1
                
    def get_cell(self,coord):
        return self.board[coord[1]][coord[0]]
    
    def found_neighbors(self,x,y):
        neighbors=[]
        if self.board[y-1][x+1]==1:
            neighbors.append([x+1,y-1])
        if self.board[y+1][x+1]==1:
            neighbors.append([x+1,y+1])
        if self.board[y+1][x-1]==1:
            neighbors.append([x-1,y+1])
        if self.board[y-1][x-1]==1:
            neighbors.append([x-1,y-1])
        
        return neighbors

    def found_neighbors1(self,x,y):
        neighbors=[]
        if self.board[y-1][x]==1:
            neighbors.append([x,y-1])
        if self.board[y][x+1]==1:
            neighbors.append([x+1,y])
        if self.board[y+1][x]==1:
            neighbors.append([x,y+1])
        if self.board[y][x-1]==1:
            neighbors.append([x-1,y])

        return neighbors
    
    def stop_cell(self,neighbors):
        for n in neighbors:
            x=n[0]
            y=n[1]
            self.board1[y-1][x]=2
            self.board1[y][x+1]=2
            self.board1[y+1][x]=2
            self.board1[y][x-1]=2
    
    def board1_clean(self):
        self.board1=[[0 for i in range(self.SIZE)] for j in range(self.SIZE)]

    def draw(self,gr):
        for y in range(1,self.SIZE-1):
            for x in range(1,self.SIZE-1):
                if self.board[y][x]==1:
                    obj=gr.can.find_closest(x*20,y*20)
                    gr.can.itemconfig(obj, fill='magenta')
                else:
                    obj=gr.can.find_closest(x*20,y*20)
                    gr.can.itemconfig(obj, fill='SkyBlue3')

    def move_atom(self):
        atom=random.choice(self.atomslist)
        directions=[[-1,0],[0,1],[1,0],[0,-1]] #[x,y]
        a=True
        while a==True:
            direction=random.choice(directions)
            new_position=[atom[0]+direction[0],atom[1]+direction[1]]
            neighbors=self.found_neighbors1(new_position[0],new_position[1])
            if len(neighbors)==1 and 1<new_position[0]<self.SIZE-3 and 1<new_position[1]<self.SIZE-3:
                self.board[new_position[1]][new_position[0]]=1
                self.board[atom[1]][atom[0]]=0
                self.atomslist.remove(atom)
                self.atomslist.append(new_position)
                a=False

class ray:
    def __init__(self,x,y,size):
        self.x=x
        self.y=y
        self.ox=0
        self.oy=0
        self.dx=0
        self.dy=0
        self.status=0
        self.length=1
        
        if y==0:
            self.dy=1
        elif y==size-1:
            self.dy=-1
            
        if x==0:
            self.dx=1
        elif x==size-1:
            self.dx=-1
    
    def new_move(self):
        self.nx=self.x+self.dx
        self.ny=self.y+self.dy
        return [self.nx,self.ny] 
    
    def move(self):
        self.ox=self.x
        self.oy=self.y 
        self.x+=self.dx
        self.y+=self.dy 
        self.length+=1

class graph:
    def __init__(self):
        self.root=Tk()
        self.can=Canvas(self.root, width=game_board.SIZE*20, height=game_board.SIZE*20, bg='white')
        self.can.pack(side=LEFT)

    def start(self):
        t1=self.T1.get(1.0, END)
    
    def render(self,gameboard):
        cells=[]
        for y in range(gameboard.SIZE):
            for x in range(gameboard.SIZE):
                if x==0 or x==gameboard.SIZE-1 or y==0 or y==gameboard.SIZE-1:
                    color='Gainsboro'
                else:
                    color='SkyBlue3'   
                rect=self.can.create_rectangle(x*20,y*20,x*20+20,y*20+20, fill=color)
                self.can.tag_bind(rect, '<Button-1>',clickLB)
                self.can.tag_bind(rect, '<Button-3>',clickRB)

def clickRB(event):
    x=event.x
    y=event.y
    xx=event.x/20
    yy=event.y/20
    obj=event.widget.find_closest(x,y)
    options=gr.can.itemconfig(obj)
    fillcolor=options['fill'][4]
    
    if fillcolor=='SkyBlue3':
        gr.can.itemconfig(obj, fill='magenta3')
    elif fillcolor=='magenta3':
        gr.can.itemconfig(obj, fill='SkyBlue3')

def clickLB(event):
    global turn, turn1, turnlist, atoms, foundatoms, game, openatoms
    x=event.x
    y=event.y
    xx=int(event.x/20)
    yy=int(event.y/20)
    obj=event.widget.find_closest(x,y)
    options=gr.can.itemconfig(obj)
    fillcolor=options['fill'][4]

    
    if xx>0 and xx<game_board.SIZE-1 and yy>0 and yy<game_board.SIZE-1 and atoms<game_board.ALLATOMS and game==True:
            
        if game_board.board[yy][xx]==1 and fillcolor=='SkyBlue3' and foundatoms<game_board.ALLATOMS:
            atoms+=1
            foundatoms+=1
            game_board.atomslist.remove([xx,yy])
            gr.can.itemconfig(obj, fill='green')
        elif game_board.board[yy][xx]==1 and fillcolor=='green':
            atoms-=1
            foundatoms-=1
            game_board.atomslist.append([xx,yy])
            gr.can.itemconfig(obj, fill='SkyBlue3')
        elif game_board.board[yy][xx]!=1 and fillcolor=='SkyBlue3' and foundatoms<game_board.ALLATOMS:
            foundatoms+=1
            gr.can.itemconfig(obj, fill='green')
        elif game_board.board[yy][xx]!=1 and fillcolor=='green':
            foundatoms-=1
            gr.can.itemconfig(obj, fill='SkyBlue3')

        gr.root.title('Отмечено {} из {}'.format(foundatoms, game_board.ALLATOMS))
        if atoms==game_board.ALLATOMS:
            gr.root.title('Вы выиграли!')
            game=False
            
    elif (xx>0 and xx<game_board.SIZE-1 and yy==0) or \
          (xx>0 and xx<game_board.SIZE-1 and yy==game_board.SIZE-1) or \
          (yy>0 and yy<game_board.SIZE-1 and xx==0) or \
          (yy>0 and yy<game_board.SIZE-1 and xx==game_board.SIZE-1):
          if game==True:
                launchray(xx, yy)
                t=gr.can.create_text(xx*20+10, yy*20+10, text=str(turn))
                turnlist.append(t)
                if turn1==6:
                    turn1=0
                    turn-=1
                    game_board.move_atom()
                    for i in turnlist:
                        gr.can.delete(i)
                        
                turn+=1
                turn1+=1
                
    else:
        openatoms+=1
        if openatoms==3:
            game=False
            printatoms(game_board)

def printatoms(gameboard):
        for y in range(1,gameboard.SIZE-2):
            for x in range(1,gameboard.SIZE-2):
                if gameboard.board[y][x]==1:
                    color='gold'
                    rect=gr.can.create_rectangle(x*20,y*20,x*20+20,y*20+20, fill=color)

def launchray(x,y):
    global turnlist
    my_ray=ray(x,y,game_board.SIZE)
    ray_status=True
        
    while ray_status==True:    
        if game_board.get_cell(my_ray.new_move())==1:
            text='Absorbtion.'
            ray_status=False
        else:
            my_ray.move()
            if my_ray.x>0 and my_ray.x<game_board.SIZE-1 and my_ray.y>0 and my_ray.y<game_board.SIZE-1:
                neighbors=game_board.found_neighbors(my_ray.x, my_ray.y)
                if neighbors!=[]:
                    game_board.stop_cell(neighbors)
                    if game_board.board1[my_ray.y-1][my_ray.x]==0 and my_ray.ox!=my_ray.x and my_ray.oy!=my_ray.y-1:
                        nx=my_ray.x
                        ny=my_ray.y-1
                    elif game_board.board1[my_ray.y][my_ray.x+1]==0 and my_ray.ox!=my_ray.x+1 and my_ray.oy!=my_ray.y:
                        nx=my_ray.x+1
                        ny=my_ray.y
                    elif game_board.board1[my_ray.y+1][my_ray.x]==0 and my_ray.ox!=my_ray.x and my_ray.oy!=my_ray.y+1:
                        nx=my_ray.x
                        ny=my_ray.y+1
                    elif game_board.board1[my_ray.y][my_ray.x-1]==0 and my_ray.ox!=my_ray.x-1 and my_ray.oy!=my_ray.y:
                        nx=my_ray.x-1
                        ny=my_ray.y
                    else:
                        nx=my_ray.x-my_ray.dx
                        ny=my_ray.y-my_ray.dy
                    
                    my_ray.dx=nx-my_ray.x
                    my_ray.dy=ny-my_ray.y
                    
                    game_board.board1_clean()    
                             
        if my_ray.length>2 and (my_ray.x==0 or my_ray.x==game_board.SIZE-1 or my_ray.y==0 or my_ray.y==game_board.SIZE-1):
            text='End ray.'
            ray_status=False
            t=gr.can.create_text(my_ray.x*20+10, my_ray.y*20+10, text=str(turn))
            turnlist.append(t)

turn=1
turn1=1
turnlist=[]
atoms=0
foundatoms=0
openatoms=0
game=True
game_board=board()
x,y=1,1
gr=graph()
gr.render(game_board)
gr.root.mainloop()