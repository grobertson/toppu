import curses
from datetime import datetime
import pdb

class Gauge(object): 
    ''' 
        A self contained "gauge" which can be updated without having to care where it lives. 
        
        Extend to make magic. (i.e. override to make pretty ascii displays)
        
        Major hat tip to https://github.com/mooseman/pd_curses_stuff/ 
        
    '''
    _normal = 7
    _high = 4
    _low = 3
    _good = 7
    
    def __init__(   self, scr, ypos, xpos, val, 
                    units=None, label=None, color=7, 
                    bold=False, bg=curses.COLOR_BLACK, 
                    highlight_minmax=False): 
        #Initialize
        self._scr = scr
        self._ypos = ypos
        self._xpos = xpos     
        self._val = val
        self._val_text = str(val)
        self._min = val
        self._max = val
        self._color = color
        self._bold = bold
        self._bg = bg
        self._highlightMinMax = highlight_minmax
        self._history = []
        
        self.label = label
        self.units = units
        
    def update(self, val):
        self.val = val    
        color = self._normal
        
        if self._highlightMinMax:
            if val > self._max:
                self._max = val
                color = self._high
            
            if val == self._max:
                color = self._high
                
        if self._highlightMinMax:
            if val < self._min:
                self._min = val
                color = self._low
            
            if val == self._min:
                color = self._low

        self.draw(color)
 
    def draw(self, color=None): 
        if color:
            self._scr.addstr(self.ypos, self.xpos, self.content, curses.color_pair(color))
            pass
        else:
            self._scr.addstr(self.ypos, self.xpos, self.content, curses.color_pair(self.color))
        self._scr.refresh()
        
    def refresh(self):
        self._scr.refresh()
        self._hasDrawn = True   
 
    def add_history(self, val):
        self._history.insert(0, val)
    
    def get_history(self):
        return self._history
    
    ''' Properties '''
    
    @property
    def content(self):
        c = " ".join([self.label, self.val_text, self.units])
        for i in range(c.__len__(), 10):
            c = " " + c
        return c

    @property
    def xpos(self):
        return self._xpos

    @xpos.setter
    def xpos(self, val):
        self._xpos = val

    @property
    def ypos(self):
        return self._ypos
    
    @ypos.setter
    def ypos(self, val):
        self._ypos = val   
    
    @property
    def max(self):
        return self._max
    
    @property
    def min(self):
        return self._min
    
    @property
    def val(self):
        return self._val
    
    @val.setter
    def val(self, val):
        self.add_history(self._val)
        self._val = val
        self._val_text = str(val)
        self._lastUpdate = datetime.now()
    
    @property
    def val_text(self):
        return self._val_text

    @property
    def label(self):
        return self._label
    
    @label.setter
    def label(self, val):
        if val:
            self._label = str(val)
            self._label_width = self._label.__len__()
        else: 
            self._label = ''
            self._label_width = self._label.__len__()

    @property
    def units(self):
        return self._units
    
    @units.setter
    def units(self, val):
        if val:
            self._units = str(val)
            self._units_width = self._units.__len__()
        else: 
            self._units = ''
            self._units_width = 0

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, val):
        self._color = int(val)

    @property
    def bg(self):
        return self._bg
    
    @bg.setter
    def bg(self, val):
        self._bg = val

    @property
    def bold(self):
        return self._bold
    
    @bold.setter
    def bold(self, val):
        self._bold = val


class HttpStatusGauge(Gauge):

    @property
    def val(self):
        return self._val
    
    @val.setter
    def val(self, val):
        self._val = val
        if int(val) in range(500,599):
            self._max = val
            self.color = self._high
        elif int(val) in range(400,499):
            self._min = val
            self.color = self._low
        elif int(val) in range(300,399):
            self._min = val
            self.color = self._low
        elif int(val) == 200: 
            self.color = self._normal
        else:
            self.color = self._good
         
        self._val_text = str(val)
        self._lastUpdate = datetime.now()
    
      
class Heading(object): 
    def __init__(self, posrange, datalist, column_padding=0):      
        self.posrange = posrange
        self.datalist = datalist


class Box(object):
    def __init__(self, scr, startx, starty, endx, endy):
        self.STDSCR = scr
        self.startx = startx
        self.endx = endx
        self.starty = starty
        self.endy = endy
        self.width = endx - startx
        self.height = endy - starty
        
        top = ""
        for i in range(startx, endx):
            top = top + chr(205)
        
        self.top = top

    def draw(self):
        self.STDSCR.addstr(self.starty, self.startx, chr(205), 15)
        self.STDSCR.addstr(self.endy - 2, self.startx, chr(205), 15)
    
