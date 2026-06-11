import control as ctrl

import matplotlib.pyplot as plt

import numpy as np

import pandas as pd



vib_signals = pd.read_csv("synthetic_mwd_signals.csv")

n_frec_in_Hertz = 200

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

    colors = "blue",

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

plt.show() 

