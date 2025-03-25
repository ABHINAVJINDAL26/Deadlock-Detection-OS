# import tkinter as tk
# from tkinter import ttk, messagebox
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# class DeadlockDetectionApp:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Deadlock Detection and Prevention")
#         self.master.geometry("1000x700")
        
#         self.num_processes = tk.IntVar()
#         self.num_resources = tk.IntVar()
        
#         self.create_initial_ui()
    
#     def create_initial_ui(self):
#         frame = ttk.Frame(self.master, padding=20)
#         frame.pack(expand=True)
        
#         ttk.Label(frame, text="Number of Processes:").grid(row=0, column=0, padx=5, pady=5)
#         ttk.Entry(frame, textvariable=self.num_processes, width=5).grid(row=0, column=1)
        
#         ttk.Label(frame, text="Number of Resources:").grid(row=1, column=0, padx=5, pady=5)
#         ttk.Entry(frame, textvariable=self.num_resources, width=5).grid(row=1, column=1)
        
#         ttk.Button(frame, text="Next", command=self.create_matrix_ui).grid(row=2, column=0, columnspan=2, pady=10)
    
#     def create_matrix_ui(self):
#         try:
#             self.process_count = self.num_processes.get()
#             self.resource_count = self.num_resources.get()
#             if self.process_count <= 0 or self.resource_count <= 0:
#                 raise ValueError
#         except ValueError:
#             messagebox.showerror("Error", "Enter valid numbers for processes and resources.")
#             return
        
#         for widget in self.master.winfo_children():
#             widget.destroy()
        
#         ttk.Label(self.master, text="Enter Allocation Matrix:").grid(row=0, column=0, columnspan=self.resource_count)
