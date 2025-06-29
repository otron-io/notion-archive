"""Example: run a Deep Research query over your Notion export.

Before running install deps and export `OPENAI_API_KEY`::

    pip install -r requirements.txt
    export OPENAI_API_KEY=sk-...

Then run::

    python examples/deep_research.py \
        --export-path /path/to/Your\ Notion\ Export \
        --query "What were the key take-aways from our Q1 strategy meetings?"
"""

import argparse
from pathlib import Path

from notion_archive import NotionArchive


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Deep Research over a Notion export.")
    parser.add_argument("--export-path", required=True, help="Path to the Notion HTML export folder")
    parser.add_argument("--query", required=True, help="Natural language question to ask")
    parser.add_argument("--top-k", type=int, default=10, help="How many internal docs to surface to the model")
    args = parser.parse_args()

    export_path = Path(args.export_path).expanduser().resolve()
    if not export_path.exists():
        parser.error(f"Export path does not exist: {export_path}")

    archive = NotionArchive()
    archive.add_export(str(export_path))
    archive.build_index()

    report = archive.deep_research(args.query, top_k=args.top_k)
    print("\n================= RESEARCH REPORT =================\n")
    print(report)


if __name__ == "__main__":
    main()