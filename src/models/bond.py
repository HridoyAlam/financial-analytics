from asset import Asset
class Bond(Asset):
    def __init__(self, 
                 ticker: str, 
                 name: str, 
                 prices: list[float],
                face_value: float,
                coupon_rate: float,
                maturity_years: float
                 ) -> None:
        super().__init__(ticker, name, prices)

        if face_value <= 0:
            raise ValueError("face_value must be greater than 0")
        
        if coupon_rate <= 0:
            raise ValueError("coupon_rate must be greater than 0")
        
        if maturity_years <= 0:
            raise ValueError("maturity_years must be greater than 0")

        self._face_value = face_value
        self._coupon_rate = coupon_rate
        self._maturity_years = maturity_years

    @property
    def face_value(self) -> float:
        return self._face_value

    @property
    def coupon_rate(self) -> float:
        return self._coupon_rate

    @property
    def maturity_years(self) -> float:
        return self._maturity_years

    def __str__(self) -> str:
        return super().__str__()+f" {self.face_value} {self.coupon_rate} {self.maturity_years}"

    def annual_coupon_payment(self) -> float:
        return self.face_value * self.coupon_rate / 100

# bond  = Bond(
#     "US10Y",
#     "US Treasury 10-Year Bond",
#     [98, 99, 100],
#     1000,
#     4.25,
#     10
# )
# print(bond)
# print(bond.current_price())
# print(bond.total_return())
# print(bond.total_return_percent())
# print(bond.annual_coupon_payment())
