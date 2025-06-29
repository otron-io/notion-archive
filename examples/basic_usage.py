#!/usr/bin/env python3
"""
Basic usage example for Notion Archive
"""

from notion_archive import NotionArchive

def main():
    print("🚀 Notion Archive - Basic Usage Example")
    
    # Example 1: Using local embedding model (free)
    print("\n📊 Example 1: Local embedding model")
    archive = NotionArchive(
        embedding_model="all-MiniLM-L6-v2",  # Free, runs offline
        db_path="./my_archive_db"
    )
    
    # Add your Notion export
    # archive.add_export('./path/to/your/notion/export')
    
    # Build the search index (one-time setup)
    # archive.build_index()
    
    # Search your knowledge base
    # results = archive.search("project planning", limit=5)
    
    print("✅ Archive initialized with local model")
    print("   Next: Add your Notion export and build index")
    
    # Example 2: Using OpenAI embedding model (premium)
    print("\n📊 Example 2: OpenAI embedding model")
    try:
        archive_openai = NotionArchive(
            embedding_model="text-embedding-3-large",  # Best quality
            openai_api_key="your-api-key-here",  # Or set OPENAI_API_KEY env var
            db_path="./my_openai_archive_db"
        )
        print("✅ Archive initialized with OpenAI model")
    except Exception as e:
        print(f"⚠️  OpenAI model requires API key: {e}")
    
    # Example 3: Search with filters
    print("\n🔍 Example 3: Searching with filters")
    search_examples = [
        ("Find meeting notes", "meeting notes"),
        ("Search in Engineering workspace", "project updates", {"workspace": "Engineering"}),
        ("Find documents with specific tags", "planning", {"tags": ["product", "roadmap"]}),
    ]
    
    for description, query, *filters in search_examples:
        print(f"   {description}:")
        print(f"     archive.search('{query}'", end="")
        if filters:
            print(f", {filters[0]}", end="")
        print(")")
    
    print(f"\n💡 Quick Start:")
    print(f"   1. Export your Notion workspace as HTML")
    print(f"   2. archive.add_export('./path/to/export')")
    print(f"   3. archive.build_index()  # One-time setup")
    print(f"   4. results = archive.search('your query')")

if __name__ == "__main__":
    main()