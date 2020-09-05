# import Libraries
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from tkinter import *

# defining the main window
window = Tk()
window.title("JustDial Scrapper")

#lbl = Label(window, text="JustDial Scrapper",fg="green", font=("Times New Roman", 22, 'bold')).pack()

# defining first frame for version selection
frame_1 = Frame(window).pack()
ver = StringVar()
ver.set("null")
Radiobutton(frame_1, text="UAE", variable=ver, value="UAE").pack()
Radiobutton(frame_1, text="USA", variable=ver, value="USA").pack()
Radiobutton(frame_1, text="India", variable=ver, value="India").pack()
Radiobutton(frame_1, text="Canada", variable=ver, value="Canada").pack()

# adding dropdown options from the text file
cat = []
with open('cat.txt', 'r') as f:
    while len(f.readline()) > 0:
        cat.append(f.readline()[0:-1])

print(cat)

lbl = Label(window, text="Choose from following",fg="green", font=("Times New Roman", 14, 'bold')).pack()
category_selected = StringVar()
category_selected.set("Choose a category")

drop = OptionMenu(window, category_selected, *cat ).pack()



window.mainloop()