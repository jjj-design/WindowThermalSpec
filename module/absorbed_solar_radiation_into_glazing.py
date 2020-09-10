from collections import namedtuple
import csv
import math
import numpy as np
import matplotlib.pyplot as plt

import IncidentSolarRadiationOnGlazing as ISROG
import DivisionDiffuseRatio as DDR

from module import multiple_reflection as mr
from module import oblique_incidence_property as oip

# %% md

# 各層の吸収日射量を計算するモジュール

# %% md

## 1. Functions

# %% md

開口面日射量（直達・天空・地表面反射）とグレージング複合体各層の日射吸収率から各層の吸収日射量を計算する。

# %% md

### 入力値

$ I_
{T, b} $ ：斜面（開口面）直達日射量(W / m < sup > 2 < / sup >)
$ I_
{T, d} $ ：斜面（開口面）天空日射量(W / m < sup > 2 < / sup >)
$ I_
{T, r} $ ：斜面（開口面）地表面反射日射量(W / m < sup > 2 < / sup >)
$ \alpha_
{glz, b, j} $ ：直達日射に対する層$j$の日射吸収率
$ \alpha_
{glz, d, j, l, m} $ ：天空上の微小要素からの入射日射に対する層$j$の日射吸収率
$ \alpha_
{glz, r, j, l, m} $ ：地表面上の微小要素からの入射日射に対する層$j$の日射吸収率
$ F_
{d, l, m} $ ：天空日射量に対する天空上の微小要素からの天空日射量の割合
$ F_
{r, l, m} $ ：地表面反射日射量に対する地表面上の微小要素からの地表面反射日射量の割合

# %% md

### 出力値

$ I_
{\alpha, j} $ ：層$j$での吸収日射量(W / m < sup > 2 < / sup >)

# %% md

### 計算方法

#### データ構造と値の範囲

$ \alpha_
{glz, b, j} $・$ \alpha_
{glz, d, j} $・$ \alpha_
{glz, r, j} $ の組み合わせをクラス『ata＿input』とする。

# %%

class ata_input():
    def __init__(self, absb, absd, absr):
        self.absb = absb
        self.absd = absd
        self.absr = absr


# absb：直達成分の日射吸収率
# absd：天空成分の日射吸収率
# absr：地表面反射成分の日射吸収率

# %% md

#### 層$j$での吸収日射量の計算

層$j$での吸収日射量の計算方法を以下に示す。

# %% md

$$
\begin
{eqnarray}
& \displaystyle
I_
{\alpha, j} = I_
{T, b} \cdot \alpha_
{glz, b, j} + I_
{T, d} \cdot \alpha_
{glz, d} + I_
{T, r} \cdot \alpha_
{glz, r} & \qquad\qquad\text
{(1)} \nonumber\ \
    \nonumber \ \
    & \displaystyle \alpha_
{glz, d} = \sum_
{l = 0} ^ {N_
{d, lat} - 1}\sum_
{m = 0} ^ {N_
{d, lon} - 1} F_
{d, l, m} \cdot \alpha_
{glz, d, j, l, m} & \qquad\qquad\text
{(2)} \nonumber\ \
    \nonumber \ \
    & \displaystyle \alpha_
{glz, r} = \sum_
{l = 0} ^ {N_
{r, lat} - 1}\sum_
{m = 0} ^ {N_
{r, lon} - 1} F_
{r, l, m} \cdot \alpha_
{glz, r, j, l, m} & \qquad\qquad\text
{(3)} \nonumber\ \
    \end
{eqnarray}
$$

# %%

# 層jの吸収日射量
def absorb_sol(L, M):
    return L.Itb * M.absb + L.Itd * M.absd + L.Itr * M.absr


# 直達日射での層jの吸収率
def actual_abs_beam(L, gl_type, phi_b):
    ly_in_b = np.empty(len(L), dtype=tuple)
    for j in range(0, len(L)):
        p = L[j].get_ang_prop(phi=phi_b)
        ly_in_b[j] = mr.SolarSpecSingleLayer(tau_f=p[0], tau_b=p[1], rho_f=p[2], rho_b=p[3])

    return mr.get_abs_multi_layer(ly_in_b)


# 天空日射での層jの吸収率
def actual_abs_diffuse(L, gl_type, Nd_lat, Nd_lon):
    F_d = np.empty((Nd_lat, Nd_lon))
    phi_d = np.empty((Nd_lat, Nd_lon))
    abs_d = np.empty((len(L), Nd_lat, Nd_lon))
    r_absd = np.zeros(len(L))
    ly_in_d = np.empty(len(L), dtype=tuple)
    for l in range(0, Nd_lat):
        for m in range(0, Nd_lon):
            dd_in = DDR.dd_input(Nd_lat, Nd_lon, l, m)
            F_d[l][m] = DDR.division_diffuse_ratio(dd_in)[0]  # 割合
            phi_d[l][m] = DDR.division_diffuse_ratio(dd_in)[3]  # 入射角

            for j in range(0, len(L)):
                p = L[j].get_ang_prop(phi=phi_b)
                ly_in_d[j] = mr.SolarSpecSingleLayer(tau_f=p[0], tau_b=p[1], rho_f=p[2], rho_b=p[3])

            x = mr.get_abs_multi_layer(ly_in_d)
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
            dr_in = DDR.dr_input(Nr_lat, Nr_lon, l, m)
            F_r[l][m] = DDR.division_reflect_ratio(dr_in)[0]  # 割合
            phi_r[l][m] = DDR.division_reflect_ratio(dr_in)[3]  # 入射角

            for j in range(0, len(L)):
                p = L[j].get_ang_prop(phi=phi_r[l][m])
                ly_in_r[j] = mr.SolarSpecSingleLayer(tau_f=p[0], tau_b=p[1], rho_f=p[2], rho_b=p[3])

            x = mr.get_abs_multi_layer(ly_in_r)
            for j in range(0, len(L)):
                abs_r[j][l][m] = x[j]
                r_absr[j] += F_r[l][m] * abs_r[j][l][m]

    return r_absr


# %% md

#### Example

# %%

if __name__ == '__main__':

    # 面材の種類
    gl_type = [0, 0, 1]  # 各層のグレージング種類（0：ガラス、1：ロールスクリーン、2：横型ブラインド、3：縦型ブラインド）

    # 面材ごとの光学特性
    gl_in = [
        oip.GlassInput(trs_0_f=0.815, trs_0_b=0.815, ref_0_f=0.072, ref_0_b=0.072, gtype=0, c_type_f=False, c_type_b=False),
        oip.GlassInput(trs_0_f=0.815, trs_0_b=0.815, ref_0_f=0.072, ref_0_b=0.072, gtype=0, c_type_f=False, c_type_b=False),
        oip.RoleInput(trs_0_f=0.3, trs_0_b=0.3, ref_0_f=0.63, ref_0_b=0.63)
    ]

    # 斜面日射量
    ita_in = ISROG.ita_input(2.6840261248 * 10. ** 6. / 3600., 0.1181932153 * 10. ** 6. / 3600.,
                             0.094 * 10. ** 6. / 3600.)

    # 直達日射の入射角
    phi_b = 31.6403837639

    # 天空分割数
    Nd_lat = 90
    Nd_lon = 180

    # 地表面反射分割数
    Nr_lat = 90
    Nr_lon = 180

    abs_b = np.zeros(len(gl_in))
    abs_d = np.zeros(len(gl_in))
    abs_r = np.zeros(len(gl_in))
    I_abs = np.zeros(len(gl_in))
    for j in range(0, len(gl_in)):
        abs_b[j] = actual_abs_beam(gl_in, gl_type, phi_b)[j]
        abs_d[j] = actual_abs_diffuse(gl_in, gl_type, Nd_lat, Nd_lon)[j]
        abs_r[j] = actual_abs_reflect(gl_in, gl_type, Nr_lat, Nr_lon)[j]

        ata_in = ata_input(abs_b[j], abs_d[j], abs_r[j])
        I_abs[j] = absorb_sol(ita_in, ata_in)  # 斜面（開口面）吸収日射量

    print(I_abs)
