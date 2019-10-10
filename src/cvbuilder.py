#!/usr/bin/env python3
from tkinter import * 
import os

def compile_latex():
    print("Compiling...")
    os.system("pdflatex ../latex/cv.tex")
    os.system("mv *.aux *.log ../latex/aux")
    os.system("mv *.pdf ../latex/out")
    print("Done.")


win = Tk()

compile_button = Button(win, text="Compile")
compile_button.pack(side=LEFT, padx=10, pady=10)
compile_button.configure(command=compile_latex)

win.mainloop()