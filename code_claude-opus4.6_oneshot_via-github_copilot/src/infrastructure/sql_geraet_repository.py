import json
from domain.repositories import IGeraetRepository
from domain.enums import GeraeteTyp, GeraeteStatus
from domain.smart_geraet_factory import SmartGeraetFactory
from infrastructure.database_connection import DatabaseConnection


class SqlGeraetRepository(IGeraetRepository):
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def _row_to_geraet(self, row):
        typ = GeraeteTyp(row[2])
        geraet = SmartGeraetFactory.create(typ, row[1])
        geraet.geraetId = row[0]
        geraet.status = GeraeteStatus(row[3])
        geraet.raumId = row[4]
        config = row[5]
        if isinstance(config, str):
            config = json.loads(config)
        geraet.configuration = config or {}
        return geraet

    def findAll(self):
        conn = self.db.get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, device_type, status, room_id, configuration "
                "FROM devices ORDER BY id"
            )
            rows = cur.fetchall()
        return [self._row_to_geraet(r) for r in rows]

    def findByStatus(self, status):
        conn = self.db.get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, device_type, status, room_id, configuration "
                "FROM devices WHERE status = %s ORDER BY id",
                (status.value,),
            )
            rows = cur.fetchall()
        return [self._row_to_geraet(r) for r in rows]

    def findById(self, id):
        conn = self.db.get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, device_type, status, room_id, configuration "
                "FROM devices WHERE id = %s",
                (id,),
            )
            r = cur.fetchone()
        if r:
            return self._row_to_geraet(r)
        return None

    def findByRaumId(self, raumId):
        conn = self.db.get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, device_type, status, room_id, configuration "
                "FROM devices WHERE room_id = %s ORDER BY id",
                (raumId,),
            )
            rows = cur.fetchall()
        return [self._row_to_geraet(r) for r in rows]

    def save(self, geraet):
        conn = self.db.get_connection()
        config_json = json.dumps(geraet.configuration, ensure_ascii=False)
        with conn.cursor() as cur:
            if geraet.geraetId:
                cur.execute(
                    "UPDATE devices SET name=%s, device_type=%s, status=%s, "
                    "room_id=%s, configuration=%s WHERE id=%s",
                    (geraet.name, geraet.typ.value, geraet.status.value,
                     geraet.raumId, config_json, geraet.geraetId),
                )
            else:
                cur.execute(
                    "INSERT INTO devices (name, device_type, status, room_id, configuration) "
                    "VALUES (%s, %s, %s, %s, %s) RETURNING id",
                    (geraet.name, geraet.typ.value, geraet.status.value,
                     geraet.raumId, config_json),
                )
                geraet.geraetId = cur.fetchone()[0]

    def delete(self, id):
        conn = self.db.get_connection()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM devices WHERE id = %s", (id,))
