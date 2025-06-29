#!/usr/bin/env python3
"""
Test script for Notion Archive
"""

import os
from notion_archive import NotionArchive

def main():
    # Test with sample export if available
    export_path = None
    for item in os.listdir('.'):
        if item.startswith('Export-') and os.path.isdir(item):
            export_path = item
            break
    
    if not export_path:
        print("ℹ️  No Notion export found for testing.")
        print("To test with your own data:")
        print("1. Export your Notion workspace as HTML")
        print("2. Place the export folder in this directory")
        print("3. Run this test script again")
        print()
        print("Testing basic functionality without data...")
        
        # Test basic initialization
        print("✅ Testing package import...")
        archive = NotionArchive(
            embedding_model="all-MiniLM-L6-v2",
            db_path="./test_archive_db"
        )
        print("✅ NotionArchive initialized successfully")
        
        # Test stats on empty archive
        stats = archive.get_stats()
        print(f"✅ Stats retrieved: {stats['total_documents']} documents")
        
        print("\n🎉 Basic functionality test completed!")
        print("Package is ready to use with your Notion exports.")
        return
    
    print(f"🧪 Testing with export: {export_path}")
    
    # Test with local model first (no API key needed)
    print("Initializing Notion Archive with local model...")
    archive = NotionArchive(
        embedding_model="all-MiniLM-L6-v2",
        db_path="./test_archive_db"
    )
    
    # Add export
    print("Adding export...")
    archive.add_export(export_path)
    
    # Build index
    print("Building search index...")
    archive.build_index()
    
    # Get stats
    print("\nArchive Statistics:")
    stats = archive.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test searches
    test_queries = [
        "meeting",
        "project",
        "plan",
        "team",
        "notes"
    ]
    
    print("\nTesting searches:")
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        results = archive.search(query, limit=3)
        
        if results:
            for i, result in enumerate(results, 1):
                print(f"  {i}. {result['title']} (Score: {result['score']:.3f})")
                print(f"     Workspace: {result['workspace']}")
                print(f"     Content: {result['content'][:100]}...")
        else:
            print("  No results found")
    
    print("\n✅ Test completed successfully!")

if __name__ == "__main__":
    main()