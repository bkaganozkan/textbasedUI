import curses
from curses import panel
import helper
import sys
import os


class Window():
    curses.initscr()
    curses.resize_term(50,150)
    curses.resizeterm(50,150)
    _windowList=[]
    _panelList=[]
    def __init__(self,height=10,width=10,yLocation=0,xLocation=0,border=True):
        self.height=height
        self.width=width
        self.yLocation=yLocation
        self.xLocation=xLocation
        self.border=border
        self.__createWindow()
        self.__createPanel()
    @property
    def bkgd(self):
        return self.window.bkgd
    @property
    def addstr(self):
        return self.window.addstr

    # Easy way to create window with panel we can use it as "GWindow Object"
    def __createWindow(self):
        self.window=curses.newwin(self.height,self.width)
        self.panel=panel.new_panel(self.window)
        if self.border==True:
            self.window.box()
        self._windowList.append(self.window)
        self.window.refresh()
        # Create Panel
    def __createPanel(self):
        self.panel.move(self.yLocation,self.xLocation)
        self._panelList.append(self.panel)

    @classmethod
    def refreshWindows(cls):
        for window in cls._windowList:
            window.refresh()
            for panelx in cls._panelList:
                if window==panelx.window():
                    panelx.top()
                    panelx.show()
                    panel.update_panels()
class MainScreen():
    def __init__(self,windows,panels):
        self.loc=0
        self.windows=windows
        self.panels=panels
        self.screen=curses.initscr()
        curses.curs_set(0)
        self.screen.keypad(1)
        curses.noecho()
    def display(self):
        dirpath=helper.changePath()
        while True:
            for index,window in enumerate(self.windows):
                Window.refreshWindows()
                if index==self.loc:
                    mode=curses.A_REVERSE
                else:
                    mode=curses.A_NORMAL
                if self.windows[0]==window:
                    pass
                else:
                    window.bkgd(mode)
                window.refresh()
                curses.doupdate()
            key = self.screen.getch()
            if key in [curses.KEY_ENTER,ord("\n")]:
                if self.loc==0:
                    while True:
                        fileList=helper.listFiles(dirpath)
                        a=helper.Menu(fileList, self.windows[0]).display()
                        dirpath=helper.changePath(a)
                        self.windows[3].addstr(1,1,str(dirpath))
                        Window.refreshWindows()
                        if a=='xx':
                            break
            elif key==9:
                self.moveWindow(1)
            elif key==27:
                break
            self.windows[2].clear()
            self.windows[2].addstr(1,1,str(key))

    def moveWindow(self,x):
        self.loc+=x
        if self.loc<0:
            self.loc=len(self.windows)-1
        elif self.loc>len(self.windows)-1:
            self.loc= 0#len(self.windows)-1

Window(32,50,0,0)
Window(30,50,0,50)
Window(30,50,0,100)
Window(10,100,30,50)
MainScreen(Window._windowList,Window._panelList).display()
