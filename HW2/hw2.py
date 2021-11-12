from GUI import DIPGUI2
from tkinter import *

def main():
    root = Tk()
    root.configure(background='gray')
    app = DIPGUI2(master=root)
    app.mainloop()
    # root.destroy()

if __name__=='__main__':
    main()