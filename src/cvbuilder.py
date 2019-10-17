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
		self.WIN = tk.Tk()
		self.IMG_AREA =None
		self.OVERLAY_AREA = None
		self.IMAGE_CANVAS = None
		self.MOUSE_IN_CANVAS = False
		self.OUTPUT_JSON_PATH = "../parameters.json"
		self.FILEPICKER_INITIAL_DIR = "/home/kavi/Desktop/misc/cv-builder"

		self.CV_IMAGE_PATH = ""
		self.CV_IMAGE_EXT = ""
		self.CV_NAME = tk.StringVar()
		self.CV_EMAIL = tk.StringVar()
		self.CV_GITHUB = tk.StringVar()
		self.CV_PHONE = tk.StringVar()
		self.CV_LOCATION_CITY = tk.StringVar()
		self.CV_LOCATION_COUNTRY = tk.StringVar()

	def strip_filename(self, filename):
		i = filename.index(".")
		print(i)
		return (filename[:i], filename[i:]) 

	def layout(self):
		header_frame = tk.Frame(self.WIN)
		header_frame.grid(row=0, column=0)

		header_frame_left = tk.Frame(header_frame)
		header_frame_left.pack(side=tk.LEFT)

		header_frame_right = tk.Frame(header_frame)
		header_frame_right.pack(side=tk.RIGHT)

		name_label = tk.Label(header_frame_left, text="Name: ").grid(row=0, column=0) 
		name_entry = tk.Entry(header_frame_left, textvariable=self.CV_NAME)
		name_entry.grid(row=0, column=1)

		github_label = tk.Label(header_frame_left, text="Github username: ").grid(row=1, column=0) 
		github_entry = tk.Entry(header_frame_left, textvariable=self.CV_GITHUB) 
		github_entry.grid(row=1, column=1)

		phone_label = tk.Label(header_frame_left, text="Phone: ").grid(row=2, column=0) 
		phone_entry = tk.Entry(header_frame_left, textvariable=self.CV_PHONE) 
		phone_entry.grid(row=2, column=1)

		location_city_label = tk.Label(header_frame_left, text="Location (city): ").grid(row=3, column=0) 
		location_city_entry = tk.Entry(header_frame_left, textvariable=self.CV_LOCATION_CITY) 
		location_city_entry.grid(row=3, column=1)

		location_country_label = tk.Label(header_frame_left, text="Location: (country)").grid(row=4, column=0) 
		location_country_entry = tk.Entry(header_frame_left, textvariable=self.CV_LOCATION_COUNTRY) 
		location_country_entry.grid(row=4, column=1)

		email_label = tk.Label(header_frame_left, text="Email: ").grid(row=5, column=0) 
		email_entry = tk.Entry(header_frame_left, textvariable=self.CV_EMAIL) 
		email_entry.grid(row=5, column=1)

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

		submit_buttons_frame = tk.Frame(submit_frame)
		submit_buttons_frame.pack(side=tk.BOTTOM)

		compile_button = tk.Button(submit_buttons_frame, text="Compile")
		compile_button.grid(row=0, column=0) 
		compile_button.configure(command=self.make_cv)

		save_button = tk.Button(submit_buttons_frame, text="Save As")
		save_button.grid(row=0, column=1) 
		save_button.configure(command=self.save_file)

		load_button = tk.Button(submit_buttons_frame, text="Load")
		load_button.grid(row=0, column=2) 
		load_button.configure(command=self.load_file)


	def run(self):
		self.WIN.title("CV builder")
		self.layout()  
		self.WIN.mainloop()

	def get_image(self, path):
		img_int = Image.open(path)
		img_int = img_int.resize((75, 100), Image.ANTIALIAS)
		image_final = ImageTk.PhotoImage(img_int)
		return image_final


	def save_json(self, out):
		parameters = {}
		parameters['cv_image'] = self.get_cv_image_path()
		parameters['cv_image_ext'] = self.get_cv_image_ext()
		parameters['name'] = self.CV_NAME.get()
		parameters['email'] = self.CV_EMAIL.get()
		parameters['github'] = self.CV_GITHUB.get()
		parameters['phone'] = self.CV_PHONE.get()
		parameters['location_city'] = self.CV_LOCATION_CITY.get()
		parameters['location_country'] = self.CV_LOCATION_COUNTRY.get()
		with open(out, 'w') as outfile:
			json.dump(parameters, outfile)

	def compile_latex(self):
		print("Compiling...")
		os.system("rm ../latex/out/*")
		os.system("lualatex ../latex/cv.tex")
		os.system("lualatex ../latex/cv.tex")
		os.system("mv *.aux *.log ../latex/aux")
		os.system("mv *.pdf ../latex/out")
		print("Done.")

	def clean(self):
		print("Cleaning temp files...")
		os.system("rm ../latex/aux/*")
		print("Done")

	def make_dirs(self):
		print("Making directories...")
		auxdir = Path("../latex/aux")
		outdir = Path("../latex/out")

		if not auxdir.is_dir():
			os.system("mkdir ../latex/aux")

		if not outdir.is_dir():
			os.system("mkdir ../latex/out")

		print("Done.")

	def make_cv(self):
		self.save_json(self.OUTPUT_JSON_PATH)
		self.make_dirs()
		self.compile_latex()
		self.clean()

	def save_file(self):
		filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("json files", "*.json")])
		if filename:
			self.save_json(filename)


	def load_file(self):
		filename =  filedialog.askopenfilename(initialdir = self.FILEPICKER_INITIAL_DIR,
				                                   title = "Select JSON file",
				                                   filetypes = [("json files","*.json")] )		
		parameters = {}
		with open(filename, 'r') as f:
			parameters = json.load(f)
			f.close()

		print("setting CV name text field to " + parameters["name"])
		self.CV_NAME.set(parameters["name"])
		self.CV_PHONE.set(parameters["phone"])
		self.CV_EMAIL.set(parameters["email"])
		self.CV_GITHUB.set(parameters["github"])
		self.CV_LOCATION_CITY.set(parameters["location_city"])
		self.CV_LOCATION_COUNTRY.set(parameters["location_country"])

		image_path = parameters["cv_image"]
		image_ext = parameters["cv_image_ext"]
		if image_path != "none": 
			self.IMAGE = self.get_image(image_path+image_ext)
			self.CV_IMAGE_PATH = image_path
			self.CV_IMAGE_EXT = image_ext
			self.CV_IMAGE_SET = True
			self.IMAGE_CANVAS.itemconfig(self.IMG_AREA, image = self.IMAGE)
		else:
			self.CV_IMAGE_SET = False
			self.CV_IMAGE_PATH = ""
			self.CV_IMAGE_EXT = ""
			self.IMAGE_CANVAS.itemconfig(self.IMG_AREA, image = self.BLANK_IMAGE)
			self.IMAGE_CANVAS.delete(self.OVERLAY_AREA)
		


	def canvas_clicked(self, event): 
		print ("clicked at", event.x, event.y)
		if not self.CV_IMAGE_SET:
			filename =  filedialog.askopenfilename(initialdir = self.FILEPICKER_INITIAL_DIR,
				                                   title = "Select CV image",
				                                   filetypes = ( ("jpeg files","*.jpg"),("png files","*.png")) )
			print("File chosen: ", filename)

			image = self.strip_filename(filename)
			image_path = image[0]
			image_ext = image[1]

			self.IMAGE = self.get_image(filename)
			self.CV_IMAGE_PATH = image_path
			self.CV_IMAGE_EXT = image_ext
			self.CV_IMAGE_SET = True
			self.IMAGE_CANVAS.itemconfig(self.IMG_AREA, image = self.IMAGE)
		else:
			if event.x > 60 and event.y < 15:
				self.CV_IMAGE_SET = False
				self.CV_IMAGE_PATH = ""
				self.CV_IMAGE_EXT = ""
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

	def get_cv_image_ext(self):
		if self.CV_IMAGE_SET:
			return self.CV_IMAGE_EXT
		else:
			return ""


cvb = CVBuilderWindow()
cvb.run()