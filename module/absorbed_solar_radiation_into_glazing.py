import numpy as np
from typing import List

from module import multiple_reflection as mr
from module import oblique_incidence_property as oip
from module import division_diffuse_ratio as ddr


# 直達日射での層jの吸収率
def actual_abs_beam(L, phi_b):

    return get_abs_multi_layer(oips=L, phi=phi_b)


# 天空日射での層jの吸収率
def actual_abs_diffuse(L, Nd_lat, Nd_lon):

    r_absd = np.zeros(len(L))

    dd_in = ddr.DdInput(Nd_lat, Nd_lon)

    # 割合, _, _, 入射角, [l][m]
    F_d, _, _, phi_d = dd_in.division_diffuse_ratios()

    for l in range(0, Nd_lat):
        for m in range(0, Nd_lon):

            x = get_abs_multi_layer(oips=L, phi=phi_d[l][m])

            for j in range(0, len(L)):
                r_absd[j] += F_d[l][m] * x[j]

    return r_absd


# 地表面反射日射での層jの吸収率
def actual_abs_reflect(L, Nr_lat, Nr_lon):

    r_absr = np.zeros(len(L))

    dr_in = ddr.DrInput(Nr_lat, Nr_lon)

    # 割合, _, _, 入射角
    F_r, _, _, phi_r = dr_in.division_reflect_ratios()

    for l in range(0, Nr_lat):
        for m in range(0, Nr_lon):

            x = get_abs_multi_layer(oips=L, phi=phi_r[l][m])

            for j in range(0, len(L)):
                r_absr[j] += F_r[l][m] * x[j]

    return r_absr


def get_abs_multi_layer(oips: List[oip.ObliqueIncidenceProperty], phi: float) -> np.ndarray:
    ps = [p.get_ang_prop(phi=phi) for p in oips]
    ly_in_d = [mr.SolarSpecSingleLayer(tau_f=p[0], tau_b=p[1], rho_f=p[2], rho_b=p[3]) for p in ps]
    g = mr.Glass(ss=ly_in_d)
    return np.array(g.get_abs_multi_layer())
