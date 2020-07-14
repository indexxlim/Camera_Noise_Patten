#-*- coding: utf-8 -*-

from Tkinter import *
import Tkinter as tk
import Tkconstants, tkFileDialog
import ttk
from tkFileDialog import askopenfilename


import make_characteristic as mc
import numpy as np
import cPickle
import glob
import math
import sys
import os
from PIL import ImageTk, Image
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot   as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from mpl_toolkits.mplot3d import axes3d, Axes3D
import tkFont







  
class mainUI():  
    def __init__(self, parent): # 생성자 시작  
        self.parent = parent      
  
        # 라벨 값 변경을 위한 객체 선언  
        self.picWidth = StringVar()  
        self.main_value = "Relational image"
        self.main_value2 = "Relational image"

        self.main_value3 = "Relational image"


        self.fir_average_value = ""
        self.sec_average_value = ""
        self.thr_average_value = ""

        
        self.log1 = 'logimage'
        self.sam1 = 'samimage'
        self.xio1 = 'xioimage'
          
        self.initUI()
        self.result_value = 0
        self.result_value2 = 0
        self.result_value3 = 0

        self.fig=plt.figure()
        self.canvasfig = FigureCanvasTkAgg(self.fig)
        self.canvasfig2 = FigureCanvasTkAgg(self.fig)
        self.canvasfig3 = FigureCanvasTkAgg(self.fig)
        self.canvasfig4 = FigureCanvasTkAgg(self.fig)



        
          
    def initUI(self):  
        self.parent.title("Pattern Noise") # 메인 윈도우 타이틀 설정 
        
    


        #self.a_label = ttk.Label(self.parent, text="A Label")
        #self.a_label.grid(column=0, row=0)  


        #self.list_frame=Frame(self.parent)
        #self.list_frame.grid(column = 0, row = 0,ipadx="3m", ipady="3m", padx="3m", pady="3m")

        #self.list_frame.pack(

        FD = "picture"

        log1_FD = os.path.join(FD,"Logitech")
        log2_FD = os.path.join(FD,"Logitech2")
        log3_FD = os.path.join(FD,"Logitech3")
        samsung1_FD = os.path.join(FD,"Samsung")
        samsung2_FD = os.path.join(FD,"Samsung2")
        samsung3_FD = os.path.join(FD,"Samsung3")
        xiaomi1_FD = os.path.join(FD,"Xiaomi")
        xiaomi2_FD = os.path.join(FD,"Xiaomi2")
        xiaomi3_FD = os.path.join(FD,"Xiaomi3")
        log1_FD_list = os.listdir(log1_FD)
        samsung1_FD_list = os.listdir(samsung1_FD)
        xiaomi1_FD_list = os.listdir(xiaomi1_FD)





        log_sample = os.path.join(FD,"Logitech_sample")
        sam_sample = os.path.join(FD,"Samsung_sample")
        xio_sample = os.path.join(FD,"Xiaomi_sample")

        small_font = tkFont.Font(size=20) 


        self.img_select = ttk.Button(self.parent, text="select image", command=self.browsefile)   
        self.img_select.grid(column=0, row=0, ipadx="0m", ipady="3m", padx="3m", pady="3m") 

        self.listbox = tk.Listbox(self.parent, selectmode='extended', height=0, font=small_font)
        self.listbox.grid(column = 0, row = 1,ipadx="0m", ipady="3m", padx="3m", pady="3m",rowspan=8)
        
        self.listbox.insert(END, str(os.path.join(log1_FD, log1_FD_list[0])))
        self.listbox.insert(END, str(os.path.join(log1_FD, log1_FD_list[1])))
        self.listbox.insert(END, str(os.path.join(log1_FD, log1_FD_list[2])))
        self.listbox.insert(END, str(os.path.join(log1_FD, log1_FD_list[3])))
        #self.listbox.insert(3, str(os.path.join(log1_FD, 'C922PRO_A_19.jpg')))
        
        
        self.listbox.insert(END, str(os.path.join(samsung1_FD, samsung1_FD_list[0])))
        self.listbox.insert(END, str(os.path.join(samsung1_FD, samsung1_FD_list[1])))
        self.listbox.insert(END, str(os.path.join(samsung1_FD, samsung1_FD_list[2])))
        self.listbox.insert(END, str(os.path.join(samsung1_FD, samsung1_FD_list[3])))
        
        self.listbox.insert(END, str(os.path.join(xiaomi1_FD, xiaomi1_FD_list[0])))
        self.listbox.insert(END, str(os.path.join(xiaomi1_FD, xiaomi1_FD_list[1])))
        self.listbox.insert(END, str(os.path.join(xiaomi1_FD, xiaomi1_FD_list[2])))
        self.listbox.insert(END, str(os.path.join(xiaomi1_FD, xiaomi1_FD_list[3])))
        

        
        self.listbox.bind("<Double-Button-1>", self.call_back)


        self.logitech = ttk.Button(self.parent, text="logitech_c922pro", command=self.log_folder)   
        self.logitech.grid(column=3, row=0)     
        self.Samsung = ttk.Button(self.parent, text="Samsung_SCP_B900W", command=self.sam_folder)   
        self.Samsung.grid(column=5, row=0)     
        self.Xiaomi = ttk.Button(self.parent, text="Xiaomi_Mijia360", command=self.xio_folder)   
        self.Xiaomi.grid(column=7, row=0)     

        #self.image = Image.open(self.image_path)
        #self.img=ImageTk.PhotoImage(self.image)

        self.canvas = tk.Canvas(self.parent, width=300, height=200)
        self.canvas.grid(column=3, row=1, columnspan=2, rowspan=2)
        #self.canvas.create_image(80, 80, image=self.img)
        self.canvas2 = tk.Canvas(self.parent, width=300, height=200)
        self.canvas2.grid(column=5, row=1, columnspan=2, rowspan=2)

        self.canvas3 = tk.Canvas(self.parent, width=300, height=200)
        self.canvas3.grid(column=7, row=1, columnspan=2, rowspan=2)

        self.main_var = Label(self.parent, text = self.main_value) 
        self.main_var.grid(column=3, row=3)  
        self.main_var2 = Label(self.parent, text = self.main_value2) 
        self.main_var2.grid(column=5, row=3)  

        self.main_var3 = Label(self.parent, text = self.main_value3) 
        self.main_var3.grid(column=7, row=3)  


        # Label for height 


        self.result_imgfir = tk.Canvas(self.parent, width=300, height=200)
        self.result_imgfir.grid(column=1, row=4, columnspan=2, rowspan=2)

        #self.result_imgsec = tk.Canvas(self.parent, width=300, height=200)
        #self.result_imgsec.grid(column=3, row=4, columnspan=2, rowspan=2)

        #self.result_imgthr = tk.Canvas(self.parent, width=300, height=200)
        #self.result_imgthr.grid(column=5, row=4, columnspan=2, rowspan=2)

        


        self.log_aver_v = Label(self.parent, text = self.fir_average_value) 
        self.log_aver_v.grid(column=5, row=4)  

        #self.sam_aver_v = Label(self.parent, text = self.sec_average_value) 
        #self.sam_aver_v.grid(column=3, row=7)  

        #self.xio_aver_v = Label(self.parent, text = self.thr_average_value) 
        #self.xio_aver_v.grid(column=5, row=7)




        self.log_3d = tk.Canvas(self.parent, width=300, height=200)
        self.log_3d.grid(column=3, row=4)

        #self.sam_3d = tk.Canvas(self.parent, width=300, height=200)
        #self.sam_3d.grid(column=3, row=8) 

        #self.xiao_3d = tk.Canvas(self.parent, width=300, height=200)
        #self.xiao_3d.grid(column=5, row=8)

        self.canvas_flag = 0

    def browsefile(self):

        Tk().withdraw() 
        self.filename = askopenfilename()
        print self.filename
        self.listbox.insert(END, self.filename)




    def call_back(self, event):
        w = event.widget
        idx = int(w.curselection()[0])
        value = w.get(idx)
        
        self.test_ch(value, self.result_imgfir, self.log1)
        self.test_button = ttk.Button(self.parent, text="test", command=self.show_var)   
        self.test_button.grid(column=1, row=6,  ipadx="0m", ipady="3m", padx="3m", pady="3m")   
        #self.thrd_pic(self.log1,self.log_3d)
        


    def show_var(self):
        self.log_aver_v.configure(text='Image Differ : '+ str(self.result_test))

        self.thrd_pic4(self.log1,self.log_3d)



    
    def log_folder(self): 
        #self.action.configure(text='make')
        #folder = "picture/Logitech_sample"
        folder = "Logitech_AA"
        self.canvasfig.get_tk_widget().destroy()

        self.make_ch(folder, self.canvas, self.main_var, 1)
    def sam_folder(self): 
        #self.action.configure(text='make')
        folder = "Samsung_AA"
        self.canvasfig2.get_tk_widget().destroy()

        self.make_ch(folder, self.canvas2, self.main_var2, 2)
    def xio_folder(self): 
        #self.action.configure(text='make')
        folder = "Xiaomi_jpg"
        self.make_ch(folder, self.canvas3, self.main_var3, 3)

    def click_me(self): 
        #self.action.configure(text='make')
        folder = tkFileDialog.askdirectory()
        print "Selected Folder:", folder
        #self.make_ch(folder)

    def click_me2(self): 
        #self.action.configure(text='test')
        folder = tkFileDialog.askdirectory()
        print "Selected Folder:", folder
        #self.test_ch(folder)


    def make_ch(self,folder, canvas, main_var, canvasfig):
        # Get a list of images to process.
        main_var.configure(text='Relational Image : '+folder)

        #file_list = glob.glob(folder + '/*.jpg')
        #print "Processing %d images" % (len(file_list),)

        # Denoise and build the numerator/denominator.
        #numerator = None
        #denominator = None
        #for i, f in enumerate(file_list):
        #    print "Processing %03d %s" % (i, f,) 
        #    (denoised_matrix, residual_matrix) = mc.get_noise_from_file(f)
        #    if numerator is None:
        #        numerator = np.zeros_like(residual_matrix)
        #        denominator = np.zeros_like(residual_matrix)
        #    numerator += denoised_matrix * residual_matrix        #residual_matrix = original - denoised_matrix
        #    denominator += denoised_matrix * denoised_matrix
        #self.result_value = numerator / denominator

        camera_noise = np.loadtxt(folder, dtype=np.float)
        camera_noise_average = np.average(np.nan_to_num(camera_noise))
        camera_noise -= camera_noise_average
        camera_noise_norm = np.sqrt(np.sum(np.nan_to_num(camera_noise * camera_noise)))





        denoised_img = Image.fromarray(camera_noise)
        self.img = ImageTk.PhotoImage(denoised_img)
        #self.canvas.create_image(80, 80, image=self.img)

        if canvasfig ==1:
            self.thrd_pic(camera_noise, canvas)
            self.result_value = camera_noise
        elif canvasfig ==2:
            self.thrd_pic2(camera_noise, canvas)
            self.result_value2 = camera_noise
        elif canvasfig ==3:
            self.thrd_pic3(camera_noise, canvas)
            self.result_value3 = camera_noise


        FD = "picture"

        log1_FD = os.path.join(FD,"Logitech")
        log2_FD = os.path.join(FD,"Logitech2")
        log3_FD = os.path.join(FD,"Logitech3")
        samsung1_FD = os.path.join(FD,"Samsung")
        samsung2_FD = os.path.join(FD,"Samsung2")
        samsung3_FD = os.path.join(FD,"Samsung3")
        xiaomi1_FD = os.path.join(FD,"Xiaomi")
        xiaomi2_FD = os.path.join(FD,"Xiaomi2")
        xiaomi3_FD = os.path.join(FD,"Xiaomi3")

        log_sample = os.path.join(FD,"Logitech_sample")
        sam_sample = os.path.join(FD,"Samsung_sample")
        xio_sample = os.path.join(FD,"Xiaomi_sample")
        #self.test_ch(log_sample, self.result_imgfir, self.log1)
        #self.test_ch2(sam_sample, self.result_imgsec, self.sam1)
        #self.test_ch3(xio_sample, self.result_imgthr, self.xio1)
        
    def test_one(self, onefile, gird_img, img):
        
        camera_noise = self.result_value
        camera_noise_average = np.average(np.nan_to_num(camera_noise))
        camera_noise -= camera_noise_average
        camera_noise_norm = np.sqrt(np.sum(np.nan_to_num(camera_noise * camera_noise)))

     
        # Get this image's noise.
        denoised_matrix2, image_noise = mc.get_noise_from_file(onefile)
        image_noise_average = np.average(image_noise)
        image_noise -= image_noise_average
        image_noise_norm = np.sqrt(np.sum(image_noise * image_noise))

        #denoised_img = Image.fromarray(denoised_matrix2)
        #self.testimg= ImageTk.PhotoImage(denoised_img)
        #gird_img.create_image(40, 40, image=self.testimg)

        # Calculate the correlation between the two signals.
        print "Dot product %s is: %s" % (onefile,
                                    np.sum(np.nan_to_num(camera_noise * image_noise)) /
                                        (camera_noise_norm * image_noise_norm))
        cor_v = np.sum(np.nan_to_num(camera_noise * image_noise)) / (camera_noise_norm * image_noise_norm)
        sumf = cor_v

        print 'sumf : ', sumf
        
        print 'sumf(average) : ', sumf 
        self.log_aver_v.configure(text='Image Differ : '+str(sumf))
        #self.thrd_pic(denoised_matrix2,self.log_3d)

    def test_ch(self, onefile, gird_img, img):
        
        camera_noise = self.result_value
        camera_noise_average = np.average(np.nan_to_num(camera_noise))
        camera_noise -= camera_noise_average
        camera_noise_norm = np.sqrt(np.sum(np.nan_to_num(camera_noise * camera_noise)))

        camera_noise2 = self.result_value2
        camera_noise_average2 = np.average(np.nan_to_num(camera_noise2))
        camera_noise2 -= camera_noise_average2
        camera_noise_norm2 = np.sqrt(np.sum(np.nan_to_num(camera_noise2 * camera_noise2)))

        camera_noise3 = self.result_value3
        camera_noise_average3 = np.average(np.nan_to_num(camera_noise3))
        camera_noise3 -= camera_noise_average3
        camera_noise_norm3 = np.sqrt(np.sum(np.nan_to_num(camera_noise3 * camera_noise3)))



        # Get this image's noise.
        denoised_matrix2, image_noise = mc.get_noise_from_file(onefile)
        image_noise_average = np.average(image_noise)
        image_noise -= image_noise_average
        image_noise_norm = np.sqrt(np.sum(image_noise * image_noise))

        denoised_img = Image.fromarray(denoised_matrix2)
        self.testimg= ImageTk.PhotoImage(denoised_img)
        gird_img.create_image(40, 40, image=self.testimg)

        # Calculate the correlation between the two signals.
        print "Dot product %s is: %s" % (onefile,
                                    np.sum(np.nan_to_num(camera_noise * image_noise)) /
                                        (camera_noise_norm * image_noise_norm))
        cor_v = np.sum(np.nan_to_num(camera_noise * image_noise)) / (camera_noise_norm * image_noise_norm)
        cor_v2 = np.sum(np.nan_to_num(camera_noise2 * image_noise)) / (camera_noise_norm2 * image_noise_norm)
        cor_v3 = np.sum(np.nan_to_num(camera_noise3 * image_noise)) / (camera_noise_norm3 * image_noise_norm)

        if cor_v>cor_v2:
            if cor_v> cor_v3:
                sumf = cor_v
                max_ch = 'Logitech'
            else:
                 sumf = cor_v3
                 max_ch = 'Xiaomi'
        else:
            if cor_v2>cor_v3:
                sumf = cor_v2
                max_ch = 'Samsung'
            else:
                 sumf = cor_v3
                 max_ch = 'Xiaomi'

        #sumf = (cor_v if cor_v> cor_v3 else cor_v3) if cor_v>cor_v2 else (cor_v2 if cor_v2>cor_v3 else cor_v3)
        #sumf = cor_v 

        print 'sumf : ', sumf
   
        self.result_test = max_ch + ' is maximnum doc value, ' + str(sumf)
        #self.log_aver_v.configure(text='Logitech Differ : '+str(sumf))
        #self.thrd_pic(denoised_matrix2,self.log_3d)
        self.log1 = image_noise

    def test_ch2(self, onefile, gird_img, img):
        
        camera_noise = self.result_value
        camera_noise_average = np.average(np.nan_to_num(camera_noise))
        camera_noise -= camera_noise_average
        camera_noise_norm = np.sqrt(np.sum(np.nan_to_num(camera_noise * camera_noise)))


        # Get this image's noise.
        denoised_matrix2, image_noise = mc.get_noise_from_file(onefile)
        image_noise_average = np.average(image_noise)
        image_noise -= image_noise_average
        image_noise_norm = np.sqrt(np.sum(image_noise * image_noise))

        denoised_img = Image.fromarray(denoised_matrix2)
        self.testimg2= ImageTk.PhotoImage(denoised_img)
        gird_img.create_image(40, 40, image=self.testimg2)

        # Calculate the correlation between the two signals.
        print "Dot product %s is: %s" % (onefile,
                                    np.sum(np.nan_to_num(camera_noise * image_noise)) /
                                        (camera_noise_norm * image_noise_norm))
        cor_v = np.sum(np.nan_to_num(camera_noise * image_noise)) / (camera_noise_norm * image_noise_norm)
        sumf = cor_v 

        print 'sumf : ', sumf
   
       
        #self.sam_aver_v.configure(text='Logitech Differ : '+str(sumf))
        #self.thrd_pic(denoised_matrix2,self.sam_3d)
        self.sam1 = denoised_matrix2
        


    def test_ch3(self, onefile, gird_img, img):
        
        camera_noise = self.result_value
        camera_noise_average = np.average(np.nan_to_num(camera_noise))
        camera_noise -= camera_noise_average
        camera_noise_norm = np.sqrt(np.sum(np.nan_to_num(camera_noise * camera_noise)))


        # Get this image's noise.
        denoised_matrix2, image_noise = mc.get_noise_from_file(onefile)
        image_noise_average = np.average(image_noise)
        image_noise -= image_noise_average
        image_noise_norm = np.sqrt(np.sum(image_noise * image_noise))

        denoised_img = Image.fromarray(denoised_matrix2)
        self.testimg3= ImageTk.PhotoImage(denoised_img)
        gird_img.create_image(40, 40, image=self.testimg3)

        # Calculate the correlation between the two signals.
        print "Dot product %s is: %s" % (onefile,
                                    np.sum(np.nan_to_num(camera_noise * image_noise)) /
                                        (camera_noise_norm * image_noise_norm))
        cor_v = np.sum(np.nan_to_num(camera_noise * image_noise)) / (camera_noise_norm * image_noise_norm)
        sumf = cor_v 

        print 'sumf : ', sumf
   
       
        #self.xio_aver_v.configure(text='Logitech Differ : '+str(sumf))
        #self.thrd_pic(denoised_matrix2,self.xiao_3d)
        self.xio1 = denoised_matrix2


    def thrd_pic(self, matrix, canvas):
        fig = plt.figure(figsize=(2,1.5))
        self.canvasfig.get_tk_widget().destroy()
        #canvas.delete(self.canvasfig)

        np_ma = np.array(matrix)
        x = np.arange(0, np_ma.shape[0], 1)             # points in the x axis
        y = np.arange(0, np_ma.shape[1], 1)              # points in the y axis
        X, Y = np.meshgrid(y, x)                # create the "base grid"
        R = np.sqrt(X**2 + Y**2)
        Z = np_ma                 # points in the z axis
        
        #fig = plt.figure()
        ax = Axes3D(fig) 

        surf = ax.plot_surface(X, Y, Z,           # data values (2D Arryas)
                            rstride=2,                    # row step size
                            cstride=2,                   # column step size
                            cmap=matplotlib.cm.get_cmap("RdPu"),        # colour map
                            linewidth=1,                # wireframe line width
                            antialiased=True)
        

        #ax.set_title('')        # title
        ax.set_xlabel('x label')                             # x label
        ax.set_ylabel('y label')                             # y label
        ax.set_zlabel('z label')                             # z label
        fig.colorbar(surf, shrink=0.5, aspect=5)   # colour bar
        plt.figure(figsize=(20,10))

        
        self.canvasfig = FigureCanvasTkAgg(fig, master=canvas)
        self.canvasfig.get_tk_widget().pack(side='top', fill='both')
        #canvasfig.get_tk_widget().destroy()

    def thrd_pic2(self, matrix, canvas):
        fig = plt.figure(figsize=(2,1.5))
        self.canvasfig2.get_tk_widget().destroy()
        #canvas.delete(self.canvasfig)

        np_ma = np.array(matrix)
        x = np.arange(0, np_ma.shape[0], 1)             # points in the x axis
        y = np.arange(0, np_ma.shape[1], 1)              # points in the y axis
        X, Y = np.meshgrid(y, x)                # create the "base grid"
        R = np.sqrt(X**2 + Y**2)
        Z = np_ma                 # points in the z axis
        
        #fig = plt.figure()
        ax = Axes3D(fig) 

        surf = ax.plot_surface(X, Y, Z,           # data values (2D Arryas)
                            rstride=2,                    # row step size
                            cstride=2,                   # column step size
                            cmap=matplotlib.cm.get_cmap("RdPu"),        # colour map
                            linewidth=1,                # wireframe line width
                            antialiased=True)
        

        #ax.set_title('')        # title
        ax.set_xlabel('x label')                             # x label
        ax.set_ylabel('y label')                             # y label
        ax.set_zlabel('z label')                             # z label
        fig.colorbar(surf, shrink=0.5, aspect=5)   # colour bar
        plt.figure(figsize=(20,10))

        
        self.canvasfig2 = FigureCanvasTkAgg(fig, master=canvas)
        self.canvasfig2.get_tk_widget().pack(side='top', fill='both')
        #canvasfig.get_tk_widget().destroy()

    def thrd_pic3(self, matrix, canvas):
        fig = plt.figure(figsize=(2,1.5))
        self.canvasfig3.get_tk_widget().destroy()
        #canvas.delete(self.canvasfig)

        np_ma = np.array(matrix)
        x = np.arange(0, np_ma.shape[0], 1)             # points in the x axis
        y = np.arange(0, np_ma.shape[1], 1)              # points in the y axis
        X, Y = np.meshgrid(y, x)                # create the "base grid"
        R = np.sqrt(X**2 + Y**2)
        Z = np_ma                 # points in the z axis
        
        #fig = plt.figure()
        ax = Axes3D(fig) 

        surf = ax.plot_surface(X, Y, Z,           # data values (2D Arryas)
                            rstride=2,                    # row step size
                            cstride=2,                   # column step size
                            cmap=matplotlib.cm.get_cmap("RdPu"),        # colour map
                            linewidth=1,                # wireframe line width
                            antialiased=True)
        

        #ax.set_title('')        # title
        ax.set_xlabel('x label')                             # x label
        ax.set_ylabel('y label')                             # y label
        ax.set_zlabel('z label')                             # z label
        fig.colorbar(surf, shrink=0.5, aspect=5)   # colour bar
        plt.figure(figsize=(20,10))

        
        self.canvasfig3 = FigureCanvasTkAgg(fig, master=canvas)
        self.canvasfig3.get_tk_widget().pack(side='top', fill='both')
        #canvasfig.get_tk_widget().destroy()

    def thrd_pic4(self, matrix, canvas):
        fig = plt.figure(figsize=(2,1.5))
        self.canvasfig4.get_tk_widget().destroy()
        #canvas.delete(self.canvasfig)

        np_ma = np.array(matrix)
        x = np.arange(0, np_ma.shape[0], 1)             # points in the x axis
        y = np.arange(0, np_ma.shape[1], 1)              # points in the y axis
        X, Y = np.meshgrid(y, x)                # create the "base grid"
        R = np.sqrt(X**2 + Y**2)
        Z = np_ma                 # points in the z axis
        
        #fig = plt.figure()
        ax = Axes3D(fig) 

        surf = ax.plot_surface(X, Y, Z,           # data values (2D Arryas)
                            rstride=2,                    # row step size
                            cstride=2,                   # column step size
                            cmap=matplotlib.cm.get_cmap("RdPu"),        # colour map
                            linewidth=1,                # wireframe line width
                            antialiased=True)
        

        #ax.set_title('')        # title
        ax.set_xlabel('x label')                             # x label
        ax.set_ylabel('y label')                             # y label
        ax.set_zlabel('z label')                             # z label
        fig.colorbar(surf, shrink=0.5, aspect=5)   # colour bar
        plt.figure(figsize=(20,10))

        
        self.canvasfig4 = FigureCanvasTkAgg(fig, master=canvas)
        self.canvasfig4.get_tk_widget().pack(side='top', fill='both')
        #canvasfig.get_tk_widget().destroy()


  

def main():  
    mainWindow = Tk()  
    mainWindow.geometry("1600x700+300+300") # 메인 윈도우의 창크기와 위치  
    app = mainUI(mainWindow)  
    mainWindow.mainloop()  
  
if __name__ == "__main__":  
    main()  


