from domain.repositories import IRaumRepository
from domain.raum import Raum
from infrastructure.database_connection import DatabaseConnection


class SqlRaumRepository(IRaumRepository):
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def findAll(self):
        conn = self.db.get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, description FROM rooms ORDER BY id")
            rows = cur.fetchall()
        return [Raum(raumId=r[0], name=r[1], beschreibung=r[2] or "") for r in rows]

    def findById(self, id):
        conn = self.db.get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, description FROM rooms WHERE id = %s", (id,))
            r = cur.fetchone()
        if r:
            return Raum(raumId=r[0], name=r[1], beschreibung=r[2] or "")
        return None

    def save(self, raum):
        conn = self.db.get_connection()
        with conn.cursor() as cur:
            if raum.raumId:
                cur.execute(
                    "UPDATE rooms SET name = %s, description = %s WHERE id = %s",
                    (raum.name, raum.beschreibung, raum.raumId),
                )
            else:
                cur.execute(
                    "INSERT INTO rooms (name, description) VALUES (%s, %s) RETURNING id",
                    (raum.name, raum.beschreibung),
                )
                raum.raumId = cur.fetchone()[0]
