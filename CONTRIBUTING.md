# Contributing to Notion Archive

We welcome contributions to Notion Archive! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/notion-archive.git`
3. Create a virtual environment: `python -m venv .venv`
4. Activate it: `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)
5. Install dependencies: `pip install -r requirements.txt`
6. Install in development mode: `pip install -e .`

## Development Setup

### Running Tests
```bash
# Run basic functionality test
python test_archive.py

# Run example usage
python example_usage.py
```

### Code Style
We use Black for code formatting and flake8 for linting:
```bash
black notion_archive/
flake8 notion_archive/
```

### Type Checking
We use mypy for type checking:
```bash
mypy notion_archive/
```

## Project Structure

```
notion-archive/
├── notion_archive/           # Main package
│   ├── __init__.py          # Package exports
│   ├── core/                # Core functionality
│   │   ├── archive.py       # Main NotionArchive class
│   │   ├── parser.py        # Notion HTML parser
│   │   └── embeddings.py    # AI embedding models
│   ├── config/              # Configuration
│   └── utils/               # Utilities
├── tests/                   # Test files (future)
├── examples/                # Example scripts
├── docs/                    # Documentation (future)
├── setup.py                 # Package setup
├── requirements.txt         # Dependencies
└── README.md               # Main documentation
```

## Contributing Guidelines

### Issues
- Search existing issues before creating new ones
- Use clear, descriptive titles
- Include steps to reproduce for bugs
- Include use case for feature requests

### Pull Requests
1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Add tests if applicable
4. Ensure code style compliance
5. Update documentation if needed
6. Commit with clear messages
7. Push and create a pull request

### Commit Messages
Use clear, descriptive commit messages:
- `feat: add support for new embedding model`
- `fix: handle empty documents in parser`
- `docs: update API reference`
- `test: add tests for search filtering`

## Types of Contributions

### Bug Fixes
- Fix issues with parsing specific Notion exports
- Improve error handling
- Performance optimizations

### Features
- Support for new embedding models
- Additional search filters
- Export format improvements
- Performance enhancements

### Documentation
- API documentation improvements
- Usage examples
- Integration guides
- Tutorial content

### Testing
- Unit tests for core functionality
- Integration tests
- Performance benchmarks

## Development Guidelines

### Code Quality
- Write clear, readable code
- Add docstrings to public functions
- Use type hints where appropriate
- Follow Python naming conventions

### Testing
- Test with different Notion export formats
- Include edge cases
- Test with both local and OpenAI models
- Verify cross-platform compatibility

### Performance
- Consider memory usage for large exports
- Optimize embedding generation
- Efficient vector database operations

## Getting Help

- Check existing issues and documentation
- Ask questions in GitHub Discussions
- Join our community channels (links in README)

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes for significant contributions
- GitHub contributor graphs

Thank you for contributing to Notion Archive! 🚀