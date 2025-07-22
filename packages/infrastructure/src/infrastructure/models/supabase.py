class UserSupabaseMetadata:
    avatar_url: str
    email: str
    full_name: str
    name: str
    picture: str

    def __init__(
            self,
            avatar_url: str = "",
            email: str = "",
            full_name: str = "",
            name: str = "",
            picture: str = "",
    ):
        self.avatar_url = avatar_url
        self.email = email
        self.full_name = full_name
        self.name = name
        self.picture = picture

    @staticmethod
    def from_json(json: dict) -> "UserSupabaseMetadata":
        return UserSupabaseMetadata(
            avatar_url=json.get("avatar_url", ""),
            email=json.get("email", ""),
            full_name=json.get("full_name", ""),
            name=json.get("name", ""),
            picture=json.get("picture", "")
        )

    def __str__(self):
        return f"UserSupabaseMetadata(avatar_url={self.avatar_url}, email={self.email}, full_name={self.full_name}, name={self.name}, picture={self.picture})"
