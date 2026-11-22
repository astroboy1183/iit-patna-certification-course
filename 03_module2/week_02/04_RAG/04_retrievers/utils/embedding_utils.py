"""
embedding_utils.py
------------------
Utility functions for creating embeddings
using OpenAI or SentenceTransformers.
"""

import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import SentenceTransformerEmbeddings

import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)

load_dotenv()

def get_embedding_model(provider: str = "local"):
    """
    Returns embedding model based on provider.
    provider = "openai" or "local"
    """
    if provider == "openai":
        print("Loading OpenAI embedding model...")
        return OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    else:
        # Local lightweight model for CPU systems
        print("Loading local lightweight embedding model for CPU systems...")
        return SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
