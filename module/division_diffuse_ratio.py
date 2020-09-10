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
            割合、高度角、方位角、入射角
        """

        dd_h = 90. * (2. * l_lat + 1) / (2. * self._n_d_lat)  # 式(4)
        dd_A = 180. * (2. * m_lon + 1) / (2. * self._n_d_lon) - 90.  # 式(5)
        dd_phi = math.degrees(math.acos(abs(math.cos(math.radians(dd_h)) * math.cos(math.radians(dd_A)))))  # 式(3)
        dd_omega = math.cos(math.radians(dd_h)) * math.pi ** 2. / (2. * self._n_d_lat * self._n_d_lon)  # 式(2)
        dd_f = 2 * dd_omega * math.cos(math.radians(dd_phi)) / math.pi  # 式(1)

        return dd_f, dd_h, dd_A, dd_phi


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
        dr_A = 180. * (2. * m_lon + 1) / (2. * self._n_r_lon) - 90.  # 式(10)
        dr_phi = math.degrees(math.acos(abs(math.cos(math.radians(dr_h)) * math.cos(math.radians(dr_A)))))  # 式(8)
        dr_omega = math.cos(math.radians(dr_h)) * math.pi ** 2. / (2. * self._n_r_lat * self._n_r_lon)  # 式(7)
        dr_f = 2 * dr_omega * math.cos(math.radians(dr_phi)) / math.pi  # 式(6)

        return dr_f, dr_h, dr_A, dr_phi

