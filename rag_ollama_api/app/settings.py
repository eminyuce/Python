from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache
import os # Although Pydantic handles env vars, os module is useful for general paths if needed

class Settings(BaseSettings):
    """
    Manages application settings, loading from environment variables or a .env file.
    """

    # --- Application Settings ---
    # `APP_NAME` will default to "RAG Chatbot" if not set in environment
    app_name: str = Field("RAG Chatbot", env="APP_NAME", description="Name of the application.")
    # `APP_ENV` indicates the current environment (e.g., 'development', 'qa', 'production')
    app_env: str = Field("development", env="APP_ENV", description="Current application environment.")
    # `DEBUG` mode for detailed logging and debugging features
    debug: bool = Field(False, env="DEBUG", description="Enable debug mode for verbose logging.")
    # Host and port for the FastAPI application
    host: str = Field("127.0.0.1", env="HOST", description="Host address for the FastAPI server.")
    port: int = Field(8000, env="PORT", description="Port for the FastAPI server.")

    # --- LLM / Ollama Settings ---
    # `OLLAMA_MODEL` specifies the LLM model to use (e.g., "llama3")
    ollama_model: str = Field("llama3", env="OLLAMA_MODEL", description="Name of the Ollama LLM model to use.")

    # --- Embedding Model Settings ---
    # `EMBEDDING_MODEL` for generating document embeddings
    embedding_model: str = Field("sentence-transformers/all-MiniLM-L6-v2",
                                  env="EMBEDDING_MODEL",
                                  description="Name of the embedding model.")
  
    # --- FAISS Index Settings ---
    # Directory where FAISS indexes are stored or loaded from
    faiss_index_dir: str = Field("faiss_index", env="FAISS_INDEX_DIR",
                                 description="Directory for storing/loading FAISS index files.")

    # --- Document Storage Settings ---
    # Directory where source documents are located
    docs_dir: str = Field("documents", env="DOCS_DIR",
                          description="Directory containing source documents for RAG.")

    # --- Pydantic Settings Configuration ---
    # `SettingsConfigDict` replaced `Config` in newer Pydantic versions
    model_config = SettingsConfigDict(
        env_file=".env",              # Look for a .env file
        env_file_encoding="utf-8",    # Specify encoding for the .env file
        extra="ignore"                # Ignore environment variables not defined in this class
    )

# --- Global Settings Instance ---
# Using `lru_cache` ensures that the settings object is created only once
# and reused across the application, improving performance.
@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached instance of the Settings object.
    This ensures settings are loaded only once.
    """
    return Settings()

# Instantiate settings for direct access if preferred, e.g., for logging setup
settings = get_settings()

if settings.debug:
    print(f"--- Application Settings ({settings.app_env.upper()} Mode) ---")
    print(f"App Name: {settings.app_name}")
    print(f"Debug Mode: {settings.debug}")
    print(f"Host: {settings.host}, Port: {settings.port}")
    print(f"Ollama Model: {settings.ollama_model}")
    print(f"Embedding Model: {settings.embedding_model}")
    print(f"FAISS Index Directory: {settings.faiss_index_dir}")
    print(f"Documents Directory: {settings.docs_dir}")
    print("----------------------------------------")