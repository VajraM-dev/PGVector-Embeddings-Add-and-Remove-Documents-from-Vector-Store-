from langchain_core.documents import Document
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector
from config.llm import embedding_model
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(".env.dev"))


# See docker command above to launch a postgres instance with pgvector enabled.
connection = os.environ.get("PG_VECTOR_CONNECTION_URI") # Uses psycopg3!
collection_name = os.environ.get("PG_VECTOR_COLLECTION_NAME")


vector_store = PGVector(
    embeddings=embedding_model,
    collection_name=collection_name,
    connection=connection,
    use_jsonb=True,
)