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
from tkinter import filedialog
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
        self.length=3
        self.modImgBool=False

        # Q1
        self.modeQ1List=['7x7 Mean','3x3 Mean','7x7 Median','3x3 Median','original']
        self.Q1NextMode=0

        # Q2(b)
        self.modeQ2bList=['Red','Green','Blue','Original']
        self.Q2bNextMode=0

        # Q2(c)
        self.modeQ2cList=['HSI Model','Hue','Saturation','Intensity','Original']
        self.Q2cNextMode=0

        # Q2(d)
        self.modeQ2dList=['Color Complment','Original']
        self.Q2dNextMode=0

        # set size of window
        master.minsize(width=1600,height=900)
        master.maxsize(width=1920,height=1080)
        self.pack()

        # set button
        self.selectBtn = Button(master, text='Open', command=self.selectFile)
        self.saveBtn=Button(master,text='Save',command=self.saveFile)
        self.Q1Btn=Button(master,text='Select Mode',command=self.Q1ModeSelect)
        self.Q2bBtn=Button(master,text='Select Mode',command=self.Q2bModeSelect)
        self.Q2cBtn=Button(master,text='Select Mode',command=self.Q2cModeSelect)
        self.Q2dBtn=Button(master,text='Select Mode',command=self.colorComple)
        self.rgbSmoothBtn=Button(master,text='RGB Smooth',command=self.rgbSmooth)
        self.rgbSharpBtn=Button(master,text='RGB Sharpen',command=self.rgbSharp)
        self.hsiSmoothBtn=Button(master,text='HSI Smooth',command=self.hsiSmooth)
        self.hsiSharpBtn=Button(master,text='HSI Sharpen',command=self.hsiSharp)
        self.difSmoothBtn=Button(master,text='dif of Smoothing',command=self.difSmooth)
        self.difSharpBtn=Button(master,text='dif of Sharpening',command=self.difSharp)
        self.Q2fBtn=Button(master,text='Feather Segmentation',command=self.featherSegment)

        # set label showing
        self.oriLbl=Label(bg="white",text="original",font=("Courier",30))
        self.modLbl=Label(bg='white',text='modified',font=("Courier", 30))
        self.Q1Label=Label(bg='white',fg='black',text='Q1',font=("Courier",15))
        self.Q2bLabel=Label(bg='white',fg='black',text='Q2(b)',font=("Courier",15))
        self.Q2cLabel=Label(bg='white',fg='black',text='Q2(c)',font=("Courier",15))
        self.Q2dLabel=Label(bg='white',fg='black',text='Q2(d)',font=("Courier",15))
        self.Q2eRGBLabel=Label(bg='white',fg='black',text='Q2(e)-RGB',font=("Courier",15))
        self.Q2eHSILabel=Label(bg='white',fg='black',text='Q2(e)-HSI',font=("Courier",15))
        self.Q2fLabel=Label(bg='white',fg='black',text='Q2(f)',font=("Courier",15))

        # place all object on frame
        self.selectBtn.place(x=60,y=50)
        self.saveBtn.place(x=60,y=100)
        self.Q1Btn.place(x=200,y=600)
        self.Q2bBtn.place(x=200,y=650)
        self.Q2cBtn.place(x=200,y=700)
        self.Q2dBtn.place(x=200,y=750)
        self.rgbSmoothBtn.place(x=600,y=600)
        self.rgbSharpBtn.place(x=730,y=600)
        self.hsiSmoothBtn.place(x=600,y=650)
        self.hsiSharpBtn.place(x=730,y=650)
        self.difSmoothBtn.place(x=550,y=700)
        self.difSharpBtn.place(x=700,y=700)
        self.Q2fBtn.place(x=600,y=750)

        self.oriLbl.place(x=200,y=50,width=str(self.WIDTH_SIZE),height=str(self.HEIGHT_SIZE))
        self.modLbl.place(x=800,y=50,width=str(self.WIDTH_SIZE),height=str(self.HEIGHT_SIZE))
        self.Q1Label.place(x=50,y=600)
        self.Q2bLabel.place(x=50,y=650)
        self.Q2cLabel.place(x=50,y=700)
        self.Q2dLabel.place(x=50,y=750)
        self.Q2eRGBLabel.place(x=450,y=600)
        self.Q2eHSILabel.place(x=450,y=650)
        self.Q2fLabel.place(x=450,y=750)

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
        self.ifile=filedialog.askopenfilename(title = "Select file",filetypes = (("tiff files","*.tif"),("tiff files","*.tiff"),("all files","*.*")))
        try:
            if str(self.ifile).find(".raw")>=0:
                self.ifile=str(self.ifile)[str(self.ifile).find("test_img/"):-2]
                rawData = open(self.ifile, "rb").read()
                self.oriImg = Image.frombytes("L", (512,512), rawData)
            else:
                self.oriImg = Image.open(self.ifile)
        except:
            return

        self.imgArray=np.array(self.oriImg)
        self.imgRaw=self.imgArray
        self.imgCurr=self.imgArray
        if len(self.imgArray.shape)==3:
            self.width,self.height,self.length=self.imgArray.shape
        else:
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
            self.Q1NextMode=0
            self.Q1Btn['text']=self.modeQ1List[self.Q1NextMode]
        else:
            currMode=self.modeQ1List.index((self.Q1Btn['text']))
            self.Q1NextMode=(currMode+1)%5
            self.Q1Btn['text']=self.modeQ1List[self.Q1NextMode]

        if self.Q1NextMode==0:
            self.meanFilter(7)
        elif self.Q1NextMode==1:
            self.meanFilter(3)
        elif self.Q1NextMode==2:
            self.medianFilter(7)
        elif self.Q1NextMode==3:
            self.medianFilter(3)
        elif self.Q1NextMode==4:
            self.display(self.imgArray,self.WIDTH_SIZE,self.HEIGHT_SIZE,0)

    # mean filter for Q1
    def meanFilter(self,filterSize):
        mask = np.ones([filterSize, filterSize], dtype = np.uint8)
        mask = mask / (filterSize*filterSize)

        print(mask)
        imgTmp=signal.convolve2d(self.imgArray,mask,boundary='symm',mode='same')

        outlier=imgTmp>0
        imgTmp[outlier]=255

        self.display(imgTmp,self.WIDTH_SIZE,self.HEIGHT_SIZE,0)

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


        self.display(imgTmp,self.HEIGHT_SIZE,self.WIDTH_SIZE,0)

    # mode select for Q2(b)
    def Q2bModeSelect(self):
        if self.Q2bBtn['text']=='Select Mode':
            self.Q2bNextMode=0
            self.Q2bBtn['text']=self.modeQ2bList[self.Q2bNextMode]
        else:
            currMode=self.modeQ2bList.index((self.Q2bBtn['text']))
            self.Q2bNextMode=(currMode+1)%4
            self.Q2bBtn['text']=self.modeQ2bList[self.Q2bNextMode]

        if self.Q2bNextMode==0:
            self.rgbComponent(0)
        elif self.Q2bNextMode==1:
            self.rgbComponent(1)
        elif self.Q2bNextMode==2:
            self.rgbComponent(2)
        elif self.Q2bNextMode==3:
            self.display(self.imgArray,self.WIDTH_SIZE,self.HEIGHT_SIZE,0)

    # rgb component function
    def rgbComponent(self,mode):
        imgTmp=np.zeros([self.height,self.width,self.length])
        if mode==0:
            imgTmp[:,:,0]=self.imgArray[:,:,0]
        elif mode==1:
            imgTmp[:,:,1]=self.imgArray[:,:,1]
        elif mode==2:
            imgTmp[:,:,2]=self.imgArray[:,:,2]
        self.display(imgTmp,self.width,self.height,self.length)

    # mode select for Q2(c)
    def Q2cModeSelect(self):
        if self.Q2cBtn['text']=='Select Mode':
            self.Q2cNextMode=0
            self.Q2cBtn['text']=self.modeQ2cList[self.Q2cNextMode]
        else:
            currMode=self.modeQ2cList.index((self.Q2cBtn['text']))
            self.Q2cNextMode=(currMode+1)%5
            self.Q2cBtn['text']=self.modeQ2cList[self.Q2cNextMode]

        if self.Q2cNextMode==0:
            imgTmp=np.zeros([self.height,self.width,self.length])
            hueTmp=self.hueConverter()
            outlier=hueTmp>255
            hueTmp[outlier]=255
            imgTmp[:,:,0]=hueTmp
            imgTmp[:,:,1]=self.satuConverter()
            imgTmp[:,:,2]=self.intenConverter()
        elif self.Q2cNextMode==1:
            hueTmp=self.hueConverter()
            outlier=hueTmp>255
            hueTmp[outlier]=255
            imgTmp=hueTmp
        elif self.Q2cNextMode==2:
            imgTmp=self.satuConverter()
        elif self.Q2cNextMode==3:
            imgTmp=self.intenConverter()
        elif self.Q2cNextMode==4:
            imgTmp=self.imgArray
        
        self.display(imgTmp,self.WIDTH_SIZE,self.HEIGHT_SIZE,0)

    # hue converter for hsi model
    def hueConverter(self):
        convTmp=np.float32(self.imgArray)/255
        red=convTmp[:,:,0]
        green=convTmp[:,:,1]
        blue=convTmp[:,:,2]

        imgTmp=np.copy(red)

        for i in range(0,self.WIDTH_SIZE):
            for j in range(0,self.HEIGHT_SIZE):
                rgSub=red[i][j]-green[i][j]
                rbSub=red[i][j]-blue[i][j]
                gbSub=green[i][j]-blue[i][j]

                den=np.sqrt(rgSub**2 +(rbSub * gbSub))
                theta=np.arccos((0.5 * (rgSub + rbSub))/den)

                if den<=0:
                    imgTmp[i][j]=0
                elif den>0:
                    imgTmp[i][j]=theta
                    if blue[i][j] > green[i][j]:
                        imgTmp[i][j]=2*np.pi-imgTmp[i][j]

        imgTmp=imgTmp*255
        return imgTmp
        
    # saturation converter for hsi model
    def satuConverter(self):
        convTmp=np.float32(self.imgArray)/255
        red=convTmp[:,:,0]
        green=convTmp[:,:,1]
        blue=convTmp[:,:,2]

        minTmp=np.minimum(np.minimum(red,green),blue)
        imgTmp=1-((3.00*minTmp)/(red+green+blue))
        
        imgTmp=imgTmp*255

        return imgTmp

    # itensity converter for hsi model
    def intenConverter(self):
        convTmp=np.float32(self.imgArray)/255
        red=convTmp[:,:,0]
        green=convTmp[:,:,1]
        blue=convTmp[:,:,2]

        imgTmp=(red+green+blue)/3.0
        return imgTmp*255

    # color complement function
    def colorComple(self):
        if self.Q2dBtn['text']=='Select Mode':
            self.Q2dNextMode=0
            self.Q2dBtn['text']=self.modeQ2dList[self.Q2dNextMode]
        else:
            currMode=self.modeQ2dList.index((self.Q2dBtn['text']))
            self.Q2dNextMode=(currMode+1)%2
            self.Q2dBtn['text']=self.modeQ2dList[self.Q2dNextMode]
        
        if self.Q2dNextMode==0:
            imgTmp=np.float32(self.imgArray)/255
            imgTmp=1-imgTmp
            imgTmp=imgTmp*255
            self.display(imgTmp,self.WIDTH_SIZE,self.HEIGHT_SIZE,3)
        elif self.Q2dNextMode==1:
            self.display(self.imgArray,self.WIDTH_SIZE,self.HEIGHT_SIZE,3)

    # smoothing process in rgb domain
    def rgbSmooth(self):
        mask = np.ones([5, 5], dtype = np.uint8)
        mask = mask / 25
        imgTmp=np.float32(self.imgArray)
        
        for l in range(0,3):
            imgTmp[:,:,l]=signal.convolve2d(imgTmp[:,:,l],mask,boundary='symm',mode='same')

        self.display(imgTmp,self.WIDTH_SIZE,self.HEIGHT_SIZE,3)

    # sharping process in rgb domain
    def rgbSharp(self):
        mask=[[0,1,0],
              [1,-4,1],
              [0,1,0]]
        imgTmp=np.float32(self.imgArray)

        for l in range(0,3):
            sharpMask=imgTmp[:,:,l]-signal.convolve2d(imgTmp[:,:,l],mask,boundary='symm',mode='same')
            outlier=sharpMask<0
            sharpMask[outlier]=0
            imgTmp[:,:,l]=sharpMask

        self.display(imgTmp,self.WIDTH_SIZE,self.HEIGHT_SIZE,3)

    # smoothing process in hsi domain
    def hsiSmooth(self):
        mask = np.ones([5, 5], dtype = np.uint8)
        mask = mask / 25

        imgTmp=np.zeros([self.height,self.width,self.length])
        imgTmp[:,:,0]=self.hueConverter()
        imgTmp[:,:,1]=self.satuConverter()
        imgTmp[:,:,2]=self.intenConverter()

        imgTmp[:,:,2]=signal.convolve2d(imgTmp[:,:,2],mask,boundary='symm',mode='same')

        imgTmp=self.hsiToRGB(imgTmp)

        self.display(imgTmp,self.WIDTH_SIZE,self.HEIGHT_SIZE,3)

    # sharping process in hsi domain
    def hsiSharp(self):
        mask=[[0,1,0],
              [1,-4,1],
              [0,1,0]]

        imgTmp=np.zeros([self.height,self.width,self.length])
        imgTmp[:,:,0]=self.hueConverter()
        imgTmp[:,:,1]=self.satuConverter()
        imgTmp[:,:,2]=self.intenConverter()

        sharpMask=imgTmp[:,:,2]-signal.convolve2d(imgTmp[:,:,2],mask,boundary='symm',mode='same')
        outlier=sharpMask<0
        sharpMask[outlier]=0
        imgTmp[:,:,2]=sharpMask

        imgTmp=self.hsiToRGB(imgTmp)

        self.display(imgTmp,self.WIDTH_SIZE,self.HEIGHT_SIZE,3)

    # difference of smoothing b/w RGB/HSI
    def difSmooth(self):
        mask = np.ones([5, 5], dtype = np.uint8)
        mask = mask / 25
        rgb_imgTmp=np.float32(self.imgArray)
        
        for l in range(0,3):
            rgb_imgTmp[:,:,l]=signal.convolve2d(rgb_imgTmp[:,:,l],mask,boundary='symm',mode='same')

        hsi_imgTmp=np.zeros([self.height,self.width,self.length])
        hsi_imgTmp[:,:,0]=self.hueConverter()
        hsi_imgTmp[:,:,1]=self.satuConverter()
        hsi_imgTmp[:,:,2]=self.intenConverter()

        hsi_imgTmp[:,:,2]=signal.convolve2d(hsi_imgTmp[:,:,2],mask,boundary='symm',mode='same')

        hsi_imgTmp=self.hsiToRGB(hsi_imgTmp)

        imgTmp=rgb_imgTmp-hsi_imgTmp

        self.display(imgTmp,self.WIDTH_SIZE,self.HEIGHT_SIZE,3)
        
    # difference of sharpening b/w RGB/HSI
    def difSharp(self):
        mask=[[0,1,0],
              [1,-4,1],
              [0,1,0]]
        rgb_imgTmp=np.float32(self.imgArray)

        for l in range(0,3):
            sharpMask=rgb_imgTmp[:,:,l]-signal.convolve2d(rgb_imgTmp[:,:,l],mask,boundary='symm',mode='same')
            outlier=sharpMask<0
            sharpMask[outlier]=0
            rgb_imgTmp[:,:,l]=sharpMask

        hsi_imgTmp=np.zeros([self.height,self.width,self.length])
        hsi_imgTmp[:,:,0]=self.hueConverter()
        hsi_imgTmp[:,:,1]=self.satuConverter()
        hsi_imgTmp[:,:,2]=self.intenConverter()

        sharpMask=hsi_imgTmp[:,:,2]-signal.convolve2d(hsi_imgTmp[:,:,2],mask,boundary='symm',mode='same')
        outlier=sharpMask<0
        sharpMask[outlier]=0
        hsi_imgTmp[:,:,2]=sharpMask

        hsi_imgTmp=self.hsiToRGB(hsi_imgTmp)

        imgTmp=rgb_imgTmp-hsi_imgTmp

        self.display(imgTmp,self.WIDTH_SIZE,self.HEIGHT_SIZE,3)

    # feather segmentation for Q2(f)
    def featherSegment(self):
        img=cv2.imread(self.ifile)
        
        hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        imgTmp=np.array(hsv)

        for i in range(0,512):
            for j in range(0,512):
                if imgTmp[i][j][0]>150 and imgTmp[i][j][0]<156:
                    imgTmp[i][j][1]=0
                    imgTmp[i][j][2]=255
                else:
                    imgTmp[i][j][1]=255

        imgTmp=self.hsiToRGB(imgTmp)
        imgTmp=cv2.cvtColor(imgTmp,cv2.COLOR_HSV2RGB)
        imgTmp=Image.fromarray(imgTmp)
        self.display(imgTmp,512,512,3)

    # convert hsi model to rgb image
    def hsiToRGB(self,hsi_img):
        rgb_img = hsi_img.copy()
        H,S,I = cv2.split(hsi_img)
        [H,S,I] = [ i/ 255.0 for i in ([H,S,I])]
        R,G,B = H,S,I
        for i in range(self.WIDTH_SIZE):
            for j in range(self.HEIGHT_SIZE):
                # h = H[i]*2*np.pi
                h = H[i][j]
                b=r=g=0
                if h>=0 and h<2*np.pi/3:
                    tmp = np.cos(np.pi / 3 - h)
                    b = I[i][j] * (1 - S[i][j])
                    r = I[i][j]*(1+S[i][j]*np.cos(h)/tmp)
                    g = 3*I[i][j]-r-b
                elif h>=2*np.pi/3 and h<4*np.pi/3:
                    tmp = np.cos(np.pi - h)
                    r = I[i][j] * (1 - S[i][j])
                    g = I[i][j]*(1+S[i][j]*np.cos(h-2*np.pi/3)/tmp)
                    b = 3 * I[i][j] - r - g
                elif h >= 4 * np.pi / 3 and h < 2 * np.pi:
                    tmp = np.cos(5 * np.pi / 3 - h)
                    g = I[i][j] * (1-S[i][j])
                    b = I[i][j]*(1+S[i][j]*np.cos(h-4*np.pi/3)/tmp)
                    r = 3 * I[i][j] - g - b

                B[i][j] = b
                G[i][j] = g
                R[i][j] = r

        rgb_img[:,:,0] = R*255
        rgb_img[:,:,1] = G*255
        rgb_img[:,:,2] = B*255
        return rgb_img

    # display image in 'modified frame' according to size and rotate degree
    def display(self,imgTmpArray,width,height,length):
        self.imgCurr=imgTmpArray
        imgTmp=Image.fromarray(np.uint8(imgTmpArray))
        if length==0:
            imgTmp=imgTmp.resize((int(width),int(height)),Image.ANTIALIAS)
        self.modImg=imgTmp

        imgTmp=ImageTk.PhotoImage(imgTmp)
        self.modLbl.config(image=imgTmp)
        self.modLbl.image=imgTmp