from domain.repositories import IGeraetRepository
from domain.enums import Berechtigung, GeraeteStatus
from application.berechtigungs_service import BerechtigungsService


class GeraetAnzeigenService:
    def __init__(self, geraet_repo: IGeraetRepository,
                 berechtigungs_service: BerechtigungsService):
        self.geraet_repo = geraet_repo
        self.berechtigungs_service = berechtigungs_service

    def execute(self, user, status_filter=None, geraetId=None):
        self.berechtigungs_service.pruefeBerechtigung(user, Berechtigung.GERAET_LESEN)
        if geraetId:
            return self.geraet_repo.findById(geraetId)
        if status_filter:
            return self.geraet_repo.findByStatus(GeraeteStatus(status_filter))
        return self.geraet_repo.findAll()
