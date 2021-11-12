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
from scipy import signal
import matplotlib.pyplot as plt

def convolve2D(image, kernel, padding=0, strides=1):
    # Cross Correlation
    kernel = np.flipud(np.fliplr(kernel))

    # Gather Shapes of Kernel + Image + Padding
    xKernShape = kernel.shape[0]
    yKernShape = kernel.shape[1]
    xImgShape = image.shape[0]
    yImgShape = image.shape[1]

    # Shape of Output Convolution
    xOutput = int(((xImgShape - xKernShape + 2 * padding) / strides) + 1)
    yOutput = int(((yImgShape - yKernShape + 2 * padding) / strides) + 1)
    output = np.zeros((xOutput, yOutput))

    # Apply Equal Padding to All Sides
    if padding != 0:
        imagePadded = np.zeros((image.shape[0] + padding*2, image.shape[1] + padding*2))
        imagePadded[int(padding):int(-1 * padding), int(padding):int(-1 * padding)] = image
        print(imagePadded)
    else:
        imagePadded = image

    # Iterate through image
    for y in range(image.shape[1]):
        # Exit Convolution
        if y > image.shape[1] - yKernShape:
            break
        # Only Convolve if y has gone down by the specified Strides
        if y % strides == 0:
            for x in range(image.shape[0]):
                # Go to next row once kernel is out of bounds
                if x > image.shape[0] - xKernShape:
                    break
                try:
                    # Only Convolve if x has moved by the specified Strides
                    if x % strides == 0:
                        output[x, y] = (kernel * imagePadded[x: x + xKernShape, y: y + yKernShape]).sum()
                except:
                    break

    return output

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

        # set scale
        self.lowLevelScale=Scale(master,orient=HORIZONTAL,from_=0,to=255,resolution=1,length=250,command=self.grayLevel)
        self.lowLevelScale.set(0)
        self.highLevelScale=Scale(master,orient=HORIZONTAL,from_=0,to=255,resolution=1,length=250,command=self.grayLevel)
        self.highLevelScale.set(0)
        self.bitPlaneScale=Scale(master,orient=HORIZONTAL,from_=0,to=7,resolution=1,length=250,command=self.bitPlane)
        self.bitPlaneScale.set(0)
        self.smoothScale=Scale(master,orient=HORIZONTAL,from_=0,to=1,resolution=0.01,length=250,command=self.smooth)
        self.smoothScale.set(0)
        self.sharpenScale=Scale(master,orient=HORIZONTAL,from_=0,to=1,resolution=0.01,length=250,command=self.sharpen)
        self.sharpenScale.set(0)

        # set label showing 
        self.oriLbl=Label(bg="white",text="original",font=("Courier",30))
        self.modLbl=Label(bg='white',text='modified',font=("Courier", 30))
        self.A1Label=Label(bg='black',text='A-1',font=("Courier",10))
        self.A2Label=Label(bg='black',text='A-2',font=("Courier",10))
        self.A3Label=Label(bg='black',text='A-3',font=("Courier",10))

        # place all object on frame
        self.selectBtn.place(x=60,y=50)
        self.saveBtn.place(x=60,y=100)
        self.modeA1Btn.place(x=200,y=600)

        self.lowLevelScale.place(x=200,y=650)
        self.highLevelScale.place(x=200,y=700)
        self.bitPlaneScale.place(x=200,y=800)
        self.smoothScale.place(x=500,y=650)
        self.sharpenScale.place(x=500,y=700)
        
        self.oriLbl.place(x=200,y=50,width=str(self.WIDTH_SIZE),height=str(self.HEIGHT_SIZE))
        self.modLbl.place(x=800,y=50,width=str(self.WIDTH_SIZE),height=str(self.HEIGHT_SIZE))
        self.A1Label.place(x=100,y=600)
        self.A2Label.place(x=100,y=800)
        self.A3Label.place(x=500,y=600)

    # select file by relative path and display it
    def selectFile(self):
        # ifile = tkinter.filedialog.askopenfile(initialdir=os.path.abspath('.'),mode='rb',title='Choose File',filetypes=[("image files",".jpg .png .tif .jpeg .gif")])
        # try:
        #     self.oriImg = Image.open(ifile)
        # except:
        #     return
        self.oriImg=Image.open('test_img/lenna_gray.tif')

        self.imgArray=np.array(self.oriImg)

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
        ofile=tkinter.filedialog.asksaveasfile(initialdir=os.path.abspath('.'),mode='w',title='Save File',filetypes=([("png files",".tif .jpg .png")]))
        if ofile:
            try:
                self.modImg.save(ofile)
            except:
                return

    def modeSelect(self):
        currMode=self.modeA1List.index((self.modeA1Btn['text']))
        self.nextMode=(currMode+1)%2
        self.modeA1Btn['text']=self.modeA1List[self.nextMode]

        self.grayLevel(currMode)

    def grayLevel(self,test):
        if not self.modImgBool:
            return
        self.lowLevel=self.lowLevelScale.get()
        self.highLevel=self.highLevelScale.get()

        mode=self.modeA1List.index(self.modeA1Btn['text'])

        imgTmp = np.zeros((self.width,self.height),dtype = np.uint8)
        
        if mode==0:
            for i in range(self.width):
                for j in range(self.height):
                    if self.highLevel>self.imgArray[i][j] and self.imgArray[i][j]>self.lowLevel:
                        imgTmp[i][j]=255
                    else:
                        imgTmp[i][j]=self.imgArray[i][j]
        elif mode==1:
            for i in range(self.width):
                for j in range(self.height):
                    if self.highLevel>self.imgArray[i][j] and self.imgArray[i][j]>self.lowLevel:
                        imgTmp[i][j]=255
                    else:
                        imgTmp[i][j]=0

        self.display(imgTmp,self.WIDTH_SIZE,self.HEIGHT_SIZE)

    def bitPlane(self,test):
        value=self.bitPlaneScale.get()

        bitAndArray=np.zeros((self.width,self.height),dtype=np.uint8)
        bitAndArray=2**value
        imgTmp=np.zeros((self.width,self.height,8),dtype=np.uint8)

        imgTmp[:,:,value]=cv2.bitwise_and(self.imgArray,bitAndArray)

        mask = imgTmp[:,:,value] > 0
        imgTmp[mask] = 255

        self.display(imgTmp[:,:,value],self.width,self.height)

    def smooth(self,test):
        sigma=self.smoothScale.get()
        if sigma==0:
            return
        x,y=np.mgrid[-1:2,-1:2]
        gauKernel=np.exp(-(x**2 + y**2) / (2*sigma**2))
        # gauKernel=np.exp(-(x**2+y**2))

        gauKernal=gauKernel/gauKernel.sum()

        # imgTmp=convolve2D(self.imgArray,gauKernel)
        imgTmp=signal.convolve2d(self.imgArray,gauKernal,boundary='symm',mode='same')

        self.display(imgTmp,self.width,self.height)

    def sharpen(self,test):
        sigma=self.sharpenScale.get()
        if sigma==0:
            return
        x,y=np.mgrid[-1:2,-1:2]
        gauKernel=np.exp(-(x**2 + y**2) / (2*sigma**2))

        gauKernal=gauKernel/gauKernel.sum()

        imgTmp=signal.convolve2d(self.imgArray,gauKernal,boundary='symm',mode='same')

        imgTmp=self.imgArray-imgTmp
        imgTmp=self.imgArray+imgTmp

        # outlier=imgTmp>255
        # imgTmp[outlier]=255

        self.display(imgTmp,self.width,self.height)

    # display image in 'modified frame' according to size and rotate degree
    def display(self,imgTmpArray,width,height):
        # self.modLbl.destroy()

        imgTmp=Image.fromarray(np.uint8(imgTmpArray))
        # imgTmpArray=np.asarray(imgTmpArray)
        # imgTmp=Image.fromarray(imgTmpArray)
        imgTmp=imgTmp.resize((int(width),int(height)),Image.ANTIALIAS)
        self.modImg=imgTmp

        imgTmp=ImageTk.PhotoImage(imgTmp)
        # self.modLbl=Label(width=self.WIDTH_SIZE,height=self.HEIGHT_SIZE,bg="white",text="modified",font=("Courier",30),image=imgTmp)
        self.modLbl.config(image=imgTmp)
        self.modLbl.image=imgTmp