from dotenv import load_dotenv
from supabase import Client, ClientOptions, create_client
import os


def get_db():
    load_dotenv()
    return create_client(
        os.environ.get("SUPABASE_URL"),
        os.environ.get("SUPABASE_KEY"),
        options=ClientOptions(
            postgrest_client_timeout=2, storage_client_timeout=2, schema="phishing_awareness_chatbot"
        ),
    )
