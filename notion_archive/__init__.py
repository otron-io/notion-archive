"""
Notion Archive - Transform your Notion exports into searchable knowledge bases

A Python library that uses AI embeddings to enable semantic search through 
exported Notion workspaces. Simply export your Notion workspace and create 
a searchable archive that developers can integrate into any application.
"""

from .core.archive import NotionArchive
from .core.deep_research import deep_research as deep_research  # re-export helper for convenience

__version__ = "0.1.0"
__author__ = "Notion Archive Contributors"
__email__ = "hello@notion-archive.com"

__all__ = ["NotionArchive", "deep_research"]