#!/usr/bin/env python3
"""
Example: Flask web API for Notion Archive
"""

from flask import Flask, request, jsonify
from notion_archive import NotionArchive
import os

app = Flask(__name__)

# Initialize archive (in production, do this once at startup)
archive = None

def init_archive():
    """Initialize the archive with your Notion export"""
    global archive
    
    # Use environment variables for configuration
    embedding_model = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    export_path = os.getenv("NOTION_EXPORT_PATH", "./notion_export")
    
    print(f"Initializing archive with model: {embedding_model}")
    
    archive = NotionArchive(
        embedding_model=embedding_model,
        openai_api_key=openai_api_key,
        db_path="./web_archive_db"
    )
    
    # Add your Notion export
    if os.path.exists(export_path):
        archive.add_export(export_path)
        archive.build_index()
        print("✅ Archive ready!")
    else:
        print(f"⚠️  Export path not found: {export_path}")
        print("   Set NOTION_EXPORT_PATH environment variable")

@app.route('/search', methods=['GET'])
def search():
    """Search endpoint"""
    if not archive:
        return jsonify({"error": "Archive not initialized"}), 500
    
    query = request.args.get('q', '')
    limit = int(request.args.get('limit', 10))
    workspace = request.args.get('workspace')
    
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400
    
    try:
        # Build filters
        filters = {}
        if workspace:
            filters['workspace'] = workspace
        
        results = archive.search(query, limit=limit, **filters)
        
        return jsonify({
            "query": query,
            "results": results,
            "count": len(results)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stats', methods=['GET'])
def stats():
    """Get archive statistics"""
    if not archive:
        return jsonify({"error": "Archive not initialized"}), 500
    
    try:
        stats = archive.get_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "archive_initialized": archive is not None
    })

@app.route('/', methods=['GET'])
def home():
    """API documentation"""
    return jsonify({
        "name": "Notion Archive API",
        "version": "1.0.0",
        "endpoints": {
            "GET /search": "Search the archive. Params: q (query), limit (default 10), workspace (optional)",
            "GET /stats": "Get archive statistics",
            "GET /health": "Health check"
        },
        "example": "/search?q=meeting notes&limit=5&workspace=Engineering"
    })

if __name__ == "__main__":
    # Initialize archive on startup
    init_archive()
    
    # Run the Flask app
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    print(f"🚀 Starting Notion Archive API on port {port}")
    app.run(host="0.0.0.0", port=port, debug=debug)