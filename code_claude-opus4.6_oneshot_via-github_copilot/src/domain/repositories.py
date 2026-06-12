from abc import ABC, abstractmethod


class IRaumRepository(ABC):
    @abstractmethod
    def findAll(self):
        pass

    @abstractmethod
    def findById(self, id):
        pass

    @abstractmethod
    def save(self, raum):
        pass


class IGeraetRepository(ABC):
    @abstractmethod
    def findAll(self):
        pass

    @abstractmethod
    def findByStatus(self, status):
        pass

    @abstractmethod
    def findById(self, id):
        pass

    @abstractmethod
    def findByRaumId(self, raumId):
        pass

    @abstractmethod
    def save(self, geraet):
        pass

    @abstractmethod
    def delete(self, id):
        pass


class IUserRepository(ABC):
    @abstractmethod
    def findAll(self):
        pass

    @abstractmethod
    def findByUsername(self, username):
        pass

    @abstractmethod
    def findById(self, id):
        pass

    @abstractmethod
    def save(self, user):
        pass


class IBackupRepository(ABC):
    @abstractmethod
    def saveJob(self, job):
        pass

    @abstractmethod
    def findJobs(self):
        pass


class IImportValidator(ABC):
    @abstractmethod
    def validate(self, importData):
        pass
