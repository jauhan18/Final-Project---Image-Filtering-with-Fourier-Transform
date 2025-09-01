import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

from proses_gambar import apply_frequency_filter

class ImageFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Filter Gambar Domain Frekuensi")
        self.root.geometry("1000x600")

        self.image_path = None
        self.original_image_cv = None

        # --- Tata Letak Utama ---
        # Frame untuk kontrol di atas
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # Frame untuk gambar di bawah
        image_frame = ttk.Frame(self.root, padding="10")
        image_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # --- Widget Kontrol ---
        # Tombol Pilih Gambar
        self.btn_select = ttk.Button(control_frame, text="Pilih Gambar...", command=self.select_image)
        self.btn_select.pack(side=tk.LEFT, padx=5, pady=5)

        # Pilihan Tipe Filter (Radio Button)
        self.filter_type = tk.StringVar(value="low")
        ttk.Label(control_frame, text="Tipe Filter:").pack(side=tk.LEFT, padx=(20, 5), pady=5)
        ttk.Radiobutton(control_frame, text="Low-pass (Blur)", variable=self.filter_type, value="low").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(control_frame, text="High-pass (Tepi)", variable=self.filter_type, value="high").pack(side=tk.LEFT, padx=5)

        # Slider untuk Radius
        ttk.Label(control_frame, text="Radius Filter:").pack(side=tk.LEFT, padx=(20, 5), pady=5)
        self.radius_slider = ttk.Scale(control_frame, from_=1, to=200, orient=tk.HORIZONTAL, length=200)
        self.radius_slider.set(30)
        self.radius_slider.pack(side=tk.LEFT, padx=5)

        # Tombol Terapkan Filter
        self.btn_apply = ttk.Button(control_frame, text="Terapkan Filter", command=self.apply_filter_and_display)
        self.btn_apply.pack(side=tk.LEFT, padx=20, pady=5)

        # --- Area Tampilan Gambar ---
        # Panel Gambar Asli
        self.panel_original = ttk.Label(image_frame, text="Gambar Asli Akan Tampil di Sini", relief="solid", anchor=tk.CENTER)
        self.panel_original.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Panel Gambar Hasil Filter
        self.panel_filtered = ttk.Label(image_frame, text="Gambar Hasil Filter Akan Tampil di Sini", relief="solid", anchor=tk.CENTER)
        self.panel_filtered.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def select_image(self):
        # Membuka dialog untuk memilih file gambar
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
        if not path:
            return
        
        self.image_path = path
        self.original_image_cv = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        
        # Tampilkan gambar asli
        self.display_image(self.original_image_cv, self.panel_original)
        # Hapus gambar hasil filter sebelumnya
        self.panel_filtered.config(image=None, text="Gambar Hasil Filter Akan Tampil di Sini")
        self.panel_filtered.image = None


    def apply_filter_and_display(self):
        if self.image_path is None:
            messagebox.showerror("Error", "Silakan pilih gambar terlebih dahulu!")
            return
            
        filter_type = self.filter_type.get()
        radius = int(self.radius_slider.get())

        # Panggil fungsi 'otak' dari file proses_gambar.py
        _, filtered_image = apply_frequency_filter(self.image_path, filter_type, radius)
        
        if filtered_image is not None:
            # Tampilkan gambar hasil filter
            self.display_image(filtered_image, self.panel_filtered)

    def display_image(self, img_cv, panel):
        # Konversi gambar dari format OpenCV/Numpy ke format yang bisa dibaca Tkinter
        img_pil = Image.fromarray(img_cv.astype(np.uint8))
        
        # Resize gambar agar pas di panel (misal, maks 450x450) tanpa merusak rasio
        w, h = img_pil.size
        max_size = 450
        if w > max_size or h > max_size:
            ratio = min(max_size / w, max_size / h)
            img_pil = img_pil.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
            
        img_tk = ImageTk.PhotoImage(image=img_pil)
        
        # Tampilkan di panel
        panel.config(image=img_tk, text="")
        panel.image = img_tk # Simpan referensi agar gambar tidak hilang (penting!)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageFilterApp(root)
    root.mainloop()