from collections import namedtuple
import csv
import math
import numpy as np
import matplotlib.pyplot as plt

from module import multiple_reflection as mr
from module import oblique_incidence_property as oip
from module import division_diffuse_ratio as ddr
from module import incident_solar_radiation_on_glazing as isrog


class tta_input():
    def __init__(self, taub, taud, taur):
        self.taub = taub
        self.taud = taud
        self.taur = taur


# taub：直達成分の日射透過率
# taud：天空成分の日射透過率
# taur：地表面反射成分の日射透過率

# 開口面透過日射量
def transmit_sol(L, M):
    return L.Itb * M.taub + L.Itd * M.taud + L.Itr * M.taur


# 直達日射での透過率
def actual_trans_beam(L, gl_type, phi_b):
    r_taub = 0.
    ly_in_b = np.empty(len(L), dtype=tuple)
    for j in range(0, len(L)):
        p = L[j].get_ang_prop(phi=phi_b)
        ly_in_b[j] = mr.SolarSpecSingleLayer(tau_f=p[0], tau_b=p[1], rho_f=p[2], rho_b=p[3])

    g = mr.Glass(list(ly_in_b))

    return g.get_total_solar_spec().tau_f


# 天空日射での透過率
def actual_trans_diffuse(L, gl_type, Nd_lat, Nd_lon):
    F_d = np.empty((Nd_lat, Nd_lon))
    phi_d = np.empty((Nd_lat, Nd_lon))
    tau_d = np.empty((Nd_lat, Nd_lon))
    r_taud = 0.
    ly_in_d = np.empty(len(L), dtype=tuple)
    for l in range(0, Nd_lat):
        for m in range(0, Nd_lon):
            dd_in = ddr.DdInput(Nd_lat, Nd_lon)
            # 割合, _, _, 入射角
            F_d[l][m], _, _, phi_d[l][m] = dd_in.division_diffuse_ratio(l_lat=l, m_lon=m)

            for j in range(0, len(L)):
                p = L[j].get_ang_prop(phi=phi_d[l][m])
                ly_in_d[j] = mr.SolarSpecSingleLayer(tau_f=p[0], tau_b=p[1], rho_f=p[2], rho_b=p[3])

            g = mr.Glass(list(ly_in_d))

            tau_d[l][m] = g.get_total_solar_spec().tau_f

            r_taud += F_d[l][m] * tau_d[l][m]

    return r_taud


# 地表面反射日射での透過率
def actual_trans_reflect(L, gl_type, Nr_lat, Nr_lon):
    F_r = np.empty((Nr_lat, Nr_lon))
    phi_r = np.empty((Nr_lat, Nr_lon))
    tau_r = np.empty((Nr_lat, Nr_lon))
    r_taur = 0.
    ly_in_r = np.empty(len(L), dtype=tuple)
    for l in range(0, Nr_lat):
        for m in range(0, Nr_lon):
            dr_in = ddr.DrInput(Nr_lat, Nr_lon)
            # 割合, _, _, 入射角
            F_r[l][m], _, _, phi_r[l][m] = dr_in.division_reflect_ratio(l, m)

            for j in range(0, len(L)):
                p = L[j].get_ang_prop(phi=phi_r[l][m])
                ly_in_r[j] = mr.SolarSpecSingleLayer(tau_f=p[0], tau_b=p[1], rho_f=p[2], rho_b=p[3])

            g = mr.Glass(list(ly_in_r))

            tau_r[l][m] = g.get_total_solar_spec().tau_f

            r_taur += F_r[l][m] * tau_r[l][m]

    return r_taur

