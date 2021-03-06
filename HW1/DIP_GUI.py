# =============Used Package===================
# tkinter:    sudo pacman -S python3-tk
# cv2:        sudo pacman -S opencv-python
# numpy:      pip install numpy
# scipy:      pip install scipy
# PIL:        pip install Pillow
# matplotlib: pip install matplotlib
# ============================================

# ===============Environment==================
# Arch Linux (Kernel version: 5.13.13-arch1-1)
# with python 3.9.6
# ============================================

import tkinter,os,cv2,math
import numpy as np
from scipy import ndimage
import tkinter.filedialog
import tkinter.font as TkFont
from tkinter import *
from PIL import  Image,ImageTk
import matplotlib.pyplot as plt


# bilinear function for sizeChange(zoom/shrink)
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

# class DIPGUI for building GUI interface
class DIPGUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        # set initial variables
        self.WIDTH_SIZE=256
        self.HEIGHT_SIZE=256
        self.widthCur=256
        self.heightCur=256
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
        self.modLbl=Label(bg='white',text='modified',font=("Courier", 30))
        self.sizeChangeLbl=Label(bg='black',text='Zoom/Shrink',font=("Courier",10))
        self.rotateLbl=Label(bg='black',text='Rotate',font=("Courier",10))

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
        self.sizeChangeLbl.place(x=100,y=470)
        self.rotateLbl.place(x=100,y=520)

    # select file by relative path and display it
    def selectFile(self):
        ifile = tkinter.filedialog.askopenfile(initialdir=os.path.abspath('.'),mode='rb',title='Choose File',filetypes=[("image files",".jpg .png .tif .jpeg .gif")])
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
        self.modLbl.configure(image=imgTmp)
        self.modLbl.image=imgTmp

    # save file from self.modImg on 'modified' frame
    def saveFile(self):
        ofile=tkinter.filedialog.asksaveasfile(initialdir=os.path.abspath('.'),mode='w',title='Save File',filetypes=([("png files",".tif .jpg .png")]))
        if ofile:
            try:
                self.modImg.save(ofile)
            except:
                return

    # set method mode by pressing 'method' button
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
            self.methodAScale.config(from_=0,to=60,resolution=1)
            self.methodBScale.config(from_=1,to=50,resolution=10)
            self.methodAScale.set(0)
            self.methodBScale.set(1)

    # use method according to the current method mode
    def method(self,test):
        if not self.modImgBool:
            return
        mode=self.methodList.index(self.methodBtn['text'])
        a=self.methodAScale.get()
        b=self.methodBScale.get()

        imgMode=self.imgArray

        if mode==0:
            imgTmpArray=a*imgMode+b


        elif mode==1:
            imgTmpArray=np.exp(a*imgMode+b)
            
# ======================================================================================
# changing equation into y=a*ln(X+b),
# because the original equation cannot see the difference easily by modified 'a' and 'b'
        elif mode==2:
            np.seterr(invalid='ignore',divide='ignore')
            imgTmpArray=np.array(np.log(imgMode+b))*a
# ======================================================================================

        outlier=imgTmpArray > 255
        imgTmpArray[outlier]=255

        self.display(imgTmpArray,self.WIDTH_SIZE,self.HEIGHT_SIZE,self.degree)
        self.imgArrayCur=imgTmpArray

    # change size of image (zoom/shrink)
    def sizeChange(self,test):
        time=2**(self.sizeChangeScale.get())
        self.widthCur=self.WIDTH_SIZE*time
        self.heightCur=self.HEIGHT_SIZE*time
        newShape=list(map(int,[self.widthCur,self.heightCur]))
        sizeImg=np.zeros(newShape,dtype=np.uint8)

        ratio=1/time

        for x in range(sizeImg.shape[0]):
            for y in range(sizeImg.shape[1]):
                oldX=ratio*x
                oldY=ratio*y
                sizeImg[x,y]=bilinear(self.imgArrayCur,oldX,oldY)


        self.display(sizeImg,self.widthCur,self.heightCur,self.degree)

    # get rotate degree and pass to 'display' function
    def rotate(self,test):
        self.degree=self.rotateScale.get()
        self.display(self.imgArrayCur,self.WIDTH_SIZE,self.HEIGHT_SIZE,self.degree)

    # turn image by using histogram equation and plot the histogram of image
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

        self.imgArrayCur=result

        imgTmp=Image.fromarray(np.uint8(result))
        self.modImg=imgTmp
        imgTmp=ImageTk.PhotoImage(imgTmp)
        self.modLbl.configure(image=imgTmp)
        self.modLbl.image=imgTmp

        plt.title("HIstogramm for Image")
        plt.xlabel("Value")
        plt.ylabel("pixels Frequency")
        plt.hist(self.imgArray)
        plt.show()

    # reset modified frame and scale
    def reset(self):
        self.WIDTH_SIZE=256
        self.HEIGHT_SIZE=256

        self.display(self.imgArray,self.WIDTH_SIZE,self.HEIGHT_SIZE,0)

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

    # display image in 'modified frame' according to size and rotate degree
    def display(self,imgTmpArray,width,height,d):
        self.modLbl.destroy()

        imgTmp=Image.fromarray(np.uint8(imgTmpArray))
        imgTmp=imgTmp.rotate(d,expand=0)
        imgTmp=imgTmp.resize((int(self.widthCur),int(self.heightCur)),Image.ANTIALIAS)
        self.modImg=imgTmp
        
        if self.widthCur>self.WIDTH_SIZE:
            p1=int((self.widthCur-self.WIDTH_SIZE)/2)
            p2=int((self.heightCur-self.HEIGHT_SIZE)/2)
            p3=int((self.widthCur+self.WIDTH_SIZE)/2)
            p4=int((self.widthCur+self.WIDTH_SIZE)/2)
            imgTmp=imgTmp.crop((p1,p2,p3,p4))

        imgTmp=ImageTk.PhotoImage(imgTmp)
        self.modLbl=Label(width=self.WIDTH_SIZE,height=self.HEIGHT_SIZE,bg="white",text="modified",font=("Courier",30),image=imgTmp)
        self.modLbl.image=imgTmp
        self.modLbl.place(x=600,y=50)