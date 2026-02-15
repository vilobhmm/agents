# Contributing to OpenClaw

Thank you for your interest in contributing to OpenClaw!

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Submit a pull request

## Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/openclaw.git
cd openclaw

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Code Style

We use:
- `black` for code formatting
- `flake8` for linting
- `mypy` for type checking

Run before committing:
```bash
black openclaw/ projects/
flake8 openclaw/ projects/
mypy openclaw/
```

## Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=openclaw tests/

# Run specific test
pytest tests/test_agent.py
```

## Adding a New Project

1. Create project directory: `projects/XX_project_name/`
2. Add required files:
   - `agent.py` - Main agent implementation
   - `main.py` - Entry point
   - `README.md` - Project documentation
   - `config.py` - Configuration (if needed)

3. Update `PROJECTS.md` with project description

4. Add tests in `tests/projects/test_XX_project_name.py`

## Adding a New Integration

1. Create integration file: `openclaw/integrations/service_name.py`
2. Implement integration class
3. Add to `openclaw/integrations/__init__.py`
4. Update `.env.example` with required credentials
5. Add documentation
6. Add tests

## Pull Request Process

1. Update documentation for any new features
2. Add tests for new functionality
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers

## Reporting Issues

When reporting issues, include:
- OS and Python version
- OpenClaw version
- Steps to reproduce
- Expected vs actual behavior
- Error messages and logs

## Feature Requests

We welcome feature requests! Please:
- Check existing issues first
- Describe the use case
- Explain why it would be valuable
- Provide examples if possible

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions.

## Questions?

Open an issue with the "question" label or join our community discussions.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
