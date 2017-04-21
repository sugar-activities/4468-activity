# g.py - globals
import pygame,utils,random

app='Soma'; ver='1'
ver='21'
ver='22'
# better search strategy & thinking smiley
ver='23'
# flush queue after clicks
ver='24'
# add arrow to 4 & 5
ver='25'
# tick on completed level changes level

UP=(264,273)
DOWN=(258,274)
LEFT=(260,276)
RIGHT=(262,275)
CROSS=(259,120)
CIRCLE=(265,111)
SQUARE=(263,32)
TICK=(257,13)
NUMBERS={pygame.K_1:1,pygame.K_2:2,pygame.K_3:3,pygame.K_4:4,\
           pygame.K_5:5,pygame.K_6:6,pygame.K_7:7,pygame.K_8:8,\
           pygame.K_9:9,pygame.K_0:0}

def init(): # called by run()
    random.seed()
    global redraw
    global screen,w,h,font1,font2,clock
    global factor,offset,imgf,message,version_display
    global pos,pointer
    redraw=True
    version_display=False
    screen = pygame.display.get_surface()
    pygame.display.set_caption(app)
    screen.fill((0,0,120))
    pygame.display.flip()
    w,h=screen.get_size()
    if float(w)/float(h)>1.5: #widescreen
        offset=(w-4*h/3)/2 # we assume 4:3 - centre on widescreen
    else:
        h=int(.75*w) # allow for toolbar - works to 4:3
        offset=0
    factor=float(h)/24 # measurement scaling factor (32x24 = design units)
    imgf=float(h)/900 # image scaling factor - all images built for 1200x900
    clock=pygame.time.Clock()
    if pygame.font:
        t=int(40*imgf); font1=pygame.font.Font(None,t)
        t=int(80*imgf); font2=pygame.font.Font(None,t)
    message=''
    pos=pygame.mouse.get_pos()
    pointer=utils.load_image('pointer.png',True)
    pygame.mouse.set_visible(False)
    
    # this activity only
    global n_c4,n_c5,n_d
    global n,found4,found5,smiley,no,wrong,thinking_img,thinking
    global to4,to5
    n=4
    found4='0'*8; found5='0'*29
    level=1
    n_c4=sx(16),sy(17); n_d=sy(3) # centre for 4/5 display
    n_c5=sx(15.4),sy(19.7)        # and size of square for click
    smiley=utils.load_image('smiley.png',True)
    thinking_img=utils.load_image('thinking.png',True); thinking=False
    no=utils.load_image('no.png',True); wrong=False
    to4=utils.load_image('to4.png',True)
    to5=utils.load_image('to5.png',True)
    
def sx(f): # scale x function
    return int(f*factor+offset+.5)

def sy(f): # scale y function
    return int(f*factor+.5)
