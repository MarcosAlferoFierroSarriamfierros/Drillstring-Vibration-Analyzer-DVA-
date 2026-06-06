
import numpy as np
import plotly.graph_objects as go  # ¡Corregido el "ploty"!
from plotly.subplots import make_subplots


tiempo = np.linspace(0, 10, 1000)
tiempo_size = 10
torsional_vibration = np.sin(2 * np.pi * 1 * tiempo) + 0.5 * np.sin(2 * np.pi * 3 * tiempo)

middle_data = 100
x_axis = np.fft.fftfreq(len(tiempo), tiempo[1] - tiempo[0])[:middle_data]
fft_vals = np.fft.fft(torsional_vibration)
amplitudes = np.abs(fft_vals)[:middle_data] / len(tiempo)
phases = np.angle(fft_vals)[:middle_data]

fig = make_subplots(
    rows = 3, cols = 1,
    shared_xaxes = False,
    vertical_spacing = 0.08,
    subplot_titles = (
        "Señal temporal original (Vibración Axial)",
        "Reconstrucción Dinámica de la Señal",
        "Espectro de amplitud (FFT)"
    )
)


fig.add_trace(go.Scatter(
    x = tiempo, y = torsional_vibration,
    mode = "lines",
    name = "Original"
), row = 1, col = 1)

fig.add_trace(go.Bar(
    x = x_axis, y = amplitudes,
    name = "FFT"
), row = 3, col = 1)



armonic_steps = [1, 2, 5, 10, 50, middle_data]
f0 = 1 / tiempo_size
perestroikaya_signali = []

for N in armonic_steps:
    perestroika_signala = np.ones_like(tiempo) * amplitudes[0] #xq en N=1 no agarraría el bucle
    step_signals = [] # Tu lista auxiliar de pasos
    
    # Usamos range(1, N) para proteger los índices de tus vectores
    for i in range(1, N):
        step = 2 * amplitudes[i] * np.cos(2 * np.pi * i * f0 * tiempo + phases[i])
        perestroika_signala += step
        
    perestroikaya_signali.append(perestroika_signala)



for idx, senal in enumerate(perestroikaya_signali):
    inicialmente_visible = True if idx == 0 else False
    fig.add_trace(
        go.Scatter(
            x = tiempo, y = senal,
            mode = "lines",
            name = f"{armonic_steps[idx]} Armónicos",
            visible = inicialmente_visible
        ),
        row = 2, col = 1
    )



pasos_slider = []

for idex, step in enumerate(armonic_steps):
    visibilidad = [True, True] # Mantiene siempre visibles la FFT y la Original
    
    for idex_senal in range(len(perestroikaya_signali)):
        if idex == idex_senal:
            visibilidad.append(True)
        else:
            visibilidad.append(False)
            
    paso = dict(
        method = "update", # Avisamos que modificamos los datos existentes
        label = f"{step} Armónicos", # Corregido para evitar el IndexError
        args = [{"visible": visibilidad}]
    )
    pasos_slider.append(paso)



fig.update_layout(
    title_text="Análisis y Reconstrucción Dinámica de Vibraciones",
    height=900, 
    showlegend=False, 
    sliders=[dict(
        active=0, 
        currentvalue={"prefix": "Visualizando: "}, 
        pad={"t": 70}, 
        steps=pasos_slider 
    )]
)


fig.show()

