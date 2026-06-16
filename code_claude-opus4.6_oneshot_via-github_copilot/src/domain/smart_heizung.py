from abc import ABC, abstractmethod
from domain.smart_geraet import SmartGeraet
from domain.enums import GeraeteTyp, GeraeteStatus


class ISmartHeizung(ABC):
    """<<interface>> ISmartHeizung"""

    @abstractmethod
    def zieltemperaturSetzen(self, temperatur: float = 21.0) -> None:
        pass


class SmartHeizung(SmartGeraet, ISmartHeizung):
    def __init__(self, geraetId: int = None, name: str = "",
                 status: GeraeteStatus = GeraeteStatus.NICHT_INSTALLIERT,
                 raumId: int = None, configuration: dict = None):
        super().__init__(geraetId, name, GeraeteTyp.HEIZUNG, status, raumId, configuration)

    def zieltemperaturSetzen(self, temperatur: float = 21.0) -> None:
        self.configuration["zieltemperatur"] = max(5.0, min(30.0, temperatur))

    def kalibrieren(self) -> None:
        self.configuration["kalibriert"] = True
