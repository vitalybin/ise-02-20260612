from domain.repositories import IRaumRepository, IGeraetRepository
from domain.enums import Berechtigung
from application.berechtigungs_service import BerechtigungsService


class RaumAnzeigenService:
    def __init__(self, raum_repo: IRaumRepository, geraet_repo: IGeraetRepository,
                 berechtigungs_service: BerechtigungsService):
        self.raum_repo = raum_repo
        self.geraet_repo = geraet_repo
        self.berechtigungs_service = berechtigungs_service

    def execute(self, user, raumId=None):
        self.berechtigungs_service.execute(user, Berechtigung.RAUM_LESEN)
        if raumId:
            raum = self.raum_repo.findById(raumId)
            if raum:
                raum.installierteGeraete = self.geraet_repo.findByRaumId(raumId)
            return raum
        raeume = self.raum_repo.findAll()
        for raum in raeume:
            raum.installierteGeraete = self.geraet_repo.findByRaumId(raum.raumId)
        return raeume
