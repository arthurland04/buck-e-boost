import numpy as np #cálculos numéricos
import matplotlib.pyplot as plt #gráficos

#parâmetros do projeto
Vin = 100.0 #tensão de entrada
Vout = 250.0 #tensão de saída desejada
Pout = 800.0 #potência de saída
Fs = 50e3 #frequência de chaveamento (50 kHz)
Ts = 1 / Fs #período de chaveamento
VIl = 0.15 #ripple de corrente (15%)
VVl = 0.015 #ripple de tensão (1,5%)

#cálculos básicos
D = (Vout - Vin) / Vout #duty cycle
Iout = Pout / Vout #corrente de saída
Iin  = Pout / Vin #corrente de entrada
R = (Vout**2) / Pout #resistência equivalente da carga

#dimensionamento
L = (Vin * D) / (Fs * VIl * Iin) #indutância
C = (Iout * D) / (Fs * VVl * Vout) #capacitância

print(f"D = {D:.3f}")
print(f"Iout = {Iout:.3f} A")
print(f"Iin = {Iin:.3f} A")
print(f"R = {R:.3f} ohms")
print(f"L = {L*1e3:.3f} mH")
print(f"C = {C*1e6:.3f} uF")

#simulação
t_end = 20e-3 #tempo total (20 ms)
dt = Ts / 200 #passo de integração
t = np.arange(0, t_end, dt)

iL = np.zeros_like(t) #corrente no indutor
vO = np.zeros_like(t) #tensão de saída

#condições iniciais
iL[0] = 0.0
vO[0] = 0.0

#loop de simulação
for k in range(len(t) - 1):

    #define on/off
    if (t[k] % Ts) < D * Ts:
        vL = Vin
    else:
        vL = Vin - vO[k]

    #corrente do indutor
    iL[k + 1] = iL[k] + (vL / L) * dt

    #corrente na carga
    iC = vO[k] / R

    #tensão do capacitor
    vO[k + 1] = vO[k] + (iL[k] - iC) / C * dt

#gráfico
plt.figure(figsize=(10, 4))
plt.plot(t * 1e3, vO, label='Tensão de saída')
plt.axhline(Vout, color='red', linestyle='--', label=f'Referência = {Vout:.1f} V')
plt.title('Tensão de saída - Boost (100 V → 250 V)')
plt.xlabel('Tempo (ms)')
plt.ylabel('Tensão (V)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
