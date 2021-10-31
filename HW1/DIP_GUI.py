import tkinter,os
import numpy as np
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
        self.methodList=['Linearly','Exponentially','Logarithmically']
        self.modImgBool=False

        # set size of window
        master.minsize(width=1080, height=720)
        master.maxsize(width=1920, height=1080)
        self.pack()

        # set button
        self.selectBtn = Button(master, text='Open', command=self.selectFile)
        self.saveBtn=Button(master,text='Save',command=self.saveFile)
        self.methodBtn=Button(master,text='Linearly',command=self.methodMode)

        # set scale
        self.methodAScale=Scale(master,orient=HORIZONTAL,from_=0,to=5,resolution=0.5,length=300,command=self.method)
        self.methodAScale.set(1)
        self.methodBScale=Scale(master,orient=HORIZONTAL,from_=-100,to=100,resolution=5,length=300,command=self.method)
        self.methodBScale.set(0)

        # set label showing image
        self.oriLbl=Label(bg="white",text="original",font=("Courier",30))
        self.modLbl=Label(bg='white',text='modified',font=("Courier", 30))

        # place all object on frame
        self.selectBtn.place(x=100,y=50)
        self.saveBtn.place(x=100,y=100)
        self.methodBtn.place(x=100,y=400)

        self.methodAScale.place(x=250,y=350)
        self.methodBScale.place(x=250,y=400)

        self.oriLbl.place(x=250,y=50,width=str(self.WIDTH_SIZE),height=str(self.HEIGHT_SIZE))
        self.modLbl.place(x=600,y=50,width=str(self.WIDTH_SIZE),height=str(self.HEIGHT_SIZE))

    def selectFile(self):
        ifile = tkinter.filedialog.askopenfile(initialdir=os.path.abspath('.'),mode='rb',title='Choose File',filetypes=[("image files",".jpg .png")])
        try:
            self.oriImg = Image.open(ifile)
        except:
            return
        self.imgArray=np.asarray(self.oriImg)
        imgTmp = self.oriImg.resize((self.WIDTH_SIZE, self.HEIGHT_SIZE),Image.ANTIALIAS)
        self.modImgBool=True

        imgTmp = ImageTk.PhotoImage(imgTmp)

        self.oriLbl.configure(image=imgTmp)
        self.oriLbl.image=imgTmp
        self.modLbl.configure(image=imgTmp)
        self.modLbl.image=imgTmp

    def saveFile(self):
        ofile=tkinter.filedialog.asksaveasfile(initialdir=os.path.abspath('.'),mode='w',title='Save File',filetypes=([("png files",".jpg .png")]))
        if ofile:
            try:
                self.modImg.save(ofile)
            except:
                return

    def methodMode(self):
        currMethod=self.methodList.index((self.methodBtn['text']))
        nextMode=(currMethod+1)%3
        self.methodBtn['text']=self.methodList[nextMode]

        if nextMode==0:
            self.methodAScale.config(from_=0,to=5,resolution=0.2)
            self.methodBScale.config(from_=-100,to=100,resolution=5)
            self.methodAScale.set(1)
            self.methodBScale.set(0)
        elif nextMode==1:
            self.methodAScale.config(from_=0,to=1,resolution=0.005,digits=5)
            self.methodBScale.config(from_=-50,to=0,resolution=0.5,digits=2)
        elif nextMode==2:
            self.methodAScale.config(from_=0,to=100000,resolution=100)
            self.methodBScale.config(from_=1,to=50,resolution=10)
            self.methodAScale.set(0)
            self.methodBScale.set(1)

    def method(self,test):
        if not self.modImgBool:
            return
        self.modLbl.config(image='')
        mode=self.methodList.index(self.methodBtn['text'])
        a=self.methodAScale.get()
        b=self.methodBScale.get()
        if mode==0:
            imgTmpArray=a*self.imgArray+b
            condition=imgTmpArray > 255
            imgTmpArray[condition]=255
            imgTmp=Image.fromarray(imgTmpArray)
            imgTmp.resize((self.WIDTH_SIZE,self.HEIGHT_SIZE),Image.ANTIALIAS)
            imgTmp=ImageTk.PhotoImage(imgTmp)
            self.modLbl.configure(image=imgTmp)
            self.modLbl.image=imgTmp