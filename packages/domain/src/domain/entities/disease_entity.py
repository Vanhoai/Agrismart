from domain.entities import BaseEntity


class DiseaseEntity(BaseEntity):
    name: str
    description: str

    def __init__(self, name: str, description: str):
        super().__init__()
        self.name = name
        self.description = description
