import numpy as np
from scipy import signal
import pandas as pd
fs = 1000 #Frecuencia de muestreo
T = 10 #Duracion de la senal
tiempo = np.linspace(0,T, fs*T, endpoint = False) #Se crea el vecto de tiempo
#Axial Vibration
#Bit Bounce
axial_fundamental = 1.2 * np.sin(2 * np.pi * 12* tiempo)
axial_armonics_1 = 0.6 * np.sin(2*np.pi * 24*tiempo)
axial_armonics_2 = 0.3 * np.sin(2*np.pi * 36*tiempo)
#Ruido blanco
axial_noise = np.random.normal(0, 0.4, size = len(tiempo))
axial_complete =  axial_fundamental + axial_armonics_2 + axial_armonics_1 + axial_noise 

#Torsional Vibration
slip_vibration = signal.sawtooth(2 * np.pi * 0.5 * tiempo, width = 0.5) 
#Asumiendo 60 RPM en la sarte de perforación y unas 50 RPM para representar las vibraciones fuertes
stick_slip_complete = 60 + 50*slip_vibration
#Transitory Vibration (Whirl)
whirl = 2.5 * np.sin(2 * np.pi * 2.3 * tiempo)
#Para que el Whirl sea una señal finita, y centrándola en 5 
envolvente  = np.exp(-((tiempo - 5)/1.5)**2)
transitory_complete = whirl * envolvente 
data_signals = {
    "Time": tiempo,
    "Axial_Vibration_G": axial_complete,
    "Torsional_Vibration_RPM": stick_slip_complete,
    "Whirl_Lateral_G": transitory_complete 
}
data_signals = pd.DataFrame(data_signals)
data_signals.to_csv("synthetic_mwd_signals.csv")



