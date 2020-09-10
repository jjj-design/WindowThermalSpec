import math
from typing import List


class GlassInput:

    def __init__(
            self,
            trs_0_f: float,
            trs_0_b: float,
            ref_0_f: float,
            ref_0_b: float,
            gtype: int,
            c_type_f: bool,
            c_type_b: bool
    ):
        """

        Args:
            trs_0_f: 正面側からの入射光に対する垂直入射時の日射透過率
            trs_0_b: 背面側からの入射光に対する垂直入射時の日射透過率
            ref_0_f: 正面側からの入射光に対する垂直入射時の日射反射率
            ref_0_b: 背面側からの入射光に対する垂直入射時の日射反射率
            gtype: ガラスの種類flag（0：透明フロート板ガラス、1：Low-Eガラス）
            c_type_f: 正面側の膜の有無（FALSE：膜なし、TRUE：膜あり）
            c_type_b: 背面側の膜の有無（FALSE：膜なし、TRUE：膜あり）
        """

        self._trs_0_f = trs_0_f
        self._trs_0_b = trs_0_b
        self._ref_0_f = ref_0_f
        self._ref_0_b = ref_0_b
        self._gtype = gtype
        self._c_type_f = c_type_f
        self._c_type_b = c_type_b

    def get_ang_prop(self, phi: float) -> (float, float, float, float):
        """
        入射角φの日射透過率及び日射反射率の計算
        Args:
            phi:入射角, degree
        Returns:

        """

        # 斜め入射のコサイン
        cos_phi = math.cos(math.radians(phi))

        # 規準化透過率(正面側)
        trs_n_f = sum([self._get_m_trs()[i] * cos_phi ** i for i in range(0, 6)])

        # 規準化透過率(背面側)
        trs_n_b = sum([self._get_m_trs()[i] * cos_phi ** i for i in range(0, 6)])

        # 規準化反射率(正面側)
        ref_n_f = sum([self.get_m_ref(c_type=self._c_type_f)[i] * cos_phi ** i for i in range(0, 6)])

        # 規準化反射率(背面側)
        ref_n_b = sum([self.get_m_ref(c_type=self._c_type_b)[i] * cos_phi ** i for i in range(0, 6)])

        # 入射角φの透過率(正面側)
        trs_f = self._trs_0_f * trs_n_f

        # 入射角φの透過率(背面側)
        trs_b = self._trs_0_b * trs_n_b

        # 入射角φの反射率(正面側)
        ref_f = self._ref_0_f + (1 - self._ref_0_f) * ref_n_f

        # 入射角φの反射率(背面側)
        ref_b = self._ref_0_b + (1 - self._ref_0_b) * ref_n_b

        return trs_f, trs_b, ref_f, ref_b

    def _get_m_trs(self) -> List[float]:
        """
        規準化透過率の計算に用いる係数mを取得する。
        Returns:
            係数m
        Notes:
            ここでは、透明フロート板ガラス及びLow-Eガラスのみを記述する。
        """

        return {
            0: [0.000, 2.552, 1.364, -11.388, 13.617, -5.146],
            1: [0.000, 2.273, 1.631, -10.358, 11.769, -4.316]
        }[self._gtype]

    def get_m_ref(self, c_type: int) -> List[float]:
        """
        規準化反射率の計算に用いる係数mを取得する。
        Args:
            c_type: 膜の有無（あり=1, なし=0)
        Returns:
            係数m
        Notes:
            ここでは、透明フロート板ガラス及びLow-Eガラスのみを記述する。
        """

        if self._gtype == 0:

            return [1.000, -5.189, 12.392, -16.593, 11.851, -3.461]

        elif self._gtype == 1:

            # 膜あり
            if c_type:
                return [1.000, -4.387, 9.175, -11.152, 7.416, -2.052]
            # 膜なし
            else:
                return [1.000, -5.084, 12.646, -18.213, 13.967, -4.316]

        else:

            raise ValueError


class RoleInput:

    def __init__(self, trs_0_f: float, trs_0_b: float, ref_0_f: float, ref_0_b: float):
        """

        Args:
            trs_0_f: 正面側からの入射光に対する垂直入射時の日射透過率
            trs_0_b: 背面側からの入射光に対する垂直入射時の日射透過率
            ref_0_f: 正面側からの入射光に対する垂直入射時の日射反射率
            ref_0_b: 背面側からの入射光に対する垂直入射時の日射反射率
        """

        self._trs_0_f = trs_0_f
        self._trs_0_b = trs_0_b
        self._ref_0_f = ref_0_f
        self._ref_0_b = ref_0_b

    #
    def get_ang_prop(self, phi):
        """
        入射角φの日射透過率及び日射反射率の計算
        Args:
            phi: 入射角
        Returns:
            日射反射率
        """
        return self._trs_0_f, self._trs_0_b, self._ref_0_f, self._ref_0_b
