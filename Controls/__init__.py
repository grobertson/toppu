import curses
from datetime import datetime

class Gauge(object): 
    ''' 
        A self contained "gauge" which can be updated without having to care where it lives. 
        
        Extend to make magic. (i.e. override to make pretty ascii displays)
        
        Major hat tip to https://github.com/mooseman/pd_curses_stuff/ 
        
    '''
    _ypos = None
    _xpos = None
    _val = None
    _val_text = None
    _label = None
    _units = None
    _color = None
    _bg = None
    _bold = None
    _hasDrawn = False
    _lastUpdate = None
    _max = 0
    _min = 0
    
    _normal = 1
    _high = 2
    _low = 3
    _good = 4
    
    def __init__(self, scr, ypos, xpos, val, units=None, label=None, color=curses.COLOR_WHITE, bold=False, bg=curses.COLOR_BLACK): 
        #Initialize
        self._scr = scr
        self.ypos = ypos
        self.xpos = xpos     
        self.val = val
        self.label = label
        self.color = color
        self.bold = bold
        self.bg = bg
        self.units = units

    def update(self, val): 
        self.val = val    
        if self._hasDrawn:
            self.draw()
        else:
            pass 
    
    def draw(self): 
        self._scr.addstr(self.ypos, self.xpos, self.content, self.color)
        self.refresh()
    
    def refresh(self):
        self._scr.refresh()
        self._hasDrawn = True   
        
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
        self._val = val
        if val > self._max:
            self._max = val
            self.color = self._high
        if val < self._min:
            self._min = val
            self.color = self._low
        if not val == self._min: 
            if not val == self._max:
                self.color = self._normal
         
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
            self._label_width = 0

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
        self._color = val

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

      
class Heading(object): 
    def __init__(self, posrange, datalist):      
        self.posrange = posrange
        self.datalist = datalist
