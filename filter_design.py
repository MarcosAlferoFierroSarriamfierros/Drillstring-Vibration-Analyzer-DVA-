import numpy as np 
import control as ctrl
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np

import pandas as pd
from scipy.signal import butter, filtfilt, cheby1

vib_signals = pd.read_csv("synthetic_mwd_signals.csv")
Axial_vibration = vib_signals["Axial_Vibration_G"].to_numpy()
time = vib_signals["Time"].to_numpy()
fs = 1000
fc = 50 

#Diseñaremos los siguientes filtros:
# 1) Butterworth LP orden 4, fc=50 Hz para eliminar 60 Hz,
# 2) Butterworth BP 5-40 Hz para aislar stick-slip, 
# 3) Chebyshev I LP orden 6 fc=50 Hz.
# Usar scipy.signal.butter, cheby1, filtfilt (zero-phase)
#Wn es la frecuencia normalizada
Wn = fc / (fs/2)

#Coeficientes para el filtro 1:

b1, a1 = butter(4, Wn, btype = "low")
filtered_signal1 = filtfilt(b1, a1, Axial_vibration)

#Coeficientes para el filtro 1:
Wn_band = [5 / (fs/2), 40 / (fs/2) ]
b2, a2 = butter(4, Wn_band, btype = "bandpass")
filtered_signal2 = filtfilt(b2, a2, Axial_vibration)

#Coeficientes para el filtro 1:
rp = 1 #para´metros de rizado (rizado máximo permitido)
b3, a3 = cheby1(6,rp , Wn, btype = "low")
filtered_signal3 = filtfilt(b3, a3, Axial_vibration)

plt.figure()
plt.subplot(2,2,1)
plt.plot(time,filtered_signal1,
color = "red",
linestyle = "--",
linewidth = 2,
label = "Butterworth LP orden 4, fc=50 Hz") 

plt.subplot(2,2,2)
plt.plot(time,filtered_signal2,
color = "green",
linestyle = "--",
linewidth = 2,
label = "Butterworth BP 5-40 Hz") 


plt.subplot(2,2,3)
plt.plot(time,filtered_signal3,
color = "blue",
linestyle = "--",
linewidth = 2,
label = "Chebyshev I LP orden 6 fc=50 Hz") 



plt.subplot(2,2,4)
plt.plot(time,Axial_vibration,
color = "black",
linestyle = "--",
linewidth = 2,
label = "Original Signal") 
import numpy as np 
import control as ctrl
import plotly.graph_objects as go
import matplotlib.pyplot as plt

import numpy as np

import pandas as pd
from scipy.signal import butter, filtfilt

vib_signals = pd.read_csv("synthetic_mwd_signals.csv")
Axial_vibration = vib_signals["Axial_Vibration_G"].to_numpy()
time = vib_signals["Time"].to_numpy()
fs = 1000
fc = 50 

#Diseñaremos los siguientes filtros:
# 1) Butterworth LP orden 4, fc=50 Hz para eliminar 60 Hz,
# 2) Butterworth BP 5-40 Hz para aislar stick-slip, 
# 3) Chebyshev I LP orden 6 fc=50 Hz.
# Usar scipy.signal.butter, cheby1, filtfilt (zero-phase)
#Wn es la frecuencia normalizada
Wn = fc / (fs/2)

#Coeficientes para el filtro 1:

b1, a1 = butter(4, Wn, btype = "low")
filtered_signal1 = filtfilt(b1, a1, Axial_vibration)

#Coeficientes para el filtro 1:
Wn_band = [5 / (fs/2), 40 / (fs/2) ]
b2, a2 = butter(4, Wn_band, btype = "bandpass")
filtered_signal2 = filtfilt(b2, a2, Axial_vibration)

#Coeficientes para el filtro 1:
rp = 1 #para´metros de rizado (rizado máximo permitido)
b3, a3 = cheby1(6,rp , Wn, btype = "low")
filtered_signal3 = filtfilt(b3, a3, Axial_vibration)

plt.figure()
plt.subplot(2,2,1)
plt.plot(time,filtered_signal1,
color = "red",
linestyle = "-",
linewidth = 2,
label = "Butterworth LP orden 4, fc=50 Hz") 
plt.xlabel("Tiempo (s)")
plt.ylabel("Aceleration G")

plt.legend()



plt.subplot(2,2,2)
plt.plot(time,filtered_signal2,
color = "green",
linestyle = "-",
linewidth = 2,
label = "Butterworth BP 5-40 Hz") 
plt.xlabel("Tiempo (s)")
plt.ylabel("Aceleration G")

plt.legend()


plt.subplot(2,2,3)
plt.plot(time,filtered_signal3,
color = "blue",
linestyle = "-",
linewidth = 2,
label = "Chebyshev I LP orden 6 fc=50 Hz") 
plt.xlabel("Tiempo (s)")
plt.ylabel("Aceleration G")

plt.legend()



plt.subplot(2,2,4)
plt.plot(time,Axial_vibration,
color = "black",
linestyle = "-",
linewidth = 2,
label = "Original Signal") 
plt.xlabel("Tiempo (s)")
plt.ylabel("Aceleration G")

plt.legend()

plt.tight_layout()
plt.savefig("Comparacion_Filtros.png")

plt.show()


fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Butterworth LP", "Butterworth BP", "Chebyshev I LP", "Señal Original")
)
fig.add_trace(
    go.Scatter(
        x = time,
        y = filtered_signal1,
        line = dict(color="red"),
    ),
        row = 1, col = 1
)

fig.add_trace(
    go.Scatter(
        x = time,
        y = filtered_signal2,
        line = dict(color="green"),
    ),
        row = 1, col = 2
)


fig.add_trace(
    go.Scatter(
        x = time,
        y = filtered_signal3,
       line = dict(color="blue"),
    ),
        row = 2, col = 1
)


fig.add_trace(
    go.Scatter(
        x = time,
        y = Axial_vibration,
       line = dict(color="black"),
    ),
        row = 2, col = 2
)

fig.write_html("filtros_interactivos.html")