import numpy as np 
import pandas as pd 
import plotly.graph_objects as go  # ¡Corregido el "ploty"!
from plotly.subplots import make_subplots
from scipy.signal import spectrogram
df = pd.read_csv("synthetic_mwd_signals.csv")
#print(df.head())
#Iniciamos analizando la vibración debido al torque
fs = 1000 #Definida en el dia 1
#La funcion scipy necesita frecuencia de muestreo 
# y la signal
#con nperseg indicamos los segundos por sección
#Definiendo una sección de 0.25 segundos para el análisis
# 1000 * 0.25 = 250 puntos por sección
frecuencias, tiempos, espectrograma = spectrogram(df["Torsional_Vibration_RPM"], fs, nperseg = 250)

# fig = go.Figure(data = go.Heatmap(
# z = espectrograma, #intensidad
# x = tiempos, #eje que no cambia
# y = frecuencias, #signal
# colorscale = "Viridis",
# colorbar = dict(
#     title = "Potencia (RPM^2 / Hz)"
# )
# )
# )
# #La seleccion de restriccion para el eje Y
# # [0, 20] se hace debido a que las frecuencias dañinas en la sarta
# #suelen estar entre los 0 y los 20 Hz (frecuencias bajas)
# fig.update_layout(
# xaxis = dict(
#     title = "Time (s)",
#     dtick = 1,
#     showgrid = True
# ),

# yaxis = dict(
#     title = "Frecuencia (Hz)",
#     range = [0, 20],
#     dtick = 1,
#     showgrid = True
# )


# )
#Se hace el mismo procedimiento para analizar la torsión axial
frecuencias_whirl, tiempos_whirl, espectrograma_whirl = spectrogram(df["Whirl_Lateral_G"], fs, nperseg = 250)

# fig_whirl = go.Figure(data = go.Heatmap(
# z = espectrograma_whirl, #intensidad
# x = tiempos_whirl, #eje que no cambia
# y = frecuencias_whirl, #signal
# colorscale = "Viridis",
# colorbar = dict(
#     title = "Potencia (G^2 / Hz)"
# )
# )
# )
# #La seleccion de restriccion para el eje Y
# # [0, 20] se hace debido a que las frecuencias dañinas en la sarta
# #suelen estar entre los 0 y los 20 Hz (frecuencias bajas)
# fig_whirl.update_layout(
# xaxis = dict(
#     title = "Time (s)",
#     dtick = 1,
#     showgrid = True
# ),

# yaxis = dict(
#     title = "Frecuencia (Hz)",
#     range = [0, 20],
#     dtick = 1,
#     showgrid = True
# )

# )

fig_mixed = make_subplots(rows = 1, cols = 2, #shared_yaxes = True,
subplot_titles = ("Vibración Torsional", "Vibración Lateral")
)
fig_mixed.add_trace(
    go.Heatmap(
        z = espectrograma,
        x = tiempos,
        y = frecuencias,
        colorscale = "Viridis",
        colorbar = dict(
            title = "RPM2/Hz",
            x = 0.45
        )
    ),
        row = 1, col = 1
)

fig_mixed.add_trace(
    go.Heatmap(
        z = espectrograma_whirl,
        x = tiempos_whirl,
        y = frecuencias_whirl,
        colorscale = "Viridis",
        colorbar = dict(
            title = "G2/Hz",
            x = 1.0
        )
    ),
        row = 1, col = 2
)


fig_mixed.update_layout(
title_text = "Comparative Analysis of MWD Vibrations",
yaxis = dict(
    title = "Frecuencia (Hz)",
    range = [0,20],
    dtick = 1,
    showgrid = True # 
),

xaxis = dict(
    title = "Time (s)",
    dtick = 0.5,
    showgrid = True # 
),
yaxis2 = dict(
    title = "Frecuencia (Hz)", # 
    range = [0,20],
    dtick = 1,
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