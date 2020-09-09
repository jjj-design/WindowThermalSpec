# %%

from collections import namedtuple
import csv
import math
import numpy as np
import matplotlib.pyplot as plt

import nbimporter
import RollershadeAngularProperty as RAP
import IncidentSolarRadiationOnGlazing as ISROG
import DivisionDiffuseRatio as DDR

from module import multiple_reflection as mr
from module import glass_angular_property as gap

# %% md

# 開口面透過日射量を計算するモジュール

# %% md

## 1. Functions

# %% md

開口面日射量（直達・天空・地表面反射）とグレージング複合体の日射透過率から開口面透過日射量を計算する。

# %% md

### 入力値

$ I_
{T, b} $ ：斜面（開口面）直達日射量(W / m < sup > 2 < / sup >)
$ I_
{T, d} $ ：斜面（開口面）天空日射量(W / m < sup > 2 < / sup >)
$ I_
{T, r} $ ：斜面（開口面）地表面反射日射量(W / m < sup > 2 < / sup >)
$ \tau_
{glz, b} $ ：直達日射に対する日射透過率
$ \tau_
{glz, d, l, m} $ ：天空上の微小要素からの入射日射に対する日射透過率
$ \tau_
{glz, r, l, m} $ ：地表面上の微小要素からの入射日射に対する日射透過率
$ F_
{d, l, m} $ ：天空日射量に対する天空上の微小要素からの天空日射量の割合
$ F_
{r, l, m} $ ：地表面反射日射量に対する地表面上の微小要素からの地表面反射日射量の割合

# %% md

### 出力値

$ I_
{\tau} $ ：開口面透過日射量(W / m < sup > 2 < / sup >)

# %% md

### 計算方法

#### データ構造と値の範囲

$ \tau_
{glz, b} $・$ \tau_
{glz, d} $・$ \tau_
{glz, r} $ の組み合わせをクラス『tta＿input』とする。

# %%

class tta_input():
    def __init__(self, taub, taud, taur):
        self.taub = taub
        self.taud = taud
        self.taur = taur


# taub：直達成分の日射透過率
# taud：天空成分の日射透過率
# taur：地表面反射成分の日射透過率

# %% md

#### 透過日射量の計算

透過日射量の計算方法を以下に示す。

# %% md

$$
\begin
{eqnarray}
& \displaystyle
I_
{\tau} = I_
{T, b} \cdot \tau_
{glz, b} + I_
{T, d} \cdot \tau_
{glz, d} + I_
{T, r} \cdot \tau_
{glz, r} & \qquad\qquad\text
{(1)} \nonumber\ \
    \nonumber \ \
    & \displaystyle \tau_
{glz, d} = \sum_
{l = 0} ^ {N_
{d, lat} - 1}\sum_
{m = 0} ^ {N_
{d, lon} - 1} F_
{d, l, m} \cdot \tau_
{glz, d, l, m} & \qquad\qquad\text
{(2)} \nonumber\ \
    \nonumber \ \
    & \displaystyle \tau_
{glz, r} = \sum_
{l = 0} ^ {N_
{r, lat} - 1}\sum_
{m = 0} ^ {N_
{r, lon} - 1} F_
{r, l, m} \cdot \tau_
{glz, r, l, m} & \qquad\qquad\text
{(3)} \nonumber\ \
    \end
{eqnarray}
$$

# %%

# 開口面透過日射量
def transmit_sol(L, M):
    return L.Itb * M.taub + L.Itd * M.taud + L.Itr * M.taur


# 直達日射での透過率
def actual_trans_beam(L, gl_type, phi_b):
    r_taub = 0.
    ly_in_b = np.empty(len(L), dtype=tuple)
    for j in range(0, len(L)):
        if gl_type[j] == 0:  # ガラス
            p = L[j].glass_ang_prop(phi=phi_b)
            ly_in_b[j] = mr.SolarSpecSingleLayer(tau_f=p[0], tau_b=p[1], rho_f=p[2], rho_b=p[3])
        elif gl_type[j] == 1:  # ロールスクリーン
            ly_in_b[j] = mr.SolarSpecSingleLayer(
                RAP.role_ang_prop(L[j], phi_b)[0],
                RAP.role_ang_prop(L[j], phi_b)[1],
                RAP.role_ang_prop(L[j], phi_b)[2],
                RAP.role_ang_prop(L[j], phi_b)[3]
            )

    return mr.get_total_solar_spec(ly_in_b).tau_f


# 天空日射での透過率
def actual_trans_diffuse(L, gl_type, Nd_lat, Nd_lon):
    F_d = np.empty((Nd_lat, Nd_lon))
    phi_d = np.empty((Nd_lat, Nd_lon))
    tau_d = np.empty((Nd_lat, Nd_lon))
    r_taud = 0.
    ly_in_d = np.empty(len(L), dtype=tuple)
    for l in range(0, Nd_lat):
        for m in range(0, Nd_lon):
            dd_in = DDR.dd_input(Nd_lat, Nd_lon, l, m)
            F_d[l][m] = DDR.division_diffuse_ratio(dd_in)[0]  # 割合
            phi_d[l][m] = DDR.division_diffuse_ratio(dd_in)[3]  # 入射角

            for j in range(0, len(L)):
                if gl_type[j] == 0:  # ガラス
                    p = L[j].glass_ang_prop(phi=phi_d[l][m])
                    ly_in_d[j] = mr.SolarSpecSingleLayer(tau_f=p[0], tau_b=p[1], rho_f=p[2], rho_b=p[3])
                elif gl_type[j] == 1:  # ロールスクリーン
                    ly_in_d[j] = mr.SolarSpecSingleLayer(
                        RAP.role_ang_prop(L[j], phi_d[l][m])[0],
                        RAP.role_ang_prop(L[j], phi_d[l][m])[1],
                        RAP.role_ang_prop(L[j], phi_d[l][m])[2],
                        RAP.role_ang_prop(L[j], phi_d[l][m])[3]
                    )

            tau_d[l][m] = mr.get_total_solar_spec(ly_in_d).tau_f

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
            dr_in = DDR.dr_input(Nr_lat, Nr_lon, l, m)
            F_r[l][m] = DDR.division_reflect_ratio(dr_in)[0]  # 割合
            phi_r[l][m] = DDR.division_reflect_ratio(dr_in)[3]  # 入射角

            for j in range(0, len(L)):
                if gl_type[j] == 0:  # ガラス
                    p = L[j].glass_ang_prop(phi=phi_r[l][m])
                    ly_in_r[j] = mr.SolarSpecSingleLayer(tau_f=p[0], tau_b=p[1], rho_f=p[2], rho_b=p[3])
                elif gl_type[j] == 1:  # ロールスクリーン
                    ly_in_r[j] = mr.SolarSpecSingleLayer(
                        RAP.role_ang_prop(L[j], phi_r[l][m])[0],
                        RAP.role_ang_prop(L[j], phi_r[l][m])[1],
                        RAP.role_ang_prop(L[j], phi_r[l][m])[2],
                        RAP.role_ang_prop(L[j], phi_r[l][m])[3]
                    )

            tau_r[l][m] = mr.get_total_solar_spec(ly_in_r).tau_f

            r_taur += F_r[l][m] * tau_r[l][m]

    return r_taur


# %% md

#### Example

# %%

if __name__ == '__main__':
    # 面材の種類
    gl_type = [0, 0, 1]  # 各層のグレージング種類（0：ガラス、1：ロールスクリーン、2：横型ブラインド、3：縦型ブラインド）

    # 面材ごとの光学特性
    gl_in = [
        gap.GlassInput(trs_0_f=0.815, trs_0_b=0.815, ref_0_f=0.072, ref_0_b=0.072, gtype=0, c_type_f=False, c_type_b=False),
        gap.GlassInput(trs_0_f=0.815, trs_0_b=0.815, ref_0_f=0.072, ref_0_b=0.072, gtype=0, c_type_f=False, c_type_b=False),
        RAP.role_input(0.3, 0.3, 0.63, 0.63)
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

    tau_b = actual_trans_beam(gl_in, gl_type, phi_b)
    tau_d = actual_trans_diffuse(gl_in, gl_type, Nd_lat, Nd_lon)
    tau_r = actual_trans_reflect(gl_in, gl_type, Nr_lat, Nr_lon)

    tta_in = tta_input(tau_b, tau_d, tau_r)
    I_tau = transmit_sol(ita_in, tta_in)  # 斜面（開口面）透過日射量

    print(I_tau)

# %%


