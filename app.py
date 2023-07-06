import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from ttkthemes import ThemedStyle
import os

class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master, padding="10")  # Add padding around the frame
        self.master = master
        # Set the window size
        self.master.geometry('600x800')  # Width x Height
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Instructions for the user
        self.instructions_label = ttk.Label(self, text="Please, fill out the information below and click RUN")
        self.instructions_label.pack(side="top", pady=(0, 10))  # Add padding at the bottom

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
        self.run_button = ttk.Button(self, text="RUN", command=self.run)
        self.run_button.pack(side="bottom", pady=(10, 0))  # Add padding at the top

        # Progress bar (initially hidden)
        self.progress = ttk.Progressbar(self, length=200, mode='indeterminate')

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
        if file_path:
            self.file_label['text'] = os.path.basename(file_path)

    def run(self):
        # Ensure all necessary fields are completed
        if not self.subtitle_text.get("1.0", tk.END).strip() or self.file_label['text'] == "No file selected":
            messagebox.showerror("Error", "Please, fill out all fields!")
            return

        # Start progress bar
        self.progress.pack(side="bottom")
        self.progress.start()

        print(f"Running in {self.mode_var.get()} mode")
        subtitle_text = self.subtitle_text.get("1.0", tk.END).strip()
        if subtitle_text:
            print(f"Subtitle text: {subtitle_text}")
        # TODO: Add functionality to generate subtitles, remove silences, and tts

        # Stop progress bar
        self.progress.stop()
        self.progress.pack_forget()

        messagebox.showinfo("Info", "Operation completed successfully!")

root = tk.Tk()
style = ThemedStyle(root)
style.set_theme("black")

app = Application(master=root)
app.mainloop()
