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

# class DIPGUI2 for building GUI interface
class DIPGUI2(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)

        # set initial variables
        self.WIDTH_SIZE=512
        self.HEIGHT_SIZE=512
        self.width=512
        self.height=512
        self.modImgBool=False

        # A1
        self.lowLevel=0
        self.highLevel=255
        self.modeA1List=['preserve','dis_black']
        self.nextMode=0

        # set size of window
        master.minsize(width=1600,height=900)
        master.maxsize(width=1920,height=1080)
        self.pack()

        # set button
        self.selectBtn = Button(master, text='Open', command=self.selectFile)
        self.saveBtn=Button(master,text='Save',command=self.saveFile)
        self.modeA1Btn=Button(master,text='preserve',command=self.modeSelect)
        self.avgMaskBtn=Button(master,text='avgMask',command=self.avgMask)
        self.medianFilterBtn=Button(master,text='medianFilter',command=self.medianFilter)
        self.laplacianMaskBtn=Button(master,text='laplacianMask',command=self.laplacianMask)
        self.resetBtn=Button(master,text='reset',command=self.reset)

        # set scale
        self.lowLevelScale=Scale(master,orient=HORIZONTAL,from_=0,to=255,resolution=1,length=250,command=self.grayLevel)
        self.lowLevelScale.set(0)
        self.highLevelScale=Scale(master,orient=HORIZONTAL,from_=0,to=255,resolution=1,length=250,command=self.grayLevel)
        self.highLevelScale.set(0)
        self.bitPlaneScale=Scale(master,orient=HORIZONTAL,from_=0,to=7,resolution=1,length=250,command=self.bitPlane)
        self.bitPlaneScale.set(0)
        self.smoothScale=Scale(master,orient=HORIZONTAL,from_=0,to=10,resolution=1,length=250,command=self.smooth)
        self.smoothScale.set(0)
        self.sharpenScale=Scale(master,orient=HORIZONTAL,from_=0,to=10,resolution=1,length=250,command=self.sharpen)
        self.sharpenScale.set(0)

        # set label showing 
        self.oriLbl=Label(bg="white",text="original",font=("Courier",30))
        self.modLbl=Label(bg='white',text='modified',font=("Courier", 30))
        self.A1Label=Label(bg='white',fg='black',text='A-1',font=("Courier",15))
        self.A2Label=Label(bg='white',fg='black',text='A-2',font=("Courier",15))
        self.A3Label=Label(bg='white',fg='black',text='A-3',font=("Courier",15))
        self.partBLabel=Label(bg='white',fg='black',text='Part B',font=("Courier",15))
        self.lowLevelLabel=Label(bg='white',fg='black',text='Low Level',font=("Courier",10))
        self.highLevelLabel=Label(bg='white',fg='black',text='High Level',font=("Courier",10))
        self.smoothLabel=Label(bg='white',fg='black',text='Smooth',font=("Courier",15))
        self.sharpenLabel=Label(bg='white',fg='black',text='Sharpen',font=("Courier",15))

        # place all object on frame
        self.selectBtn.place(x=60,y=50)
        self.saveBtn.place(x=60,y=100)
        self.modeA1Btn.place(x=200,y=600)
        self.avgMaskBtn.place(x=1000,y=650)
        self.medianFilterBtn.place(x=1000,y=700)
        self.laplacianMaskBtn.place(x=1000,y=750)
        self.resetBtn.place(x=60,y=150)

        self.lowLevelScale.place(x=200,y=650)
        self.highLevelScale.place(x=200,y=700)
        self.bitPlaneScale.place(x=200,y=800)
        self.smoothScale.place(x=700,y=650)
        self.sharpenScale.place(x=700,y=700)
        
        self.oriLbl.place(x=200,y=50,width=str(self.WIDTH_SIZE),height=str(self.HEIGHT_SIZE))
        self.modLbl.place(x=800,y=50,width=str(self.WIDTH_SIZE),height=str(self.HEIGHT_SIZE))
        self.A1Label.place(x=100,y=600)
        self.A2Label.place(x=100,y=800)
        self.A3Label.place(x=700,y=600)
        self.lowLevelLabel.place(x=90,y=650)
        self.highLevelLabel.place(x=90,y=700)
        self.partBLabel.place(x=1000,y=600)
        self.smoothLabel.place(x=600,y=650)
        self.sharpenLabel.place(x=600,y=700)

    # select file by relative path and display it
    def selectFile(self):
        ifile = tkinter.filedialog.askopenfile(initialdir=os.path.abspath('.'),mode='rb',title='Choose File',filetypes=[("image files",".tif .raw .tiff .jpg .png .jpeg .gif")])
        try:
            if str(ifile).find(".raw")>=0:
                ifile=str(ifile)[str(ifile).find("test_img/"):-2]
                rawData = open(ifile, "rb").read()
                # print(len([ord(c) for c in str(rawData)]))
                # print(len(str(rawData)))
                self.oriImg = Image.frombytes("L", (512,512), rawData)
                # print(len(list(self.oriImg.getdata())))
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

    # save file from self.modImg on 'modified' frame
    def saveFile(self):
        ofile=tkinter.filedialog.asksaveasfile(initialdir=os.path.abspath('.'),mode='w',title='Save File',filetypes=([("png files",".tiff .jpg .png")]))
        if ofile:
            try:
                # if str(ofile).find(".raw")>=0:
                #     print("in raw")
                #     self.imgRaw=self.imgRaw.flatten()
                #     # self.imgRaw=chr(self.imgRaw)
                #     imgSave=''.join(chr(i) for i in self.imgRaw)
                #     # print(imgSave)
                #     ofile=str(ofile)[str(ofile).find("test_img/"):-26]
                #     print(ofile)
                #     with open("test_img/test.raw", 'w') as f:
                #         f.write(imgSave)
                # else:
                self.modImg.save(ofile) 
            except:
                return

    # selecting mode by user for preserving unselected area or make it black
    def modeSelect(self):
        currMode=self.modeA1List.index((self.modeA1Btn['text']))
        self.nextMode=(currMode+1)%2
        self.modeA1Btn['text']=self.modeA1List[self.nextMode]

        self.grayLevel(currMode)

    # show gray-level slicing image defined by user
    def grayLevel(self,test):
        if not self.modImgBool:
            return
        self.lowLevel=self.lowLevelScale.get()
        self.highLevel=self.highLevelScale.get()

        mode=self.modeA1List.index(self.modeA1Btn['text'])

        imgTmp = np.zeros((self.width,self.height),dtype = np.uint8)

        imgCompare=self.imgArray
        
        if mode==0:
            for i in range(self.width):
                for j in range(self.height):
                    if self.highLevel>imgCompare[i][j] and imgCompare[i][j]>self.lowLevel:
                        imgTmp[i][j]=255
                    else:
                        imgTmp[i][j]=imgCompare[i][j]
        elif mode==1:
            for i in range(self.width):
                for j in range(self.height):
                    if self.highLevel>imgCompare[i][j] and imgCompare[i][j]>self.lowLevel:
                        imgTmp[i][j]=255
                    else:
                        imgTmp[i][j]=0

        self.display(imgTmp,self.WIDTH_SIZE,self.HEIGHT_SIZE)

    # show corresponding bit plane image according to the bitPlaneScale
    def bitPlane(self,test):
        value=self.bitPlaneScale.get()

        bitAndArray=np.zeros((self.width,self.height),dtype=np.uint8)
        bitAndArray=2**value
        imgTmp=np.zeros((self.width,self.height,8),dtype=np.uint8)

        imgTmp[:,:,value]=cv2.bitwise_and(self.imgArray,bitAndArray)
        # imgTmp[:,:,value]=cv2.bitwise_and(self.imgCurr,bitAndArray)

        mask = imgTmp[:,:,value] > 0
        imgTmp[mask] = 255

        self.display(imgTmp[:,:,value],self.width,self.height)

    # smoothing image by gaussian filter
    def smooth(self,test):
        level=self.smoothScale.get()
        if level==0:
            # self.display(self.imgArray,self.width,self.height)
            self.display(self.imgCurr,self.width,self.height)
            return
        x,y=np.mgrid[-1:2,-1:2]
        gauKernel=np.exp(-(x**2 + y**2) / (2*0.7**2))

        gauKernal=gauKernel/gauKernel.sum()

        imgTmp=signal.convolve2d(self.imgArray,gauKernal,boundary='symm',mode='same')
        # imgTmp=signal.convolve2d(self.imgCurr,gauKernal,boundary='symm',mode='same')
        for i in range(level-1):
            imgTmp=signal.convolve2d(imgTmp,gauKernal,boundary='symm',mode='same')

        self.display(imgTmp,self.width,self.height)

    # sharpen image by unsharp mask
    def sharpen(self,test):
        level=self.sharpenScale.get()
        if level==0:
            self.display(self.imgArray,self.width,self.height)
            return
        x,y=np.mgrid[-1:2,-1:2]
        gauKernel=np.exp(-(x**2 + y**2) / (2*0.7**2))

        gauKernal=gauKernel/gauKernel.sum()

        imgBlur=signal.convolve2d(self.imgArray,gauKernal,boundary='symm',mode='same')
        # imgBlur=signal.convolve2d(self.imgCurr,gauKernal,boundary='symm',mode='same')
        for i in range(level-1):
            imgBlur=signal.convolve2d(imgBlur,gauKernal,boundary='symm',mode='same')

        mask=self.imgArray-imgBlur
        outlier=mask<0
        mask[outlier]=0
        imgTmp=self.imgArray+mask

        self.display(imgTmp,self.width,self.height)

    # apply averaging mask by pressing button
    def avgMask(self):
        mask = np.ones([3, 3], dtype = np.uint8)
        mask = mask / 9
        
        # Convolve the 3X3 mask over the image
        imgTmp = np.zeros([self.width, self.height])
        imgOri=self.imgArray

        for i in range(1,self.width-1):
            for j in range(1,self.height-1):
                pixelTmp = imgOri[i-1, j-1]*mask[0, 0]+imgOri[i-1, j]*mask[0, 1]+imgOri[i-1, j + 1]*mask[0, 2]+imgOri[i, j-1]*mask[1, 0]+ imgOri[i, j]*mask[1, 1]+imgOri[i, j + 1]*mask[1, 2]+imgOri[i + 1, j-1]*mask[2, 0]+imgOri[i + 1, j]*mask[2, 1]+imgOri[i + 1, j + 1]*mask[2, 2]
                imgTmp[i, j]= pixelTmp

        self.display(imgTmp,self.width,self.height)

    # apply 3x3 median filter by pressing button
    def medianFilter(self):
        imgTmp=np.zeros([self.width,self.height])
        # imgOri=self.imgArray
        imgOri=self.imgCurr

        for i in range(1,self.width-1):
            for j in range(1,self.height-1):
                pixelTmp=int(statistics.median([imgOri[i-1,j-1],imgOri[i-1,j],imgOri[i-1,j+1],imgOri[i,j-1],imgOri[i,j],imgOri[i,j+1],imgOri[i+1,j-1],imgOri[i+1,j],imgOri[i+1,j+1],]))
                imgTmp[i,j]=pixelTmp

        self.display(imgTmp,self.width,self.height)

    # apply laplacian mask from figure 3.37(b)
    def laplacianMask(self):
        mask=[[1,1,1],
              [1,-8,1],
              [1,1,1]]

        imgTmp=signal.convolve2d(self.imgArray,mask,boundary='symm',mode='same')

        outlier=imgTmp<0
        imgTmp[outlier]=0

        self.display(imgTmp,self.width,self.height)
    
    # reset modified image
    def reset(self):
        self.display(self.imgArray,self.width,self.height)
        self.lowLevelScale.set(0)
        self.highLevelScale.set(0)
        self.bitPlaneScale.set(0)
        self.smoothScale.set(0)
        self.sharpenScale.set(0)
    
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