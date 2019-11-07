#!/usr/bin/env python3
import os
import json
import tkinter as tk 
from pathlib import Path
from tkinter import filedialog
from PIL import ImageTk,Image

class ChecklistNameWindow(object):
	def __init__(self,master):
		top = self.top = tk.Toplevel(master)
		self.FAVICON_PATH = "../img/cvfavicon.ico"

		favicon = ImageTk.PhotoImage(Image.open(self.FAVICON_PATH))
		top.tk.call('wm', 'iconphoto', top._w, favicon)
		self.l = tk.Label(top,text="Enter checklist name:")
		self.l.pack()
		self.e = tk.Entry(top)
		self.e.pack()
		self.b = tk.Button(top,text='Ok',command=self.cleanup)
		self.b.pack()

		self.e.bind('<Control-a>', self.callback)
		# self.e.bind('<Control-c>', self.callback)
		# self.e.bind('<Control-x>', self.callback)
		# self.e.bind('<Control-v>', self.callback)


	def callback(self, event):
		if event.keysym == "a":
			self.top.after(50, self.select_all, event.widget)
		# elif event.keysym == "c":
		# 	self.top.after(50, self.select_all, event.widget)
		# elif event.keysym == "v":
		# 	self.top.after(50, self.select_all, event.widget)
		# elif event.keysym == "x":
		# 	self.top.after(50, self.select_all, event.widget)

	def select_all(self, widget):
		widget.select_range(0, 'end')
		widget.icursor('end')

	def cleanup(self):
		try:
			self.value=self.e.get()
			if self.value == "":
				raise Exception("Checklist name cannot be empty")
			self.top.destroy()
		except:
			pass 

class CVBuilderWindow():
	def __init__(self):
		self.BLANK_IMAGE_PATH = "../img/blank_image.png" 
		self.OVERLAY_PATH = "../img/overlay.png"
		self.FAVICON_PATH = "../img/cvfavicon.ico"
		self.IMAGE = None 
		self.OVERLAY = None
		self.BLANK_IMAGE = None
		self.CV_IMAGE_SET = False 
		self.WIN = tk.Tk()
		self.IMG_AREA =None
		self.OVERLAY_AREA = None
		self.IMAGE_CANVAS = None
		self.MOUSE_IN_CANVAS = False
		self.OUTPUT_JSON_PATH = "../latex/aux/temp.json"
		self.FILEPICKER_INITIAL_DIR = "./"
		self.CHECKLIST_SECTION_FRAME = None
		self.ADD_CHECKLIST_BUTTON = None

		self.CV_IMAGE_PATH = ""
		self.CV_IMAGE_EXT = ""
		self.CV_NAME = tk.StringVar()
		self.CV_EMAIL = tk.StringVar()
		self.CV_GITHUB = tk.StringVar()
		self.CV_PHONE = tk.StringVar()
		self.CV_LOCATION_CITY = tk.StringVar()
		self.CV_LOCATION_COUNTRY = tk.StringVar()
		self.TOGGLE_ELEMENTS = []


	def callback(self, event):
		if event.keysym == "a":
			# after releasing keys <Control-a> selection is 
			# removed so I use after() to execute selection after 50ms. 
			# It selects all text (but it moves cursor to the beginning) 
			# and moves cursor to the end.
			self.WIN.after(50, self.select_all, event.widget)
		# elif event.keysym == "c":
		# 	self.top.after(50, self.select_all, event.widget)
		# elif event.keysym == "v":
		# 	self.top.after(50, self.select_all, event.widget)
		# elif event.keysym == "x":
		# 	self.top.after(50, self.select_all, event.widget)

	def select_all(self, widget):
		widget.select_range(0, 'end')
		widget.icursor('end')

	def strip_filename(self, filename):
		i = filename.index(".")
		print(i)
		return (filename[:i], filename[i:])

	def param_list_to_rawtext(self, param_list):
		rawtext = ""
		for index, item in enumerate(param_list):
			if index != len(param_list)-1:
				rawtext += item[0] + ","
			else:
				rawtext += item[0]
		return rawtext

	def log(self, message="default message"):
		print ("LOG: ", message)

	def get_toggle_element_state(self, name):
		for element in self.TOGGLE_ELEMENTS:
			if element["name"] == name:
				return element

		return None
	
	def set_toggle_element_state(self, name, state):
		for element in self.TOGGLE_ELEMENTS:
			if element["name"] == name:
				element = state 

	def get_toggle_elements_serialisable(self):
		elements = []
		for element in self.TOGGLE_ELEMENTS:
			sub_element_name = element["name"] 
			sub_element_items = element["items"] 

			counter = 0
			for child in element["itemcontainer"].winfo_children():
				checkbox_value = child.val.get()
				sub_element_items[counter][1] = checkbox_value
				counter += 1

			e = [sub_element_name, sub_element_items]
			elements.append(e)
		return elements

	def toggle_widget(self, checklist_type):
		widget_state = self.get_toggle_element_state(checklist_type)
		currently_visible = widget_state["visible"]
		widgets = widget_state["widgets"]
		rawtext = widget_state["rawtext"].get()
		checkbox_widget = widget_state["itemcontainer"]


		if currently_visible == 0:
			widgets[0].grid_remove()
			widgets[1].grid() 
			
			widget_state["visible"] = 1
			new_items_text = []
			if len(rawtext) > 0:
				new_items_text = rawtext.split(",") 


			new_widget_state_items = []
			for text in new_items_text:
				is_new_item = True
				for item in widget_state["items"]: 
					if text in item:
						new_widget_state_items.append(item)
						is_new_item = False
						break
				if is_new_item:
					new_item = [text, 0]
					new_widget_state_items.append(new_item)

			widget_state["items"] = new_widget_state_items

			self.set_toggle_element_state(checklist_type, widget_state)

			for child in checkbox_widget.winfo_children():
			    child.destroy()
			
			for item in widget_state["items"]: 
				var = tk.IntVar()
				var.set(item[1])
				c = tk.Checkbutton(checkbox_widget, text=item[0], variable=var)
				c.val = var
				c.pack()
		else:
			widgets[1].grid_remove()
			widgets[0].grid()

			widget_state["visible"] = 0
			self.set_toggle_element_state(checklist_type, widget_state)
			

	def make_separator(self, parent_frame):
		padding = 25
		width = parent_frame.winfo_reqwidth()

		container = tk.Frame(parent_frame)
		padding_top = tk.Frame(container, height=padding)
		padding_top.pack(side=tk.TOP)

		separator = tk.Frame(container, height=1, width=width, bg="black")
		separator.pack()

		padding_bottom = tk.Frame(container, height=padding)
		padding_bottom.pack(side=tk.BOTTOM)

		return container

	def make_checklist_entry(self, parent_frame, checklist_type):
		words = tk.StringVar()
		word_entry_label_text = "Enter " + checklist_type + " separated by ',':"
		checklist_type_text = "Select " + checklist_type + " as needed:"
		currently_visible = 1

		container = tk.Frame(parent_frame)

		word_entry_frame = tk.Frame(container)
		word_entry_frame.grid(row=0, column=0)

		word_entry_label = tk.Label(word_entry_frame, text=word_entry_label_text)
		word_entry_label.grid(row=0, column=0)
		word_entry_label.pack()

		word_entry = tk.Entry(word_entry_frame, textvariable=words, width=50)
		word_entry.bind('<Control-a>', self.callback)
		word_entry.grid(row=1, column=0)
		word_entry.pack()

		word_entry_submit = tk.Button(word_entry_frame, text="Finish")
		word_entry_submit.grid(row=2, column=0)
		word_entry_submit.pack()

#############################################################################################################
		checklist_frame = tk.Frame(container)
		checklist_frame.grid(row=1, column=0)

		checklist_type_label = tk.Label(checklist_frame, text=checklist_type_text)
		checklist_type_label.grid(row=0, column=0)
		checklist_type_label.pack()

		checklist_container_frame = tk.Frame(checklist_frame)
		checklist_container_frame.grid(row=1, column=0)
		checklist_container_frame.pack()

		checklist_submit = tk.Button(checklist_frame, text="Add items")
		checklist_submit.grid(row=2, column=0)
		checklist_submit.pack()

		add_checklist_button = tk.Button(container, text="+")
		add_checklist_button.grid(row=3, column=0, sticky=tk.E)
		add_checklist_button.configure(command=lambda button=add_checklist_button:self.add_new_checklist(button))

		remove_checklist_button = tk.Button(container, text="-")
		remove_checklist_button.grid(row=3, column=0, sticky=tk.W)
		#pass on button context to my function
		remove_checklist_button.configure(command= lambda button=remove_checklist_button, chk_type=checklist_type:self.remove_checklist(button, checklist_type))

#############################################################################################################

		toggle_widget_state = { "name": checklist_type, 
								"visible": currently_visible, 
								"widgets": [word_entry_frame, checklist_frame],
								"rawtext": words,
								"items": [],
								"itemcontainer": checklist_container_frame}
		
		word_entry_submit.configure(command=lambda:self.toggle_widget(checklist_type))
		checklist_submit.configure(command=lambda:self.toggle_widget(checklist_type))
 
		self.TOGGLE_ELEMENTS.append(toggle_widget_state)
		self.toggle_widget(checklist_type)

		return (container, toggle_widget_state)


	def layout(self):
		header_frame = tk.Frame(self.WIN)
		header_frame.grid(row=0, column=0)

		header_frame_left = tk.Frame(header_frame)
		header_frame_left.pack(side=tk.LEFT)

		header_frame_right = tk.Frame(header_frame)
		header_frame_right.pack(side=tk.RIGHT)

		name_label = tk.Label(header_frame_left, text="Name: ").grid(row=0, column=0) 
		name_entry = tk.Entry(header_frame_left, textvariable=self.CV_NAME)
		name_entry.bind('<Control-a>', self.callback)
		name_entry.grid(row=0, column=1)

		github_label = tk.Label(header_frame_left, text="Github username: ").grid(row=1, column=0) 
		github_entry = tk.Entry(header_frame_left, textvariable=self.CV_GITHUB)
		github_entry.bind('<Control-a>', self.callback) 
		github_entry.grid(row=1, column=1)

		phone_label = tk.Label(header_frame_left, text="Phone: ").grid(row=2, column=0) 
		phone_entry = tk.Entry(header_frame_left, textvariable=self.CV_PHONE)
		phone_entry.bind('<Control-a>', self.callback) 
		phone_entry.grid(row=2, column=1)

		location_city_label = tk.Label(header_frame_left, text="Location (city): ").grid(row=3, column=0) 
		location_city_entry = tk.Entry(header_frame_left, textvariable=self.CV_LOCATION_CITY)
		location_city_entry.bind('<Control-a>', self.callback) 
		location_city_entry.grid(row=3, column=1)

		location_country_label = tk.Label(header_frame_left, text="Location: (country)").grid(row=4, column=0) 
		location_country_entry = tk.Entry(header_frame_left, textvariable=self.CV_LOCATION_COUNTRY)
		location_country_entry.bind('<Control-a>', self.callback) 
		location_country_entry.grid(row=4, column=1)

		email_label = tk.Label(header_frame_left, text="Email: ").grid(row=5, column=0) 
		email_entry = tk.Entry(header_frame_left, textvariable=self.CV_EMAIL)
		email_entry.bind('<Control-a>', self.callback) 
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

		header_sep = self.make_separator(self.WIN)
		header_sep.grid(row=1, column=0)

		#############################################################################################################
		experience_frame = tk.Frame(self.WIN)
		experience_frame.grid(row=2, column=0)

		work_exp_label = tk.Label(experience_frame, text="Work experience: ").grid(row=0, column=0) 
		work_exp_button = tk.Button(experience_frame, text="Load from file")
		work_exp_button.grid(row=0, column=1) 

		education_label = tk.Label(experience_frame, text="Education: ").grid(row=1, column=0) 
		education_button = tk.Button(experience_frame, text="Load from file")
		education_button.grid(row=1, column=1)

		projects_label = tk.Label(experience_frame, text="Projects: ").grid(row=2, column=0) 
		projects_button = tk.Button(experience_frame, text="Load from file")
		projects_button.grid(row=2, column=1)

		experience_sep = self.make_separator(self.WIN)
		experience_sep.grid(row=3, column=0)

		##############################################################################################################
		self.CHECKLIST_SECTION_FRAME = tk.Frame(self.WIN)
		self.CHECKLIST_SECTION_FRAME.grid(row=4, column=0)

		self.ADD_CHECKLIST_BUTTON = tk.Button(self.CHECKLIST_SECTION_FRAME, text="Add checklist")
		self.ADD_CHECKLIST_BUTTON.grid(row=0, column=0, sticky=tk.E)
		self.ADD_CHECKLIST_BUTTON.configure(command=lambda button=self.ADD_CHECKLIST_BUTTON:self.add_new_checklist(button))
		if len(self.TOGGLE_ELEMENTS) == 0:
			self.ADD_CHECKLIST_BUTTON.grid()
 

		checklist_sep = self.make_separator(self.WIN)
		checklist_sep.grid(row=5, column=0)

		##############################################################################################################

		submit_frame = tk.Frame(self.WIN)
		submit_frame.grid(row=6, column=0)

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

	def add_new_checklist(self, button):
		self.checklist_popup = ChecklistNameWindow(self.WIN)
		self.WIN.wait_window(self.checklist_popup.top)
		info = button.master.grid_info()
		row = int(info["row"])

		checklist_type = self.checklist_popup.value
		checklist_entry = self.make_checklist_entry(self.CHECKLIST_SECTION_FRAME, checklist_type)
		checklist_container = checklist_entry[0]

		if button.cget('text') == "Add checklist":
			checklist_container.grid(row=1, column=0)
		else:
			self.insert_into_container_at(self.CHECKLIST_SECTION_FRAME, checklist_container, row+1)

		if len(self.TOGGLE_ELEMENTS) > 0:
			self.ADD_CHECKLIST_BUTTON.grid_remove() 
		

		
	def remove_checklist(self, button, chk_type):
		for item in self.TOGGLE_ELEMENTS[:]:
			if item["name"] == chk_type:
				self.TOGGLE_ELEMENTS.remove(item)
		info = button.master.grid_info()
		row = int(info["row"])
		button.master.destroy()

		if len(self.TOGGLE_ELEMENTS) == 0:
			self.ADD_CHECKLIST_BUTTON.grid()

	def insert_into_container_at(self, container, checklist, pos):
		for widget in reversed(container.winfo_children()):
			info = widget.grid_info()
			if type(widget) != type(tk.Button()) and len(info.keys()) > 0: 
				row = int(info["row"])
				if row >= pos:
					widget.grid(row=row+1, column=0) 

		checklist.grid(row=pos, column=0)


	def run(self):
		self.WIN.title("CV builder")
		self.layout() 

		favicon = ImageTk.PhotoImage(Image.open(self.FAVICON_PATH))
		self.WIN.tk.call('wm', 'iconphoto', self.WIN._w, favicon)
		self.WIN.mainloop()

	def get_image(self, path):
		img_int = Image.open(path)
		img_int = img_int.resize((75, 100), Image.ANTIALIAS)
		image_final = ImageTk.PhotoImage(img_int)
		return image_final

	def compile_latex(self):
		print("Compiling...")
		os.system("rm ../latex/out/*")
		os.system("latexmk -lualatex ../latex/cv.tex") 
		os.system("mv *.aux *.log *.fls *.fdb_latexmk ../latex/aux")
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
		self.make_dirs()
		self.save_json(self.OUTPUT_JSON_PATH)
		self.compile_latex()
		self.clean()

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
		parameters['checklists'] = self.get_toggle_elements_serialisable()
		parameters['num_skills'] = len(parameters['checklists'])
		with open(out, 'w') as outfile:
			json.dump(parameters, outfile) 

	def load_file(self):
		filename =  filedialog.askopenfilename(initialdir = self.FILEPICKER_INITIAL_DIR,
				                                   title = "Select JSON file",
				                                   filetypes = [("json files","*.json")] )		
		parameters = {}
		with open(filename, 'r') as f:
			parameters = json.load(f)
			f.close()

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
		
		if parameters["num_skills"] > 0:
			self.ADD_CHECKLIST_BUTTON.grid_remove()
		else:
			self.ADD_CHECKLIST_BUTTON.grid()

		self.TOGGLE_ELEMENTS = []
		for child in self.CHECKLIST_SECTION_FRAME.winfo_children():
			if type(child) != type(tk.Button()):
				child.grid_forget()

		for index, checklist in enumerate(parameters["checklists"]):
			name = checklist[0]
			list_items = checklist[1]
			currently_visible = 1
			rawtext_value = self.param_list_to_rawtext(list_items) 
 
			new_checklist_entry = self.make_checklist_entry(self.CHECKLIST_SECTION_FRAME, name)
			new_checklist_frame =new_checklist_entry[0]
			widget_state = new_checklist_entry[1]

			widget_state["name"] = name
			widget_state["visible"] = currently_visible
			widget_state["rawtext"].set(rawtext_value)
			widget_state["items"] = list_items
  
			new_checklist_frame.grid(row=index+1, column=0) 
 

	def save_file(self):
		filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("json files", "*.json")])
		if filename:
			self.save_json(filename)

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