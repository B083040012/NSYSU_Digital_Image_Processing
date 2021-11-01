import tkinter,os
import numpy as np
from tkinter import *
import tkinter.filedialog
import tkinter.font as TkFont
from PIL import  Image,ImageTk
import cv2

def bilinear(array,x,y):

    p1=min(int(x),array.shape[0]-1)
    q1=min(int(y),array.shape[1]-1)
    mu=x-p1
    lamb=y=q1
    p2=min(p1+1,array.shape[0]-1)
    q2=min(q1+1,array.shape[1]-1)

    leftUp=array[p1,q1]
    leftDown=array[p2,q1]
    rightUp=array[p1,q2]
    rightDown=array[p2,q2]

    value1=mu*rightDown+(1-mu)*leftDown
    value2=mu*rightUp+(1-mu)*leftDown

    level=lamb*value1+(1-lamb)*value2


    return level

class DIPGUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.WIDTH_SIZE=300
        self.HEIGHT_SIZE=300
        self.methodList=['Linearly','Exponentially','Logarithmically']
        self.modImgBool=False
        self.nextMode=0
        self.degree=0

        # set size of window
        master.minsize(width=1080, height=720)
        master.maxsize(width=1920, height=1080)
        self.pack()

        # set button
        self.selectBtn = Button(master, text='Open', command=self.selectFile)
        self.saveBtn=Button(master,text='Save',command=self.saveFile)
        self.methodBtn=Button(master,text='Linearly',command=self.methodMode)
        self.histoBtn=Button(master,text='Histogram',command=self.histogram)
        self.resetBtn=Button(master,text='reset',command=self.reset)

        # set scale
        self.methodAScale=Scale(master,orient=HORIZONTAL,from_=0,to=5,resolution=0.5,length=300,command=self.method)
        self.methodAScale.set(1)
        self.methodBScale=Scale(master,orient=HORIZONTAL,from_=-100,to=100,resolution=5,length=300,command=self.method)
        self.methodBScale.set(0)
        self.sizeChangeScale=Scale(master,orient=HORIZONTAL,from_=-5,to=1,resolution=1,length=300,command=self.sizeChange)
        self.sizeChangeScale.set(0)
        self.rotateScale=Scale(master,orient=HORIZONTAL,from_=-180,to=180,resolution=1,length=300,command=self.rotate)
        self.rotateScale.set(0)

        # set label showing image
        self.oriLbl=Label(bg="white",text="original",font=("Courier",30))
        # self.canvas=tkinter.Canvas(master,bg='white',width=self.WIDTH_SIZE,height=self.HEIGHT_SIZE)
        self.modLbl=Label(bg='white',text='modified',font=("Courier", 30))
        self.sizeChangeLbl=Label(bg='blue',text='Zoom/Shrink',font=("Courier",10))
        self.rotateLbl=Label(bg='blue',text='Rotate',font=("Courier",10))

        # place all object on frame
        self.selectBtn.place(x=100,y=50)
        self.saveBtn.place(x=100,y=100)
        self.methodBtn.place(x=100,y=400)
        self.histoBtn.place(x=100,y=570)
        self.resetBtn.place(x=100,y=150)

        self.methodAScale.place(x=250,y=350)
        self.methodBScale.place(x=250,y=400)
        self.sizeChangeScale.place(x=250,y=450)
        self.rotateScale.place(x=250,y=500)

        self.oriLbl.place(x=250,y=50,width=str(self.WIDTH_SIZE),height=str(self.HEIGHT_SIZE))
        self.modLbl.place(x=600,y=50,width=str(self.WIDTH_SIZE),height=str(self.HEIGHT_SIZE))
        # self.canvas.place(x=600,y=50)
        self.sizeChangeLbl.place(x=100,y=470)
        self.rotateLbl.place(x=100,y=520)

    def selectFile(self):
        ifile = tkinter.filedialog.askopenfile(initialdir=os.path.abspath('.'),mode='rb',title='Choose File',filetypes=[("image files",".jpg .png")])
        try:
            self.oriImg = Image.open(ifile)
        except:
            return
        self.imgArray=np.asarray(self.oriImg)
        self.imgArrayCur=self.imgArray
        imgTmp = self.oriImg.resize((self.WIDTH_SIZE, self.HEIGHT_SIZE),Image.ANTIALIAS)
        self.modImgBool=True
        self.modImg=imgTmp

        imgTmp = ImageTk.PhotoImage(imgTmp)

        self.oriLbl.configure(image=imgTmp)
        self.oriLbl.image=imgTmp
        # self.canvasObj=self.canvas.create_image(self.WIDTH_SIZE/2,self.HEIGHT_SIZE/2,image=imgTmp)
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
        self.nextMode=(currMethod+1)%3
        self.methodBtn['text']=self.methodList[self.nextMode]

        if self.nextMode==0:
            self.methodAScale.config(from_=0,to=5,resolution=0.2)
            self.methodBScale.config(from_=-100,to=100,resolution=5)
            self.methodAScale.set(1)
            self.methodBScale.set(0)
        elif self.nextMode==1:
            self.methodAScale.config(from_=0,to=1,resolution=0.005,digits=5)
            self.methodBScale.config(from_=-50,to=0,resolution=0.5,digits=2)
            self.methodAScale.set(0)
            self.methodBScale.set(0)
        elif self.nextMode==2:
            self.methodAScale.config(from_=0,to=100,resolution=1)
            self.methodBScale.config(from_=1,to=50,resolution=10)
            self.methodAScale.set(0)
            self.methodBScale.set(1)

    def method(self,test):
        if not self.modImgBool:
            return
        # self.modLbl.config(image='')
        mode=self.methodList.index(self.methodBtn['text'])
        a=self.methodAScale.get()
        b=self.methodBScale.get()

        if mode==0:
            imgTmpArray=a*self.imgArray+b


        elif mode==1:
            imgTmpArray=np.exp(a*self.imgArray+b)
            

        elif mode==2:
            imgTmpArray=np.log(a*self.imgArray+b)

        outlier=imgTmpArray > 255
        imgTmpArray[outlier]=255

        self.display(imgTmpArray,self.WIDTH_SIZE,self.HEIGHT_SIZE,self.degree)
        self.imgArrayCur=imgTmpArray

        # imgTmp=Image.fromarray(np.uint8(imgTmpArray))
        # imgTmp=imgTmp.resize((self.WIDTH_SIZE,self.WIDTH_SIZE),Image.ANTIALIAS)
        # self.modImg=imgTmp
        # imgTmp=ImageTk.PhotoImage(imgTmp)
        # self.modLbl.configure(image=imgTmp)
        # self.modLbl.image=imgTmp

    def sizeChange(self,test):
        time=2**(self.sizeChangeScale.get())
        # newShape=list(map(int,[self.imgArray.shape[0]*time,self.imgArray.shape[1]*time]))
        width=self.WIDTH_SIZE*time
        height=self.HEIGHT_SIZE*time
        newShape=list(map(int,[width,height]))
        sizeImg=np.zeros(newShape,dtype=np.uint8)

        ratio=1/time

        for x in range(sizeImg.shape[0]):
            for y in range(sizeImg.shape[1]):
                oldX=ratio*x
                oldY=ratio*y
                sizeImg[x,y]=bilinear(self.imgArray,oldX,oldY)
                # sizeImg[x,y]=bilinear(self.imgArrayCur,oldX,oldY)


        self.display(sizeImg,int(width),int(height),0)
        # self.display(sizeImg,sizeImg.shape[0],sizeImg.shape[1],0)

        # self.modLbl.destroy()
        # imgTmp=Image.fromarray(np.uint8(sizeImg))
        # imgTmp=imgTmp.resize((sizeImg.shape[0],sizeImg.shape[1]),Image.ANTIALIAS)
        # self.modImg=imgTmp
        # imgTmp=ImageTk.PhotoImage(imgTmp)
        # self.modLbl=Label(bg="white",text="modified",font=("Courier",30),image=imgTmp)
        # self.modLbl.image=imgTmp
        # self.modLbl.place(x=600,y=50)

    def rotate(self,test):
        self.degree=self.rotateScale.get()
        self.display(self.imgArrayCur,self.WIDTH_SIZE,self.HEIGHT_SIZE,d=self.degree)
        # self.modLbl.destroy()
        # # self.canvas.delete(self.canvasObj)
        # imgTmp=Image.fromarray(np.uint8(self.imgArray))
        # imgTmp=imgTmp.resize((self.WIDTH_SIZE,self.HEIGHT_SIZE),Image.ANTIALIAS)
        # imgTmp=imgTmp.rotate(degree)
        # self.modImg=imgTmp
        # imgTmp=ImageTk.PhotoImage(imgTmp)
        # # self.canvasObj=self.canvas.create_image(self.WIDTH_SIZE/2,self.HEIGHT_SIZE/2,image=self.imgRo)
        # self.modLbl=Label(bg="white",text="modified",font=("Courier",30),image=imgTmp)
        # self.modLbl.image=imgTmp
        # self.modLbl.place(x=600,y=50)

    def histogram(self):
        height=self.imgArray.shape[0]
        width=self.imgArray.shape[1]

        hisCount=np.zeros([256],np.int32)

        for h in range(0,height):
            for w in range(0,width):
                hisCount[self.imgArray[h,w]]+=1

        hisPdf=hisCount/hisCount.sum()
        hisCdf=np.zeros(256,float)

        hisCdf[0] = hisPdf[0]
        for i in range(1, 256):
            hisCdf[i] = hisCdf[i-1] + hisPdf[i]

        sK = np.round(hisCdf*255, 0)
        result = np.zeros((height,width))

        for h in range(0,height):
            for w in range(0,width):
                oriLevel = self.imgArray[h, w]
                newLevel = sK[oriLevel]
                result[h,w] = newLevel

        overfit=result > 255
        result[overfit]=255

        underfit=result < 0
        result[underfit]=0
        imgTmp=Image.fromarray(np.uint8(result))
        imgTmp=ImageTk.PhotoImage(imgTmp)
        self.modLbl.configure(image=imgTmp)
        self.modLbl.image=imgTmp

    def reset(self):
        self.WIDTH_SIZE=300
        self.HEIGHT_SIZE=300

        self.display(self.imgArray,self.WIDTH_SIZE,self.HEIGHT_SIZE,0)
        # imgTmp=Image.fromarray(np.uint8(self.imgArray))
        # imgTmp=imgTmp.resize((self.WIDTH_SIZE,self.WIDTH_SIZE),Image.ANTIALIAS)

        # self.modImg=imgTmp
        # imgTmp=ImageTk.PhotoImage(imgTmp)

        # self.modLbl.configure(image=imgTmp)
        # self.modLbl.image=imgTmp

        self.sizeChangeScale.set(0)
        self.rotateScale.set(0)

        if self.nextMode==0:
            self.methodAScale.set(1)
            self.methodBScale.set(0)
        elif self.nextMode==1:
            self.methodAScale.set(0)
            self.methodBScale.set(0)
        elif self.nextMode==2:
            self.methodAScale.set(0)
            self.methodBScale.set(1)

    def display(self,imgTmpArray,width,height,d):
        # self.modLbl.configure(image='')
        self.modLbl.destroy()
        # imgTmp=Image.fromarray(np.uint8(imgTmpArray))
        imgTmp=Image.fromarray(np.uint8(imgTmpArray))
        imgTmp=imgTmp.resize((width,height),Image.ANTIALIAS)
        imgTmp=imgTmp.rotate(d)

        self.modImg=imgTmp
        
        imgTmp=ImageTk.PhotoImage(imgTmp)
        self.modLbl=Label(bg="white",text="modified",font=("Courier",30),image=imgTmp)
        self.modLbl.image=imgTmp
        self.modLbl.place(x=600,y=50)