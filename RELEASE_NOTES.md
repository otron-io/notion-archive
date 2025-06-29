# Notion Archive v0.1.0 - Initial Release

**Basic semantic search for Notion HTML exports.**

## What is Notion Archive?

A simple Python library that parses your exported Notion workspace and adds AI-powered search using embeddings. It's a basic tool for searching through Notion content using natural language instead of just keywords.

## What it includes

- HTML parser for Notion exports
- Support for OpenAI and local embedding models  
- ChromaDB vector storage
- Basic search functionality
- Simple Python API

## Installation

```bash
pip install notion-archive
```

## Basic usage

```python
from notion_archive import NotionArchive

# Initialize
archive = NotionArchive(embedding_model="text-embedding-3-large")

# Add your exported Notion folder
archive.add_export('./notion_export')

# Build search index (costs money with OpenAI)
archive.build_index()

# Search
results = archive.search("meeting notes")
```

## What's included

- Basic Notion HTML parser
- OpenAI and sentence-transformers embedding support
- ChromaDB for vector storage
- Simple search API
- Basic examples (web API, CLI)

## Limitations

- Only works with HTML exports
- No incremental updates  
- Basic metadata extraction
- Can be expensive with large workspaces + OpenAI

## Links

- Repository: https://github.com/otron-io/notion-archive
- Issues: https://github.com/otron-io/notion-archive/issues

---

A basic tool for adding semantic search to Notion exports.