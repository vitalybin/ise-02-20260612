from typing import List


class Raum:
    def __init__(self, raumId: int = None, name: str = "", beschreibung: str = "",
                 installierteGeraete: List = None):
        self.raumId: int = raumId
        self.name: str = name
        self.beschreibung: str = beschreibung
        self.installierteGeraete: List = installierteGeraete or []

    def geraetHinzufuegen(self, geraet) -> None:
        if geraet not in self.installierteGeraete:
            self.installierteGeraete.append(geraet)

    def geraetEntfernen(self, geraet) -> None:
        if geraet in self.installierteGeraete:
            self.installierteGeraete.remove(geraet)
