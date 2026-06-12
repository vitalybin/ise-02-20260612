from domain.smart_geraet import SmartGeraet
from domain.enums import GeraeteTyp, GeraeteStatus


class SmartHeizung(SmartGeraet):
    def __init__(self, geraetId: int = None, name: str = "",
                 status: GeraeteStatus = GeraeteStatus.NICHT_INSTALLIERT,
                 raumId: int = None, configuration: dict = None):
        super().__init__(geraetId, name, GeraeteTyp.HEIZUNG, status, raumId, configuration)

    def zieltemperaturSetzen(self, temperatur: float = 21.0) -> None:
        self.configuration["zieltemperatur"] = max(5.0, min(30.0, temperatur))
