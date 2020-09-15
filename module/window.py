from typing import List

from module import oblique_incidence_property
from module import solar_radiation_of_glazing as srg


class Window:

    def __init__(
            self,
            oips: List[oblique_incidence_property.ObliqueIncidenceProperty],
            n_d_lat: int = 90,
            n_d_lon: int = 180,
            n_r_lat: int = 90,
            n_r_lon: int = 180
    ):
        """

        Args:
            oips:
            n_d_lat: 緯度方向の天空分割数
            n_d_lon: 経度方向の天空分割数
            n_r_lat: 緯度方向の地表面反射分割数
            n_r_lon: 経度方向の地表面反射分割数
        """

        self._oips = oips
        self._n_d_lat = n_d_lat
        self._n_d_lon = n_d_lon
        self._n_r_lat = n_r_lat
        self._n_r_lon = n_r_lon

    def actual_trans_beam(self, phi):
        return srg.actual_trans_beam(oips=self._oips, phi_b=phi)

    def actual_abs_beam(self, phi):
        return srg.actual_abs_beam(oips=self._oips, phi_b=phi)

    def actual_trans_diffuse(self) -> float:
        return srg.actual_trans_diffuse(oips=self._oips, Nd_lat=self._n_d_lat, Nd_lon=self._n_d_lon)

    def actual_abs_diffuse(self):
        return srg.actual_abs_diffuse(oips=self._oips, Nd_lat=self._n_d_lat, Nd_lon=self._n_d_lon)

    def actual_trans_reflect(self):
        return srg.actual_trans_reflect(oips=self._oips, Nr_lat=self._n_r_lat, Nr_lon=self._n_r_lon)

    def actual_abs_reflect(self):
        return srg.actual_trans_reflect(oips=self._oips, Nr_lat=self._n_r_lat, Nr_lon=self._n_r_lon)

