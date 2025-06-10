# fuzzy_engine.py

import numpy as np
import skfuzzy as fuzz 
from skfuzzy import control as ctrl

# 1. Definisikan Variabel (Antecedent & Consequent)
suhu = ctrl.Antecedent(np.arange(5, 51, 1), 'suhu')
kecepatan_charging = ctrl.Consequent(np.arange(0, 101, 1), 'kecepatan_charging')

# 2. Definisikan Fungsi Keanggotaan (Membership Functions)
# Untuk Suhu
suhu['sangat_dingin'] = fuzz.trapmf(suhu.universe, [5, 5, 8, 12])
suhu['dingin'] = fuzz.trapmf(suhu.universe, [8, 12, 16, 21])
suhu['normal'] = fuzz.trapmf(suhu.universe, [17, 24, 36, 43])
suhu['panas'] = fuzz.trapmf(suhu.universe, [39, 42, 46, 48])
suhu['sangat_panas'] = fuzz.trapmf(suhu.universe, [45, 47, 50, 50])

# Untuk Kecepatan Charging
kecepatan_charging['safe'] = fuzz.trimf(kecepatan_charging.universe, [0, 25, 50])
kecepatan_charging['normal'] = fuzz.trimf(kecepatan_charging.universe, [40, 65, 90])
kecepatan_charging['hyper'] = fuzz.trimf(kecepatan_charging.universe, [80, 90, 100])

# 3. Definisikan Aturan (Rules)
rule1 = ctrl.Rule(suhu['sangat_dingin'], kecepatan_charging['safe'])
rule2 = ctrl.Rule(suhu['dingin'], kecepatan_charging['normal'])
rule3 = ctrl.Rule(suhu['normal'], kecepatan_charging['hyper'])
rule4 = ctrl.Rule(suhu['panas'], kecepatan_charging['normal'])
rule5 = ctrl.Rule(suhu['sangat_panas'], kecepatan_charging['safe'])

# 4. Buat Sistem Kontrol dan Simulasi
charging_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
charging_simulation = ctrl.ControlSystemSimulation(charging_ctrl)

def prediksi_kecepatan(temperatur_input):
    
    # Fungsi utama untuk melakukan prediksi berdasarkan input suhu.
    # Mengembalikan nilai numerik dan kategori.
    
    # Menangani outlier
    if temperatur_input < 5:
        return "Suhu < 5°C: Terlalu Dingin", "Tidak Charging"
    if temperatur_input > 50:
        return "Suhu > 50°C: Terlalu Panas", "Tidak Charging"

    charging_simulation.input['suhu'] = temperatur_input
    
    try:
        charging_simulation.compute()
        output_charging = charging_simulation.output['kecepatan_charging']

        # Mengkategorikan hasil output
        if output_charging <= 40:
            kategori = "Safe Charging"
        elif output_charging <= 75:
            kategori = "Normal Charging"
        else:
            kategori = "Hyper Charging"
        return f"{output_charging:.2f}", kategori
        
    except ValueError:
        return "Tidak ada aturan aktif", "Tidak Terdefinisi"
    except Exception as e:
        return f"Error: {e}", "Tidak Terdefinisi"