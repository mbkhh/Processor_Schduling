import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from _func import *
from page1 import *
import sys


class PageTwo(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        ttk.Button(self, text="Back to Plot Page", command=lambda: master.show_page(PageOne)).grid(row=0, column=0, pady=10)

        self.bottom_label = ttk.Label(self, font=("Arial", 18), foreground="black",
                                      text="Scheduling Program\n", justify="left")
        self.bottom_label.grid(row=1, column=0,  padx=(0, 0), sticky="ew")

        self.bottom_label2 = ttk.Label(self,font=("Arial", 14), foreground="black", text="""Plot Interpreting note:\n\t
        1-Each task arrival is marked with vertical black line on top of center line of time line.\n\t
        2-Dead lines of each task is marked with a vertical red line under center line of timeline (for rm because dead line are arrival time of task deadlines are not shown).\n\t
        3-If task completed before deadline it color will be green otherwise will be yellow.\n\t
        4-In plot task are shown with same order of input and NOT their priority.\n\t
        5-Aperiodic Server color is red.\n """, justify="left")
        self.bottom_label2.grid( column=0,  padx=(0, 0), sticky="ew")

        self.bottom_label2 = ttk.Label(self,font=("Arial", 14), foreground="black", text="""Other note:\n\t
        1-Exact analysis are shown on bottom of the page for three different priority order.\n\t
        2-Exact analysis will not consider Aperiodic tasks.\n\t
        5-Aperiodic Server color is red. """, justify="left")
        self.bottom_label2.grid( column=0,  padx=(0, 0), sticky="ew")

    def load_data(self):
        for i, row in enumerate(self.data):
            self.tree.insert("", "end", iid=i, values=row)

    def delete_selected(self):
        selected = self.tree.selection()
        for sel in selected:
            self.tree.delete(sel)