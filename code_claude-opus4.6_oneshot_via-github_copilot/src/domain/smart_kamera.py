from domain.smart_geraet import SmartGeraet
from domain.enums import GeraeteTyp, GeraeteStatus


class SmartKamera(SmartGeraet):
    def __init__(self, geraetId: int = None, name: str = "",
                 status: GeraeteStatus = GeraeteStatus.NICHT_INSTALLIERT,
                 raumId: int = None, configuration: dict = None):
        super().__init__(geraetId, name, GeraeteTyp.KAMERA, status, raumId, configuration)

    def modusAendern(self, modus: str = "normal") -> None:
        self.configuration["modus"] = modus
