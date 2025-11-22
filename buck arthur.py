import numpy as np #cálculos numéricos
import matplotlib.pyplot as plt #gráficos

#parâmetros do projeto
Vin = 36.0 #tensão de entrada (V)
Fs = 25e3 #frequência de chaveamento (Hz) = 25 kHz
D = 0.5 #duty cycle (50%) -> Vout ≈ 18 V

Ts = 1 / Fs #período de chaveamento (s)

#carga e componentes de filtro
R = 2.16 #resistência de carga (ohms) -> ~150 W em 18 V
L = 220e-6 #indutância do indutor (H)  = 220 µH
C = 56e-6 #capacitância do capacitor (F) = 56 µF

#valor médio de saída esperado
Vout_med = D * Vin #~18 V

#tempo de simulação
t_end = 8e-3 #8 ms de simulação
dt = Ts / 300 #passo de tempo: 1 período dividido em 300 passos
t = np.arange(0, t_end, dt)

#vetores de simulação
iL = np.zeros_like(t) #corrente no indutor
vout = np.zeros_like(t) #tensão no capacitor/saída

#condições iniciais
iL[0] = 0.0
vout[0] = 0.0

#integração numérica (euler explícito)
for k in range(len(t) - 1):
    #tempo dentro do período de chaveamento
    t_cycle = t[k] % Ts

    #define estado da chave: on (ligada) ou off (desligada)
    if t_cycle < D * Ts:
        #fase on: chave fecha, indutor vê Vin - vout
        vL = Vin - vout[k]
    else:
        #fase off: chave abre, indutor descarrega no capacitor/carga
        vL = -vout[k]

    #atualiza corrente do indutor
    iL[k + 1] = iL[k] + (vL / L) * dt

    #corrente na carga (resistor)
    i_load = vout[k] / R

    #atualiza tensão no capacitor
    vout[k + 1] = vout[k] + (iL[k] - i_load) / C * dt

#gráficos
plt.figure(figsize=(10, 4))
plt.plot(t * 1e3, vout, label='Tensão de saída (vout)')
plt.axhline(Vout_med, color='red', linestyle='--',
            label=f'Referência ideal = {Vout_med:.1f} V')
plt.title('Resposta da tensão de saída - Conversor Buck (36 V → ~18 V)')
plt.xlabel('Tempo (ms)')
plt.ylabel('Tensão (V)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
