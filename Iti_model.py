import control as ctrl
import plotly.graph_objects as go
import matplotlib.pyplot as plt

import numpy as np

import pandas as pd
from scipy.signal import spectrogram

from plotly.subplots import make_subplots
vib_signals = pd.read_csv("synthetic_mwd_signals.csv")

n_frec_in_Hertz = 200
fs = 1000

natural_frequency = n_frec_in_Hertz * 2 * np.pi  #200 Hz

zeta = 0.7

num = [natural_frequency**2]

den = [1, 2*natural_frequency*zeta, natural_frequency**2]

G = ctrl.TransferFunction(num, den)

print(G)



time, response = ctrl.impulse_response(G)



plt.plot(time, response)

plt.title("Impulse Response")

plt.xlabel("Time (s)")

plt.ylabel("Amplitude")

plt.grid(True)

plt.savefig("Impulse_Response.png")



ctrl.bode_plot(

    G,

    dB = True,

    Hz = True,

    deg = True,

    margins = True,

    color = "blue",

    initial_phase = 0

)

plt.savefig("Bode Diagram")

Axial_vibration = vib_signals["Axial_Vibration_G"].to_numpy()

tiempo = vib_signals["Time"].to_numpy()

t_out, y_out = ctrl.forced_response(G, tiempo, Axial_vibration)

plt.figure()

plt.plot(t_out, y_out)

plt.plot(tiempo, Axial_vibration)

plt.title("System Forced Response")

plt.xlabel("Tiempo (s)")

plt.ylabel("Amplitud")

plt.grid(True)



plt.savefig("System_Forced_response.png")
#Es pectrograma para la señal de salida del sensor
frecuencias, tiempos, espectrograma = spectrogram(y_out, fs, nperseg = 250)
#Espectrograma para la señal orginal
frecuencias_r, tiempos_r, espectrograma_r = spectrogram(Axial_vibration, fs, nperseg = 250)

plt.show() 


fig_mixed = make_subplots(rows = 1, cols = 2, #shared_yaxes = True,
subplot_titles = ("Signal throught sensor", "Real Signal")
)
fig_mixed.add_trace(
    go.Heatmap(
        z = espectrograma,
        x = tiempos,
        y = frecuencias,
        colorscale = "Viridis",
        colorbar = dict(
            title = "G2/Hz",
            x = 0.45
        )
    ),
        row = 1, col = 1
)

fig_mixed.add_trace(
    go.Heatmap(
        z = espectrograma_r,
        x = tiempos_r,
        y = frecuencias_r,
        colorscale = "Viridis",
        colorbar = dict(
            title = "G2/Hz",
            x = 1.0
        )
    ),
        row = 1, col = 2
)

fig_mixed.update_layout(
title_text = "Real Signal VS Detected Signal by Sensor",
yaxis = dict(
    title = "Frequency (Hz)",
    range = [0,500],
    dtick = 50,
    showgrid = True # 
),

xaxis = dict(
    title = "Time (s)",
    dtick = 0.5,
    showgrid = True # 
),
yaxis2 = dict(
    title = "Frequency (Hz)", # 
    range = [0,500],
    dtick = 50,
    showgrid = True # 
),

xaxis2 = dict(
    title = "Time (s)",
    dtick = 0.5,
    showgrid = True # 
)

)
# fig.show()
# fig_whirl.show()

fig_mixed.show()


# APÉNDICE
#En esta parte uso SYMPY como librería para trabjar de forma algebráica
#los polos y ceros del sensor.

import sympy as sp

s = sp.symbols("s")
num = natural_frequency**2
den = s**2 + 2*natural_frequency*zeta*s + natural_frequency**2
#Definimos la expresión del sensor
H_s = num/den  

roots = sp.solve(H_s, s)
print(roots)