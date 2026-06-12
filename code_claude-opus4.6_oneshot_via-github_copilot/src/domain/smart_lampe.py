from domain.smart_geraet import SmartGeraet
from domain.enums import GeraeteTyp, GeraeteStatus


class SmartLampe(SmartGeraet):
    def __init__(self, geraetId: int = None, name: str = "",
                 status: GeraeteStatus = GeraeteStatus.NICHT_INSTALLIERT,
                 raumId: int = None, configuration: dict = None):
        super().__init__(geraetId, name, GeraeteTyp.LAMPE, status, raumId, configuration)

    def helligkeitAendern(self, helligkeit: int = 100) -> None:
        self.configuration["helligkeit"] = max(0, min(100, helligkeit))

    def farbeAendern(self, farbe: str = "weiss") -> None:
        self.configuration["farbe"] = farbe
