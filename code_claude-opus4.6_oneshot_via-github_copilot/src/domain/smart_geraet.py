from abc import ABC, abstractmethod
from domain.enums import GeraeteTyp, GeraeteStatus


class ISmartGeraet(ABC):
    """<<interface>> ISmartGeraet"""

    @abstractmethod
    def einschalten(self) -> None:
        pass

    @abstractmethod
    def ausschalten(self) -> None:
        pass

    @abstractmethod
    def konfigurieren(self, **kwargs) -> None:
        pass

    @abstractmethod
    def kalibrieren(self) -> None:
        pass

    @abstractmethod
    def installieren(self, raum) -> None:
        pass

    @abstractmethod
    def istSteuerbar(self) -> bool:
        pass


class SmartGeraet(ISmartGeraet):
    """<<abstract>> Basisklasse fuer alle Smart-Geraete
    Nicht direkt instanziierbar – nur ueber konkrete Subklassen (SmartLampe, SmartHeizung, etc.).
    """

    def __init__(self, geraetId: int = None, name: str = "",
                 typ: GeraeteTyp = None,
                 status: GeraeteStatus = GeraeteStatus.NICHT_INSTALLIERT,
                 raumId: int = None, configuration: dict = None):
        self.geraetId: int = geraetId
        self.name: str = name
        self.typ: GeraeteTyp = typ
        self.status: GeraeteStatus = status
        self.raumId: int = raumId
        self.configuration: dict = configuration or {}

    def installieren(self, raum) -> None:
        self.raumId = raum.raumId
        self.status = GeraeteStatus.INSTALLIERT
        raum.geraetHinzufuegen(self)

    def istSteuerbar(self) -> bool:
        return self.status == GeraeteStatus.INSTALLIERT

    def einschalten(self) -> None:
        self.configuration["eingeschaltet"] = True

    def ausschalten(self) -> None:
        self.configuration["eingeschaltet"] = False

    def konfigurieren(self, **kwargs) -> None:
        self.configuration.update(kwargs)

    # kalibrieren() bleibt abstrakt – SmartGeraet ist nicht direkt instanziierbar
