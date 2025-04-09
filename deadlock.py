import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import winsound

class DeadlockDetectionApp:
    def __init__(self, master):
        self.master = master
        # self.master.title("Deadlock Detection System")
        self.master.title("Smart Deadlock Detection & Prevention System: A Visual & Analytical Approach")

        self.num_processes = tk.IntVar()
        self.num_resources = tk.IntVar()
        self.theme_var = tk.StringVar(value="superhero")
        self.mode = tk.StringVar(value="Detection")  # Toggle button variable
        self.style = tb.Style(theme=self.theme_var.get())

        self.create_widgets()

    def create_widgets(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        theme_frame = tb.Frame(self.master)
        theme_frame.pack(pady=10)
        tb.Label(theme_frame, text="Theme:", font=("Helvetica", 11)).pack(side="left", padx=5)
        theme_menu = tb.OptionMenu(theme_frame, self.theme_var, self.theme_var.get(), *self.style.theme_names(), command=self.change_theme)
        theme_menu.pack(side="left")

        mode_frame = tb.Frame(self.master)
        mode_frame.pack(pady=5)
        tb.Label(mode_frame, text="Mode:", font=("Helvetica", 11)).pack(side="left", padx=5)
        tb.OptionMenu(mode_frame, self.mode, self.mode.get(), "Detection", "Prevention").pack(side="left")

        input_frame = tb.Frame(self.master)
        input_frame.pack(pady=10)

        tb.Label(input_frame, text="Processes:", font=("Helvetica", 13)).grid(row=0, column=0, padx=5, pady=5)
        tb.Entry(input_frame, textvariable=self.num_processes, width=10).grid(row=0, column=1, padx=5)

        tb.Label(input_frame, text="Resources:", font=("Helvetica", 13)).grid(row=1, column=0, padx=5, pady=5)
        tb.Entry(input_frame, textvariable=self.num_resources, width=10).grid(row=1, column=1, padx=5)

        tb.Button(input_frame, text="Next", command=self.create_matrix_inputs, bootstyle="primary").grid(row=2, column=0, columnspan=2, pady=10)

    def change_theme(self, theme):
        self.style.theme_use(theme)
        self.create_widgets()

    def create_matrix_inputs(self):
        try:
            self.p = self.num_processes.get()
            self.r = self.num_resources.get()
            if self.p <= 0 or self.r <= 0:
                raise ValueError
        except:
            messagebox.showerror("Invalid", "Enter valid positive integers.")
            return

        for widget in self.master.winfo_children()[3:]:
            widget.destroy()

        self.alloc_entries = []
        self.req_entries = []

        matrix_frame = tb.Frame(self.master)
        matrix_frame.pack()

        tb.Label(matrix_frame, text="Allocation Matrix", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=self.r)
        for i in range(self.p):
            row = []
            for j in range(self.r):
                entry = tb.Entry(matrix_frame, width=5)
                entry.grid(row=i + 1, column=j)
                row.append(entry)
            self.alloc_entries.append(row)

        offset = self.p + 2
        tb.Label(matrix_frame, text="Request Matrix", font=("Helvetica", 14)).grid(row=offset, column=0, columnspan=self.r)
        for i in range(self.p):
            row = []
            for j in range(self.r):
                entry = tb.Entry(matrix_frame, width=5)
                entry.grid(row=offset + i + 1, column=j)
                row.append(entry)
            self.req_entries.append(row)

        tb.Label(matrix_frame, text="Available:", font=("Helvetica", 13)).grid(row=offset + self.p + 2, column=0, columnspan=2)
        self.available_entries = [tb.Entry(matrix_frame, width=5) for _ in range(self.r)]
        for j, entry in enumerate(self.available_entries):
            entry.grid(row=offset + self.p + 3, column=j)

        button_label = "Detect Deadlock" if self.mode.get() == "Detection" else "Prevent Deadlock"
        tb.Button(self.master, text=button_label, command=self.detect_or_prevent_deadlock, bootstyle="danger").pack(pady=10)

    def detect_or_prevent_deadlock(self):
        try:
            alloc = [[int(e.get()) for e in row] for row in self.alloc_entries]
            req = [[int(e.get()) for e in row] for row in self.req_entries]
            avail = [int(e.get()) for e in self.available_entries]
        except:
            messagebox.showerror("Error", "Fill all matrix values with integers.")
            return

        if self.mode.get() == "Detection":
            self.deadlock_detection(alloc, req, avail)
        else:
            self.deadlock_prevention(alloc, req, avail)

    def deadlock_detection(self, alloc, req, avail):
        work = avail[:]
        finish = [False] * self.p
        safe_seq = []

        while True:
            allocated = False
            for i in range(self.p):
                if not finish[i] and all(req[i][j] <= work[j] for j in range(self.r)):
                    for j in range(self.r):
                        work[j] += alloc[i][j]
                    finish[i] = True
                    safe_seq.append(f'P{i}')
                    allocated = True
            if not allocated:
                break

        if all(finish):
            messagebox.showinfo("✅ Safe State", f"System is in Safe State.\nSafe Sequence: {' ➝ '.join(safe_seq)}")
            self.show_rag_graph(alloc, req, [])
        else:
            winsound.Beep(1000, 1200)
            deadlocked = [f'P{i}' for i, done in enumerate(finish) if not done]
            messagebox.showerror("❌ Deadlock Detected", f"Deadlock in: {', '.join(deadlocked)}")
            self.show_rag_graph(alloc, req, deadlocked)

        self.show_charts(alloc)

    def deadlock_prevention(self, alloc, req, avail):
        work = avail[:]
        finish = [False] * self.p
        safe_seq = []

        for i in range(self.p):
            if all(req[i][j] <= work[j] for j in range(self.r)):
                for j in range(self.r):
                    work[j] += alloc[i][j]
                finish[i] = True
                safe_seq.append(f'P{i}')

        if all(finish):
            messagebox.showinfo("✅ No Deadlock", f"Deadlock Prevented Successfully.\nSafe Execution Order: {' ➝ '.join(safe_seq)}")
            self.show_rag_graph(alloc, req, [])
        else:
            messagebox.showwarning("⚠️ Deadlock Prevention", "Deadlock could not be fully prevented for all processes.")
            deadlocked = [f'P{i}' for i, done in enumerate(finish) if not done]
            self.show_rag_graph(alloc, req, deadlocked)

        self.show_charts(alloc)

    def show_rag_graph(self, alloc, req, deadlocked):
        window = tb.Toplevel(self.master)
        window.title("Resource Allocation Graph")
        fig, ax = plt.subplots(figsize=(6, 4))
        G = nx.DiGraph()

        for i in range(self.p):
            G.add_node(f'P{i}', color='red' if f'P{i}' in deadlocked else 'skyblue')
        for j in range(self.r):
            G.add_node(f'R{j}', color='orange')

        for i in range(self.p):
            for j in range(self.r):
                if alloc[i][j] > 0:
                    G.add_edge(f'R{j}', f'P{i}')
                if req[i][j] > 0:
                    G.add_edge(f'P{i}', f'R{j}')

        pos = nx.spring_layout(G)
        colors = [data['color'] for _, data in G.nodes(data=True)]
        nx.draw(G, pos, with_labels=True, node_color=colors, node_size=1000, font_size=10, ax=ax)
        ax.set_title("RAG Graph")
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.get_tk_widget().pack(fill='both', expand=True)
        canvas.draw()

    def show_charts(self, alloc):
        alloc_sum = np.sum(alloc, axis=0)
        fig, axs = plt.subplots(1, 2, figsize=(9, 4))

        axs[0].pie(alloc_sum, labels=[f'R{i}' for i in range(self.r)], autopct='%1.1f%%', startangle=90)
        axs[0].set_title("Resource Allocation Pie Chart")

        axs[1].bar([f'R{i}' for i in range(self.r)], alloc_sum, color='lightgreen')
        axs[1].set_title("Resource Allocation Bar Chart")
        axs[1].set_ylabel("Units Allocated")

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    root = tb.Window(themename="superhero")
    app = DeadlockDetectionApp(root)
    root.mainloop()
