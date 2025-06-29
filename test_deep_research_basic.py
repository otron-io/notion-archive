import types
import sys

# NOTE: pytest is provided as a dev dependency; type checkers may lack stubs.
import pytest  # type: ignore

# Patch the OpenAI client used inside deep_research to avoid real API calls.
class _DummyResponses:
    """Stub `responses` namespace with the signature used in deep_research."""

    def create(self, *_, **__):  # noqa: D401, ANN001
        # Mimic the minimal response object shape expected:
        dummy_text = types.SimpleNamespace(text="dummy research report")
        dummy_content = types.SimpleNamespace(content=[dummy_text])
        return types.SimpleNamespace(output=[dummy_content])


class _DummyOpenAI:  # noqa: D401
    def __init__(self, *_, **__):  # noqa: ANN001
        self.responses = _DummyResponses()


def test_deep_research_returns_report(monkeypatch):
    """Ensure `deep_research` returns the model's final report text."""

    # Inject dummy openai module before importing deep_research.
    dummy_openai_module = types.ModuleType("openai")
    dummy_openai_module.OpenAI = _DummyOpenAI  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "openai", dummy_openai_module)

    # Import after patching so deep_research picks up the dummy.
    from notion_archive.core import deep_research as dr

    # Dummy archive providing a minimal `search` implementation.
    class _DummyArchive:
        def search(self, *_args, **_kwargs):  # noqa: D401, ANN001
            return [
                {
                    "content": "Internal doc",
                    "title": "Sample",
                }
            ]

    report = dr.deep_research(archive=_DummyArchive(), query="test query", openai_api_key="sk-test")  # type: ignore[arg-type]
    assert report == "dummy research report"