# -*- coding: utf-8 -*-
"""
Generate Pseudo dataset of time response
Output format to the text file
  [y0, y1, ... , ymax], respond_type

@author: Eko Mursito Budi
di sini, gw cuma edit tipis2 aja

kekny banyak yg salah di kode ini.
"""
import random as rd
import time as time
import scipy.signal as ss
import numpy as np
import matplotlib.pyplot as plt


# Output file
file_name = "orde2_updated.csv"

# number of data, defaulnya 1000
max_data = 1000

# Minimal 128
max_sample = 256

# orde 2 parameter range
range_gain = [1, 3]
range_wn = [0.1, 1]

# maximum noise
max_noise = 0.05

# maximum data yang diplot ke grfik
max_plot = 10

# response type
response_types = ["undamped", "under_damped","critically_damped","over_damped"]

# waktu
x_time = np.arange(max_sample)

def step_orde2(gain=1, psi=1, wn=10):
    # buat sistem orde 2
    a0 = 1.0
    a1 = 2.0 * psi / wn
    a2 = 1 / (wn * wn)

    b0 = gain

    sys = ss.lti([b0], [a2, a1, a0])

    # hitung step response
    t,y = ss.step(sys, T=x_time)

    # tambah sedikit noise
    noise = max_noise * np.random.normal(size=y.shape)
    y_noisy = y + noise

    return y_noisy


def gen_step():
    # random parameter orde 2
    k = rd.uniform(range_gain[0], range_gain[1])
    wn = rd.uniform(range_wn[0], range_wn[1])
    """
    Disini, gw cuma mau coba bikin kode yg variasi dari class-nya, hampir mirip agar MEMUDAHKAN PROSES TRAINING.
    yk, klo lu berhadapan dengan class imbalance, akan lebih menyakitkan lagi saat melakukan proses oversampling atau class weighting (utk yg minor).
    Anggep aja, ini adalah salah satu proses dari "Data Cleaning"
    """

    # Menghasilkan angka acak antara 0 dan 99 (100 kemungkinan nilai)
    # Kita bagi 100 kemungkinan ini menjadi 4 bagian yang kurang lebih sama
    rtype_val = rd.randint(0, 99)

    if rtype_val < 25:         # Peluang 25/100 (25%) untuk undamped
        psi = 0
        d = 0
    elif rtype_val < 50:       # Peluang (50-25)/100 = 25/100 (25%) untuk under_damped
        psi = 0.05 + rd.random()*0.9 # Menjaga range psi yang valid untuk under_damped
        d = 1
    elif rtype_val < 75:       # Peluang (75-50)/100 = 25/100 (25%) untuk critically_damped
        psi = 1.0
        d = 2
    else:                      # Peluang (100-75)/100 = 25/100 (25%) untuk over_damped
        psi = 1.05 + rd.random()*10 # Menjaga range psi yang valid untuk over_damped
        d = 3

    y = step_orde2(gain=k, psi=psi, wn=wn)

    return y, d, k, wn, psi


# Main program

# Randomize based on time
current_time = time.time()
rd.seed(current_time)

# simpan untuk plot
y_plot=[]
l_plot=[]
i_plot = 0

# counter type
ctype = [0,0,0,0]

# buat dataset
# open file
with open(file_name, 'w') as file:

    header = "response, type"
    print(header)
    file.write(header+"\n")

    for i in range(max_data):
        y, rtype, k, wn, psi = gen_step()

        tt = response_types[rtype]

        # count the types
        ctype[rtype] += 1

        # simpan ke file
        # Mengubah format penyimpanan y agar lebih mudah dibaca dan diproses nanti
        """
        fyi, di sini gw cuman ngubah agar output dalam excelnya itu berbentuk "[array1 array2 array3], tipe"
        karena, di kode "gen_orde2" awal ngga kek gitu hasilnya. dah, 'sami'na wa atho'na" aja yagesya
        """
        # [y0 y1 ... y_max_sample-1]
        y_str = " ".join(map(str, y)) # Pisahkan nilai y dengan spasi
        line = f"[{y_str}],{tt}"
        file.write(line+"\n")

        # simpan untuk plot
        if i_plot < max_plot:
            i_plot += 1
            y_plot.append(y)
            desc = tt
            l_plot.append(desc)
            # Hanya print data yang akan diplot untuk mengurangi output console
            if i < max_plot:
                print(f"Data {i+1}: Type={tt}, k={k:.2f}, wn={wn:.2f}, psi={psi:.2f}")


# Laporkan hasilnya
print("----------------")
print("Response Count:")
for i in range(4):
    print(f"{response_types[i]} : {ctype[i]}")


# Plot hasilnya sebanyak max_plot saja
plt.figure(figsize=(10, 5))
for i in range(max_plot):
    plt.plot(x_time, y_plot[i], label=l_plot[i])

plt.legend(loc='upper right', bbox_to_anchor=(1.25, 1))

plt.xlabel("Time (s)")
plt.ylabel("Response")
plt.title("Step Response of Second-Order System")
plt.tight_layout()
plt.grid(True)
plt.show()
