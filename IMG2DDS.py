import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import numpy as np
from PIL import Image

def browse_input_dir():
    filename = filedialog.askdirectory()
    input_dir_entry.delete(0, tk.END)
    input_dir_entry.insert(0, filename)

def browse_output_dir():
    filename = filedialog.askdirectory()
    output_dir_entry.delete(0, tk.END)
    output_dir_entry.insert(0, filename)

def apply_color(img, color):
    data = np.array(img)
    red, green, blue, alpha = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    mask = (red != 0) | (green != 0) | (blue != 0) | (alpha != 0)
    data[:,:,:3][mask] = color[:3]
    return Image.fromarray(data)

def apply_mask(image, mask_path):
    mask = Image.open(mask_path).convert("RGBA")
    return Image.composite(image.resize(mask.size, Image.ANTIALIAS), mask, mask)

def resize_and_paste_images(input_dir, output_dir, size, base_image_path, mask_image_path, color, compression_format, resize_after, invert_paste, apply_mask_flag):
    files = os.listdir(input_dir)
    number_of_files = len(files)
    progress_bar["maximum"] = number_of_files

    base_image = Image.open(base_image_path).convert("RGBA") if base_image_path else None

    for i, filename in enumerate(files):
        input_path = os.path.join(input_dir, filename)
        temp_output = os.path.join(output_dir, filename)
        dds_output = os.path.join(output_dir, os.path.splitext(filename)[0] + ".dds")
        img = Image.open(input_path).convert("RGBA")

        if color:
            img = apply_color(img, color)

        if apply_mask_checkbox_var.get() and mask_image_path:
            img = apply_mask(img, mask_image_path)

        if base_image:
            if invert_paste and resize_after:
                base = base_image.copy()
                position = ((img.width - base.width) // 2, (img.height - base.height) // 2)
                img.paste(base, position, base)
                base = img.resize(size, Image.ANTIALIAS)
            elif invert_paste or resize_after:
                if invert_paste:
                    img = img.resize(size, Image.ANTIALIAS)
                    base = base_image.copy()
                    position = ((img.width - base.width) // 2, (img.height - base.height) // 2)
                    img.paste(base, position, base)
                    base = img
                else:
                    base = base_image.copy()
                    position = ((base.width - img.width) // 2, (base.height - img.height) // 2)
                    base.paste(img, position, img)
                    base = base.resize(size, Image.ANTIALIAS)
            else:
                base = base_image.copy()
                img = img.resize(size, Image.ANTIALIAS)
                position = ((base.width - img.width) // 2, (base.height - img.height) // 2)
                base.paste(img, position, img)
        else:
            base = img.resize(size, Image.ANTIALIAS) if size else img

        base.save(temp_output, "PNG")
        try:
            subprocess.call(["nvcompress", compression_format, temp_output, dds_output])
            os.remove(temp_output)
        except Exception as e:
            messagebox.showerror("Error", f"Error during nvcompress execution: {str(e)}")

        progress_bar["value"] = i+1
        root.update_idletasks()

def reset_fields():
    input_dir_entry.delete(0, tk.END)
    output_dir_entry.delete(0, tk.END)
    compression_format_combobox.set('')
    width_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    base_image_combobox.set('')
    mask_image_combobox.set('')
    color_combobox.set('')
    resize_checkbox_var.set(0)
    invert_paste_checkbox_var.set(0)
    apply_mask_checkbox_var.set(0)


def convert_images():
    input_dir = input_dir_entry.get()
    output_dir = output_dir_entry.get()
    compression_format = compression_format_combobox.get()
    width = width_entry.get()
    height = height_entry.get()
    base_image_name = base_image_combobox.get()
    mask_image_name = mask_image_combobox.get()
    color_name = color_combobox.get()
    resize_after = resize_checkbox_var.get()
    invert_paste = invert_paste_checkbox_var.get()
    apply_mask_flag = apply_mask_checkbox_var.get()

    color = color_options.get(color_name, None)

    if not os.path.isdir(input_dir):
        messagebox.showerror("Error", f"Input directory does not exist: {input_dir}")
        return
    if not os.path.isdir(output_dir):
        messagebox.showerror("Error", f"Output directory does not exist: {output_dir}")
        return
    if width and not width.isnumeric():
        messagebox.showerror("Error", f"Invalid width: {width}")
        return
    if height and not height.isnumeric():
        messagebox.showerror("Error", f"Invalid height: {height}")
        return

    size = None
    if width and height:
        size = (int(width), int(height))
    base_image_path = None
    if base_image_name:
        base_image_path = os.path.join("Base_Image", base_image_name)
    mask_image_path = None
    if mask_image_name:
        mask_image_path = os.path.join("Mask_Image", mask_image_name)

    resize_and_paste_images(input_dir, output_dir, size, base_image_path, mask_image_path, color, compression_format, resize_after, invert_paste, apply_mask_flag)

class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None

    def show_tip(self, tip_text):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(tw, text=tip_text, background="#ffffe0", relief=tk.SOLID, borderwidth=1)
        label.pack(ipadx=1)

    def hide_tip(self):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

def create_tooltip(widget, tip_text):
    tooltip = ToolTip(widget)

    def enter(event):
        tooltip.show_tip(tip_text)

    def leave(event):
        tooltip.hide_tip()

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)



root = tk.Tk()
root.title('PNG to DDS Converter')

compression_options = ['-fast', '-production', '-highest', '-nocuda', '-rgb', '-lumi', '-bc1', '-bc1n', '-bc1a', '-bc2', '-bc3', '-bc3n', '-bc4', '-bc4s', '-ati2', '-bc5', '-bc5s', '-bc6', '-bc6s', '-bc7', '-bc3_rgbm', '-astc_ldr_4x4', '-astc_ldr_5x4', '-astc_ldr_12x12']
color_options = {'Nomal': [0, 36, 31], 'Corporate': [12, 12, 5], 'Machine': [0, 23, 33], 'Hive': [232, 221, 195], 'Agenda': [166, 255, 214], 'Bad': [35, 4, 0], 'Red': [255, 0, 0], 'Green': [0, 255, 0], 'Blue': [0, 0, 255], 'Black': [0, 0, 0], 'White': [255, 255, 255], None: None}

input_dir_label = tk.Label(root, text="Input Directory:")
input_dir_label.pack()
input_dir_entry = tk.Entry(root, width=50)
input_dir_entry.pack()
browse_input_dir_button = tk.Button(root, text="Browse...", command=browse_input_dir)
browse_input_dir_button.pack()

output_dir_label = tk.Label(root, text="Output Directory:")
output_dir_label.pack()
output_dir_entry = tk.Entry(root, width=50)
output_dir_entry.pack()
browse_output_dir_button = tk.Button(root, text="Browse...", command=browse_output_dir)
browse_output_dir_button.pack()

compression_format_label = tk.Label(root, text="Compression Format:")
compression_format_label.pack()
compression_format_combobox = ttk.Combobox(root, values=compression_options)
compression_format_combobox.pack()

width_label = tk.Label(root, text="Width:")
width_label.pack()
width_entry = tk.Entry(root, width=10)
create_tooltip(width_entry, "Enter the width here.")
width_entry.pack()

height_label = tk.Label(root, text="Height:")
height_label.pack()
height_entry = tk.Entry(root, width=10)
create_tooltip(height_entry, "Enter the height here.")
height_entry.pack()

base_image_label = tk.Label(root, text="Base Image:")
base_image_label.pack()
base_image_combobox = ttk.Combobox(root, values=os.listdir("Base_Image"), width=30)
base_image_combobox.pack()

mask_image_label = tk.Label(root, text="Mask Image:")
mask_image_label.pack()
mask_image_combobox = ttk.Combobox(root, values=os.listdir("Mask_Image"), width=30)
mask_image_combobox.pack()

apply_mask_checkbox_var = tk.IntVar()
apply_mask_checkbox = tk.Checkbutton(root, text="Apply Mask", variable=apply_mask_checkbox_var)
apply_mask_checkbox.pack()

color_label = tk.Label(root, text="Color:")
color_label.pack()
color_combobox = ttk.Combobox(root, values=list(color_options.keys()))
color_combobox.pack()

resize_checkbox_var = tk.IntVar()
resize_checkbox = tk.Checkbutton(root, text="Resize after paste", variable=resize_checkbox_var)
resize_checkbox.pack()

invert_paste_checkbox_var = tk.IntVar()
invert_paste_checkbox = tk.Checkbutton(root, text="Invert paste order", variable=invert_paste_checkbox_var)
invert_paste_checkbox.pack()

progress_bar = ttk.Progressbar(root, length=200)
progress_bar.pack()

convert_images_button = tk.Button(root, text="Convert Images", command=convert_images)
convert_images_button.pack()

reset_button = tk.Button(root, text="Reset", command=reset_fields)
reset_button.pack()

root.mainloop()
