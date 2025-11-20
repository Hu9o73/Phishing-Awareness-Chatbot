import os

from supabase import Client, create_client
from supabase.client import ClientOptions


def get_db() -> Client:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(
        url,
        key,
        options=ClientOptions(
            postgrest_client_timeout=2, storage_client_timeout=2, schema="phishing_awareness_chatbot"
        ),
    )
    return supabase
