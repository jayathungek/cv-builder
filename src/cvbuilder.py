#!/usr/bin/env python3
import os
import json
import tkinter as tk 
from pathlib import Path
from tkinter import filedialog
from PIL import ImageTk,Image

class CVBuilderWindow():
	def __init__(self):
		self.BLANK_IMAGE_PATH = "../img/blank_image.png" 
		self.OVERLAY_PATH = "../img/overlay.png" 
		self.IMAGE = None 
		self.OVERLAY = None
		self.BLANK_IMAGE = None
		self.CV_IMAGE_SET = False 
		self.CV_IMAGE_PATH = ""
		self.WIN = tk.Tk()
		self.IMG_AREA =None
		self.OVERLAY_AREA = None
		self.IMAGE_CANVAS = None
		self.MOUSE_IN_CANVAS = False
		self.OUTPUT_JSON_PATH = "./parameters.json"

	def strip_filename(self, filename):
		i = filename.index(".")
		print(i)
		return filename[:i] 

	def header_layout(self):
		header_frame = tk.Frame(self.WIN)
		header_frame.grid(row=0, column=0)

		header_frame_left = tk.Frame(header_frame)
		header_frame_left.pack(side=tk.LEFT)

		header_frame_right = tk.Frame(header_frame)
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

		self.IMAGE_CANVAS = tk.Canvas(header_frame_right, width = 75, height = 100)
		self.IMAGE = self.get_image(self.BLANK_IMAGE_PATH)
		self.BLANK_IMAGE = self.get_image(self.BLANK_IMAGE_PATH)
		self.IMG_AREA = self.IMAGE_CANVAS.create_image(0, 0, anchor=tk.NW, image=self.IMAGE)
		self.OVERLAY = self.get_image(self.OVERLAY_PATH)
		self.IMAGE_CANVAS.bind("<Button-1>", self.canvas_clicked)
		self.IMAGE_CANVAS.bind("<Enter>", self.canvas_enter)
		self.IMAGE_CANVAS.bind("<Leave>", self.canvas_leave)
		self.IMAGE_CANVAS.pack() 

		#############################################################################################################
		experience_frame = tk.Frame(self.WIN)
		experience_frame.grid(row=1, column=0)

		work_exp_label = tk.Label(experience_frame, text="Work experience: ").grid(row=0, column=0) 
		work_exp_button = tk.Button(experience_frame, text="Load from file")
		work_exp_button.grid(row=0, column=1) 

		education_label = tk.Label(experience_frame, text="Education: ").grid(row=1, column=0) 
		education_button = tk.Button(experience_frame, text="Load from file")
		education_button.grid(row=1, column=1)

		projects_label = tk.Label(experience_frame, text="Projects: ").grid(row=2, column=0) 
		projects_button = tk.Button(experience_frame, text="Load from file")
		projects_button.grid(row=2, column=1)

		##############################################################################################################
		submit_frame = tk.Frame(self.WIN)
		submit_frame.grid(row=2, column=0)

		compile_button = tk.Button(submit_frame, text="Compile")
		compile_button.pack(side=tk.LEFT)
		compile_button.configure(command=self.make_cv)

	def run(self):
		self.WIN.title("CV builder")
		self.header_layout()  
		self.WIN.mainloop()

	def get_image(self, path):
		img_int = Image.open(path)
		img_int = img_int.resize((75, 100), Image.ANTIALIAS)
		image_final = ImageTk.PhotoImage(img_int)
		return image_final


	def save_json(self):
		parameters = {}
		parameters['cv_image'] = self.get_cv_image_path()
		with open(self.OUTPUT_JSON_PATH, 'w') as outfile:
			json.dump(parameters, outfile)

	def compile_latex(self):
		print("Compiling...")
		os.system("rm ../out/*")
		os.system("lualatex cv.tex")
		os.system("lualatex cv.tex")
		os.system("mv *.aux *.log ../aux")
		os.system("mv *.pdf ../out")
		print("Done.")

	def clean(self):
		print("Cleaning temp files...")
		os.system("rm ../aux/*")
		print("Done")

	def make_dirs(self):
		print("Making directories...")
		auxdir = Path("../aux")
		outdir = Path("../out")

		if not auxdir.is_dir():
			os.system("mkdir ../aux")

		if not outdir.is_dir():
			os.system("mkdir ../out")

		print("Done.")



	def make_cv(self):
		self.save_json()
		self.make_dirs()
		self.compile_latex()
		self.clean()

	def canvas_clicked(self, event): 
		print ("clicked at", event.x, event.y)
		if not self.CV_IMAGE_SET:
			filename =  filedialog.askopenfilename(initialdir = "/home/kavi/Pictures",
				                                   title = "Select file",
				                                   filetypes = (("jpeg files","*.jpg"),("png files","*.png")))
			print("File chosen: ", filename)
			self.IMAGE = self.get_image(filename)
			self.CV_IMAGE_PATH = self.strip_filename(filename)
			self.CV_IMAGE_SET = True
			self.IMAGE_CANVAS.itemconfig(self.IMG_AREA, image = self.IMAGE)
		else:
			if event.x > 60 and event.y < 15:
				self.CV_IMAGE_SET = False
				self.CV_IMAGE_PATH = ""
				self.IMAGE_CANVAS.itemconfig(self.IMG_AREA, image = self.BLANK_IMAGE)
				self.IMAGE_CANVAS.delete(self.OVERLAY_AREA)


	def canvas_enter(self, event):
		if self.CV_IMAGE_SET:
			self.OVERLAY_AREA = self.IMAGE_CANVAS.create_image(0, 0, anchor=tk.NW, image=self.OVERLAY)

	def canvas_leave(self, event):
		if self.CV_IMAGE_SET:
			self.IMAGE_CANVAS.delete(self.OVERLAY_AREA)

	def get_cv_image_path(self):
		if self.CV_IMAGE_SET:
			return self.CV_IMAGE_PATH
		else:
			return "none"


cvb = CVBuilderWindow()
cvb.run()