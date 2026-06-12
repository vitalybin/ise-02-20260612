from domain.enums import GeraeteStatus


class GeraeteRegelService:
    def darfInstalliertWerden(self, geraet) -> bool:
        if geraet.status == GeraeteStatus.BESTELLT:
            return False
        if geraet.status == GeraeteStatus.DEFEKT:
            return False
        if geraet.status == GeraeteStatus.INSTALLIERT:
            return False
        return True

    def darfGesteuertWerden(self, geraet) -> bool:
        if geraet.status != GeraeteStatus.INSTALLIERT:
            return False
        if geraet.status == GeraeteStatus.DEFEKT:
            return False
        return True

    def pruefeRaumZuordnung(self, geraet, raum) -> None:
        if geraet.raumId is not None and geraet.raumId != raum.raumId:
            raise ValueError(
                f"Geraet '{geraet.name}' ist bereits Raum {geraet.raumId} zugeordnet"
            )
