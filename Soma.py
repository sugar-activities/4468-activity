#!/usr/bin/python
# Soma.py
"""
    Copyright (C) 2011  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import g,pygame,utils,sys,buttons,load_save,som
try:
    import gtk
except:
    pass

class Soma:

    def __init__(self):
        self.journal=True # set to False if we come in via main()
        self.canvas=None # set to the pygame canvas if we come in via activity.py

    def display(self):
        g.screen.fill((0,0,120))
        self.som.draw()
        if self.som.complete():
            buttons.off(['cream','yellow']); buttons.on('black')
        else:
            buttons.on(['cream','yellow']); buttons.off('black')
        buttons.draw()

    def do_click(self):
        if self.som.click(): self.flush_queue(); return True
        d=g.n_d; d2=d/2
        if g.n==4: x,y=g.n_c4
        else: x,y=g.n_c5
        if utils.mouse_in(x-d2,y-d2,x+d2,y+d2):
            if g.n==4: self.som=self.som5; g.n=5
            else: self.som=self.som4; g.n=4
            return True
        return False

    def do_button(self,bu):
        if bu=='cream': self.som.setup()
        elif bu=='yellow':
            g.thinking=True; self.display(); pygame.display.flip() 
            self.som.check(); g.thinking=False; self.flush_queue()
        elif bu=='black': self.som.clear_found()

    def do_key(self,key):
        if key==pygame.K_v: g.version_display=not g.version_display
        elif key in g.TICK:
            if self.som.complete():
                if g.n==4: self.som=self.som5; g.n=5
                else: self.som=self.som4; g.n=4
            else:    
                self.do_button('yellow')
        elif key in g.SQUARE: self.do_button('cream')
        elif key==pygame.K_4: self.som=self.som4; g.n=4
        elif key==pygame.K_5: self.som=self.som5; g.n=5
        elif key in g.RIGHT: self.som.right()
        elif key in g.LEFT: self.som.left()
        elif key in g.UP: self.som.up()
        elif key in g.DOWN: self.som.down()
        elif key in g.CROSS: self.do_click()
        elif key in g.CIRCLE: self.som.right_click(); self.flush_queue()

    def buttons_setup(self):
        cx=g.sx(11.6)
        buttons.Button('yellow',(cx,g.sy(15.4)))
        buttons.Button('cream',(cx,g.sy(18.5)))
        buttons.Button('black',(cx,g.sy((15.4+18.5)/2))); buttons.off('black')

    def flush_queue(self):
        flushing=True
        while flushing:
            flushing=False
            if self.journal:
                while gtk.events_pending(): gtk.main_iteration()
            for event in pygame.event.get(): flushing=True

    def run(self):
        g.init()
        if not self.journal: utils.load()
        load_save.retrieve()
        self.som4=som.Som(4)
        self.som5=som.Som(5)
        self.som4.setup(); self.som5.setup()
        if g.n==4: self.som=self.som4
        else: self.som=self.som5
        self.som4.found=g.found4; self.som5.found=g.found5
        self.buttons_setup()
        if self.canvas<>None: self.canvas.grab_focus()
        ctrl=False
        pygame.key.set_repeat(600,120); key_ms=pygame.time.get_ticks()
        going=True
        while going:
            if self.journal:
                # Pump GTK messages.
                while gtk.events_pending(): gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    if not self.journal: utils.save()
                    going=False
                elif event.type == pygame.MOUSEMOTION:
                    g.pos=event.pos
                    g.redraw=True
                    if self.canvas<>None: self.canvas.grab_focus()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    g.redraw=True
                    if event.button==1:
                        if self.do_click():
                            pass
                        else:
                            bu=buttons.check()
                            if bu!='': self.do_button(bu); self.flush_queue()
                    if event.button==3:
                        self.som.right_click(); self.flush_queue()
                elif event.type == pygame.KEYDOWN:
                    # throttle keyboard repeat
                    if pygame.time.get_ticks()-key_ms>110:
                        key_ms=pygame.time.get_ticks()
                        if ctrl:
                            if event.key==pygame.K_q:
                                if not self.journal: utils.save()
                                going=False; break
                            else:
                                ctrl=False
                        if event.key in (pygame.K_LCTRL,pygame.K_RCTRL):
                            ctrl=True; break
                        self.do_key(event.key); g.redraw=True
                        self.flush_queue()
                elif event.type == pygame.KEYUP:
                    ctrl=False
            if not going: break
            if g.redraw:
                self.display()
                if g.version_display: utils.version_display()
                g.screen.blit(g.pointer,g.pos)
                pygame.display.flip()
                g.redraw=False
            g.clock.tick(40)

if __name__=="__main__":
    pygame.init()
    pygame.display.set_mode((1024,768),pygame.FULLSCREEN)
    game=Soma()
    game.journal=False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
