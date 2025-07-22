from domain.entities import BaseEntity


class SubmissionEntity(BaseEntity):
    account_id: str
    disease_id: str
    image_url: str
    confidence: float

    def __init__(self, account_id: str, disease_id: str, image_url: str, confidence: float):
        super().__init__()
        self.account_id = account_id
        self.disease_id = disease_id
        self.image_url = image_url
        self.confidence = confidence
