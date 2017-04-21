# grid_surface.py
import pygame

def grid(nr,nc,side,colr,px=1): # px=line width
    s=pygame.Surface((side,side))
    dx=0.0+side/nc; dy=0.0+side/nr
    s.fill((0,0,0))#; s.set_colorkey((0,0,0))
    x1=0; x2=x1+side; y=0
    for r in range(nr+1):
        pygame.draw.line(s,colr,(x1,y),(x2,y),px)
        y+=dy
    x=0; y1=0; y2=y1+side
    for c in range(nc+1):
        pygame.draw.line(s,colr,(x,y1),(x,y2),px)
        x+=dx
    return s
    
    
    
