import tkinter,os
from tkinter import *
import tkinter.filedialog
import tkinter.font as TkFont
from PIL import  Image,ImageTk
import cv2


class DIPGUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.WIDTH_SIZE=300
        self.HEIGHT_SIZE=300

        # set size of window
        master.minsize(width=1080, height=720)
        master.maxsize(width=1920, height=1080)
        self.pack()

        # set button
        self.selectBtn = Button(master, text='Open', command=self.selectFile)
        self.saveBtn=Button(master,text='Save',command=self.saveFile)

        # set label showing image
        self.oriLbl=Label(bg="white",text="original",font=("Courier",30))
        self.modLbl=Label(bg='white',text='modified',font=("Courier", 30))

        # place all object on frame
        self.selectBtn.place(x=100,y=100)
        self.saveBtn.place(x=100,y=150)
        self.oriLbl.place(x=250,y=100,width=str(self.WIDTH_SIZE),height=str(self.HEIGHT_SIZE))
        self.modLbl.place(x=600,y=100,width=str(self.WIDTH_SIZE),height=str(self.HEIGHT_SIZE))

    def selectFile(self):
        ifile = tkinter.filedialog.askopenfile(initialdir=os.path.abspath('.'),mode='rb',title='Choose File',filetypes=[("image files",".jpg .png")])
        try:
            self.oriImg = Image.open(ifile)
        except:
            return
        self.oriImg = self.oriImg.resize((self.WIDTH_SIZE, self.HEIGHT_SIZE))

        self.modImg=self.oriImg

        self.img1 = ImageTk.PhotoImage(self.oriImg)

        self.oriLbl.configure(image=self.img1)
        self.oriLbl.image=self.img1
        self.modLbl.configure(image=self.img1)
        self.modLbl.image=self.img1

    def saveFile(self):
        ofile=tkinter.filedialog.asksaveasfile(initialdir=os.path.abspath('.'),mode='w',title='Save File',filetypes=([("png files",".jpg .png")]))
        if ofile:
            try:
                self.modImg.save(ofile)
            except:
                return