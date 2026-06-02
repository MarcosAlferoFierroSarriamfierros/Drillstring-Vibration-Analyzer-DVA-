import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
def find_armonics(num_desired_armonics, signal, periodo_fundamental, tiempo):
    #i = num_desired_armonics
    #reconstructed_signal = 0
    gotted_armonics = []
    for i in range(1,num_desired_armonics + 1):
        exp_term = np.exp(-2*np.pi * i * (tiempo/periodo_fundamental)*1j)
        c_i = 1/(tiempo_size) * np.trapezoid(signal * exp_term, tiempo)
        gotted_armonics.append(c_i)
    return(gotted_armonics)
def perestroika_signal(gotted_armonics, c0, tiempo, periodo_fundamental):
    perestroikaya_signala = 0
    gotted_components = []
    for i in range(0, len(gotted_armonics)):
        n = i+1
        exp_term = np.exp(2*np.pi * n * (tiempo/periodo_fundamental)*1j)
        componente_i = 2 * np.real(gotted_armonics[i] * exp_term)
        gotted_components.append(componente_i)
        perestroikaya_signala += componente_i  
    return c0 + perestroikaya_signala, gotted_components

tiempo_size = 10;
fs_torsional = 0.5
num_ciclos = tiempo_size * fs_torsional
periodo_fundamental = tiempo_size/num_ciclos 
df = pd.read_csv("synthetic_mwd_signals.csv")
tiempo = df["Time"].to_numpy()
axial_vibration = df["Axial_Vibration_G"].to_numpy()
torsional_vibration = df["Torsional_Vibration_RPM"].to_numpy()
whirl_lateral = df["Whirl_Lateral_G"].to_numpy()
c0 = np.mean(torsional_vibration)
gotted_armonics = find_armonics(10, torsional_vibration, periodo_fundamental, tiempo)
reconstructed_signal, components = perestroika_signal(gotted_armonics, c0, tiempo, periodo_fundamental) 
#El proyecto solicita calcular recontrucciones con N =1,3,5,10,50
cases_results = {}
for i in [1,3,5,10,50]:
    gotted_armonics = find_armonics(i, torsional_vibration, periodo_fundamental, tiempo)
    reconstructed_signal, components = perestroika_signal(gotted_armonics, c0, tiempo, periodo_fundamental) 
    name = "N" + str(i)
    cases_results[name] = [gotted_armonics, components, reconstructed_signal]
#Para graficar

for i in [1,3,5,10,50]:
    key = "N" + str(i)
    plt.figure()
    plt.plot(tiempo, cases_results[key][2], label = "Reconstruida")
    plt.plot(tiempo, torsional_vibration, label = "Original" )
    plt.title("Señal Original vs Señal Reconstruida para los primeros "+ str(i)+ " armónicos" )
    plt.xlabel("Tiempo (s)")
    plt.ylabel("RPM")
    plt.legend()
    plt.grid(True)
    # Reemplazamos plt.show() por esto:
    plt.savefig("convergencia_" + key + ".png")
    plt.close()
    
#Finalmente hacemos el Espectro de Amplitud y Fase 
#Usamos N = 50
amplitude_points = []
phase_points = []
x_axis = range(1, len(cases_results["N50"][0]) + 1 )
for i in cases_results["N50"][0]:
    amplitude_point = np.abs(i)
    phase_point = np.angle(i)
    amplitude_points.append(amplitude_point)
    phase_points.append(phase_point)
# Gráfico de Amplitud
plt.figure()
plt.plot(x_axis, amplitude_points, label = "Amplitud")
plt.xlabel("Armonico")
plt.ylabel("RPM")
plt.savefig("espectro_amplitud.png")
plt.close()

# Gráfico de Fase
plt.figure()
plt.plot(x_axis, phase_points, label = "Phase")
plt.xlabel("Armonico")
plt.ylabel("Desplazamiento de fase")
plt.savefig("espectro_fase.png")
plt.close()