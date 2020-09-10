from collections import namedtuple
import csv
import math
import numpy as np

from module import multiple_reflection as mr
from module import oblique_incidence_property as oip
from module import division_diffuse_ratio as ddr
from module import incident_solar_radiation_on_glazing as isrog


class ata_input():
    def __init__(self, absb, absd, absr):
        self.absb = absb
        self.absd = absd
        self.absr = absr


# absb：直達成分の日射吸収率
# absd：天空成分の日射吸収率
# absr：地表面反射成分の日射吸収率


# 層jの吸収日射量
def absorb_sol(L, M):
    return L.Itb * M.absb + L.Itd * M.absd + L.Itr * M.absr


# 直達日射での層jの吸収率
def actual_abs_beam(L, gl_type, phi_b):

    ly_in_b = np.empty(len(L), dtype=tuple)

    for j in range(0, len(L)):
        p = L[j].get_ang_prop(phi=phi_b)
        ly_in_b[j] = mr.SolarSpecSingleLayer(tau_f=p[0], tau_b=p[1], rho_f=p[2], rho_b=p[3])

    g = mr.Glass(ss=list(ly_in_b))

    return g.get_abs_multi_layer()


# 天空日射での層jの吸収率
def actual_abs_diffuse(L, gl_type, Nd_lat, Nd_lon):
    F_d = np.empty((Nd_lat, Nd_lon))
    phi_d = np.empty((Nd_lat, Nd_lon))
    abs_d = np.empty((len(L), Nd_lat, Nd_lon))
    r_absd = np.zeros(len(L))
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
            x = g.get_abs_multi_layer()
            for j in range(0, len(L)):
                abs_d[j][l][m] = x[j]
                r_absd[j] += F_d[l][m] * abs_d[j][l][m]

    return r_absd


# 地表面反射日射での層jの吸収率
def actual_abs_reflect(L, gl_type, Nr_lat, Nr_lon):
    F_r = np.empty((Nr_lat, Nr_lon))
    phi_r = np.empty((Nr_lat, Nr_lon))
    abs_r = np.empty((len(L), Nr_lat, Nr_lon))
    r_absr = np.zeros(len(L))
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

            x = g.get_abs_multi_layer()

            for j in range(0, len(L)):
                abs_r[j][l][m] = x[j]
                r_absr[j] += F_r[l][m] * abs_r[j][l][m]

    return r_absr
