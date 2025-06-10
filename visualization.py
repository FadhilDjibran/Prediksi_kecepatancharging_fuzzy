# visualization.py

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch 

# Impor variabel dan fungsi yang dibutuhkan dari engine fuzzy
from fuzzy_engine import suhu, kecepatan_charging, prediksi_kecepatan


def tampilkan_grafik_mf():
    plt.close('all') 
    plt.style.use('seaborn-v0_8-whitegrid')

    # Membuat 1 figure dengan 2 subplot yang disusun vertikal
    fig, (ax0, ax1) = plt.subplots(nrows=2, figsize=(8, 9))
    
    # Grafik 1: Fungsi Keanggotaan Suhu HP
    ax0.set_title('Fungsi Keanggotaan Suhu HP')
    for term_name, mf_object in suhu.terms.items():
        ax0.plot(suhu.universe, mf_object.mf, label=term_name)
    ax0.set_xlabel('Suhu (°C)')
    ax0.set_ylabel('Derajat Keanggotaan')
    ax0.legend()
    ax0.grid(True)

    # Grafik 2: Fungsi Keanggotaan Kecepatan Charging 
    ax1.set_title('Fungsi Keanggotaan Kecepatan Charging')
    for term_name, mf_object in kecepatan_charging.terms.items():
        ax1.plot(kecepatan_charging.universe, mf_object.mf, label=term_name)
    ax1.set_xlabel('Kecepatan Charging (%)')
    ax1.set_ylabel('Derajat Keanggotaan')
    ax1.legend()
    ax1.grid(True)
    plt.subplots_adjust(hspace=0.3)
    plt.show()


def tampilkan_grafik_pengelompokan():
    plt.close('all')
    plt.style.use('seaborn-v0_8-whitegrid')
    suhu_inputs_plot = np.arange(0, 55.5, 0.5)
    kecepatan_numerik_plot = []
    
    for temp in suhu_inputs_plot:
        hasil_num_str, kat = prediksi_kecepatan(temp)
        try:
            kecepatan_numerik_plot.append(float(hasil_num_str))
        except (ValueError, TypeError):
            if kat == "Tidak Charging":
                kecepatan_numerik_plot.append(0)
            else:
                kecepatan_numerik_plot.append(np.nan)
    
    plt.figure(figsize=(12, 7))
    plt.plot(suhu_inputs_plot, kecepatan_numerik_plot, color='black', linestyle='--', label='_nolegend_')
    plt.axvspan(0, 5, alpha=0.15, color='cyan', label='_nolegend_')
    plt.axvspan(18, 41, alpha=0.15, color='lightgreen', label='_nolegend_')
    plt.axvspan(50, 55, alpha=0.15, color='lightcoral', label='_nolegend_')
    
    legend_elements = [
        plt.Line2D([0], [0], color='black', linestyle='--', lw=2, label='Tren Kecepatan Prediksi'),
        Patch(facecolor='cyan', alpha=0.3, label='Zona Terlalu Dingin (<5°C)'),
        Patch(facecolor='lightgreen', alpha=0.3, label='Zona Ideal (Hyper)'),
        Patch(facecolor='lightcoral', alpha=0.3, label='Zona Terlalu Panas (>50°C)')
    ]
    plt.legend(handles=legend_elements, loc='best')
    
    plt.title('Pemetaan Input Suhu ke Output Kecepatan Charging')
    plt.xlabel('Suhu HP (°C)')
    plt.ylabel('Prediksi Kecepatan Charging (%)')
    plt.grid(True)
    plt.ylim(-5, 105)
    plt.xlim(0, 55)
    
    plt.show()