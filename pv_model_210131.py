"""
 pv modeling, 1/31/21 -- OLD MODEL
 Contains functions for current equations, etc
 so I would like to keep it as a reference.
 USE PV_MODEL CLASS INSTEAD.
"""
import math
import numpy as np
import matplotlib.pyplot as plt
# k = boltzmann's constnat = 1.3806503 * 10 ** (-23) J/K


# is there some way to pass in the python file name and import that
# into this function instead?
def find_resistors(self, Iscn, Vocn, Imp, Vmp, Kv, Ki, Ns, Gn, Tn, Egap, err):
    q = 1.602 * 10 ** -19 # charge on electron
    k = 1.3806503 * 10 ** -23 # boltzmann constant
    Pmax_e = Vmp * Imp
    
    G = Gn 
    T = Tn 
    Vtn = k * Tn / q
    Vt = k * T / q
    deltaT = T - Tn
    a = 1

    Rs_max = (Vocn - Vmp) / Imp
    Rp_min = Vmp / (Iscn - Imp) - Rs_max

    Rp = Rp_min
    Rs_vals = np.arange(0, Rs_max, 0.001)
    itr = 0
    v = np.arange(0.1, Vocn, 0.1)
    #i = np.arange(Iscn, 0, -0.1)
    i = np.zeros_like(v)

    err = 0.001
    p_dif = Pmax_e
    Rp_prev = Rp

    while p_dif >= err and itr < len(v):
        #print("outer")
        Rs = Rs_vals[itr]

        Ipvn = Iscn * (Rs+Rp)/Rp 
        Ipv = (Ipvn + Ki*deltaT) * G/Gn
        Isc = (Iscn + Ki*deltaT) * G/Gn
        I0n = (Ipv - Vocn/Rp) / (math.exp(Vocn/Vt/a/Ns)-1)
        I0 = I0n

        a = (Kv - Vocn/Tn) / (Ns * Vtn * (Ki/Ipvn - 3./Tn - Egap/(k*(Tn**2))))

        Rp = Vmp * (Vmp + Imp*Rs) / (Vmp * Ipv - Vmp* I0 * math.exp((Vmp+Imp*Rs)/Vt/Ns/a)+Vmp*I0-Pmax_e)

        _i = i[0]
        for idx in range(len(v)):
            _v = v[idx]
            _g = Ipv - I0 * (math.exp((_v + _i*Rs)/Vt/Ns/a)-1) - (_v + _i*Rs)/Rp - _i
            while abs(_g) > err:
                _g = Ipv - I0 * (math.exp((_v + _i*Rs)/Vt/Ns/a)-1) - (_v + _i*Rs)/Rp - _i
                _glin = -I0 * Rs/Vt/Ns/a * math.exp((_v + _i*Rs)/Vt/Ns/a) - Rs/Rp - 1
                _i = _i - _g/_glin
                i[idx] = _i

        P = np.zeros_like(v)
        for idx1 in range(len(v)):
            _v = v[idx1]
            _i = i[idx1]
            _p = (Ipv - I0 * (math.exp((_v + _i*Rs)/Vt/Ns/a)-1)-(_v + _i*Rs)/Rp)*_v
            P[idx1] = _p
        P_idx = np.argmax(P)
        Pmax_m = P[P_idx]

        p_dif = Pmax_m - Pmax_e
        itr += 1

    return Rs, Rp, a

# calculates light generated current
# Only necessary when Rs and Rp are not known
def pv_current(i_nominal, ki, temp_nominal, temp_actual, irradiation_nominal, irradiation_actual):
    delta_temp = temp_nominal - temp_actual
    i_current = (i_nominal + ki*delta_temp) * irradiation_actual / irradiation_nominal
    return i_current


# calculates the diode saturation current
def saturation_current(i_sc_nom, v_oc_nom, v_t_nom, a, temp_nom, temp_act, bandgap_energy):
    # equation 5
    # v_t_nom is thermal voltage of Ns cells connected in series
    q = 1.602 * math.pow(10, -19) # charge on electron
    k = 1.3806503 * math.pow(10, -23) # boltzmann constant
    i0_n = i_sc_nom / (math.exp(v_oc_nom / (a * v_t_nom)) - 1)
    temp_energy_charge = (q * bandgap_energy / (a * k)) * ((1/temp_nom) - (1/temp_act))
    I0 = i0_n * (math.pow(temp_nom / temp_act, 3) * math.exp(temp_energy_charge))
    return I0


# calculates total current leaving pv
def current(Ipv, I0, V, T, a, Rp=None, Rs=None, I_i=None):
    k = 1.3806503 * math.pow(10, -23) # boltzmann constant
    q = 1.602 * math.pow(10, -19) # charge on electron
    I = 0
    if Rp == None and Rs == None:
        # ideal equation
        I = Ipv - I0 * (math.exp(q * V / (a*k*T)) - 1) # take out 1000 later!! Just for math range err
    else:
        #non ideal equation
        I = Ipv - I0*(math.exp((V+Rs*I_i)/(Vt*a)-1)) - (V+Rs*I_i)/Rp
    return I


# plots different voltage current pairs on an IV curve
def iv_curve(Vocn, Ipv, I0, Tn, a):
    v = np.arange(0, Vocn, 0.1)
    i = []
    for V in v:
        i.append(current(Ipv, I0, V, Tn, a))
    figure = plt.figure(1)
    plt.plot(v, i)
    #plt.show()
    return figure


def main():
    v_oc_n = 0
    iv_curve(v_oc_n)

if __name__ == '__main__':
    main()
