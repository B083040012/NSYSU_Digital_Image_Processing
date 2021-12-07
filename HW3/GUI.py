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

import tkinter,os,cv2,math,statistics
import numpy as np
from scipy import ndimage
import tkinter.filedialog
import tkinter.font as TkFont
from tkinter import *
from PIL import  Image,ImageTk
from scipy import signal
import matplotlib.pyplot as plt

class DIPGUI3(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)

        # set initial variables
        self.WIDTH_SIZE=512
        self.HEIGHT_SIZE=512
        self.width=512
        self.height=512
        self.modImgBool=False

        # Q1
        self.modeQ1List=['7x7 Mean','3x3 Mean','7x7 Median','3x3 Median']
        self.Q1nextMode=0

        # set size of window
        master.minsize(width=1600,height=900)
        master.maxsize(width=1920,height=1080)
        self.pack()

        # set button
        self.selectBtn = Button(master, text='Open', command=self.selectFile)
        self.saveBtn=Button(master,text='Save',command=self.saveFile)
        self.Q1Btn=Button(master,text='Select Mode',command=self.Q1ModeSelect)

        # set label showing
        self.oriLbl=Label(bg="white",text="original",font=("Courier",30))
        self.modLbl=Label(bg='white',text='modified',font=("Courier", 30))
        self.Q1Label=Label(bg='white',fg='black',text='Q1',font=("Courier",15))

        # place all object on frame
        self.selectBtn.place(x=60,y=50)
        self.saveBtn.place(x=60,y=100)
        self.Q1Btn.place(x=200,y=600)

        self.oriLbl.place(x=200,y=50,width=str(self.WIDTH_SIZE),height=str(self.HEIGHT_SIZE))
        self.modLbl.place(x=800,y=50,width=str(self.WIDTH_SIZE),height=str(self.HEIGHT_SIZE))
        self.Q1Label.place(x=50,y=600)

    # save file from self.modImg on 'modified' frame
    def saveFile(self):
        ofile=tkinter.filedialog.asksaveasfile(initialdir=os.path.abspath('.'),mode='w',title='Save File',filetypes=([("png files",".tiff .jpg .png")]))
        if ofile:
            try:
                self.modImg.save(ofile) 
            except:
                return

    # select file by relative path and display it
    def selectFile(self):
        ifile = tkinter.filedialog.askopenfile(initialdir=os.path.abspath('.'),mode='rb',title='Choose File',filetypes=[("image files",".tif .raw .tiff .jpg .png .jpeg .gif")])
        try:
            if str(ifile).find(".raw")>=0:
                ifile=str(ifile)[str(ifile).find("test_img/"):-2]
                rawData = open(ifile, "rb").read()
                self.oriImg = Image.frombytes("L", (512,512), rawData)
            else:
                self.oriImg = Image.open(ifile)
        except:
            return

        self.imgArray=np.array(self.oriImg)
        self.imgRaw=self.imgArray
        self.imgCurr=self.imgArray
        self.width,self.height=self.imgArray.shape

        imgTmp = self.oriImg.resize((self.WIDTH_SIZE, self.HEIGHT_SIZE),Image.ANTIALIAS)
        self.modImgBool=True
        self.modImg=imgTmp

        imgTmp = ImageTk.PhotoImage(imgTmp)

        self.oriLbl.configure(image=imgTmp)
        self.oriLbl.image=imgTmp
        self.modLbl.configure(image=imgTmp)
        self.modLbl.image=imgTmp

    # modeSelect for Q1
    def Q1ModeSelect(self):
        if self.Q1Btn['text']=='Select Mode':
            self.Q1nextMode=0
            self.Q1Btn['text']=self.modeQ1List[self.Q1nextMode]
        else:
            currMode=self.modeQ1List.index((self.Q1Btn['text']))
            self.Q1nextMode=(currMode+1)%4
            self.Q1Btn['text']=self.modeQ1List[self.Q1nextMode]

        if self.Q1nextMode==0:
            self.meanFilter(7)
        elif self.Q1nextMode==1:
            self.meanFilter(3)
        elif self.Q1nextMode==2:
            self.medianFilter(7)
        elif self.Q1nextMode==3:
            self.medianFilter(3)

    # mean filter for Q1
    def meanFilter(self,filterSize):
        submask=[1.0]*filterSize
        # submask=[x/(filterSize*filterSize) for x in submask]
        mask=[submask]*filterSize

        print(mask)
        imgTmp=signal.convolve2d(self.imgArray,mask,boundary='symm',mode='same')

        outlier=imgTmp>0
        imgTmp[outlier]=255

        self.display(imgTmp,self.WIDTH_SIZE,self.HEIGHT_SIZE)

    # median filter for Q2
    def medianFilter(self,filterSize):
        imgTmp=np.zeros([self.height,self.width])
        imgOri=self.imgCurr

        maskSize=int((filterSize-1)/2)

        print(maskSize)

        for i in range(maskSize,self.width-maskSize):
            for j in range(maskSize,self.height-maskSize):
                pixelTmpList=[]
                for maskX in range(-(maskSize),maskSize+1):
                    for maskY in range(-(maskSize),maskSize+1):
                        pixelTmpList.append(imgOri[i+maskX,j+maskY])
                # pixelTmp=int(statistics.median([imgOri[i-1,j-1],imgOri[i-1,j],imgOri[i-1,j+1],imgOri[i,j-1],imgOri[i,j],imgOri[i,j+1],imgOri[i+1,j-1],imgOri[i+1,j],imgOri[i+1,j+1],]))
                pixelTmp=int(statistics.median(pixelTmpList))
                imgTmp[i,j]=pixelTmp


        self.display(imgTmp,self.HEIGHT_SIZE,self.WIDTH_SIZE)

    # display image in 'modified frame' according to size and rotate degree
    def display(self,imgTmpArray,width,height):
        self.imgCurr=imgTmpArray
        imgTmp=Image.fromarray(np.uint8(imgTmpArray))
        # imgTmpArray=np.asarray(imgTmpArray)
        # imgTmp=Image.fromarray(imgTmpArray)
        imgTmp=imgTmp.resize((int(width),int(height)),Image.ANTIALIAS)
        self.modImg=imgTmp

        imgTmp=ImageTk.PhotoImage(imgTmp)
        # self.modLbl=Label(width=self.WIDTH_SIZE,height=self.HEIGHT_SIZE,bg="white",text="modified",font=("Courier",30),image=imgTmp)
        self.modLbl.config(image=imgTmp)
        self.modLbl.image=imgTmp