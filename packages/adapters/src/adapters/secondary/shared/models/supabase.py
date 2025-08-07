class UserSupabaseMetadata:
    uid: str
    avatar_url: str
    email: str
    full_name: str
    name: str
    picture: str
    provider_id: str

    def __init__(
        self,
        uid: str = "",
        avatar_url: str = "",
        email: str = "",
        full_name: str = "",
        name: str = "",
        picture: str = "",
        provider_id: str = "",
    ):
        self.uid = uid
        self.avatar_url = avatar_url
        self.email = email
        self.full_name = full_name
        self.name = name
        self.picture = picture
        self.provider_id = provider_id

    @staticmethod
    def from_json(uid: str, json: dict) -> "UserSupabaseMetadata":
        return UserSupabaseMetadata(
            uid=uid,
            avatar_url=json.get("avatar_url", ""),
            email=json.get("email", ""),
            full_name=json.get("full_name", ""),
            name=json.get("name", ""),
            picture=json.get("picture", ""),
            provider_id=json.get("provider_id", ""),
        )
