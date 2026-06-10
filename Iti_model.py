import control as ctrl 
import matplotlib.pyplot as plt
natural_frequency = 200 #200 Hz
zeta = 0.7
num = [natural_frequency^2]
den = [1, 2*natural_frequency*zeta, natural_frequency^2]
G = ctrl.TransferFunction(num, den)
print(G)

time, response = ctrl.impulse_response(G)

plt.plot(time, response)
plt.title("Impulse Response")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.savefig("Impulse_Response.png")
plt.show()
