# pv modeling, 1/31/21
import math
import numpy as np
import matplotlib.pyplot as plt
# k = boltzmann's constnat = 1.3806503 * 10 ** (-23) J/K

# calculates light generated current
def pv_current(i_nominal, temp_nominal, temp_actual, irradiation_nominal, irradiation_actual):
    k1 = 1 # some constant
    delta_temp = temp_nominal - temp_actual
    temp = k1 * delta_temp
    i_current = (i_nominal + temp) * irradiation_actual / irradiation_nominal
    return i_current

# calculates the diode saturation current
def saturation_current(i_sc_nom, v_oc_nom, v_t_nom, a, temp_nom, temp_act, bandgap_energy):
    # equation 5
    # v_t_nom is thermal voltage of Ns cells connected in series
    q = 1.602 * math.pow(10, -19) # charge on electron
    k = 0 # some constant?
    i0_n = i_sc_nom / (math.exp(v_oc_nom / (a * v_t_nom)) - 1)
    temp_energy_charge = (q * bandgap_energy / (a * k)) * (1/temp_nom - 1/temp_act)
    i0 = i0_n * (math.pow(temp_nom / temp_act, 3) * math.exp(temp_energy_charge)
    return i0

def current(i_pv, i_0, V, temp, a):
    # ideal equation
    q = 1.602 * math.pow(10, -19) # charge on electron
    return i_pv - i_0 * (math.exp(q * V / (a*k*temp)) - 1)

def iv_curve(v_oc_n):
    v = np.arange(0, v_oc_n, 0.1)
    i = []
    for num in v:
        i.append(current(num))
    figure = plt.figure(1)
    plt.plot(v, i)
    plt.show()

def main():
    v_oc_n = 0
    iv_curve(v_oc_n)

if __name__ == '__main__':
    main()
