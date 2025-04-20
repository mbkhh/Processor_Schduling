import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Patch
import webbrowser
from _func import *
import sys

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CPU Scheduling")
        self.geometry("1500x870")

        self.pages = {}
        for Page in (PageOne, PageTwo, PageThree):
            page = Page(self)
            self.pages[Page] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_page(PageOne)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def show_page(self, page_class):
        page = self.pages[page_class]
        page.tkraise()
    def on_closing(self):
        print("Closing app...")
        self.destroy()  
        sys.exit()      

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
        2-Exact analysis will consider Aperiodic tasks as normal periodic task (period is aperiodic server period and lenght is budget).\n\t
        5-Aperiodic Server color is red. """, justify="left")
        self.bottom_label2.grid( column=0,  padx=(0, 0), sticky="ew")

        self.bottom_label3 = ttk.Label(self,font=("Arial", 15), foreground="black", text="Project BY Mohammad Bagher Khandan ", justify="left")
        self.bottom_label3.grid( column=0,  padx=(0, 0), sticky="ew")

        self.link = tk.Label(self, text="GitHub Repository of Project", fg="blue", cursor="hand2", font=("Arial", 13, "underline"))
        self.link.grid( column=0,  padx=(0, 0), sticky="ew")
        self.link.bind("<Button-1>", self.open_link)
    def open_link(self,event):
        webbrowser.open_new("https://github.com/mbkhh/Processor_Schduling")
    def load_data(self):
        for i, row in enumerate(self.data):
            self.tree.insert("", "end", iid=i, values=row)

    def delete_selected(self):
        selected = self.tree.selection()
        for sel in selected:
            self.tree.delete(sel)

class PageThree(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=2, padx=(0,0), pady=(0,0), sticky="nsew")

        table_frame = ttk.Frame(self)
        table_frame.grid(row=0, column=0, sticky="nsew", padx=(30, 0), pady=(20 , 5))
        ttk.Label(table_frame, text="Task Table", font=("Arial", 12, "bold")).pack(anchor="w")

        self.task_table = ttk.Treeview(
            table_frame,
            columns=("Name", "T", "C", "D"),
            show="headings",
            height=3,
            selectmode="browse" 
        )
        for col in ("Name", "T", "C", "D"):
            self.task_table.heading(col, text=col)
            self.task_table.column(col, width=50)
        self.task_table.pack(fill="both", expand=True)

        # Form Frame (below table)
        form = ttk.Frame(self)
        form.grid(row=1, column=0, sticky="n", padx=(30,0), pady=(5, 10))

        # Task Name Input
        ttk.Label(form, text="Task Name:").grid(row=0, column=0, sticky="w")
        self.task_name_input = ttk.Entry(form)
        self.task_name_input.grid(row=0, column=1)

        self.num_inputs = []
        for i, label in enumerate(["Period:", "Job length:", "Deadline:"]):
            ttk.Label(form, text=label).grid(row=i+1, column=0, sticky="w")
            num_input = ttk.Entry(form)
            num_input.grid(row=i+1, column=1)
            self.num_inputs.append(num_input)
        ttk.Separator(form, orient='horizontal').grid(row=4, column=0, columnspan=2, sticky='ew', pady=10)
        ttk.Label(form, text="Number of Processor:").grid(row=5, column=0, sticky="w")
        self.processor_count_input = ttk.Entry(form)
        self.processor_count_input.grid(row=5, column=1)
        self.processor_count_input.insert(0,str(numberOfProcessor))

        self.scheduling_type_input = tk.StringVar(value="EDF")
        ttk.Label(form, text="Algorithm:").grid(row=6, column=0, sticky="w")
        for i, val in enumerate([ "EDF", "P-Fair"]):
            r = ttk.Radiobutton(form, text=val, variable=self.scheduling_type_input, value=val)
            r.grid(row=7+i, column=0, columnspan=2, sticky="w")
        ttk.Label(form, text="Simulation Lenght:").grid(row=9, column=0, sticky="w")
        self.simulation_time = ttk.Entry(form)
        self.simulation_time.grid(row=9, column=1)
        self.simulation_time.insert(0,str(simulationTime))
        ttk.Button(form, text="Submit", command=self.submit_data).grid(row=10, column=0, pady=5)
        ttk.Button(form, text="Help", command=lambda: master.show_page(PageTwo)).grid(row=10, column=1, pady=5)
        ttk.Button(form, text="Single Processor", command=lambda: master.show_page(PageOne)).grid(row=11, column=1, pady=5)
        ttk.Button(form, text="Delete Selected Row", command=self.delete_selected_task).grid(row=11, column=0, columnspan=1, pady=5)

        self.bottom_label = ttk.Label(form,font=("Arial", 13), foreground="blue", text="Utilization: N", justify="left")
        self.bottom_label.grid()
    def submit_data(self, justPlot = False):
        if not justPlot and self.task_name_input.get() != "":
            try:
                numbers = [float(n.get()) for n in self.num_inputs]
                multiTasksName.append(self.task_name_input.get())
                multiTasksPeriod.append(int(numbers[0]))
                multiTasksJob.append(int(numbers[1]))
                multiTasksDeadline.append(int(numbers[2]))
                self.task_table.insert("", "end", values=(self.task_name_input.get(), int(numbers[0]), int(numbers[1]), int(numbers[2])))
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numbers.")
                return
        try:
            numberOfProcessor = int(self.processor_count_input.get())
            simulationTime = int(self.simulation_time.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")
            return
        
        self.examples =[multiTasksPeriod,multiTasksJob,multiTasksDeadline]
        T, C, D = self.examples[0], self.examples[1], self.examples[2]

        utilization = 0
        
        for i in range(len(T)):
            utilization += C[i]/T[i]
        self.bottom_label['text'] =  f"Utilization: {np.round(utilization,2)}"
        
        if(self.scheduling_type_input.get() == 'EDF'):
            self.results = multiProcessor_edf(self.examples,numberOfProcessor, simulationTime) 
        elif(self.scheduling_type_input.get() == 'P-Fair'):
            self.results = multiProcessor_pfair(self.examples,numberOfProcessor, simulationTime) 

        self.title = "Schedule Plot"

        self.plot_schedule(self.examples,self.results,self.title, numberOfProcessor)
        self.task_name_input.delete(0, tk.END)
        for n in self.num_inputs:
            n.delete(0, tk.END)
    def plot_schedule(self, examples, results, title,numberOfProcessor):
        self.ax.clear()
        T, C, D = examples[0], examples[1], examples[2]
        tasks = np.array(results)
        num_tasks, time_slots = tasks.shape

        self.ax.set_xticks(range(time_slots))
        self.ax.set_yticks(range(num_tasks))
        
        self.ax.set_yticklabels([f"{multiTasksName[i]}" for i in range(num_tasks)])
        self.ax.set_xlabel("Real-Time clock")
        self.ax.set_ylabel("Tasks")
        self.ax.set_title(title)
        colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'black', 'white',
                    'gray', 'grey', 'orange', 'purple', 'brown', 'pink', 'lime', 'olive',
                    'navy', 'teal', 'maroon', 'aqua', 'fuchsia', 'gold', 'beige', 'coral']
        
        legend_elements = []
        for i in range(numberOfProcessor):
            legend_elements.append(Patch(facecolor=colors[i+1], edgecolor='black', label="Processor "+str(i)))

        self.ax.legend(handles=legend_elements, loc='upper right')

        for task_idx in range(num_tasks):
            for time in range(time_slots):
                if tasks[task_idx, time] != 0:
                    color = colors[tasks[task_idx, time]] #if missed[time] == 0 else 'orange'
                    self.ax.add_patch(plt.Rectangle((time, task_idx - 0.4), 1, 0.8, color=color))

                if time % T[task_idx] == 0:
                    self.ax.plot([time, time + .1], [task_idx, task_idx - 0.5], color='black', lw=2)
                if time % T[task_idx] == D[task_idx] :
                    self.ax.plot([time, time], [task_idx + 0.5, task_idx], color='red', lw=2)

        self.ax.grid(True, linestyle="--", linewidth=0.5)
        self.ax.set_xticks(np.arange(0, time_slots, 1), minor=False)
        self.ax.set_yticks(np.arange(0, num_tasks, 1), minor=False)
        self.ax.invert_yaxis()

        self.canvas.draw()
    def delete_selected_task(self):
        selected_item = self.task_table.selection()
        if selected_item:
            values = self.task_table.item(selected_item, "values")
            name, T, C, D = values

            T, C, D = int(T), int(C), int(D)

            try:
                idx = multiTasksName.index(name)
                if multiTasksPeriod[idx] == T and multiTasksJob[idx] == C and multiTasksDeadline[idx] == D:
                    del multiTasksName[idx]
                    del multiTasksPeriod[idx]
                    del multiTasksJob[idx]
                    del multiTasksDeadline[idx]
            except ValueError:
                pass  # Not found — just ignore

            self.task_table.delete(selected_item)
            self.submit_data( True)
        else:
            messagebox.showwarning("No selection", "Please select a task to delete.")


        
class PageOne(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title = "Schedule Plot"

        self.examples = []

        # --- Main layout: 2 columns: Left for table + inputs, Right for plot ---
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=2, padx=(0,0), pady=(0,0), sticky="nsew")

        # === Left side: Top = Table, Bottom = Form ===

        # Table Frame
        table_frame = ttk.Frame(self)
        table_frame.grid(row=0, column=0, sticky="nsew", padx=(30, 0), pady=(20 , 5))
        ttk.Label(table_frame, text="Task Table", font=("Arial", 12, "bold")).pack(anchor="w")

        self.task_table = ttk.Treeview(
            table_frame,
            columns=("Name", "T", "C", "D"),
            show="headings",
            height=3,
            selectmode="browse" 
        )
        for col in ("Name", "T", "C", "D"):
            self.task_table.heading(col, text=col)
            self.task_table.column(col, width=50)
        self.task_table.pack(fill="both", expand=True)

        form = ttk.Frame(self)
        form.grid(row=1, column=0, sticky="n", padx=(30,0), pady=(5, 10))

        # Task Name Input
        ttk.Label(form, text="Task Name:").grid(row=0, column=0, sticky="w")
        self.task_name_input = ttk.Entry(form)
        self.task_name_input.grid(row=0, column=1)

        self.num_inputs = []
        for i, label in enumerate(["Period:", "Job length:", "Deadline:"]):
            ttk.Label(form, text=label).grid(row=i+1, column=0, sticky="w")
            num_input = ttk.Entry(form)
            num_input.grid(row=i+1, column=1)
            self.num_inputs.append(num_input)

        ttk.Separator(form, orient='horizontal').grid(row=4, column=0, columnspan=2, sticky='ew', pady=10)

        self.have_aperiodic = tk.BooleanVar()
        chk = ttk.Checkbutton(form, text="Have Aperiodic Server", variable=self.have_aperiodic)
        chk.grid(row=5, column=0, columnspan=2, sticky="w")
        
        ttk.Label(form, text="Aperiodic Period:").grid(row=6, column=0, sticky="w")
        self.aperiodic_period = ttk.Entry(form)
        self.aperiodic_period.insert(0,'0')
        self.aperiodic_period.grid(row=6, column=1)

        ttk.Label(form, text="Aperiodic Budget:").grid(row=7, column=0, sticky="w")
        self.aperiodic_budget = ttk.Entry(form,textvariable="0")
        self.aperiodic_budget.insert(0,'0')
        self.aperiodic_budget.grid(row=7, column=1)

        table_frame2 = ttk.Frame(form)
        table_frame2.grid(row=8, column=0,columnspan=2, sticky="nsew")
        ttk.Label(table_frame2, text="Aperiodic Task Table", font=("Arial", 12, "bold")).pack(anchor="w")

        self.aperiodic_table = ttk.Treeview(
            table_frame2,
            columns=("Arrival", "Lenght"),
            show="headings",
            height=3,
            selectmode="browse" 
        )
        for col in ("Arrival", "Lenght"):
            self.aperiodic_table.heading(col, text=col)
            self.aperiodic_table.column(col, width=50)
        self.aperiodic_table.pack(fill="both", expand=True)

        ttk.Label(form, text="Aperiodic Task Arrival:").grid(row=9, column=0, sticky="w")
        self.aperiodic_task_arrival = ttk.Entry(form)
        self.aperiodic_task_arrival.grid(row=9, column=1)

        ttk.Label(form, text="Aperiodic Task Lenght:").grid(row=10, column=0, sticky="w")
        self.aperiodic_task_lenght = ttk.Entry(form)
        self.aperiodic_task_lenght.grid(row=10, column=1)

        self.aperiodic_server_type = tk.StringVar(value="Dumb")
        ttk.Label(form, text="Aperiodic Server Type:").grid(row=11, column=0, sticky="w")
        for i, val in enumerate(["Dumb", "Smart"]):
            r = ttk.Radiobutton(form, text=val, variable=self.aperiodic_server_type, value=val)
            r.grid(row=12+i, column=0, columnspan=2, sticky="w")

        self.scheduling_type_input = tk.StringVar(value="RMS")
        ttk.Label(form, text="Algorithm:").grid(row=14, column=0, sticky="w")
        for i, val in enumerate(["RMS", "DM", "EDF"]):
            r = ttk.Radiobutton(form, text=val, variable=self.scheduling_type_input, value=val)
            r.grid(row=15+i, column=0, columnspan=2, sticky="w")

        ttk.Label(form, text="Simulation Lenght:").grid(row=18, column=0, sticky="w")
        self.simulation_time = ttk.Entry(form)
        self.simulation_time.grid(row=18, column=1)
        self.simulation_time.insert(0,str(simulationTime))

        ttk.Button(form, text="Submit", command=self.submit_data).grid(row=19, column=0, pady=5)
        ttk.Button(form, text="Help", command=lambda: master.show_page(PageTwo)).grid(row=19, column=1, pady=5)
        ttk.Button(form, text="Multi Processor", command=lambda: master.show_page(PageThree)).grid(row=20, column=1, pady=5)
        ttk.Button(form, text="Delete Selected Row", command=self.delete_selected_task).grid(row=20, column=0, columnspan=1, pady=5)

        self.bottom_label = ttk.Label(form,font=("Arial", 13), foreground="blue", text="Utilization: N \nLiu & Layland Bound: N", justify="left")
        self.bottom_label.grid()

        self.bottom_label2 = ttk.Label(self, font=("Arial", 13), anchor="center",text="Response time of each task based on Period: Response time of each task based on Period:\nResponse time of each task based on Period: Response time of each task based on Period:\nResponse time of each task based on Period: Response time of each task based on Period:")
        self.bottom_label2.grid( column=0, columnspan=3, padx=(0, 0), sticky="ew")  

    def calculateExact(self):
        T, C, D = self.examples[0], self.examples[1], self.examples[2]

        if(self.have_aperiodic.get()):
            T = np.append(T,np.array(int(self.aperiodic_period.get())))
            C = np.append(C,np.array(int(self.aperiodic_budget.get())))
            D = np.append(D,np.array(int(self.aperiodic_period.get())))
            tasksName2 = list(tasksName)
            tasksName2.append('Server')
        else:
            tasksName2 = list(tasksName)
        utilization = 0
        for i in range(len(T)):
            utilization += C[i]/T[i]
        liuLaylandBound = len(T) * (np.power(2,1/len(T)) - 1)

        self.bottom_label['text'] =  f"Utilization: {np.round(utilization,2)} \nLiu & Layland Bound: {np.round(liuLaylandBound,3)}"

        maxIteration = 1000

        ResponseTimePeriod = []
        ResponseFailPeriod = 0
        sortedT = np.argsort(T)
        for i in range(len(T)):
            lastVal = -1
            currentVal = 0
            converged = 0
            for j in range(maxIteration):
                if(currentVal == lastVal):
                    converged = 1
                    ResponseTimePeriod.append(int(currentVal))
                    break
                lastVal = currentVal
                temp = 0
                for p in range(i):
                    temp += np.ceil(lastVal/T[sortedT[p]])*C[sortedT[p]]
                currentVal = temp + C[sortedT[i]]
            if (converged == 0):
                ResponseFailPeriod = 1
                
        if(ResponseFailPeriod):
            Message = 'Exact analysis was not possible for Response time based on period'
        else:
            Message = "Response time of each task based on Period: "+"; ".join("R "+tasksName2[sortedT[i]]+" = "+str(ResponseTimePeriod[sortedT[i]]) for i in range(len(T)))
        
        
        ResponseTimePriority = []
        ResponseFailPriority = 0
        for i in range(len(T)):
            lastVal = -1
            currentVal = 0
            converged = 0
            for j in range(maxIteration):
                if(currentVal == lastVal):
                    converged = 1
                    ResponseTimePriority.append(int(currentVal))
                    break
                lastVal = currentVal
                temp = 0
                for p in range(i):
                    temp += np.ceil(lastVal/T[p])*C[p]
                currentVal = temp + C[i]
            if (converged == 0):
                ResponseFailPriority = 1
        if(ResponseFailPriority):
            Message += '\nExact analysis was not possible for Response time based on Priority'
        else:
            Message += "\nResponse time of each task based on Priority: "+"; ".join("R "+tasksName2[i]+" = "+str(ResponseTimePeriod[i]) for i in range(len(T)))

        ResponseTimeDeadLine = []
        ResponseFailDeadLine = 0
        sortedT = np.argsort(D)
        for i in range(len(T)):
            lastVal = -1
            currentVal = 0
            converged = 0
            for j in range(maxIteration):
                if(currentVal == lastVal):
                    converged = 1
                    ResponseTimeDeadLine.append(int(currentVal))
                    break
                lastVal = currentVal
                temp = 0
                for p in range(i):
                    temp += np.ceil(lastVal/T[sortedT[p]])*C[sortedT[p]]
                currentVal = temp + C[sortedT[i]]
            if (converged == 0):
                ResponseFailDeadLine = 1
        if(ResponseFailDeadLine):
            Message += '\nExact analysis was not possible for Response time based on Deadline'
        else:
            Message += "\nResponse time of each task based on Deadline: "+"; ".join("R "+tasksName2[sortedT[i]]+" = "+str(ResponseTimePeriod[sortedT[i]]) for i in range(len(T)))    
        self.bottom_label2['text'] = Message
        

    def delete_selected_task(self):
        selected_item = self.task_table.selection()
        selected_item2 = self.aperiodic_table.selection()
        if selected_item:
            values = self.task_table.item(selected_item, "values")
            name, T, C, D = values

            T, C, D = int(T), int(C), int(D)

            try:
                idx = tasksName.index(name)
                if tasksPeriod[idx] == T and tasksJob[idx] == C and tasksDeadline[idx] == D:
                    del tasksName[idx]
                    del tasksPeriod[idx]
                    del tasksJob[idx]
                    del tasksDeadline[idx]
            except ValueError:
                pass  # Not found — just ignore

            self.task_table.delete(selected_item)
        if selected_item2:
            index = int(selected_item2[0][1:])
            del aperiodicArrival[index-1]
            del aperiodicLenght[index-1]

            self.aperiodic_table.delete(selected_item2)
        if not selected_item and not selected_item2:
            messagebox.showwarning("No selection", "Please select a task to delete.")
        else:
            self.submit_data( True)

    def update_plot(self):
        self.plot_schedule(self.examples, self.results, self.title, self.haveIntrupt, self.showDeadline)

    def plot_schedule(self, examples, results, title, haveIntrupt, showDeadline):
        print(results)
        self.ax.clear()
        T, C, D = examples[0], examples[1], examples[2]
        tasks = np.array(results[0:-1])
        missed = np.array(results[-1])
        num_tasks, time_slots = tasks.shape

        self.ax.set_xticks(range(time_slots))
        self.ax.set_yticks(range(num_tasks))
        if(haveIntrupt):
            tasksName2 = list(tasksName)
            tasksName2.append('Server')
            tasksName2.append('Budget')
        else:
            tasksName2 = list(tasksName)
        print(tasksName)
        print(tasksName2)
        print(num_tasks)
        self.ax.set_yticklabels([f"{tasksName2[i]}" for i in range(num_tasks)])
        self.ax.set_xlabel("Real-Time clock")
        self.ax.set_ylabel("Tasks")
        self.ax.set_title(title)

        for task_idx in range(num_tasks):
            if haveIntrupt and task_idx == num_tasks - 1:
                # self.ax.plot(range(time_slots), tasks[task_idx]/(-10), color='blue', linewidth=2, label='Special Plot')
                values = tasks[task_idx]
                normalized = values /max(values)  # maps 0 -> -1, 1 -> +1

                # Scale and center it in the task row
                y_offset = task_idx
                height = 0.4  # how tall the line visually appears within the row
                scaled_values = normalized * -height + y_offset

                self.ax.plot(range(time_slots), scaled_values, color='blue', linewidth=2, label='budget usage')
                continue

            for time in range(time_slots):
                if tasks[task_idx, time] == 1:
                    color = 'green' if missed[time] == 0 else 'orange'
                    if haveIntrupt and task_idx == num_tasks - 2:
                        color = 'red'
                    self.ax.add_patch(plt.Rectangle((time, task_idx - 0.4), 1, 0.8, color=color))

                if not haveIntrupt or (haveIntrupt and task_idx != num_tasks - 2 and task_idx != num_tasks - 1):
                    if time % T[task_idx] == 0:
                        self.ax.plot([time, time + .1], [task_idx, task_idx - 0.5], color='black', lw=2)
                    if time % T[task_idx] == D[task_idx] and showDeadline:
                        self.ax.plot([time, time], [task_idx + 0.5, task_idx], color='red', lw=2)

        self.ax.grid(True, linestyle="--", linewidth=0.5)
        self.ax.set_xticks(np.arange(0, time_slots, 1), minor=False)
        self.ax.set_yticks(np.arange(0, num_tasks, 1), minor=False)
        self.ax.invert_yaxis()

        self.canvas.draw()


    def submit_data(self, justPlot = False):
        if not justPlot and self.task_name_input.get() != "":
            try:
                numbers = [float(n.get()) for n in self.num_inputs]
                tasksName.append(self.task_name_input.get())
                tasksPeriod.append(int(numbers[0]))
                tasksJob.append(int(numbers[1]))
                tasksDeadline.append(int(numbers[2]))
                self.task_table.insert("", "end", values=(self.task_name_input.get(), int(numbers[0]), int(numbers[1]), int(numbers[2])))
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numbers.")
                return
        if not justPlot and self.aperiodic_task_arrival.get() != "":
            try:
                arrival = float(self.aperiodic_task_arrival.get())
                lenght = float(self.aperiodic_task_lenght.get())
                aperiodicArrival.append(arrival)
                aperiodicLenght.append(lenght)
                self.aperiodic_table.insert("", "end", values=(int(arrival), int(lenght)))
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numbers.")
                return
        try:
            aperiodicPeriod = int(self.aperiodic_period.get())
            aperiodicbudget = int(self.aperiodic_budget.get())
            simulationTime = int(self.simulation_time.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")
            return
        
        self.examples =[tasksPeriod,tasksJob,tasksDeadline]

        if(self.scheduling_type_input.get() == 'RMS'):
            self.showDeadline = False
            if(self.have_aperiodic.get() and int(self.aperiodic_period.get()) != 0):
                self.results = rm_scheduler_aperiodic(self.examples,aperiodicPeriod,aperiodicbudget,aperiodicArrival,aperiodicLenght,self.aperiodic_server_type.get(),simulationTime)
                self.haveIntrupt = True
            else:
                self.results = rm_scheduler(self.examples,simulationTime)
                self.haveIntrupt = False
        elif (self.scheduling_type_input.get() == 'EDF'):
            self.showDeadline = True
            if(self.have_aperiodic.get() and int(self.aperiodic_period.get()) != 0):
                self.results = dm_scheduler_aperiodic(self.examples,aperiodicPeriod,aperiodicbudget,aperiodicArrival,aperiodicLenght,self.aperiodic_server_type.get(),simulationTime)
                self.haveIntrupt = True
            else:
                self.results = ed_scheduler(self.examples,simulationTime)
                self.haveIntrupt = False
        else:
            self.showDeadline = True
            if(self.have_aperiodic.get() and int(self.aperiodic_period.get()) != 0):
                self.results = dm_scheduler_aperiodic(self.examples,aperiodicPeriod,aperiodicbudget,aperiodicArrival,aperiodicLenght,self.aperiodic_server_type.get(),simulationTime)
                self.haveIntrupt = True
            else:
                self.results = dm_scheduler(self.examples,simulationTime)
                self.haveIntrupt = False
        self.update_plot()
        self.calculateExact()

        self.task_name_input.delete(0, tk.END)
        self.aperiodic_task_arrival.delete(0, tk.END)
        self.aperiodic_task_lenght.delete(0, tk.END)
        for n in self.num_inputs:
            n.delete(0, tk.END)


    def clear_inputs(self):
        self.task_name_input.delete(0, tk.END)
        for n in self.num_inputs:
            n.delete(0, tk.END)
        for v in self.check_vars:
            v.set(False)
        self.radio_var.set("A")
        self.plot_initial()


if __name__ == "__main__":
    app = App()
    app.mainloop()


