import math


class glass_input():

    def __init__(self, TRS0f, TRS0b, REF0f, REF0b, gtype, ctypef, ctypeb):

        self.TRS0f = TRS0f
        self.TRS0b = TRS0b
        self.REF0f = REF0f
        self.REF0b = REF0b
        self.gtype = gtype
        self.ctypef = ctypef
        self.ctypeb = ctypeb

# TRS0f：正面側からの入射光に対する垂直入射時の日射透過率
# TRS0f：正面側からの入射光に対する垂直入射時の日射透過率
# TRS0b：背面側からの入射光に対する垂直入射時の日射透過率
# REF0f：正面側からの入射光に対する垂直入射時の日射反射率
# REF0b：背面側からの入射光に対する垂直入射時の日射反射率
# gtype：ガラスの種類flag（0：透明フロート板ガラス、1：Low-Eガラス）
# ctypef：正面側の膜の有無flag（0：膜なし、1：膜あり）
# ctypeb：背面側の膜の有無flag（0：膜なし、1：膜あり）


# 入射角φの日射透過率及び日射反射率の計算
def glass_ang_prop(L, phi):
    TRSnf = 0.
    TRSnb = 0.
    REFnf = 0.
    REFnb = 0.
    for i in range(0, 6):
        TRSnf += glass_mTRS(L)[i] * math.cos(math.radians(phi)) ** i  # 規準化透過率(正面側)
        TRSnb += glass_mTRS(L)[i] * math.cos(math.radians(phi)) ** i  # 規準化透過率(背面側)
        if L.ctypef == 0:
            REFnf += glass_mREFg(L)[i] * math.cos(math.radians(phi)) ** i  # 規準化反射率(正面側、膜なし)
        elif L.ctypef == 1:
            REFnf += glass_mREFc(L)[i] * math.cos(math.radians(phi)) ** i  # 規準化反射率(正面側、膜あり)

        if L.ctypeb == 0:
            REFnb += glass_mREFg(L)[i] * math.cos(math.radians(phi)) ** i  # 規準化反射率(背面側、膜なし)
        elif L.ctypeb == 1:
            REFnb += glass_mREFc(L)[i] * math.cos(math.radians(phi)) ** i  # 規準化反射率(背面側、膜あり)

    TRSf = L.TRS0f * TRSnf  # 入射角φの透過率(正面側)
    TRSb = L.TRS0b * TRSnb  # 入射角φの透過率(背面側)
    REFf = L.REF0f + (1 - L.REF0f) * REFnf  # 入射角φの反射率(正面側)
    REFb = L.REF0b + (1 - L.REF0b) * REFnb  # 入射角φの反射率(背面側)

    return TRSf, TRSb, REFf, REFb


# 係数mの選択。ここでは、透明フロート板ガラス及びLow-Eガラスのみを記述する。
def glass_mTRS(L):
    if L.gtype == 0:
        return [0.000, 2.552, 1.364, -11.388, 13.617, -5.146]
    elif L.gtype == 1:
        return [0.000, 2.273, 1.631, -10.358, 11.769, -4.316]
    else:
        return ValueError


def glass_mREFg(L):
    if L.gtype == 0:
        return [1.000, -5.189, 12.392, -16.593, 11.851, -3.461]
    elif L.gtype == 1:
        return [1.000, -5.084, 12.646, -18.213, 13.967, -4.316]
    else:
        return ValueError


def glass_mREFc(L):
    if L.gtype == 0:
        return ValueError
    elif L.gtype == 1:
        return [1.000, -4.387, 9.175, -11.152, 7.416, -2.052]
    else:
        return ValueError


