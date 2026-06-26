import tkinter as tk
from tkinter import ttk, messagebox
from .test_case import TestCase
from .test_manager import TestManager

class Tooltip:
    """Simple tooltip implementation for Tkinter widgets."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def hide(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class MultiModelTesterUI:
    """Main application UI."""
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Multi-Model Tester")
        self.manager = TestManager()
        self._build_ui()

    def _build_ui(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame, text="Test Name:").grid(row=0, column=0, sticky="w")
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(frame, textvariable=self.name_var)
        name_entry.grid(row=0, column=1, sticky="ew")
        Tooltip(name_entry, "Enter a unique name for the test case")

        ttk.Label(frame, text="Description:").grid(row=1, column=0, sticky="w")
        self.desc_var = tk.StringVar()
        desc_entry = ttk.Entry(frame, textvariable=self.desc_var)
        desc_entry.grid(row=1, column=1, sticky="ew")
        Tooltip(desc_entry, "Optional description")

        ttk.Label(frame, text="Steps (comma separated):").grid(row=2, column=0, sticky="w")
        self.steps_var = tk.StringVar()
        steps_entry = ttk.Entry(frame, textvariable=self.steps_var)
        steps_entry.grid(row=2, column=1, sticky="ew")
        Tooltip(steps_entry, "List steps separated by commas")

        ttk.Label(frame, text="Expected Result:").grid(row=3, column=0, sticky="w")
        self.result_var = tk.StringVar()
        result_entry = ttk.Entry(frame, textvariable=self.result_var)
        result_entry.grid(row=3, column=1, sticky="ew")
        Tooltip(result_entry, "What should happen when the test runs")

        add_btn = ttk.Button(frame, text="Add Test", command=self.add_test)
        add_btn.grid(row=4, column=0, columnspan=2, pady=5)

        self.listbox = tk.Listbox(frame, height=8)
        self.listbox.grid(row=5, column=0, columnspan=2, sticky="nsew")
        Tooltip(self.listbox, "List of created test cases")

        del_btn = ttk.Button(frame, text="Delete Selected", command=self.delete_selected)
        del_btn.grid(row=6, column=0, columnspan=2, pady=5)

        frame.columnconfigure(1, weight=1)

    def add_test(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Test name cannot be empty")
            return
        steps = [s.strip() for s in self.steps_var.get().split(",") if s.strip()]
        test = TestCase(name=name, description=self.desc_var.get(), steps=steps, expected_result=self.result_var.get())
        try:
            self.manager.add_test(test)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        self.listbox.insert(tk.END, name)
        self._clear_fields()

    def delete_selected(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "No test selected")
            return
        idx = selection[0]
        name = self.listbox.get(idx)
        try:
            self.manager.remove_test(name)
        except KeyError:
            pass
        self.listbox.delete(idx)

    def _clear_fields(self):
        self.name_var.set("")
        self.desc_var.set("")
        self.steps_var.set("")
        self.result_var.set("")
