from supabase import create_client, Client
from fastapi.encoders import jsonable_encoder

from core.configuration import Configuration
from adapters.shared.models import UserSupabaseMetadata


class Supabase:
    def __init__(self, config: Configuration):
        url: str = config.SUPABASE_URL
        key: str = config.SUPABASE_KEY
        self.client: Client = create_client(url, key)

    def sign_in_google(self, id_token: str, raw_nonce: str) -> UserSupabaseMetadata:
        response = self.client.auth.sign_in_with_id_token(
            {
                "provider": "google",
                "token": id_token,
                "nonce": raw_nonce,
            }
        )

        uid = response.user.id  # type: ignore
        if not uid:
            raise Exception("Failed to retrieve user ID from Supabase response")

        user = UserSupabaseMetadata.from_json(uid, jsonable_encoder(response.user.user_metadata))  # type: ignore
        return user
