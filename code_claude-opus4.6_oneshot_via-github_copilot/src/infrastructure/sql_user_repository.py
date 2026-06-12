from domain.repositories import IUserRepository
from domain.user import User
from domain.enums import Rolle
from infrastructure.database_connection import DatabaseConnection


class SqlUserRepository(IUserRepository):
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def _row_to_user(self, row):
        return User(
            userId=row[0],
            username=row[1],
            passwordHash=row[2],
            anzeigename=row[3],
            rolle=Rolle(row[4]),
            active=row[5],
        )

    def findAll(self):
        conn = self.db.get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, username, password_hash, display_name, role, active "
                "FROM users ORDER BY id"
            )
            rows = cur.fetchall()
        return [self._row_to_user(r) for r in rows]

    def findByUsername(self, username):
        conn = self.db.get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, username, password_hash, display_name, role, active "
                "FROM users WHERE username = %s",
                (username,),
            )
            r = cur.fetchone()
        if r:
            return self._row_to_user(r)
        return None

    def findById(self, id):
        conn = self.db.get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, username, password_hash, display_name, role, active "
                "FROM users WHERE id = %s",
                (id,),
            )
            r = cur.fetchone()
        if r:
            return self._row_to_user(r)
        return None

    def save(self, user):
        conn = self.db.get_connection()
        with conn.cursor() as cur:
            if user.userId:
                cur.execute(
                    "UPDATE users SET username=%s, password_hash=%s, display_name=%s, "
                    "role=%s, active=%s WHERE id=%s",
                    (user.username, user.passwordHash, user.anzeigename,
                     user.rolle.value, user.active, user.userId),
                )
            else:
                cur.execute(
                    "INSERT INTO users (username, password_hash, display_name, role, active) "
                    "VALUES (%s, %s, %s, %s, %s) RETURNING id",
                    (user.username, user.passwordHash, user.anzeigename,
                     user.rolle.value, user.active),
                )
                user.userId = cur.fetchone()[0]
