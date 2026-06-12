class BackupAuftrag:
    def __init__(self, id: int = None, jobType: str = "",
                 filePath: str = "", createdBy: str = "",
                 status: str = "erfolgreich"):
        self.id: int = id
        self.jobType: str = jobType
        self.filePath: str = filePath
        self.createdBy: str = createdBy
        self.status: str = status
