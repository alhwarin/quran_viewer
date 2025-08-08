# domain/entities/sura_entity.py
class SuraEntity:
    def __init__(self, id: int, start: int, name: str, ename: str, ayas: int):
        self.id = id
        self.start = start
        self.name = name
        self.ename = ename
        self.ayas = ayas

    def __repr__(self):
        return f"SuraEntity(id={self.id}, name={self.name}, ayas={self.ayas})"