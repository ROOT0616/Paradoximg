import os
import tkinter as tk
from tkinter import filedialog, ttk, Scale
from PIL import Image, ImageTk
import numpy as np
import imageio.v3 as imageio

THUMBNAIL_SIZE = (100, 100)
DISPLAY_SIZE = (500, 500)

class ScrollableFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.frame = tk.Frame(self.canvas)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.frame.bind("<Configure>", self.on_frame_configure)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

class ImageGallery(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.images_frame = ScrollableFrame(self)
        self.images_frame.grid(row=0, column=0, sticky="nsew")
        
        self.filename_label = tk.Label(self, text="No Image Selected")
        self.filename_label.grid(row=1, column=0, sticky="n")
        
        self.zoomed_image_label = tk.Label(self)
        self.zoomed_image_label.grid(row=2, column=0, columnspan=2)
        
        self.zoom_level = 1
        self.zoom_slider = Scale(self, from_=0.4, to=5, resolution=0.1, orient="horizontal", command=self.update_zoom)
        self.zoom_slider.set(1)
        self.zoom_slider.grid(row=3, column=0, sticky="ew")
        
        self.reload_button = tk.Button(self, text="Reload", command=self.reload_folder)
        self.reload_button.grid(row=4, column=0, sticky="ew")
        
        self.images = []
        self.current_index = None
        self.current_folder = None
        self.num_columns = 5  # 画像を表示する列数
    
    def clear_images(self):
        for widget in self.images_frame.frame.winfo_children():
            widget.destroy()
        self.images.clear()
        self.current_index = None
        self.filename_label.config(text="No Image Selected")
        self.zoomed_image_label.config(image="")
    
    def add_image(self, filepath):
        try:
            image = load_and_convert_dds(filepath)
            thumbnail = image.copy()
            thumbnail.thumbnail(THUMBNAIL_SIZE)
            self.images.append((image, filepath))
            tk_image = ImageTk.PhotoImage(thumbnail)
            image_label = tk.Label(self.images_frame.frame, image=tk_image)
            image_label.image = tk_image
            image_label.bind("<Button-1>", lambda event, index=len(self.images)-1: self.show_image(index))
            
            row = len(self.images) // self.num_columns
            col = len(self.images) % self.num_columns
            image_label.grid(row=row, column=col, padx=5, pady=5)
        except Exception as e:
            print(f"Failed to load {filepath}: {e}")
    
    def show_image(self, index):
        self.current_index = index
        _, filepath = self.images[self.current_index]
        self.filename_label.config(text=filepath)
        self.update_zoomed_image()
    
    def update_zoom(self, value):
        self.zoom_level = float(value)
        self.update_zoomed_image()
    
    def update_zoomed_image(self):
        if self.current_index is None:
            return
        image, _ = self.images[self.current_index]
        resized_image = image.resize((int(DISPLAY_SIZE[0] * self.zoom_level), int(DISPLAY_SIZE[1] * self.zoom_level)))
        tk_image = ImageTk.PhotoImage(resized_image)
        self.zoomed_image_label.config(image=tk_image)
        self.zoomed_image_label.image = tk_image
    
    def reload_folder(self):
        if self.current_folder:
            update_image_list(self.current_folder)

def load_and_convert_dds(dds_file_path):
    try:
        image_data = imageio.imread(dds_file_path)
        return Image.fromarray(image_data)
    except Exception as e:
        raise IOError(f"Could not read DDS file: {e}")

def update_folder_tree(root_folder):
    folder_tree.delete(*folder_tree.get_children())
    def add_nodes(parent, path, depth=0):
        if depth > 2:
            return
        for subdir in os.listdir(path):
            subdir_path = os.path.join(path, subdir)
            if os.path.isdir(subdir_path):
                node = folder_tree.insert(parent, "end", iid=subdir_path, text=subdir, open=True)
                folder_tree.set(node, "fullpath", subdir_path)
                add_nodes(node, subdir_path, depth + 1)
    add_nodes("", root_folder)

def update_image_list(folder_path):
    gallery.clear_images()
    gallery.current_folder = folder_path
    for file in os.listdir(folder_path):
        if file.endswith('.dds'):
            gallery.add_image(os.path.join(folder_path, file))

def on_folder_select(event):
    selected_item = folder_tree.selection()
    if selected_item:
        folder_path = folder_tree.set(selected_item[0], "fullpath")
        update_image_list(folder_path)

def open_folder_dialog():
    folder_path = filedialog.askdirectory()
    if folder_path:
        update_folder_tree(folder_path)
        update_image_list(folder_path)

root = tk.Tk()
root.title("DDS Image Viewer")
root.geometry("800x600")

button = tk.Button(root, text="Open DDS Folder", command=open_folder_dialog)
button.pack()

folder_tree = ttk.Treeview(root, columns=("fullpath",), displaycolumns="")
folder_tree.pack(side="left", fill="y")
folder_tree.bind("<<TreeviewSelect>>", on_folder_select)

gallery = ImageGallery(root)
gallery.pack(expand=True, fill="both")

root.mainloop()
