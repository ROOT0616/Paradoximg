import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
import numpy as np
from PIL import Image
import json

# --- カレントディレクトリ対策 ---
# スクリプトのあるディレクトリを取得し、そのフォルダを基準に各種フォルダのパスを生成
script_dir = os.path.dirname(os.path.abspath(__file__))
base_image_dir = os.path.join(script_dir, "Base_Image")
mask_image_dir = os.path.join(script_dir, "Mask_Image")
FAVORITES_FILE = os.path.join(script_dir, "favorite_settings.json")
# ---------------------------------

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
    return Image.composite(image.resize(mask.size, Image.LANCZOS), mask, mask)

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

        # 色変換
        if color:
            img = apply_color(img, color)

        # 「マスクを適用」チェックがあり、かつ「マスクを最後に適用」チェックがOFFの場合は、早い段階でマスクを適用
        if apply_mask_checkbox_var.get() and mask_image_path and not mask_last_checkbox_var.get():
            img = apply_mask(img, mask_image_path)

        # 基本画像との合成処理
        if base_image:
            # invert_paste と resize_after の両方がTrueの場合
            if invert_paste and resize_after:
                if size:
                    base = base_image.copy()
                    position = ((img.width - base.width) // 2, (img.height - base.height) // 2)
                    img.paste(base, position, base)
                    base = img.resize(size, Image.LANCZOS)
                else:
                    # サイズ指定がない場合はリサイズせずそのまま貼り付け
                    base = base_image.copy()
                    position = ((img.width - base.width) // 2, (img.height - base.height) // 2)
                    img.paste(base, position, base)
                    base = img
            # invert_paste または resize_after のどちらかがTrueの場合
            elif invert_paste or resize_after:
                if invert_paste:
                    if size:
                        img = img.resize(size, Image.LANCZOS)
                    base = base_image.copy()
                    position = ((img.width - base.width) // 2, (img.height - base.height) // 2)
                    img.paste(base, position, base)
                    base = img
                else:  # resize_after のみTrueの場合
                    base = base_image.copy()
                    position = ((base.width - img.width) // 2, (base.height - img.height) // 2)
                    base.paste(img, position, img)
                    if size:
                        base = base.resize(size, Image.LANCZOS)
            else:
                # どちらのチェックもされていない場合
                base = base_image.copy()
                if size:
                    img = img.resize(size, Image.LANCZOS)
                position = ((base.width - img.width) // 2, (base.height - img.height) // 2)
                base.paste(img, position, img)
        else:
            # Base Image が指定されていない場合は入力画像自体をサイズ変更（指定があれば）して出力
            if size:
                base = img.resize(size, Image.LANCZOS)
            else:
                base = img

        # 「マスクを最後に適用」チェックがONの場合は、合成後にマスクを適用
        if apply_mask_checkbox_var.get() and mask_image_path and mask_last_checkbox_var.get():
            base = apply_mask(base, mask_image_path)

        base.save(temp_output, "PNG")
        try:
            subprocess.call(["nvcompress", compression_format, temp_output, dds_output])
            os.remove(temp_output)
        except Exception as e:
            messagebox.showerror("Error", f"Error during nvcompress execution: {str(e)}")

        progress_bar["value"] = i + 1
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
    mask_last_checkbox_var.set(0)

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
        default_size = (256, 256)  # デフォルトサイズ
        size = (int(width), int(height)) if width and height else default_size
    base_image_path = None
    if base_image_name:
        # 絶対パスでBase_Imageフォルダ内を指定
        base_image_path = os.path.join(base_image_dir, base_image_name)
    mask_image_path = None
    if mask_image_name:
        # 絶対パスでMask_Imageフォルダ内を指定
        mask_image_path = os.path.join(mask_image_dir, mask_image_name)

    resize_and_paste_images(input_dir, output_dir, size, base_image_path, mask_image_path, color, compression_format, resize_after, invert_paste, apply_mask_flag)

def save_favorite_settings():
    """現在の各種設定をお気に入りとして JSON ファイルに保存する（複数保存可能）"""
    fav_name = simpledialog.askstring("お気に入りの保存", "お気に入り設定の名前を入力してください：")
    if not fav_name:
        return

    settings = {
        "input_dir": input_dir_entry.get(),
        "output_dir": output_dir_entry.get(),
        "compression_format": compression_format_combobox.get(),
        "width": width_entry.get(),
        "height": height_entry.get(),
        "base_image": base_image_combobox.get(),
        "mask_image": mask_image_combobox.get(),
        "color": color_combobox.get(),
        "resize_after": resize_checkbox_var.get(),
        "invert_paste": invert_paste_checkbox_var.get(),
        "apply_mask": apply_mask_checkbox_var.get(),
        "mask_last": mask_last_checkbox_var.get()
    }

    # 既存のお気に入りを読み込み
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
            favorites = json.load(f)
    else:
        favorites = {}

    # 同名のお気に入りが存在する場合は上書き確認
    if fav_name in favorites:
        if not messagebox.askyesno("上書き確認", f"「{fav_name}」は既に存在します。上書きしてもよろしいですか？"):
            return

    favorites[fav_name] = settings

    try:
        with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
            json.dump(favorites, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("お気に入り保存", "お気に入り設定を保存しました。")
        update_favorites_combobox()
    except Exception as e:
        messagebox.showerror("エラー", f"お気に入り設定の保存に失敗しました: {str(e)}")

def load_favorite_settings():
    """コンボボックスで選択されたお気に入り設定を読み込み、各ウィジェットに反映する"""
    fav_name = favorites_combobox.get()
    if not fav_name:
        messagebox.showerror("エラー", "読み込みたいお気に入りを選択してください。")
        return

    try:
        with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
            favorites = json.load(f)
        settings = favorites.get(fav_name)
        if not settings:
            messagebox.showerror("エラー", "選択されたお気に入り設定が見つかりません。")
            return

        input_dir_entry.delete(0, tk.END)
        input_dir_entry.insert(0, settings.get("input_dir", ""))
        output_dir_entry.delete(0, tk.END)
        output_dir_entry.insert(0, settings.get("output_dir", ""))
        compression_format_combobox.set(settings.get("compression_format", ""))
        width_entry.delete(0, tk.END)
        width_entry.insert(0, settings.get("width", ""))
        height_entry.delete(0, tk.END)
        height_entry.insert(0, settings.get("height", ""))
        base_image_combobox.set(settings.get("base_image", ""))
        mask_image_combobox.set(settings.get("mask_image", ""))
        color_combobox.set(settings.get("color", ""))
        resize_checkbox_var.set(settings.get("resize_after", 0))
        invert_paste_checkbox_var.set(settings.get("invert_paste", 0))
        apply_mask_checkbox_var.set(settings.get("apply_mask", 0))
        mask_last_checkbox_var.set(settings.get("mask_last", 0))
        messagebox.showinfo("お気に入り読み込み", f"お気に入り設定「{fav_name}」を読み込みました。")
    except Exception as e:
        messagebox.showerror("エラー", f"お気に入り設定の読み込みに失敗しました: {str(e)}")

def update_favorites_combobox():
    """お気に入り設定のファイルから、コンボボックスの項目を更新する"""
    if os.path.exists(FAVORITES_FILE):
        try:
            with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
                favorites = json.load(f)
            fav_names = list(favorites.keys())
        except Exception:
            fav_names = []
    else:
        fav_names = []
    favorites_combobox['values'] = fav_names

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

# Input Directory
frame_input_dir = tk.Frame(root)
frame_input_dir.pack(padx=5, pady=2, anchor='center')
input_dir_label = tk.Label(frame_input_dir, text="Input Directory:")
input_dir_label.pack(side=tk.LEFT)

input_dir_entry = tk.Entry(root, width=50)
input_dir_entry.pack(anchor='center')
browse_input_dir_button = tk.Button(root, text="Browse...", command=browse_input_dir)
browse_input_dir_button.pack(anchor='center')

# Output Directory
frame_output_dir = tk.Frame(root)
frame_output_dir.pack(padx=5, pady=2, anchor='center')
output_dir_label = tk.Label(frame_output_dir, text="Output Directory:")
output_dir_label.pack(side=tk.LEFT)

output_dir_entry = tk.Entry(root, width=50)
output_dir_entry.pack(anchor='center')
browse_output_dir_button = tk.Button(root, text="Browse...", command=browse_output_dir)
browse_output_dir_button.pack(anchor='center')

# Compression Format
frame_compression = tk.Frame(root)
frame_compression.pack(padx=5, pady=2, anchor='center')
compression_format_label = tk.Label(frame_compression, text="Compression Format:")
compression_format_label.pack(side=tk.LEFT)
explain_compression_button = tk.Button(frame_compression, text="説明", command=lambda: messagebox.showinfo("Compression Format", "画像をDDS形式に変換する際の圧縮オプションを選択します。"))
explain_compression_button.pack(side=tk.LEFT, padx=5)

compression_format_combobox = ttk.Combobox(root, values=compression_options)
compression_format_combobox.pack(anchor='center')

# Width
frame_width = tk.Frame(root)
frame_width.pack(padx=5, pady=2, anchor='center')
width_label = tk.Label(frame_width, text="Width:")
width_label.pack(side=tk.LEFT)
explain_width_button = tk.Button(frame_width, text="説明", command=lambda: messagebox.showinfo("Width", "変換後の画像の幅を指定します。数字のみ入力可能です。"))
explain_width_button.pack(side=tk.LEFT, padx=5)

width_entry = tk.Entry(root, width=10)
create_tooltip(width_entry, "Enter the width here.")
width_entry.pack(anchor='center')

# Height
frame_height = tk.Frame(root)
frame_height.pack(padx=5, pady=2, anchor='center')
height_label = tk.Label(frame_height, text="Height:")
height_label.pack(side=tk.LEFT)
explain_height_button = tk.Button(frame_height, text="説明", command=lambda: messagebox.showinfo("Height", "変換後の画像の高さを指定します。数字のみ入力可能です。"))
explain_height_button.pack(side=tk.LEFT, padx=5)

height_entry = tk.Entry(root, width=10)
create_tooltip(height_entry, "Enter the height here.")
height_entry.pack(anchor='center')

# Base Image
frame_base_image = tk.Frame(root)
frame_base_image.pack(padx=5, pady=2, anchor='center')
base_image_label = tk.Label(frame_base_image, text="Base Image:")
base_image_label.pack(side=tk.LEFT)
explain_base_image_button = tk.Button(frame_base_image, text="説明", command=lambda: messagebox.showinfo("Base Image", "貼り付けの基準となる画像を選択します。"))
explain_base_image_button.pack(side=tk.LEFT, padx=5)

# os.listdir()の対象を絶対パスに変更
base_image_combobox = ttk.Combobox(root, values=os.listdir(base_image_dir), width=30)
base_image_combobox.pack(anchor='center')

# Mask Image
frame_mask_image = tk.Frame(root)
frame_mask_image.pack(padx=5, pady=2, anchor='center')
mask_image_label = tk.Label(frame_mask_image, text="Mask Image:")
mask_image_label.pack(side=tk.LEFT)
explain_mask_image_button = tk.Button(frame_mask_image, text="説明", command=lambda: messagebox.showinfo("Mask Image", "マスクを適用する際のマスク画像を選択します。"))
explain_mask_image_button.pack(side=tk.LEFT, padx=5)

mask_image_combobox = ttk.Combobox(root, values=os.listdir(mask_image_dir), width=30)
mask_image_combobox.pack(anchor='center')

# Apply Mask Checkbox
apply_mask_checkbox_var = tk.IntVar()
frame_apply_mask = tk.Frame(root)
frame_apply_mask.pack(padx=5, pady=2, anchor='center')
apply_mask_checkbox = tk.Checkbutton(frame_apply_mask, text="Apply Mask", variable=apply_mask_checkbox_var)
apply_mask_checkbox.pack(side=tk.LEFT)
explain_apply_mask_button = tk.Button(frame_apply_mask, text="説明", command=lambda: messagebox.showinfo("Apply Mask", "チェックすると、指定したマスク画像が適用されます。"))
explain_apply_mask_button.pack(side=tk.LEFT, padx=5)

# Mask Last Checkbox（マスクを合成後に適用するかどうか）
mask_last_checkbox_var = tk.IntVar()
frame_mask_last = tk.Frame(root)
frame_mask_last.pack(padx=5, pady=2, anchor='center')
mask_last_checkbox = tk.Checkbutton(frame_mask_last, text="マスクを最後に適用", variable=mask_last_checkbox_var)
mask_last_checkbox.pack(side=tk.LEFT)
explain_mask_last_button = tk.Button(frame_mask_last, text="説明", command=lambda: messagebox.showinfo("マスクを最後に適用", "チェックすると、画像の合成処理が完了した後に、マスク画像を適用します。"))
explain_mask_last_button.pack(side=tk.LEFT, padx=5)

# Color
frame_color = tk.Frame(root)
frame_color.pack(padx=5, pady=2, anchor='center')
color_label = tk.Label(frame_color, text="Color:")
color_label.pack(side=tk.LEFT)
explain_color_button = tk.Button(frame_color, text="説明", command=lambda: messagebox.showinfo("Color", "画像の色調補正に使用する色を選択します。"))
explain_color_button.pack(side=tk.LEFT, padx=5)

color_combobox = ttk.Combobox(root, values=list(color_options.keys()))
color_combobox.pack(anchor='center')

# Resize after paste Checkbox
resize_checkbox_var = tk.IntVar()
frame_resize = tk.Frame(root)
frame_resize.pack(padx=5, pady=2, anchor='center')
resize_checkbox = tk.Checkbutton(frame_resize, text="Resize after paste", variable=resize_checkbox_var)
resize_checkbox.pack(side=tk.LEFT)
explain_resize_button = tk.Button(frame_resize, text="説明", command=lambda: messagebox.showinfo("Resize after paste", "チェックすると、貼り付け後にリサイズ処理を行います。"))
explain_resize_button.pack(side=tk.LEFT, padx=5)

# Invert paste order Checkbox
invert_paste_checkbox_var = tk.IntVar()
frame_invert = tk.Frame(root)
frame_invert.pack(padx=5, pady=2, anchor='center')
invert_paste_checkbox = tk.Checkbutton(frame_invert, text="Invert paste order", variable=invert_paste_checkbox_var)
invert_paste_checkbox.pack(side=tk.LEFT)
explain_invert_button = tk.Button(frame_invert, text="説明", command=lambda: messagebox.showinfo("Invert paste order", "チェックすると、貼り付ける順序が反転します。"))
explain_invert_button.pack(side=tk.LEFT, padx=5)

# Progress Bar
frame_progress = tk.Frame(root)
frame_progress.pack(padx=5, pady=2, anchor='center')
progress_bar = ttk.Progressbar(frame_progress, length=200)
progress_bar.pack(side=tk.LEFT)

# Convert Images Button
frame_convert = tk.Frame(root)
frame_convert.pack(padx=5, pady=2, anchor='center')
convert_images_button = tk.Button(frame_convert, text="Convert Images", command=convert_images)
convert_images_button.pack(side=tk.LEFT)

# Reset Button
frame_reset = tk.Frame(root)
frame_reset.pack(padx=5, pady=2, anchor='center')
reset_button = tk.Button(frame_reset, text="Reset", command=reset_fields)
reset_button.pack(side=tk.LEFT)

# お気に入り設定保存／読み込み用ボタンとコンボボックス
frame_favorites = tk.Frame(root)
frame_favorites.pack(padx=5, pady=2, anchor='center')

save_favorite_button = tk.Button(frame_favorites, text="お気に入りを保存", command=save_favorite_settings)
save_favorite_button.pack(side=tk.LEFT, padx=5)

load_favorite_button = tk.Button(frame_favorites, text="お気に入りを読み込み", command=load_favorite_settings)
load_favorite_button.pack(side=tk.LEFT, padx=5)

favorites_label = tk.Label(frame_favorites, text="保存済みお気に入り:")
favorites_label.pack(side=tk.LEFT, padx=5)

favorites_combobox = ttk.Combobox(frame_favorites, width=20)
favorites_combobox.pack(side=tk.LEFT)
update_favorites_combobox()

root.mainloop()
