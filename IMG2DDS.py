import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
import subprocess

def resize_and_convert_images(input_dir, output_dir, size=None, base_image_path=None, compression_format="-bc1"):
    for root, dirs, files in os.walk(input_dir):
        total_files = len(files)  # for progressbar update
        for i, file in enumerate(files):
            try:
                img_path = os.path.join(root, file)
                img = Image.open(img_path)

                # Make the image's untransparent parts black
                data = img.getdata()
                new_data = []
                for item in data:
                    # change all white (also shades of whites)
                    # pixels to yellow
                    if item[0] > 200 or item[1] > 200 or item[2] > 200:
                        new_data.append((0, 0, 0, item[3]))
                    else:
                        new_data.append(item)
                img.putdata(new_data)

                if size is not None:
                    img = img.resize(size, Image.LANCZOS)

                if base_image_path is not None:
                    base_image = Image.open(base_image_path)
                    base_image.paste(img, (int((base_image.width - img.width) / 2), int((base_image.height - img.height) / 2)), img)
                    img = base_image

                output = os.path.join(output_dir, os.path.splitext(file)[0] + '.png')
                img.save(output)

                temp_output = output
                dds_output = os.path.join(output_dir, os.path.splitext(file)[0] + '.dds')
                subprocess.call(["nvcompress", compression_format, temp_output, dds_output])
                os.remove(temp_output)  # remove temporary png file after creating dds file

                progress_var.set(i + 1)  # update progressbar
                root.update_idletasks()  # update GUI

            except Exception as e:
                messagebox.showerror("Error", f"Error during nvcompress execution: {str(e)}")

def browse_input_dir():
    filename = filedialog.askdirectory()
    input_dir_entry.insert(0, filename)

def browse_output_dir():
    filename = filedialog.askdirectory()
    output_dir_entry.insert(0, filename)

root = tk.Tk()
root.geometry("500x200")  # adjust window size
root.title("Image to DDS Converter")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

input_dir_label = tk.Label(frame, text="Input Directory:")
input_dir_label.grid(column=0, row=0, sticky="W")
input_dir_entry = tk.Entry(frame, width=50)
input_dir_entry.grid(column=1, row=0, sticky="W")
input_dir_button = tk.Button(frame, text="Browse", command=browse_input_dir)
input_dir_button.grid(column=2, row=0, sticky="W")

output_dir_label = tk.Label(frame, text="Output Directory:")
output_dir_label.grid(column=0, row=1, sticky="W")
output_dir_entry = tk.Entry(frame, width=50)
output_dir_entry.grid(column=1, row=1, sticky="W")
output_dir_button = tk.Button(frame, text="Browse", command=browse_output_dir)
output_dir_button.grid(column=2, row=1, sticky="W")

# Add entries for Width and Height
width_label = tk.Label(frame, text="Width:")
width_label.grid(column=0, row=2, sticky="W")
width_entry = tk.Entry(frame, width=10)
width_entry.grid(column=1, row=2, sticky="W")

height_label = tk.Label(frame, text="Height:")
height_label.grid(column=0, row=3, sticky="W")
height_entry = tk.Entry(frame, width=10)
height_entry.grid(column=1, row=3, sticky="W")

# Add dropdown menu for compression format
compression_label = tk.Label(frame, text="Compression Format:")
compression_label.grid(column=0, row=4, sticky="W")
compression_var = tk.StringVar(root)
compression_var.set("-bc1")  # default value
compression_formats = ["-fast", "-production", "-highest", "-nocuda", "-rgb", "-lumi", "-bc1", "-bc1n", "-bc1a", "-bc2", "-bc3", "-bc3n", "-bc4", "-bc4s", "-ati2", "-bc5", "-bc5s", "-bc6", "-bc6s", "-bc7", "-bc3_rgbm", "-astc_ldr_4x4"]
compression_menu = tk.OptionMenu(frame, compression_var, *compression_formats)
compression_menu.grid(column=1, row=4, sticky="W")

# Add progressbar
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(frame, length=200, mode='determinate', variable=progress_var)
progress_bar.grid(column=1, row=6, columnspan=2, sticky="W")

def convert_images():
    input_dir = input_dir_entry.get()
    output_dir = output_dir_entry.get()
    compression_format = compression_var.get()

    width = width_entry.get()
    height = height_entry.get()

    if width and height:
        size = (int(width), int(height))
    else:
        size = None

    if base_image_var.get() != "None":
        base_image_path = os.path.join("Base_Image", base_image_var.get())
    else:
        base_image_path = None

    resize_and_convert_images(input_dir, output_dir, size, base_image_path, compression_format)

    messagebox.showinfo("Success", "Images have been successfully converted and saved!")

# Add convert button
convert_button = tk.Button(frame, text="Convert Images", command=convert_images)
convert_button.grid(column=0, row=7, columnspan=3)

root.mainloop()
