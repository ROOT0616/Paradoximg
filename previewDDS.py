import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import numpy as np
import imageio

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
        self.zoomed_image_label = tk.Label(self)
        self.zoom_level = 1  # add a zoom level
        self.zoom_in_button = tk.Button(self, text="+", command=self.zoom_in)  # add zoom in button
        self.zoom_out_button = tk.Button(self, text="-", command=self.zoom_out)  # add zoom out button
        self.next_button = tk.Button(self, text="Next", command=self.show_next)
        self.prev_button = tk.Button(self, text="Prev", command=self.show_prev)

        self.images_frame.pack(side="left", fill="both", expand=True)
        self.zoomed_image_label.pack(side="top", fill="both")
        self.zoom_in_button.pack(side="left")
        self.zoom_out_button.pack(side="left")
        self.prev_button.pack(side="left")
        self.next_button.pack(side="right")

        self.images = []
        self.current_index = None

    def add_image(self, filepath):
        image = load_and_convert_dds(filepath)
        self.images.append((image, filepath))

        tk_image = ImageTk.PhotoImage(image)
        image_label = tk.Label(self.images_frame.frame, image=tk_image)
        image_label.image = tk_image  # keep a reference to the image
        image_label.bind("<Button-1>", lambda event, index=len(self.images)-1: self.show_image(index))
        image_label.grid(row=len(self.images) // 10, column=len(self.images) % 10)

    def show_image(self, index):
        self.current_index = index
        self.update_zoomed_image()

    def update_zoomed_image(self):
        image, filepath = self.images[self.current_index]
        image = image.resize((image.size[0]*self.zoom_level, image.size[1]*self.zoom_level))  # zoom the image

        tk_image = ImageTk.PhotoImage(image)
        self.zoomed_image_label.config(image=tk_image)
        self.zoomed_image_label.image = tk_image  # keep a reference to the image

    def zoom_in(self):
        if self.zoom_level < 10:  # max zoom level is 4
            self.zoom_level += 1
            self.update_zoomed_image()

    def zoom_out(self):
        if self.zoom_level > 1:  # min zoom level is 1
            self.zoom_level -= 1
            self.update_zoomed_image()

    def show_next(self):
        if self.current_index is not None and self.current_index < len(self.images) - 1:
            self.show_image(self.current_index + 1)

    def show_prev(self):
        if self.current_index is not None and self.current_index > 0:
            self.show_image(self.current_index - 1)

def load_and_convert_dds(dds_file_path):
    image_data = imageio.imread(dds_file_path)
    image = Image.fromarray(image_data)
    return image

def open_folder_dialog():
    folder_path = filedialog.askdirectory()
    if folder_path:
        dds_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.dds')]
        for dds_file in dds_files:
            gallery.add_image(dds_file)

root = tk.Tk()
button = tk.Button(root, text="Open DDS Folder", command=open_folder_dialog)
button.pack()
gallery = ImageGallery(root)
gallery.pack(fill="both", expand=True)
root.mainloop()
