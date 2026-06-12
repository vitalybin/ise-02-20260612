from domain.smart_geraet import SmartGeraet
from domain.enums import GeraeteTyp, GeraeteStatus


class SmartSensor(SmartGeraet):
    def __init__(self, geraetId: int = None, name: str = "",
                 status: GeraeteStatus = GeraeteStatus.NICHT_INSTALLIERT,
                 raumId: int = None, configuration: dict = None):
        super().__init__(geraetId, name, GeraeteTyp.SENSOR, status, raumId, configuration)

    def messwertAuslesen(self) -> float:
        return self.configuration.get("messwert", 0.0)

    def kalibrieren(self) -> None:
        self.configuration["kalibriert"] = True
