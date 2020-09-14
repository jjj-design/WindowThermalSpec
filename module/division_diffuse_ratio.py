from collections import namedtuple
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ptick
from mpl_toolkits.mplot3d import axes3d


class DdInput:

    def __init__(self, n_d_lat: int, n_d_lon: int):
        """

        Args:
            n_d_lat: 天空の緯度方向の分割数
            n_d_lon: 天空の経度方向の分割数
        """

        self._n_d_lat = n_d_lat
        self._n_d_lon = n_d_lon

    def division_diffuse_ratio(self, l_lat: int, m_lon: int) -> (float, float, float, float):
        """
        微小要素からの天空日射の割合の計算
        Args:
            l_lat: 天空の緯度方向のi番目の分割要素
            m_lon: 天空の経度方向のj番目の分割要素
        Returns:
            以下の4つの変数からなるタプル
                dd_f: 割合
                dd_h: 高度角
                dd_a: 方位角
                dd_phi: 入射角
        """

        dd_h = 90. * (2. * l_lat + 1) / (2. * self._n_d_lat)  # 式(4)
        dd_a = 180. * (2. * m_lon + 1) / (2. * self._n_d_lon) - 90.  # 式(5)
        dd_phi = math.degrees(math.acos(abs(math.cos(math.radians(dd_h)) * math.cos(math.radians(dd_a)))))  # 式(3)
        dd_omega = math.cos(math.radians(dd_h)) * math.pi ** 2. / (2. * self._n_d_lat * self._n_d_lon)  # 式(2)
        dd_f = 2 * dd_omega * math.cos(math.radians(dd_phi)) / math.pi  # 式(1)

        return dd_f, dd_h, dd_a, dd_phi

    def division_diffuse_ratios(self):

        # TODO: 将来的に numpy を使用して直接的に記述すること。

        dd_fs = np.empty((self._n_d_lat, self._n_d_lon))
        dd_hs = np.empty((self._n_d_lat, self._n_d_lon))
        dd_as = np.empty((self._n_d_lat, self._n_d_lon))
        dd_phis = np.empty((self._n_d_lat, self._n_d_lon))

        for l in range(0, self._n_d_lat):
            for m in range(0, self._n_d_lon):
                # 割合, _, _, 入射角
                dd_fs[l][m], dd_hs[l][m], dd_as[l][m], dd_phis[l][m] = self.division_diffuse_ratio(l_lat=l, m_lon=m)

        return dd_fs, dd_hs, dd_as, dd_phis


class DrInput:

    def __init__(self, n_r_lat: int, n_r_lon: int):
        """

        Args:
            n_r_lat: 地表面の緯度方向の分割数
            n_r_lon: 地表面の経度方向の分割数
        """

        self._n_r_lat = n_r_lat
        self._n_r_lon = n_r_lon

    def division_reflect_ratio(self, l_lat: int, m_lon: int) -> (float, float, float, float):
        """
        微小要素からの地表面反射日射の割合の計算
        Args:
            l_lat: 地表面の緯度方向のi番目の分割要素
            m_lon: 地表面の経度方向のj番目の分割要素
        Returns:
            割合、高度角、方位角、入射角
        """

        dr_h = 90. * (2. * l_lat + 1) / (2. * self._n_r_lat) - 90.  # 式(9)
        dr_a = 180. * (2. * m_lon + 1) / (2. * self._n_r_lon) - 90.  # 式(10)
        dr_phi = math.degrees(math.acos(abs(math.cos(math.radians(dr_h)) * math.cos(math.radians(dr_a)))))  # 式(8)
        dr_omega = math.cos(math.radians(dr_h)) * math.pi ** 2. / (2. * self._n_r_lat * self._n_r_lon)  # 式(7)
        dr_f = 2 * dr_omega * math.cos(math.radians(dr_phi)) / math.pi  # 式(6)

        return dr_f, dr_h, dr_a, dr_phi

    def division_reflect_ratios(self):

        # TODO: 将来的に numpy を使用して直接的に記述すること。

        dr_fs = np.empty((self._n_r_lat, self._n_r_lon))
        dr_hs = np.empty((self._n_r_lat, self._n_r_lon))
        dr_as = np.empty((self._n_r_lat, self._n_r_lon))
        dr_phis = np.empty((self._n_r_lat, self._n_r_lon))

        for l in range(0, self._n_r_lat):
            for m in range(0, self._n_r_lon):
                # 割合, _, _, 入射角
                dr_fs[l][m], dr_hs[l][m], dr_as[l][m], dr_phis[l][m] = self.division_reflect_ratio(l_lat=l, m_lon=m)

        return dr_fs, dr_hs, dr_as, dr_phis
