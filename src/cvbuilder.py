#!/usr/bin/env python3
import os
import tkinter as tk 
from PIL import ImageTk,Image

BLANK_IMAGE_PATH = "../img/blank_image.png"
CV_IMAGE_PATH = ""

def header_layout(win, img):
	header_frame_left = tk.Frame(win)
	header_frame_left.pack(side=tk.LEFT)

	header_frame_right = tk.Frame(win)
	header_frame_right.pack(side=tk.RIGHT)

	name_label = tk.Label(header_frame_left, text="Name: ").grid(row=0, column=0)
	name_entry_text = tk.StringVar()
	name_entry = tk.Entry(header_frame_left, textvariable=name_entry_text)
	name_entry.grid(row=0, column=1)

	github_label = tk.Label(header_frame_left, text="Github: ").grid(row=1, column=0)
	github_entry_text = tk.StringVar()
	github_entry = tk.Entry(header_frame_left, textvariable=github_entry_text) 
	github_entry.grid(row=1, column=1)

	phone_label = tk.Label(header_frame_left, text="Phone: ").grid(row=2, column=0)
	phone_entry_text = tk.StringVar()
	phone_entry = tk.Entry(header_frame_left, textvariable=phone_entry_text) 
	phone_entry.grid(row=2, column=1)

	location_label = tk.Label(header_frame_left, text="Location: ").grid(row=3, column=0)
	location_entry_text = tk.StringVar()
	location_entry = tk.Entry(header_frame_left, textvariable=location_entry_text) 
	location_entry.grid(row=3, column=1)

	image_canvas = tk.Canvas(header_frame_right, width = 150, height = 200)
	image_canvas.create_image(0, 0, anchor=tk.NW, image=img)
	image_canvas.pack() 

def experience_layout(win):
	experience_frame = tk.Frame(win)
	experience_frame.pack()

	work_exp_label = tk.Label(experience_frame, text="Work experience: ").grid(row=0, column=0) 
	work_exp_button = tk.Button(experience_frame, text="Load from file")
	work_exp_button.grid(row=0, column=1) 


def compile_latex():
    print("Compiling...")
    os.system("pdflatex ../latex/cv.tex")
    os.system("mv *.aux *.log ../latex/aux")
    os.system("mv *.pdf ../latex/out")
    print("Done.")

def get_image(path):
	img_int = Image.open(path)
	img_int = img_int.resize((150, 200), Image.ANTIALIAS)
	image_final = ImageTk.PhotoImage(img_int)
	return image_final

def make_window():
	win = tk.Tk()
	blank_image = get_image(BLANK_IMAGE_PATH)
	header_layout(win, blank_image) 
	# experience_layout(win)

	win.mainloop()

make_window()
# compile_button = Button(win, text="Compile")
# compile_button.pack(side=LEFT, padx=10, pady=10)
# compile_button.configure(command=compile_latex)

