from abc import ABC, abstractmethod
from domain.smart_geraet import SmartGeraet
from domain.enums import GeraeteTyp, GeraeteStatus


class ISmartSteckdose(ABC):
    """<<interface>> ISmartSteckdose"""

    @abstractmethod
    def stromverbrauchAuslesen(self) -> float:
        pass


class SmartSteckdose(SmartGeraet, ISmartSteckdose):
    def __init__(self, geraetId: int = None, name: str = "",
                 status: GeraeteStatus = GeraeteStatus.NICHT_INSTALLIERT,
                 raumId: int = None, configuration: dict = None):
        super().__init__(geraetId, name, GeraeteTyp.STECKDOSE, status, raumId, configuration)

    def stromverbrauchAuslesen(self) -> float:
        return self.configuration.get("stromverbrauch", 0.0)

    def kalibrieren(self) -> None:
        self.configuration["kalibriert"] = True
