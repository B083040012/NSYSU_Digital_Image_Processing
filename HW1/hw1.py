from DIP_GUI import DIPGUI
from tkinter import *

def main():
    root = Tk()
    app = DIPGUI(master=root)
    app.mainloop()
    # root.destroy()

if __name__=='__main__':
    main()