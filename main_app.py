# main_app.py

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

# Impor fungsi prediksi dari engine fuzzy
from fuzzy_engine import prediksi_kecepatan
# Impor fungsi-fungsi visualisasi
from visualization import tampilkan_grafik_mf, tampilkan_grafik_pengelompokan

class ChargingApp:
    def __init__(self, master):
        self.master = master
        master.title("Prediksi Kecepatan Charging HP & Visualisasi Fuzzy")
        master.geometry("440x500") 

        main_frame = ttk.Frame(master, padding="10 10 10 10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Bagian Input
        input_frame = ttk.LabelFrame(main_frame, text="Input Suhu", padding="10", bootstyle="info")
        input_frame.pack(pady=10, fill=tk.X)
        self.entry_suhu_var = tk.StringVar(value="25")
        
        ttk.Label(input_frame, text="Masukkan Suhu HP (°C):").pack(side=tk.LEFT, padx=(0, 5))
        
        entry_suhu = ttk.Entry(input_frame, width=10, textvariable=self.entry_suhu_var, justify=tk.CENTER)
        entry_suhu.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(input_frame, text="(5-50°C)").pack(side=tk.LEFT)

        ttk.Button(main_frame, text="Prediksi Kecepatan Charging", command=self.tampilkan_prediksi, bootstyle="primary").pack(pady=10, fill=tk.X, ipady=5)

        # Bagian Hasil
        result_frame = ttk.LabelFrame(main_frame, text="Hasil Prediksi", padding="10", bootstyle="info")
        result_frame.pack(pady=10, expand=True, fill=tk.BOTH)
        self.hasil_numerik_var = tk.StringVar(value="-")
        self.hasil_kategori_var = tk.StringVar(value="-")
        
        ttk.Label(result_frame, text="Kecepatan Numerik (%):").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        ttk.Label(result_frame, textvariable=self.hasil_numerik_var, font=("-size 12 -weight bold")).grid(row=1, column=0, sticky=tk.W)
        ttk.Label(result_frame, text="Kategori Charging:").grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        ttk.Label(result_frame, textvariable=self.hasil_kategori_var, font=("-size 12 -weight bold"), bootstyle="success").grid(row=3, column=0, sticky=tk.W)
        result_frame.columnconfigure(0, weight=1)

        # Tombol Grafik
        graph_button_frame = ttk.Frame(main_frame)
        graph_button_frame.pack(pady=10, fill=tk.X)
        ttk.Button(graph_button_frame, text="Grafik Fungsi Keanggotaan", command=tampilkan_grafik_mf, bootstyle="success-outline").pack(side=tk.LEFT, expand=True, padx=5)
        ttk.Button(graph_button_frame, text="Grafik Pemetaan", command=tampilkan_grafik_pengelompokan, bootstyle="success-outline").pack(side=tk.LEFT, expand=True, padx=5)

        self.tampilkan_prediksi()

    def tampilkan_prediksi(self):
        try:
            suhu_input = float(self.entry_suhu_var.get())
            hasil_numerik, kategori = prediksi_kecepatan(suhu_input)
            self.hasil_numerik_var.set(hasil_numerik)
            self.hasil_kategori_var.set(kategori)

            if "Terlalu" in hasil_numerik:
                messagebox.showwarning("Peringatan Suhu", f"{hasil_numerik}. Tidak ada proses charging.", parent=self.master)
                self.hasil_numerik_var.set("-")
        except ValueError:
            messagebox.showerror("Input Tidak Valid", "Masukkan angka yang valid untuk suhu.", parent=self.master)
            self.hasil_numerik_var.set("-")
            self.hasil_kategori_var.set("Error Input")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan tak terduga: {e}", parent=self.master)

# Titik masuk aplikasi
if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = ChargingApp(root)
    root.mainloop()