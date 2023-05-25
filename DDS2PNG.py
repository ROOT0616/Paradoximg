import os
import imageio
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox

def select_input_dir():
    input_dir = filedialog.askdirectory()
    input_entry.delete(0, tk.END)
    input_entry.insert(0, input_dir)

def select_output_dir():
    output_dir = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_dir)

def convert_images():
    input_dir = input_entry.get()
    output_dir = output_entry.get()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.dds'):
            dds_image = imageio.imread(os.path.join(input_dir, filename))
            img = Image.fromarray(dds_image)
            base_filename = os.path.splitext(filename)[0]
            img.save(os.path.join(output_dir, f'{base_filename}.png'))

    messagebox.showinfo('Info', 'Conversion completed!')

root = tk.Tk()
root.title('DDS to PNG Converter')

input_label = tk.Label(root, text='Input Directory:')
input_label.grid(row=0, column=0, padx=(20, 10), pady=(20, 0))

input_entry = tk.Entry(root, width=50)
input_entry.grid(row=0, column=1, pady=(20, 0))

input_button = tk.Button(root, text='Select', command=select_input_dir)
input_button.grid(row=0, column=2, padx=(10, 20), pady=(20, 0))

output_label = tk.Label(root, text='Output Directory:')
output_label.grid(row=1, column=0, padx=(20, 10), pady=(10, 0))

output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1, pady=(10, 0))

output_button = tk.Button(root, text='Select', command=select_output_dir)
output_button.grid(row=1, column=2, padx=(10, 20), pady=(10, 0))

convert_button = tk.Button(root, text='Convert', command=convert_images)
convert_button.grid(row=2, column=0, columnspan=3, pady=20)

root.mainloop()
