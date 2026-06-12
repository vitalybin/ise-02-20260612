from domain.repositories import IBackupRepository
from domain.backup_auftrag import BackupAuftrag
from infrastructure.database_connection import DatabaseConnection


class SqlBackupRepository(IBackupRepository):
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def saveJob(self, job):
        conn = self.db.get_connection()
        with conn.cursor() as cur:
            if job.id:
                cur.execute(
                    "UPDATE backup_jobs SET job_type=%s, file_path=%s, "
                    "created_by=%s, status=%s WHERE id=%s",
                    (job.jobType, job.filePath, job.createdBy, job.status, job.id),
                )
            else:
                cur.execute(
                    "INSERT INTO backup_jobs (job_type, file_path, created_by, status) "
                    "VALUES (%s, %s, %s, %s) RETURNING id",
                    (job.jobType, job.filePath, job.createdBy, job.status),
                )
                job.id = cur.fetchone()[0]

    def findJobs(self):
        conn = self.db.get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, job_type, file_path, created_by, status "
                "FROM backup_jobs ORDER BY id DESC"
            )
            rows = cur.fetchall()
        return [
            BackupAuftrag(id=r[0], jobType=r[1], filePath=r[2],
                          createdBy=r[3], status=r[4])
            for r in rows
        ]
