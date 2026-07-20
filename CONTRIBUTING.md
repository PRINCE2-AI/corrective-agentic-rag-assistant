# Contributing

Thanks for considering a contribution.

## Development

```bash
python -m venv .venv
pip install -r requirements.txt
pytest -q
```

## Guidelines

- Keep the default test suite offline.
- Do not commit API keys, private documents, generated vector indexes, or `.env`.
- Prefer small, focused pull requests.
- Add tests for routing, retrieval scoring, refinement, or evaluation changes.
- Document any new external service in `.env.example` and the README.

