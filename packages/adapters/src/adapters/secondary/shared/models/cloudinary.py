from fastapi_camelcase import CamelModel


class CloudinaryAsset(CamelModel):
    asset_id: str
    public_id: str
    width: int
    height: int
    format: str
    resource_type: str
    created_at: str
    bytes: int
    type: str
    url: str
    secure_url: str
    asset_folder: str
    display_name: str

    @staticmethod
    def from_json(json: dict) -> "CloudinaryAsset":
        return CloudinaryAsset(
            asset_id=json.get("asset_id", ""),
            public_id=json.get("public_id", ""),
            width=json.get("width", 0),
            height=json.get("height", 0),
            format=json.get("format", ""),
            resource_type=json.get("resource_type", ""),
            created_at=json.get("created_at", ""),
            bytes=json.get("bytes", 0),
            type=json.get("type", ""),
            url=json.get("url", ""),
            secure_url=json.get("secure_url", ""),
            asset_folder=json.get("asset_folder", ""),
            display_name=json.get("display_name", "")
        )
