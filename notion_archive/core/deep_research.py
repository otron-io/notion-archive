from __future__ import annotations

"""Minimal integration with the OpenAI Deep Research API.

This helper is intentionally *very* light-weight.  It lets callers turn a
natural-language query into a structured research report that combines the
power of the OpenAI Deep-Research models **and** the user's private Notion
knowledge base that is already indexed by :class:`~notion_archive.core.archive.NotionArchive`.

Usage::

    from notion_archive.core.archive import NotionArchive

    archive = NotionArchive()
    archive.add_export("/path/to/export")
    archive.build_index()

    # Generate a research report that cites your private docs when relevant.
    report = archive.deep_research("What are the main OKR themes we had last year?")
    print(report)

The helper follows the pattern laid out in the OpenAI cookbook
https://cookbook.openai.com/examples/deep_research_api/introduction_to_deep_research_api
but strips it down to the bare minimum: it only calls the Deep-Research
endpoint with `web_search_preview` enabled and supplies the *k* most relevant
private documents up front so the model can ground its answer.
"""

from typing import List, Optional
import os

# We purposefully import lazily so that users without the SDK installed still
# have functioning core search capabilities.
try:
    from openai import OpenAI  # type: ignore
except ImportError:  # pragma: no cover – optional dependency
    OpenAI = None  # type: ignore

from .archive import NotionArchive


DEFAULT_MODEL = "o4-mini-deep-research-2025-06-26"  # lightweight generally available deep research model


def _format_documents(results: List[dict]) -> str:
    """Turn search results into a markdown block that the model can read.

    We keep this extremely simple: each document gets a heading with its title
    (or the first 32 characters of the content as a fallback) followed by the
    raw text content.  We *do not* send metadata that would leak private
    information beyond what is strictly necessary.
    """
    blocks: List[str] = []
    for idx, res in enumerate(results, 1):
        title = res.get("title") or res["content"][:32].replace("\n", " ")
        blocks.append(f"### Doc {idx}: {title}\n{res['content']}\n")
    return "\n".join(blocks)


def deep_research(
    *,
    archive: NotionArchive,
    query: str,
    top_k: int = 10,
    model: Optional[str] = None,
    openai_api_key: Optional[str] = None,
) -> str:
    """Run a Deep-Research query that is grounded in the given *archive*.

    Parameters
    ----------
    archive
        A :class:`~notion_archive.core.archive.NotionArchive` with an index
        already built.
    query
        The natural language question.
    top_k
        How many internal documents to surface to the model.
    model
        Name of the Deep-Research model.  Defaults to
        ``"o4-mini-deep-research-2025-06-26"`` which is the fastest model
        that, at the time of writing, everyone with Deep Research access can
        use.  Feel free to override.
    openai_api_key
        Explicit OpenAI API key.  If omitted we fall back to the
        ``OPENAI_API_KEY`` environment variable.

    Returns
    -------
    str
        The model's final report as plain markdown.
    """

    if OpenAI is None:  # pragma: no cover
        raise ImportError(
            "The `openai` package is required for deep research.  Install it "
            "via `pip install openai>=1.0.0`."
        )

    # ---------------------------------------------------------------------
    # 1. Pull the most relevant Notion chunks so that the model can cite them.
    # ---------------------------------------------------------------------
    internal_results = archive.search(query, limit=top_k)
    internal_context = (
        _format_documents(internal_results)
        if internal_results
        else "No relevant Notion documents found."
    )

    # ---------------------------------------------------------------------
    # 2. Prepare the Deep-Research call.
    # ---------------------------------------------------------------------
    model = model or DEFAULT_MODEL
    api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY.")

    client = OpenAI(api_key=api_key)

    system_msg = (
        "You are a professional researcher. Use the *internal Notion "
        "documents* supplied by the developer message when relevant. Cite "
        "them by the heading given (e.g. 'Doc 3'). If you also need public "
        "information, you may call the web_search_preview tool."
    )

    input_payload = [
        {
            "role": "developer",
            "content": [
                {"type": "input_text", "text": system_msg},
                {
                    "type": "input_text",
                    "text": f"INTERNAL NOTION DOCUMENTS:\n{internal_context}",
                },
            ],
        },
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": query},
            ],
        },
    ]

    # ------------------------------------------------------------------
    # 3. Hit the Deep-Research endpoint.
    # ------------------------------------------------------------------
    response = client.responses.create(
        model=model,
        input=input_payload,
        reasoning={"summary": "auto"},
        tools=[{"type": "web_search_preview"}],
    )

    # The final report is always the *last* item in `.output`.
    try:
        final_report: str = response.output[-1].content[0].text  # type: ignore[attr-defined]
    except Exception as exc:  # pragma: no cover – defensive
        raise RuntimeError(f"Unexpected Deep Research response format: {exc}")

    return final_report