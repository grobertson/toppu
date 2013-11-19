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
    _high = 1
    _low = 6
    _good = 2
    
    def __init__(   self, scr, ypos, xpos, val, 
                    units=None, label=None, color=7, 
                    bold=False, bg=curses.COLOR_BLACK, width=0, left=False): 
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
        self._width = width
        self._left = left
        self._history = []
        
        self.label = label
        self.units = units
        
    def update(self, val):
        self.val = val    
        self.draw()
 
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
 
    ''' Properties '''
    
    @property
    def content(self):
        data = [self.label, self.val_text, self.units, "    "]            
        c = " ".join(data)                
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


class HistoryGauge(Gauge):
    
    @property
    def val(self):
        return self._val        

    @val.setter
    def val(self, val):
        self.add_history(self._val)
        self._val = val
        self._val_text = str(val)
        self._lastUpdate = datetime.now()

    def add_history(self, val):
        self._history.insert(0, val)
        if self._history.__len__() > 50:
            self._history.pop()
    
    def get_history(self):
        return self._history

    def max(self):
        try:
            val = max(self._history)
        except (TypeError, ZeroDivisionError, ValueError), e:
            val = 0
        return val        

    def min(self):
        try:
            val = min(self._history)
        except (TypeError, ZeroDivisionError), e:
            val = None
        return val


class MinMaxGauge(Gauge):

    def update(self, val):
        self.val = val    
        color = self._normal
    
        if val > self._max:
            self._max = val
            color = self._high
        
        if val == self._max:
            color = self._high
            
        if val < self._min:
            self._min = val
            color = self._low
        
        if val == self._min:
            color = self._low

        self.draw(color)    

class MinGauge(HistoryGauge):
    def dummy(self):
        pass
        
class MaxGauge(HistoryGauge):    
    @property
    def content(self):
        if self.max() > self.val:
            data = [self.label, str(self.max()), self.units, "    "]
        else:
            data = [self.label, str(self.val), self.units, "    "]        
        c = " ".join(data)                
        return c
    

class ColorMinMaxGauge(HistoryGauge):

    def update(self, val):
        self.val = val    
        color = self._normal
    
        if val > self.max():
            color = self._high
        
        if val == self.max():
            color = self._high
            
        if val < self.min():
            color = self._low
        
        if val == self.min():
            color = self._low

        self.draw(color)    

    

        
class AverageGauge(HistoryGauge):   

    def avg(self):
        try:
            avg = sum(self._history) / self._history.__len__()
        except (TypeError, ZeroDivisionError), e:
            avg = None
        return avg
    
    @property
    def content(self):
        if not self.avg():
            c = " ".join([self.label, self.val_text, self.units])
        else:
            data = [self.label, str(self.avg()), self.units, "    "]            
            c = " ".join(data)
        return c



class HttpStatusGauge(Gauge):

    def update(self, val):
        self.val = val    
        color = self._normal
    
        if int(val) in range(500,599):
            self._max = val
            color = self._high
        elif int(val) in range(400,499):
            self._min = val
            color = self._low
        elif int(val) in range(300,399):
            self._min = val
            color = self._good
        elif int(val) == 200: 
            color = self._good
        else:
            color = self._high

        self.draw(color)
 
class Clock(object):
    def __init__(self, scr, ypos, xpos): 
        #Initialize
        self._scr = scr
        self._ypos = ypos
        self._xpos = xpos     
        self._val = datetime.now()
        self._val_text = str(self._val)

    def update(self):
        self.val = datetime.now()    
        self.draw()
    
    def draw(self, color=None): 
        self._scr.addstr(self.ypos, self.xpos, self._val_text, curses.color_pair(7))
        self._scr.refresh()  
 
    ''' Properties '''
    @property
    def xpos(self):
        return self._xpos

    @xpos.setter
    def xpos(self, val):
        self._xpos = val

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, val):
        self._val = val
        self._val_text = val.strftime('%I:%M:%S %p')


    @property
    def ypos(self):
        return self._ypos
    
    @ypos.setter
    def ypos(self, val):
        self._ypos = val   
       
      
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
            #TODO: extended chars aren't displaying as expected. docs suck. -FGR
            top = top + chr(205)
        
        self.top = top

    def draw(self):
        self.STDSCR.addstr(self.starty, self.startx, chr(205), 15)
        self.STDSCR.addstr(self.endy - 2, self.startx, chr(205), 15)
    
