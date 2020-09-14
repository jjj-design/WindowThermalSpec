"""
開口面入射日射量を計算するモジュール
"""


class ItaInput:

    def __init__(self, itb: float, itd: float, itr: float):
        """

        Args:
            itb: 斜面（開口面）直達日射量, W/m2
            itd: 斜面（開口面）天空日射量, W/m2
            itr: 斜面（開口面）地表面反射日射量, W/m2
        """

        self._itb = itb
        self._itd = itd
        self._itr = itr

    @property
    def itb(self):
        return self._itb

    @property
    def itd(self):
        return self._itd

    @property
    def itr(self):
        return self._itr

    def incident_sol(self):
        """
        開口面入射日射量（合計値）を求める。
        Returns:
            開口面入射日射量（合計値）, W/m2
        """

        return self._itb + self._itd + self._itr


if __name__ == '__main__':

    ita_in = ItaInput(2.6840261248 * 10. ** 6. / 3600., 0.1181932153 * 10. ** 6. / 3600., 0.094 * 10. ** 6. / 3600.)

    # 斜面（開口面）全天日射量
    I_in = ita_in.incident_sol()

    print(I_in)

