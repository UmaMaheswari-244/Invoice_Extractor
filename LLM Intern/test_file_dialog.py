import tkinter as tk
from tkinter import filedialog

def test_file_dialog():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        filetypes=[("PDF files", "*.pdf"), ("PNG files", "*.png")]
    )
    print(f"Selected file: {file_path}")

test_file_dialog()
