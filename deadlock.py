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
#         self.allocation_entries = self.create_matrix_input(1, self.process_count, self.resource_count)
        
#         ttk.Label(self.master, text="Enter Request Matrix:").grid(row=self.process_count+1, column=0, columnspan=self.resource_count)
#         self.request_entries = self.create_matrix_input(self.process_count+2, self.process_count, self.resource_count)
        
#         ttk.Label(self.master, text="Available Resources:").grid(row=(self.process_count*2)+2, column=0, columnspan=self.resource_count)
#         self.available_entries = self.create_vector_input((self.process_count*2)+3, self.resource_count)
        
#         ttk.Button(self.master, text="Detect Deadlock", command=self.detect_deadlock).grid(row=(self.process_count*2)+4, column=0, columnspan=self.resource_count, pady=10)
    
#     def create_matrix_input(self, start_row, rows, cols):
#         matrix_entries = []
#         for i in range(rows):
#             row_entries = []
#             for j in range(cols):
#                 entry = ttk.Entry(self.master, width=5)
#                 entry.grid(row=start_row+i, column=j, padx=5, pady=2)
#                 row_entries.append(entry)
#             matrix_entries.append(row_entries)
#         return matrix_entries
    
#     def create_vector_input(self, start_row, size):
#         entries = []
#         for i in range(size):
#             entry = ttk.Entry(self.master, width=5)
#             entry.grid(row=start_row, column=i, padx=5, pady=2)
#             entries.append(entry)
#         return entries
    
#     def get_matrix_values(self, matrix_entries):
#         try:
#             return np.array([[int(entry.get()) for entry in row] for row in matrix_entries])
#         except ValueError:
#             messagebox.showerror("Error", "Invalid input! Enter only numbers.")
#             return None
    
#     def get_vector_values(self, vector_entries):
#         try:
#             return np.array([int(entry.get()) for entry in vector_entries])
#         except ValueError:
#             messagebox.showerror("Error", "Invalid input! Enter only numbers.")
#             return None
    
#     def detect_deadlock(self):
#         allocation = self.get_matrix_values(self.allocation_entries)
#         request = self.get_matrix_values(self.request_entries)
#         available = self.get_vector_values(self.available_entries)
        
#         if allocation is None or request is None or available is None:
#             return
        
#         work = available.copy()
#         finish = np.full(self.process_count, False)
#         safe_sequence = []
        
#         for _ in range(self.process_count):
#             found = False
#             for i in range(self.process_count):
#                 if not finish[i] and np.all(request[i] <= work):
#                     work += allocation[i]
#                     finish[i] = True
#                     safe_sequence.append(i)
#                     found = True
#                     break
#             if not found:
#                 break
        
#         if np.all(finish):
#             self.show_charts(allocation, available, safe_sequence)
#             messagebox.showinfo("Result", f"No Deadlock! Safe Sequence: {safe_sequence}")
#         else:
#             messagebox.showerror("Result", "Deadlock Detected!")
    
#     def show_charts(self, allocation, available, safe_sequence):
#         chart_window = tk.Toplevel(self.master)
#         chart_window.title("Resource Allocation & Safe Sequence")
        
#         fig, axes = plt.subplots(1, 2, figsize=(10, 5))
        
#         # Pie Chart for Allocation
#         total_allocated = np.sum(allocation, axis=0)
#         axes[0].pie(total_allocated, labels=[f'Resource {i}' for i in range(len(total_allocated))], autopct='%1.1f%%')
#         axes[0].set_title("Resource Allocation Distribution")
        
#         # Bar Chart for Available Resources
#         axes[1].bar([f'Resource {i}' for i in range(len(available))], available, color='skyblue')
#         axes[1].set_title("Available Resources")
#         axes[1].set_ylabel("Count")
        
#         plt.tight_layout()
#         canvas = FigureCanvasTkAgg(fig, master=chart_window)
#         canvas.get_tk_widget().pack()
#         canvas.draw()


# def main():
#     root = tk.Tk()
#     app = DeadlockDetectionApp(root)
#     root.mainloop()

# if __name__ == "__main__":
#     main()





import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import winsound
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DeadlockDetectionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Deadlock Detection and Prevention")
        self.master.geometry("1000x700")
        
        self.num_processes = tk.IntVar()
        self.num_resources = tk.IntVar()
        
        self.create_initial_ui()
    
    def create_initial_ui(self):
        frame = ttk.Frame(self.master, padding=20)
        frame.pack(expand=True)
        
        ttk.Label(frame, text="Number of Processes:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.num_processes, width=5).grid(row=0, column=1)
        
        ttk.Label(frame, text="Number of Resources:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.num_resources, width=5).grid(row=1, column=1)
        
        ttk.Button(frame, text="Next", command=self.create_matrix_ui).grid(row=2, column=0, columnspan=2, pady=10)
    
    def create_matrix_ui(self):
        try:
            self.process_count = self.num_processes.get()
            self.resource_count = self.num_resources.get()
            if self.process_count <= 0 or self.resource_count <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter valid numbers for processes and resources.")
            return
        
        for widget in self.master.winfo_children():
            widget.destroy()
        
        ttk.Label(self.master, text="Enter Allocation Matrix:").grid(row=0, column=0, columnspan=self.resource_count)
        self.allocation_entries = self.create_matrix_input(1, self.process_count, self.resource_count)
        
        ttk.Label(self.master, text="Enter Request Matrix:").grid(row=self.process_count+1, column=0, columnspan=self.resource_count)
        self.request_entries = self.create_matrix_input(self.process_count+2, self.process_count, self.resource_count)
        
        ttk.Label(self.master, text="Available Resources:").grid(row=(self.process_count*2)+2, column=0, columnspan=self.resource_count)
        self.available_entries = self.create_vector_input((self.process_count*2)+3, self.resource_count)
        
        ttk.Button(self.master, text="Detect Deadlock", command=self.detect_deadlock).grid(row=(self.process_count*2)+4, column=0, columnspan=self.resource_count, pady=10)
    
    def create_matrix_input(self, start_row, rows, cols):
        matrix_entries = []
        for i in range(rows):
            row_entries = []
            for j in range(cols):
                entry = ttk.Entry(self.master, width=5)
                entry.grid(row=start_row+i, column=j, padx=5, pady=2)
                row_entries.append(entry)
            matrix_entries.append(row_entries)
        return matrix_entries
    
    def create_vector_input(self, start_row, size):
        entries = []
        for i in range(size):
            entry = ttk.Entry(self.master, width=5)
            entry.grid(row=start_row, column=i, padx=5, pady=2)
            entries.append(entry)
        return entries
    
    def get_matrix_values(self, matrix_entries):
        try:
            return np.array([[int(entry.get()) for entry in row] for row in matrix_entries])
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Enter only numbers.")
            return None
    
    def get_vector_values(self, vector_entries):
        try:
            return np.array([int(entry.get()) for entry in vector_entries])
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Enter only numbers.")
            return None
    
    def detect_deadlock(self):
        allocation = self.get_matrix_values(self.allocation_entries)
        request = self.get_matrix_values(self.request_entries)
        available = self.get_vector_values(self.available_entries)
        
        if allocation is None or request is None or available is None:
            return
        
        work = available.copy()
        finish = np.full(self.process_count, False)
        safe_sequence = []
        
        for _ in range(self.process_count):
            found = False
            for i in range(self.process_count):
                if not finish[i] and np.all(request[i] <= work):
                    work += allocation[i]
                    finish[i] = True
                    safe_sequence.append(i)
                    found = True
                    break
            if not found:
                break
        
        if np.all(finish):
            messagebox.showinfo("Result", f"No Deadlock! Safe Sequence: {safe_sequence}")
            self.show_charts(allocation, available)
            self.show_rag_graph(allocation, request)
        else:
            self.show_warning_effect()
            messagebox.showerror("Result", "Deadlock Detected!")
            self.show_rag_graph(allocation, request)
    
    def show_charts(self, allocation, available):
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))
        
        total_allocated = np.sum(allocation, axis=0)
        axes[0].pie(total_allocated, labels=[f'Resource {i}' for i in range(len(total_allocated))], autopct='%1.1f%%')
        axes[0].set_title("Resource Allocation Distribution")
        
        axes[1].bar([f'Resource {i}' for i in range(len(available))], available, color='skyblue')
        axes[1].set_title("Available Resources")
        axes[1].set_ylabel("Count")
        
        plt.tight_layout()
        plt.show()
    
    def show_rag_graph(self, allocation, request):
        G = nx.DiGraph()
        
        for p in range(self.process_count):
            G.add_node(f'P{p}')
        for r in range(self.resource_count):
            G.add_node(f'R{r}')
        
        for p in range(self.process_count):
            for r in range(self.resource_count):
                if allocation[p][r] > 0:
                    G.add_edge(f'R{r}', f'P{p}')
                if request[p][r] > 0:
                    G.add_edge(f'P{p}', f'R{r}')
        
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='black')
        plt.show()
    
    def show_warning_effect(self):
        winsound.Beep(1000, 4000)
        

def main():
    root = tk.Tk()
    app = DeadlockDetectionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
