from abc import ABC, abstractmethod
from domain.smart_geraet import SmartGeraet
from domain.enums import GeraeteTyp, GeraeteStatus


class ISmartKamera(ABC):
    """<<interface>> ISmartKamera"""

    @abstractmethod
    def modusAendern(self, modus: str = "normal") -> None:
        pass


class SmartKamera(SmartGeraet, ISmartKamera):
    def __init__(self, geraetId: int = None, name: str = "",
                 status: GeraeteStatus = GeraeteStatus.NICHT_INSTALLIERT,
                 raumId: int = None, configuration: dict = None):
        super().__init__(geraetId, name, GeraeteTyp.KAMERA, status, raumId, configuration)

    def modusAendern(self, modus: str = "normal") -> None:
        self.configuration["modus"] = modus

    def kalibrieren(self) -> None:
        self.configuration["kalibriert"] = True
