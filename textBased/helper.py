import curses
from curses import panel
import os,sys
from math import floor


class Menu():
    def __init__ (self,items,window):
        self.window=window.subwin(1,1)
        self.window.keypad(1)
        self.panel=panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()
        self.window.scrollok(True)
        self.position=0
        self.items=items
        self.maxItems=len(items)
        self.items.append(('..'))
        self.map=floor(len(self.items)/30)
        self.mainItems=self.__divideList()
        # MAKE SCROLL MANUAL

    def __divideList(self):
        mainList=[]
        for i in range(0,self.map+1):
            mainList.append(self.items[i*30:i*30+30])
        return mainList

    def navigate(self,n):
        self.position+=n
        if self.position<0:
            self.position=0
        elif self.position>=self.maxItems+1:
            self.position=0

    def display(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()

        mainList=self.__divideList()
        while True:
            self.window.clear()
            self.window.refresh()
            curses.doupdate()
            d=floor(self.position/30)
            if self.mainItems[d]!=None:
                self.items=self.mainItems[d]
            elif self.maxItems[d]==[]:
                pass
            for index,item in enumerate(self.items):
                if index==self.position-(d*30):
                    mode =curses.A_REVERSE
                else:
                    mode=curses.A_NORMAL
                msg="{}".format(item)
                if index+1<self.window.getmaxyx()[0]:
                    self.window.addstr(index,1,msg,mode)

            key=self.window.getch()
            if key in [curses.KEY_ENTER,ord("\n")]:
                if self.position==len(self.items)-1:
                    return self.items[self.position-(d*30)][0:]
                else:
                    return self.items[self.position-(d*30)][0:]
            elif key==curses.KEY_UP:
                self.navigate(-1)
            elif key==curses.KEY_DOWN:
                self.navigate(1)
            elif key==curses.KEY_BACKSPACE:
                return '..'

            elif key==27:
                return 'xx'
        # self.window.clear()
            elif key==9:
                global path
                path=os.path.split(path)[0]
                return path
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()



#               TRIP INTO THE DIRECTORIES:
def listFiles(path=""):
    fileList=[]
    try:
        for files in os.listdir(path):
            if files[0]=='.':
                pass
            else:
                fileList.append(files)
        return fileList
    except:
        path=os.path.split(path)[0]
        for files in os.listdir(path):
            if files[0]=='.':
                pass
            else:
                fileList.append(files)
        return fileList


path=os.getcwd()
def changePath(item=''):
    global path
    try:
        if os.path.exists(os.path.join(path,item))==True:
            if os.path.split(path)[1]=='..':
                path=os.path.split(path)[0]
                path=os.path.split(path)[0]
            if item==None or os.path.isfile(os.path.join(path,item)) :
            # path,bad=os.path.split(path)
                return path
            else:
                if path==os.path.join(path,item):
                    return path
                else:
                    path=os.path.join(path,item)
                    return path
        else:
            return path
    except:
        path=os.path.split(path)[0]
        return path

#           END OF THE FUNCTIONS FOR DIRECTORIES
