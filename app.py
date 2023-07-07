import tkinter as tk
from tkinter import filedialog, messagebox, Entry
from tkinter import ttk
from ttkthemes import ThemedStyle

from tkinter import *
from tkinter.scrolledtext import ScrolledText
import os
import sys
import subprocess
import re
import datetime

import subtitle_generator
import silence_remover


class CreateToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tw, text=self.text, justify='left',
                      background="#ffffff", relief='solid', borderwidth=1,
                      wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()


class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(padx=20, pady=20)  # Padding for the entire frame
        self.file_path = ""
        self.create_widgets()

    def validate_project_name(self, new_text):
        """Validates the project name input"""
        if re.match("^[A-Za-z0-9_-]*$", new_text):
            return True
        else:
            messagebox.showwarning("Invalid Project Name", "The project name can only contain letters, numbers, underscores, and dashes.")
            return False
    
    def create_widgets(self):
        # Project name field
        self.project_label = ttk.Label(self, text="Project Name")
        self.project_label.pack(side="top")
        self.project_name = Entry(self, validate="key")
        self.project_name['validatecommand'] = (self.project_name.register(self.validate_project_name), '%P')
        self.project_name.pack(side="top")
        self.tooltip = CreateToolTip(self.project_name, "Allowed characters: A-Z, a-z, 0-9, underscore (_), and dash (-). Spaces and special characters are not allowed.")

        # Instructions for the user
        # self.instructions_label = ttk.Label(self, text="Please, fill out the information below and click RUN")
        # self.instructions_label.pack(side="top", pady=(0, 10))  # Add padding at the bottom

        # Subtitle text area
        self.subtitle_label = ttk.Label(self, text="Subtitle Text")
        self.subtitle_label.pack(side="top")
        self.subtitle_text = tk.Text(self, height=10)
        self.subtitle_text.pack(side="top", pady=(0, 10))  # Add padding at the bottom

        # MP4 file selection
        self.file_label = ttk.Label(self, text="No file selected")
        self.file_label.pack(side="top")
        self.file_button = ttk.Button(self, text="Select MP4 file", command=self.select_file)
        self.file_button.pack(side="top", pady=(0, 10))  # Add padding at the bottom

        # Mode selection
        self.mode_label = ttk.Label(self, text="Mode")
        self.mode_label.pack(side="top")
        self.mode_var = tk.StringVar(self)
        self.mode_var.set("subtitle")  # default value
        self.mode_options = ttk.OptionMenu(self, self.mode_var, "subtitle", "subtitle", "remove_silence", "tts")
        self.mode_options.pack(side="top", pady=(0, 10))  # Add padding at the bottom

        # Run button
        self.run_button = ttk.Button(self, text="RUN", command=self.check)
        self.run_button.pack(side="bottom", pady=(10, 0))  # Add padding at the top
        
        # Open Output Folder button
        self.open_folder_button = ttk.Button(self, text="Open Output Folder", command=self.open_output_folder)
        self.open_folder_button.pack(side="bottom", pady=(10, 0))  # Add padding at the top

        # Progress bar (initially hidden)
        self.progress = ttk.Progressbar(self, length=200, mode='indeterminate')

    def open_output_folder(self):
        output_dir = os.path.join('output', datetime.datetime.now().strftime('%Y%m%d'))
        if sys.platform == 'win32':
            os.startfile(output_dir)
        else:
            subprocess.call(['open', output_dir])
    
    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
        if self.file_path:
            self.file_label['text'] = os.path.basename(self.file_path)
            
    def check(self):
        if self.mode_var.get() == "subtitle":
            if self.project_name.get() == "" or self.subtitle_text.get("1.0", 'end-1c') == "":
                messagebox.showwarning("Missing Fields", "Please fill all fields.")
            else:
                self.run(project_name=self.project_name.get(), subtitle_text=self.subtitle_text.get("1.0", 'end-1c'))
        elif self.mode_var.get() == "remove_silence":
            if self.project_name.get() == "" or self.file_path == "":
                messagebox.showwarning("Missing Fields", "Please fill all fields.")
            else:
                self.run(project_name=self.project_name.get(), file_path=self.file_path)

    def run(self, project_name=None, subtitle_text=None, file_path=None):
        # Start progress bar
        self.progress.pack(side="bottom")
        self.progress.start()

        try:
            print(f"Running in {self.mode_var.get()} mode")

            if self.mode_var.get() == "subtitle":
                subtitle_generator.generate_subtitles(subtitle_text, project_name)
            elif self.mode_var.get() == "remove_silence":
                silence_remover.remove_silence(file_path, project_name)

            messagebox.showinfo("Info", "Operation completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            # Stop progress bar
            self.progress.stop()
            self.progress.pack_forget()

root = tk.Tk()
style = ThemedStyle(root)
style.set_theme("black")

app = Application(master=root)
app.mainloop()