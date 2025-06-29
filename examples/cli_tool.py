#!/usr/bin/env python3
"""
Example: Command-line interface for Notion Archive
"""

import argparse
import os
import sys
from notion_archive import NotionArchive

def build_command(args):
    """Build search index from Notion export"""
    print(f"🔨 Building index from: {args.export_path}")
    
    archive = NotionArchive(
        embedding_model=args.model,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        db_path=args.db_path
    )
    
    try:
        archive.add_export(args.export_path)
        archive.build_index()
        
        stats = archive.get_stats()
        print(f"✅ Index built successfully!")
        print(f"   Documents: {stats['total_documents']}")
        print(f"   Chunks: {stats['total_chunks']}")
        print(f"   Workspaces: {len(stats['workspaces'])}")
        
    except Exception as e:
        print(f"❌ Error building index: {e}")
        sys.exit(1)

def search_command(args):
    """Search the archive"""
    print(f"🔍 Searching for: '{args.query}'")
    
    archive = NotionArchive(
        embedding_model=args.model,
        db_path=args.db_path
    )
    
    try:
        # Build filters
        filters = {}
        if args.workspace:
            filters['workspace'] = args.workspace
        if args.tags:
            filters['tags'] = args.tags.split(',')
        
        results = archive.search(args.query, limit=args.limit, **filters)
        
        if not results:
            print("No results found.")
            return
        
        print(f"\nFound {len(results)} results:\n")
        
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}")
            print(f"   Score: {result['score']:.3f}")
            print(f"   Workspace: {result['workspace']}")
            if result['tags']:
                print(f"   Tags: {', '.join(result['tags'])}")
            print(f"   Preview: {result['content'][:150]}...")
            print()
            
    except Exception as e:
        print(f"❌ Error searching: {e}")
        sys.exit(1)

def stats_command(args):
    """Show archive statistics"""
    print("📊 Archive Statistics")
    
    archive = NotionArchive(db_path=args.db_path)
    
    try:
        stats = archive.get_stats()
        
        print(f"\nDocuments: {stats['total_documents']}")
        print(f"Chunks: {stats['total_chunks']}")
        print(f"Model: {stats.get('embedding_model', 'Unknown')}")
        print(f"Dimension: {stats.get('embedding_dimension', 'Unknown')}")
        
        if stats['workspaces']:
            print(f"\nWorkspaces ({len(stats['workspaces'])}):")
            for workspace in stats['workspaces']:
                print(f"  • {workspace}")
        
        if stats['tags']:
            print(f"\nTags ({len(stats['tags'])}):")
            for tag in stats['tags'][:10]:  # Show first 10
                print(f"  • {tag}")
            if len(stats['tags']) > 10:
                print(f"  ... and {len(stats['tags']) - 10} more")
                
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Notion Archive CLI - Search your Notion exports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build index from export
  python cli_tool.py build ./my_notion_export

  # Search with local model
  python cli_tool.py search "meeting notes" --limit 5

  # Search with OpenAI model (set OPENAI_API_KEY)
  python cli_tool.py search "AI strategy" --model text-embedding-3-large

  # Search in specific workspace
  python cli_tool.py search "planning" --workspace Engineering

  # Show statistics
  python cli_tool.py stats
        """
    )
    
    parser.add_argument(
        '--db-path', 
        default='./cli_archive_db',
        help='Path to vector database (default: ./cli_archive_db)'
    )
    
    parser.add_argument(
        '--model',
        default='all-MiniLM-L6-v2',
        help='Embedding model to use (default: all-MiniLM-L6-v2)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Build command
    build_parser = subparsers.add_parser('build', help='Build search index from Notion export')
    build_parser.add_argument('export_path', help='Path to Notion export folder')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search the archive')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--limit', type=int, default=10, help='Number of results (default: 10)')
    search_parser.add_argument('--workspace', help='Filter by workspace')
    search_parser.add_argument('--tags', help='Filter by tags (comma-separated)')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show archive statistics')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'build':
        build_command(args)
    elif args.command == 'search':
        search_command(args)
    elif args.command == 'stats':
        stats_command(args)

if __name__ == "__main__":
    main()