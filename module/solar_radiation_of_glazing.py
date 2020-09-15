import numpy as np
from typing import List

from module import multiple_reflection as mr
from module import oblique_incidence_property as oip
from module import division_diffuse_ratio as ddr


# 直達日射での透過率
def actual_trans_beam(oips: List[oip.ObliqueIncidenceProperty], phi_b):

    spec = get_total_solar_spec(oips=oips, phi=phi_b)

    return spec.tau_f


# 直達日射での層jの吸収率
def actual_abs_beam(oips, phi_b):

    return get_abs_multi_layer(oips=oips, phi=phi_b)


def actual_trans_diffuse(oips: List[oip.ObliqueIncidenceProperty], Nd_lat: int, Nd_lon: int) -> float:
    """
    天空日射での透過率を求める。
    Args:
        oips:
        Nd_lat:
        Nd_lon:

    Returns:
        天空日射での透過率
    """

    r_taud = 0.

    dd_in = ddr.DdInput(Nd_lat, Nd_lon)

    # 割合, _, _, 入射角
    F_d, _, _, phi_d = dd_in.division_diffuse_ratios()

    for l in range(0, Nd_lat):
        for m in range(0, Nd_lon):

            g = get_total_solar_spec(oips=oips, phi=phi_d[l][m])
            r_taud += F_d[l][m] * g.tau_f

    return r_taud


# 地表面反射日射での透過率
def actual_trans_reflect(oips: List[oip.ObliqueIncidenceProperty], Nr_lat, Nr_lon):

    tau_r = np.empty((Nr_lat, Nr_lon))
    r_taur = 0.

    dr_in = ddr.DrInput(Nr_lat, Nr_lon)

    # 割合, _, _, 入射角
    F_r, _, _, phi_r = dr_in.division_reflect_ratios()

    for l in range(0, Nr_lat):
        for m in range(0, Nr_lon):

            g = get_total_solar_spec(oips=oips, phi=phi_r[l][m])

            tau_r[l][m] = g.tau_f

            r_taur += F_r[l][m] * tau_r[l][m]

    return r_taur


# 天空日射での層jの吸収率
def actual_abs_diffuse(oips, Nd_lat, Nd_lon):

    r_absd = np.zeros(len(oips))

    dd_in = ddr.DdInput(Nd_lat, Nd_lon)

    # 割合, _, _, 入射角, [l][m]
    F_d, _, _, phi_d = dd_in.division_diffuse_ratios()

    for l in range(0, Nd_lat):
        for m in range(0, Nd_lon):

            x = get_abs_multi_layer(oips=oips, phi=phi_d[l][m])

            for j in range(0, len(oips)):
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


def get_total_solar_spec(oips: List[oip.ObliqueIncidenceProperty], phi: float) -> mr.SolarSpecMultiLayer:
    ps = [p.get_ang_prop(phi=phi) for p in oips]
    ly_in_d = [mr.SolarSpecSingleLayer(tau_f=p[0], tau_b=p[1], rho_f=p[2], rho_b=p[3]) for p in ps]
    g = mr.Glass(ss=ly_in_d)
    return g.get_total_solar_spec()


def get_abs_multi_layer(oips: List[oip.ObliqueIncidenceProperty], phi: float) -> np.ndarray:
    ps = [p.get_ang_prop(phi=phi) for p in oips]
    ly_in_d = [mr.SolarSpecSingleLayer(tau_f=p[0], tau_b=p[1], rho_f=p[2], rho_b=p[3]) for p in ps]
    g = mr.Glass(ss=ly_in_d)
    return np.array(g.get_abs_multi_layer())
