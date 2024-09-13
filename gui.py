import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

def run_script():
    file1 = file1_entry.get()
    file2 = file2_entry.get()
    output_folder = output_entry.get()

    # Check if the paths are valid
    if not (os.path.isfile(file1) and os.path.isfile(file2)):
        messagebox.showerror("Error", "Please select valid input files.")
        return
    if not os.path.isdir(output_folder):
        messagebox.showerror("Error", "Please select a valid output folder.")
        return

    try:
        # Run your script and capture the output
        result = subprocess.run(["python", "main.py", file1, file2, output_folder], capture_output=True, text=True)
        if result.returncode == 0:
            messagebox.showinfo("Success", "Script executed successfully!")
        else:
            messagebox.showerror("Error", f"Script failed with return code {result.returncode}: {result.stderr}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def select_file1():
    file_path = filedialog.askopenfilename()
    file1_entry.delete(0, tk.END)
    file1_entry.insert(0, file_path)

def select_file2():
    file_path = filedialog.askopenfilename()
    file2_entry.delete(0, tk.END)
    file2_entry.insert(0, file_path)

def select_output_folder():
    folder_path = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, folder_path)

# Create the main window
root = tk.Tk()
root.title("Script Runner")

# Create labels and entry fields for file selection
tk.Label(root, text="File 1:").grid(row=0, column=0, padx=10, pady=10)
file1_entry = tk.Entry(root, width=50)
file1_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse...", command=select_file1).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="File 2:").grid(row=1, column=0, padx=10, pady=10)
file2_entry = tk.Entry(root, width=50)
file2_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse...", command=select_file2).grid(row=1, column=2, padx=10, pady=10)

tk.Label(root, text="Output Folder:").grid(row=2, column=0, padx=10, pady=10)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=2, column=1, padx=10, pady=10)
tk.Button(root, text="Browse...", command=select_output_folder).grid(row=2, column=2, padx=10, pady=10)

# Run script button
tk.Button(root, text="Run Script", command=run_script).grid(row=3, column=0, columnspan=3, padx=10, pady=20)

# Start the GUI event loop
root.mainloop()
