# Notion Archive

Transform your Notion exports into intelligent, searchable knowledge bases using AI embeddings.

## What is Notion Archive?

Notion Archive is a Python library that takes your exported Notion workspace and creates a powerful semantic search engine. Instead of keyword matching, it uses AI embeddings to understand the meaning of your content, enabling natural language search across all your documents.

## Key Features

- **🧠 AI-Powered Search**: Uses OpenAI or local models for semantic understanding
- **📚 Multiple Workspaces**: Support for multiple Notion exports in one archive
- **🏷️ Rich Metadata**: Preserves tags, breadcrumbs, timestamps, and workspace organization
- **⚡ Fast Performance**: Vector database for instant search after one-time indexing
- **🔧 Developer-Friendly**: Clean Python API for easy integration
- **🌐 Model Flexibility**: Support for OpenAI models and local Sentence Transformers

## Installation

```bash
pip install notion-archive
```

For OpenAI embeddings (recommended):
```bash
pip install notion-archive[openai]
```

## Quick Start

```python
from notion_archive import NotionArchive

# Initialize with your preferred embedding model
archive = NotionArchive(embedding_model="text-embedding-3-large")

# Add your Notion export(s)
archive.add_export('./my_notion_export')

# Build the search index (one-time setup)
archive.build_index()

# Search your knowledge base
results = archive.search("AI strategy meetings")

for result in results:
    print(f"Title: {result['title']}")
    print(f"Score: {result['score']:.3f}")
    print(f"Content: {result['content'][:200]}...")
    print(f"Workspace: {result['workspace']}")
    print("---")
```

## Usage Examples

### Basic Search
```python
# Simple text search
results = archive.search("project planning")

# Search with filters
results = archive.search(
    "quarterly review", 
    workspace="Engineering",
    limit=5
)

# Search with tag filters
results = archive.search(
    "customer feedback",
    tags=["support", "product"]
)
```

### Multiple Exports
```python
# Add multiple Notion exports
archive = NotionArchive()
archive.add_export('./engineering_export')
archive.add_export('./marketing_export')
archive.add_export('./hr_export')
archive.build_index()

# Search across all workspaces
results = archive.search("hiring process")
```

### Different Embedding Models
```python
# OpenAI models (best quality)
archive = NotionArchive(embedding_model="text-embedding-3-large")  # Premium
archive = NotionArchive(embedding_model="text-embedding-3-small")  # Faster

# Local models (free, runs offline)
archive = NotionArchive(embedding_model="all-MiniLM-L6-v2")
archive = NotionArchive(embedding_model="all-mpnet-base-v2")
```

### Configuration
```python
archive = NotionArchive(
    embedding_model="text-embedding-3-large",
    openai_api_key="sk-...",  # or set OPENAI_API_KEY env var
    db_path="./my_archive_db",
    chunk_size=1500,  # Larger chunks for longer context
    chunk_overlap=300
)
```

## How It Works

1. **Export**: Export your Notion workspace as HTML
2. **Parse**: Extract content, metadata, and structure from HTML files
3. **Embed**: Generate AI embeddings for semantic understanding
4. **Index**: Store embeddings in a vector database for fast search
5. **Search**: Query using natural language, get relevant results

## Supported Embedding Models

### OpenAI Models (Recommended)
- `text-embedding-3-large` (3072 dimensions) - Best quality
- `text-embedding-3-small` (1536 dimensions) - Faster, cheaper
- `text-embedding-ada-002` (1536 dimensions) - Legacy model

### Local Models (Free)
- `all-MiniLM-L6-v2` - Good balance of speed and quality
- `all-mpnet-base-v2` - Higher quality, slower
- Any model from [Sentence Transformers](https://www.sbert.net/docs/pretrained_models.html)

## API Reference

### NotionArchive Class

```python
archive = NotionArchive(
    embedding_model="text-embedding-3-large",
    openai_api_key=None,
    db_path="./notion_archive_db",
    collection_name="documents",
    chunk_size=1000,
    chunk_overlap=200
)
```

### Methods

#### `add_export(export_path: str)`
Add a Notion export to the archive.

#### `build_index(show_progress: bool = True)`
Generate embeddings and build the search index.

#### `search(query: str, limit: int = 10, workspace: str = None, tags: List[str] = None, **filters)`
Search the archive using natural language.

#### `get_stats()`
Get statistics about the indexed archive.

#### `clear_index()`
Clear the search index.

## Integration Examples

### Web Application
```python
from flask import Flask, request, jsonify
from notion_archive import NotionArchive

app = Flask(__name__)
archive = NotionArchive()
archive.add_export('./company_wiki')
archive.build_index()

@app.route('/search')
def search():
    query = request.args.get('q')
    results = archive.search(query, limit=10)
    return jsonify(results)
```

### CLI Tool
```python
import sys
from notion_archive import NotionArchive

def main():
    if len(sys.argv) < 3:
        print("Usage: search.py <export_path> <query>")
        return
    
    export_path = sys.argv[1]
    query = " ".join(sys.argv[2:])
    
    archive = NotionArchive()
    archive.add_export(export_path)
    archive.build_index()
    
    results = archive.search(query)
    for result in results:
        print(f"{result['title']} ({result['score']:.3f})")

if __name__ == "__main__":
    main()
```

### Slack Bot
```python
from slack_bolt import App
from notion_archive import NotionArchive

app = App(token="xoxb-...")
archive = NotionArchive()
archive.add_export('./company_docs')
archive.build_index()

@app.message("search")
def handle_search(message, say):
    query = message['text'].replace('search', '').strip()
    results = archive.search(query, limit=3)
    
    response = "Here's what I found:\n"
    for result in results:
        response += f"• {result['title']} ({result['score']:.2f})\n"
    
    say(response)
```

## Requirements

- Python 3.8+
- Notion export in HTML format
- OpenAI API key (for OpenAI models)

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- 📖 [Documentation](https://github.com/otron-io/notion-archive)
- 🐛 [Issue Tracker](https://github.com/otron-io/notion-archive/issues)
- 💬 [Discussions](https://github.com/otron-io/notion-archive/discussions)

---

Transform your Notion exports into intelligent search engines with just a few lines of Python! 🚀