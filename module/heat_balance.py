"""面材の熱抵抗を計算するモジュール

面材の厚さと熱伝導率から面材の熱抵抗を計算する。

"""

from typing import List
import numpy as np
from scipy import optimize


class GlassLayer:
    """面材の熱抵抗を計算するクラス

    面材の厚さと熱伝導率から面材の熱抵抗を計算する。

    """

    def __init__(self, d: List[float], lmd: List[float], ia: float, epf: float, epb: float):
        """

        Args:
            d: 面材を構成する材料の厚さ, m
            lmd: 面材を構成する材料の熱伝導率, W/mK
            ia: 吸収日射量, W/m2
            epf: 正面側の放射率
            epb: 背面側の放射率
        """

        # 面材を構成する材料の暑さ, m
        self.d = d

        # 面材を構成する材料の熱伝導率, W/mK
        self.lmd = lmd

        # 面材を構成する材料の厚さから判断した材料の数
        d_len = len(d)
        # 面材を構成する材料の熱伝導率から判断した材料の数
        lmd_len = len(lmd)
        # 面材を構成する材料の厚さから判断した材料の数 と 面材を構成する材料の熱伝導率から判断した材料の数　が
        # 一致しているかどうかを判断し、一致していない場合はエラーをだす。
        if d_len != lmd_len:
            raise ValueError('次元が違います。')

        # 面材を構成する材料の数
        self.n = d_len

        # 吸収日射量, W/m2
        self.ia = ia

        # 正面側の放射率
        self.epf = epf

        # 背面側の放射率
        self.epb = epb

    def get_resistance(self):
        """面材の熱抵抗を計算する。

        Returns:
            面材の熱抵抗, m2K/W

        Notes:
            JIS R 2103：2014 5.4.3 面材の熱抵抗
        """

        return sum([self.d[i] / self.lmd[i] for i in range(self.n)])


class AirLayer:
    """中空層を表すクラス

    """

    def __init__(self, eps1: float, eps2: float, s: float, gastype1: int, gastype2: int, gasratio1: float, gasdir: int):
        """

        Args:
            eps1: 面1の修正放射率
            eps2: 面2の修正放射率
            s: 中空層の厚さ (m)
            gastype1: 気体1の種類flag（0：空気、1：アルゴン、2：SF6、3：クリプトン）
            gastype2: 気体2の種類flag（0：空気、1：アルゴン、2：SF6、3：クリプトン）
            gasratio1: 気体1の容積割合（0.0～1.0）
            gasdir: 中空層の熱流方向flag（0：中空層が垂直で熱流方向が水平、1：中空層が水平で熱流方向が上向き、2：中空層が45度で熱流方向が上向き）
        """

        self.eps1 = eps1
        self.eps2 = eps2
        self.s = s
        self.gastype1 = gastype1
        self.gastype2 = gastype2
        self.gasratio1 = gasratio1
        self.gasdir = gasdir

    def get_resistance(self, tmc1: float, tmc2: float) -> float:
        """

        Args:
            tmc1: 面1の表面温度, degree C
            tmc2: 面2の表面温度, degree C

        Returns:

        Notes:
            JIS R 3107:1998 4.1 基礎式
        """

        gasratio2 = 1.0 - self.gasratio1
        gap_dT = abs(tmc1 - tmc2)
        gap_Tmc = (tmc1 + tmc2) / 2.
        gap_Tm = gap_Tmc + 273.15
        ave_Tm = gap_Tm

        if self.gasdir == 0:
            gap_A = 0.035
            gap_n = 0.38
        elif self.gasdir == 1:
            gap_A = 0.16
            gap_n = 0.28
        elif self.gasdir == 2:
            gap_A = 0.1
            gap_n = 0.31

        sgm = 5.67 * 10. ** (-8.)

        for j in range(1, 5):
            gas_mix = gas_prop(self.gastype1, gap_Tmc, j) * self.gasratio1 + gas_prop(self.gastype2, gap_Tmc, j) * gasratio2
            if j == 1:
                gas_rho = gas_mix
            elif j == 2:
                gas_mu = gas_mix * 10. ** (-5.)
            elif j == 3:
                gas_lmd = gas_mix * 10. ** (-2.)
            elif j == 4:
                gas_c = gas_mix * 10. ** 3.
        gas_Gr = 9.81 * self.s ** 3. * gap_dT * gas_rho ** 2. / (gap_Tm * gas_mu ** 2.)
        gas_Pr = gas_mu * gas_c / gas_lmd
        gas_Nu = gap_A * (gas_Gr * gas_Pr) ** gap_n
        if gas_Nu <= 1.: gas_Nu = 1.
        gap_hg = gas_Nu * gas_lmd / self.s
        gap_hr = 4. * sgm * (1. / self.eps1 + 1. / self.eps2 - 1.) ** (-1.) * ave_Tm ** 3.
        return 1. / (gap_hr + gap_hg)


def gas_prop(gastype, gap_Tmc, j):

    if gastype == 0:  # 空気
        gp = np.array([[-10.0, 1.326, 1.661, 2.336, 1.008], [0.0, 1.277, 1.711, 2.416, 1.008],
                       [10.0, 1.232, 1.761, 2.496, 1.008], [20.0, 1.189, 1.811, 2.576, 1.008]])

    elif gastype == 1:  # アルゴン
        gp = np.array([[-10.0, 1.829, 2.038, 1.584, 0.519], [0.0, 1.762, 2.101, 1.634, 0.519],
                       [10.0, 1.699, 2.164, 1.684, 0.519], [20.0, 1.640, 2.228, 1.734, 0.519]])

    elif gastype == 2:  # SF6
        gp = np.array([[-10.0, 6.844, 1.383, 1.119, 0.614], [0.0, 6.602, 1.421, 1.197, 0.614],
                       [10.0, 6.360, 1.459, 1.275, 0.614], [20.0, 6.118, 1.497, 1.354, 0.614]])

    elif gastype == 3:  # クリプトン
        gp = np.array([[-10.0, 3.832, 2.260, 0.842, 0.245], [0.0, 3.690, 2.330, 0.870, 0.245],
                       [10.0, 3.560, 2.400, 0.900, 0.245], [20.0, 3.430, 2.470, 0.926, 0.245]])

    for i in range(1, 4):
        if i == 1 and gap_Tmc < gp[i - 1, 0]:
            break
        elif gp[i - 1, 0] <= gap_Tmc and gap_Tmc < gp[i, 0]:
            break
        elif i == 3 and gp[i, 0] <= gap_Tmc:
            break

    gp_cal = gp[i - 1, j] + (gp[i, j] - gp[i - 1, j]) * (gap_Tmc - gp[i - 1, 0]) / (gp[i, 0] - gp[i - 1, 0])

    return gp_cal


class SurfaceLayer:

    def __init__(self, t_mcr:float, eps: float, cnvtype: str):
        """

        Args:
            t_mcr: 周囲の放射温度（℃）
            eps: 表面放射率
            cnvtype: 対流熱伝達のflag（0：夏期室内、1：夏期屋外、2：冬期室内、3：冬期屋外）
        """

        self.t_mcr = t_mcr
        self.eps = eps
        self.shc_hc = {
            'summer_inside': 2.5,
            'summer_outside': 8.0,
            'winter_inside': 3.6,
            'winter_outside': 20.0
        }[cnvtype]

    def get_resistance(self, t_mcs):

        tms = t_mcs + 273.15
        tmr = self.t_mcr + 273.15
        sgm = 5.67 * 10.0 ** (-8.0)
        shc_hr = self.eps * sgm * (tms ** 4 - tmr ** 4) / (tms - tmr)

        return 1.0 / (shc_hr + self.shc_hc)


def Heat_balance(gls: List[GlassLayer], als: List[AirLayer], season:str, te:float, ti:float):
    """

    Args:
        gls:
        als:
        season: {summer, winter}
        te: 外気温度, degree C
        ti: 室温, degree C

    Returns:

    """

    # 面材の層数
    n = len(gls)

    q_b = np.zeros(2 * n)
    for i in range(0, n):
        q_b[2 * i] = gls[i].ia / 2.0
        q_b[2 * i + 1] = gls[i].ia / 2.0

    # 表面レイヤー
    sl_out = SurfaceLayer(
        t_mcr=te,
        eps=gls[0].epf,
        cnvtype={'summer': 'summer_outside', 'winter': 'winter_outside'}[season]
    )
    sl_in = SurfaceLayer(
        t_mcr=ti,
        eps=gls[n - 1].epb,
        cnvtype={'summer': 'summer_inside', 'winter': 'winter_inside'}[season]
    )

    def get_r(t):

        # 熱抵抗の初期化
        r = np.zeros(2 * n + 1)

        # 熱抵抗の配列
        # 室外側表面の熱抵抗
        r[0] = sl_out.get_resistance(t_mcs=t[0])
        for i in range(n):
            # 面材の熱抵抗
            r[2 * i + 1] = gls[i].get_resistance()
        for i in range(n - 1):
            # 面材間の中空層の熱抵抗
            r[2 * (i + 1)] = als[i].get_resistance(tmc1=t[2 * i + 1], tmc2=t[2 * (i + 1)])
        # 室内側表面の熱抵抗
        r[2 * n] = sl_in.get_resistance(t_mcs=t[2 * n - 1])

        return r

    def get_heat_flow(t):

        r = get_r(t)

        # 行列式の生成
        ca = np.zeros((2 * n, 2 * n))

        for i in range(2 * n):
            ca[i][i] = 1 / r[i] + 1 / r[i + 1]
        for i in range(2 * n - 1):
            ca[i + 1][i] = - 1 / r[i + 1]
            ca[i][i + 1] = - 1 / r[i + 1]

        cb = np.zeros((2 * n))

        for i in range(2 * n):

            if i == 0:
                cb[i] = q_b[i] + te / r[i]
            elif i == 2 * n - 1:
                cb[i] = q_b[i] + ti / r[i + 1]
            else:
                cb[i] = q_b[i]

        return cb - np.dot(ca, t.reshape(-1, 1)).flatten()

    result = optimize.root(get_heat_flow, np.full(2 * n, (te + ti) / 2), method='lm')

    theta_g = result.x

    return np.append(np.insert(theta_g, 0, te), ti), get_r(theta_g)


if __name__ == '__main__':

    gl1 = GlassLayer(d=[0.003, 0.006], lmd=[1.0, 0.5], ia=None, epf=None, epb=None)
    print(gl1.get_resistance())

    gl2 = GlassLayer(d=[0.005], lmd=[1.0], ia=None, epf=None, epb=None)
    print(gl2.get_resistance())

    al1 = AirLayer(eps1=0.837, eps2=0.837, s=0.012, gastype1=0, gastype2=0, gasratio1=1.0, gasdir=0)
    print(al1.get_resistance(tmc1=0.0, tmc2=20.0))

    al2 = AirLayer(eps1=0.837, eps2=0.837, s=0.012, gastype1=0, gastype2=0, gasratio1=1.0, gasdir=0)
    print(al2.get_resistance(tmc1=30.0, tmc2=25.0))

    al3 = AirLayer(eps1=0.837, eps2=0.837, s=0.012, gastype1=1, gastype2=0, gasratio1=0.8, gasdir=0)
    print(al3.get_resistance(tmc1=0.0, tmc2=20.0))

    sl1 = SurfaceLayer(t_mcr=20.0, eps=0.837, cnvtype='winter_inside')
    print(sl1.get_resistance(t_mcs=16.0))

    sl2 = SurfaceLayer(t_mcr=0.0, eps=0.837, cnvtype='winter_outside')
    print(sl2.get_resistance(t_mcs=4.0))

    season = 'cooling'

    # 外気温度
    te = {
        'cooling': 30.0,
        'heating': 0.0
    }[season]

    # 室温
    ti = {
        'cooling': 25.0,
        'heating': 20.0
    }[season]

    gls = [
        GlassLayer(
            d=[0.003, 0.006],  # グレージングの厚さ
            lmd=[1.0, 0.5],  # グレージングの熱伝導率
            ia=9.55935027,  # 各層の吸収日射量
            epf=0.837,  # 各層の正面側の放射率
            epb=0.837  # 各層の背面側の放射率
        ),
        GlassLayer(
            d=[0.003],  # グレージングの厚さ
            lmd=[1.0],  # グレージングの熱伝導率
            ia=6.8267886,  # 各層の吸収日射量
            epf=0.837,  # 各層の正面側の放射率
            epb=0.837  # 各層の背面側の放射率
        ),
        GlassLayer(
            d=[0.003],  # グレージングの厚さ
            lmd=[1.0],  # グレージングの熱伝導率
            ia=4.76774099,  # 各層の吸収日射量
            epf=0.837,  # 各層の正面側の放射率
            epb=0.837  # 各層の背面側の放射率
        )
    ]

    als = [
        AirLayer(
            eps1=gls[0].epb,
            eps2=gls[1].epf,
            s=0.012,  # 中空層の厚さ
            gastype1=0,  # 中空層の気体1の種類flag（0：空気、1：アルゴン、2：SF6、3：クリプトン）
            gastype2=0,  # 中空層の気体2の種類flag（0：空気、1：アルゴン、2：SF6、3：クリプトン）
            gasratio1=1.0,  # 中空層の気体1の容積割合（0.0～1.0）
            gasdir=0  # 中空層の熱流方向flag（0：中空層が垂直で熱流方向が水平、1：中空層が水平で熱流方向が上向き、2：中空層が45度で熱流方向が上向き）
        ),
        AirLayer(
            eps1=gls[1].epb,
            eps2=gls[2].epf,
            s=0.012,  # 中空層の厚さ
            gastype1=0,  # 中空層の気体1の種類flag（0：空気、1：アルゴン、2：SF6、3：クリプトン）
            gastype2=0,  # 中空層の気体2の種類flag（0：空気、1：アルゴン、2：SF6、3：クリプトン）
            gasratio1=1.0,  # 中空層の気体1の容積割合（0.0～1.0）
            gasdir=0  # 中空層の熱流方向flag（0：中空層が垂直で熱流方向が水平、1：中空層が水平で熱流方向が上向き、2：中空層が45度で熱流方向が上向き）
        )
    ]

    hbr = Heat_balance(gls=gls, als=als, season='summer', te=te, ti=ti)

    tglz = hbr[0][0 : 2 * (len(gls) + 1)]
    Rglz = hbr[1][0 : 2 * len(gls) + 1]

    print ('tglz', tglz)
    print ('Rglz', Rglz)


