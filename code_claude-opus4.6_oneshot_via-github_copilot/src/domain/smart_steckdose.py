from domain.smart_geraet import SmartGeraet
from domain.enums import GeraeteTyp, GeraeteStatus


class SmartSteckdose(SmartGeraet):
    def __init__(self, geraetId: int = None, name: str = "",
                 status: GeraeteStatus = GeraeteStatus.NICHT_INSTALLIERT,
                 raumId: int = None, configuration: dict = None):
        super().__init__(geraetId, name, GeraeteTyp.STECKDOSE, status, raumId, configuration)

    def stromverbrauchAuslesen(self) -> float:
        return self.configuration.get("stromverbrauch", 0.0)
