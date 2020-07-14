import Tkinter as tk
import Tkconstants, tkFileDialog
import ttk


import make_characteristic as mc
import numpy as np
import cPickle
import glob
import math
import sys
from PIL import ImageTk, Image






def click_me(): 
    action.configure(text='Hello ')
    folder = tkFileDialog.askdirectory()
    print "Selected Folder:", folder
    #make_ch(folder)


def make_ch(folder):
    # Get a list of images to process.
    file_list = glob.glob(folder + '/*.jpg')
    print "Processing %d images" % (len(file_list),)

    # Denoise and build the numerator/denominator.
    numerator = None
    denominator = None
    for i, f in enumerate(file_list):
        print "Processing %03d %s" % (i, f,) 
        (denoised_matrix, residual_matrix) = mc.get_noise_from_file(f)
        if numerator is None:
            numerator = np.zeros_like(residual_matrix)
            denominator = np.zeros_like(residual_matrix)
        numerator += denoised_matrix * residual_matrix        #residual_matrix = original - denoised_matrix
        denominator += denoised_matrix * denoised_matrix
    return numerator / denominator

    



root = tk.Tk()
root.title("Camera Pattern Noise")
root.geometry("700x700")
root.resizable(True, True)


a_label = ttk.Label(root, text="A Label")
a_label.grid(column=0, row=0)   

# Adding a Button
action = ttk.Button(root, text="Click Me!", command=click_me)   
action.grid(column=1, row=0)                                 # <= change column to 1    

image_path = "image1.jpg"
img=ImageTk.PhotoImage(Image.open(image_path))

canvas = tk.Canvas(root, width=500, height=500)
canvas.grid(column=0, row=1, columnspan=2, rowspan=2)
#canvas.imageList = []
#canvas.create_rectangle(80, 80, 120, 120, fill="blue")
#canvas.pack()
canvas.create_image(80, 80, image=img)
#canvas.imageList.append(img)

#img=tk.PhotoImage(Image.open("image1.png"))


#label=tk.Label(root, image=image)
#label.pack(side = "bottom", fill = "both", expand = "yes")
#label.pack()


# Adding a Button
action = ttk.Button(root, text="Click Me!", command=click_me)   
action.grid(column=2, row=0)  

#======================
# Start GUI
#======================
root.mainloop()