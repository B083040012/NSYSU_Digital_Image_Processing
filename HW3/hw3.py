from GUI import DIPGUI3
from tkinter import *

def main():
    root=Tk()
    root.configure(background='gray')
    app=DIPGUI3(master=root)
    app.mainloop()

if __name__=='__main__':
    main()