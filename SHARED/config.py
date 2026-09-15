from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    chroma_path: str = "./chroma_storage"
    embedding_model: str = "/home/rahim/.cache/modelscope/models/BAAI--bge-small-en-v1.5/snapshots/master"

settings = Settings()