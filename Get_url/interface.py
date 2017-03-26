'''
Created on 2017年3月24日

@author: HL
'''
from tkinter import *
import os

from Get_url import ready_to_get

class DemoGUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self["background"] = "pink"
    def createWidgets(self):
        self.Text_for_save1 = Label(self, text = u"姓名", font = 16, background = "PaleVioletRed2")
        self.Text_for_save1.grid(row=0, column=1)
        
if __name__ == '__main__':
    root = Tk() # Tk Object
    root.title("Ann")
    if not os.path.exists('./Pics/PCHOME_0.jpg'):
        get_url = ready_to_get() 
        get_url.get_PCHOME_timelimite()  
    app = DemoGUI(master=root)
    #start the program
    app.mainloop()