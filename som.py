# som.py
import pygame,g,utils,grid_surface,copy,os

COLOURS=[(255,151,151),(255,238,95),(0,236,33),(161,183,255),(252,161,255)]

class Square:
    def __init__(self,r,c,x,y,ind):
        self.r=r; self.c=c; self.x=x; self.y=y; self.ind=ind
        self.colrs=[]

class Som:
    def __init__(self,n): # n= 4 or 5 = no of blocks
        t=120 # plan grid
        side=g.sy(8); colr=(t,t,t); x0=g.sx(1.5); y0=g.sy(13.3)
        self.squares=[]
        y=y0; d=side/5; ind=0
        for r in range(5):
            x=x0
            for c in range(5):
                sq=Square(r,c,x,y,ind); self.squares.append(sq)
                x+=d; ind+=1
            y+=d
        self.copy1=copy.deepcopy(self.squares) # result area
        self.copy2=copy.deepcopy(self.squares) # temp area
        self.outline=grid_surface.grid(5,5,side,colr)
        self.x0=x0; self.y0=y0; self.d=d; self.n=n;
        self.blocks=[]
        for ind in range(n):
            img=utils.load_image(str(ind+1)+'.png',True)
            self.blocks.append(img)
        self.soln_img=utils.load_image('soln'+str(n)+'.png',True)
        if n==4:
            self.soln_xy=g.sx(12.9),g.sy(1.4); self.cols=3; self.rows=3
            self.count=8; self.found='0'*self.count
        if n==5:
            self.soln_xy=g.sx(13.8),g.sy(.9); self.cols=5; self.rows=6
            self.count=29; self.found='0'*self.count
        self.soln_d=self.soln_img.get_width()/self.cols
        self.x03d=g.sx(3.84); self.y03d=g.sy(7); self.d3d=g.sy(1.6)
        fname=os.path.join('data','soln'+str(self.n)+'.txt')
        f=open(fname, 'r')
        self.solns=[]
        for line in f.readlines():
            line=line.rstrip(); self.solns.append(line)
        f.close
        self.green=self.squares[0]; self.set_green(0)

    def clear_found(self):
        self.found='0'*self.count
        if self.n==4: g.found4=self.found
        else: g.found5=self.found
        
    def setup(self):
        for sq in self.squares: sq.colrs=[]
        self.colours=range(self.n-1,-1,-1) # drawing colours
        self.red_ind=None; self.yellow_ind=None; g.wrong=False

    def draw(self):
        # draw plan
        g.screen.blit(self.outline,(self.x0,self.y0))
        for sq in self.squares:
            ln=len(sq.colrs)
            if ln>0:
                colr=sq.colrs.pop(); sq.colrs.append(colr)
                if colr!=None:
                    rect=(sq.x,sq.y,self.d,self.d)
                    pygame.draw.rect(g.screen,COLOURS[colr],rect)
        if self.green!=None:
            sq=self.green
            rect=(sq.x,sq.y,self.d,self.d)
            pygame.draw.rect(g.screen,(0,128,0),rect,g.sy(.15))
        # 3D display
        x0=self.x03d; y0=self.y03d; d=self.d3d; d2=d/2
        for r in range(5):
            y=y0
            for h in range(5):
                x=x0
                for c in range(5):
                    sq=self.sqr(self.squares,r,c)
                    if len(sq.colrs)>h:
                        colr=sq.colrs[h]
                        if colr!=None:
                            g.screen.blit(self.blocks[colr],(x,y))
                    x+=d
                y-=d
            x0-=d2; y0+=d2
        # result grid
        g.screen.blit(self.soln_img,self.soln_xy)
        x0,y=self.soln_xy; ind=0; d=self.soln_d-6
        for r in range(self.rows):
            x=x0
            for c in range(self.cols):
                if r==(self.rows-1) and c==0:
                    pass
                else:
                    if self.found[ind]=='0':
                        rect=(x+3,y+3,d,d)
                        pygame.draw.rect(g.screen,utils.BLACK,rect)
                    if ind==self.red_ind:
                        red_rect=(x,y,self.soln_d,self.soln_d)
                    if ind==self.yellow_ind:
                        yellow_rect=(x,y,self.soln_d,self.soln_d)
                    ind+=1
                x+=self.soln_d
            y+=self.soln_d
        # red rect
        if self.red_ind!=None:
            pygame.draw.rect(g.screen,utils.RED,red_rect,g.sy(.2))
        # yellow rect
        if self.yellow_ind!=None:
            pygame.draw.rect(g.screen,utils.YELLOW,yellow_rect,g.sy(.2))
        # 4/5/smiley
        img=None
        if self.complete(): img=g.smiley
        if g.wrong: img=g.no
        if g.thinking: img=g.thinking_img
        if self.n==4:
            if img!=None:
                utils.centre_blit(g.screen,img,g.n_c4)
            else:
                utils.centre_blit(g.screen,g.to5,g.n_c4)
        else:
            if img!=None:
                utils.centre_blit(g.screen,img,g.n_c5)
            else:
                utils.centre_blit(g.screen,g.to4,g.n_c5)
                    
    def click(self):
        self.red_ind=None; self.yellow_ind=None; g.wrong=False
        for sq in self.squares:
            if utils.mouse_in(sq.x,sq.y,sq.x+self.d,sq.y+self.d):
                if len(self.colours)>0:
                    colr=self.colours.pop()
                    sq.colrs.append(colr)
                else:
                    if len(sq.colrs)<5:
                        sq.colrs=[None]+sq.colrs
                return True
        return False
                
    def right_click(self):
        self.red_ind=None; self.yellow_ind=None; g.wrong=False
        for sq in self.squares:
            if utils.mouse_in(sq.x,sq.y,sq.x+self.d,sq.y+self.d):
                if len(sq.colrs)>0:
                    colr=sq.colrs.pop(); self.colours.append(colr)
                    if len(sq.colrs)>0:
                        t=sq.colrs.pop()
                        if t==None: sq.colrs=[]
                        else: sq.colrs.append(t)
                return True
        return False

    def check(self):
        self.red_ind=None; self.yellow_ind=None; g.wrong=False
        if self.colours!=[]: g.wrong=True; return # not enough blocks
        if not self.joined(self.squares): g.wrong=True; return # not joined
        # have candidate - find it & check if already found
        self.copy1=copy.deepcopy(self.squares)
        self.move(self.copy1)
        if self.look_for(self.copy1): return
        self.extended_look_for() # applies all possible transformations
        return
        
    def extended_look_for(self):
        # starts with legal copy1 already moved
        for i in range(4): # rotate about h
            self.rotate(); self.move(self.copy1)
            if self.look_for(self.copy1): return
            for j in range(4): # rotate about r
                self.rotate_r(); self.move(self.copy1)
                if self.look_for(self.copy1): return
                for k in range(4): # rotate about c
                    self.rotate_c(); self.move(self.copy1)
                    if self.look_for(self.copy1): return
        
    # if this legal layout is in the solutions list
    #   set self.soln_ind and ...
    #   check if it's already found ...
    #     if it has been, set self.red_ind
    #     else add it
    def look_for(self,sqs):
        self.soln_ind=None; self.red_ind=None
        s0=self.encode(sqs)
        ind=0
        for s in self.solns:
            if s==s0: self.soln_ind=ind; break
            ind+=1
        found=False
        if self.soln_ind!=None:
            if self.found[self.soln_ind]=='1':
                self.red_ind=self.soln_ind; found=True
            else:
                self.add()
        return found

    def add(self): # adds self.soln_ind to player's found
        self.found=utils.ch_set(self.found,self.soln_ind,'1')
        self.yellow_ind=self.soln_ind
        if self.n==4: g.found4=self.found
        else: g.found5=self.found

    def move(self,sqs): # move to origin
        minr=6; minc=6; minh=6
        for r in range(5):
            for c in range(5):
                for h in range(5):
                    if self.color(sqs,r,c,h)!=None:
                        if r<minr: minr=r
                        if c<minc: minc=c
                        if h<minh: minh=h
        if minr>0:
            for sq in sqs:
                r=sq.r+minr; c=sq.c
                if r>4: colrs=[]
                else: colrs=self.sqr(sqs,r,c).colrs
                sq.colrs=colrs
        if minc>0:
            for sq in sqs:
                r=sq.r; c=sq.c+minc
                if c>4: colrs=[]
                else: colrs=self.sqr(sqs,r,c).colrs
                sq.colrs=colrs
        if minh>0:
            for sq in sqs:
                if sq.colrs!=[]: sq.colrs=sq.colrs[minh:]
            
    def rotate(self): # rotates self.copy1
        for r in range(5):
            for c in range(5):
                ind=r*5+c; sq=self.copy1[ind]
                for h in range(5):
                    v=None
                    if h<len(sq.colrs): v=sq.colrs[h]
                    self.put(self.copy2,c,4-r,h,v)
        self.collapse(self.copy2)
        self.copy1=copy.deepcopy(self.copy2)
        
    def rotate_r(self): # rotates self.copy1
        for r in range(5):
            for c in range(5):
                ind=r*5+c; sq=self.copy1[ind]
                for h in range(5):
                    v=None
                    if h<len(sq.colrs): v=sq.colrs[h]
                    self.put(self.copy2,r,4-h,c,v)
        self.collapse(self.copy2)
        self.copy1=copy.deepcopy(self.copy2)
        
    def rotate_c(self): # rotates self.copy1
        for r in range(5):
            for c in range(5):
                ind=r*5+c; sq=self.copy1[ind]
                for h in range(5):
                    v=None
                    if h<len(sq.colrs): v=sq.colrs[h]
                    self.put(self.copy2,4-h,c,r,v)
        self.collapse(self.copy2)
        self.copy1=copy.deepcopy(self.copy2)
        
    def collapse(self,sqs):
        for sq in sqs:
            for ind in range(len(sq.colrs)):
                t=sq.colrs.pop()
                if t!=None: sq.colrs.append(t); break

    def sqr(self,sqs,r,c):
        ind=r*5+c
        return sqs[ind]
        
    def color(self,sqs,r,c,h):
        ind=r*5+c; sq=sqs[ind]
        if h<len(sq.colrs): return sq.colrs[h]
        return None

    def put(self,sqs,r,c,h,v):
        ind=r*5+c
        sq=sqs[ind]; ln=len(sq.colrs); sq.colrs+=[None]*(h-ln+1)
        sq.colrs[h]=v
        
    def mark(self,r,c,h):
        if self.color(self.squares,r,c,h)!=None:
            if self.color(self.copy2,r,c,h)==0:
                ind=r*5+c; self.copy2[ind].colrs[h]=1 # mark it as checked
                if r<4:
                    self.mark(r+1,c,h)
                if r>0:
                    self.mark(r-1,c,h)
                if c<4:
                    self.mark(r,c+1,h)
                if c>0:
                    self.mark(r,c-1,h)
                if h<4:
                    self.mark(r,c,h+1)
                if h>0:
                    self.mark(r,c,h-1)
            
    def joined(self,sqs):
        for r in range(5):
            for c in range(5):
                ind=r*5+c; self.copy2[ind].colrs=[0]*5 # clear 'marks'
                for h in range(5):
                    if self.color(self.squares,r,c,h)!=None:
                        r0=r; c0=c; h0=h # save a starting point
        # start @ (r0,c0,h0) & mark neigbours
        self.mark(r0,c0,h0)
        # should be 4/5 marked
        k=0
        for r in range(5):
            for c in range(5):
                for h in range(5):
                    if self.color(self.copy2,r,c,h)==1: k+=1
        if k==self.n: return True
        return False
                    
    def encode(self,sqs):
        s=''
        for sq in sqs:
            ind=0
            for colr in sq.colrs:
                if colr!=None: s+=str(sq.r)+str(sq.c)+str(ind)
                ind+=1
        return s

    def complete(self):
        if '0' in self.found: return False
        return True
        
    def right(self):
        ind=self.green.ind+1
        if self.green.c==4: ind-=5
        self.set_green(ind)
        
    def left(self):
        ind=self.green.ind-1
        if self.green.c==0: ind+=5
        self.set_green(ind)
        
    def down(self):
        ind=self.green.ind+5
        if self.green.r==4: ind-=len(self.squares)
        self.set_green(ind)
        
    def up(self):
        ind=self.green.ind-5
        if self.green.r==0: ind+=len(self.squares)
        self.set_green(ind)

    def set_green(self,ind):
        self.green=self.squares[ind]
        d=self.d-g.sy(.5); x=self.green.x+d; y=self.green.y+d
        pygame.mouse.set_pos((x,y)); g.pos=(x,y)
                
                

                
                
        


