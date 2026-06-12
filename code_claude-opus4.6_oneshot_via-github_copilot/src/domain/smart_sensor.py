from abc import ABC, abstractmethod
from domain.smart_geraet import SmartGeraet
from domain.enums import GeraeteTyp, GeraeteStatus


class ISmartSensor(ABC):
    """<<interface>> ISmartSensor"""

    @abstractmethod
    def messwertAuslesen(self) -> float:
        pass

    @abstractmethod
    def kalibrieren(self) -> None:
        pass


class SmartSensor(SmartGeraet, ISmartSensor):
    def __init__(self, geraetId: int = None, name: str = "",
                 status: GeraeteStatus = GeraeteStatus.NICHT_INSTALLIERT,
                 raumId: int = None, configuration: dict = None):
        super().__init__(geraetId, name, GeraeteTyp.SENSOR, status, raumId, configuration)

    def messwertAuslesen(self) -> float:
        return self.configuration.get("messwert", 0.0)

    def kalibrieren(self) -> None:
        self.configuration["kalibriert"] = True
