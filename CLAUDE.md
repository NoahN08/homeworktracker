# homeworktracker — CLAUDE.md

## What this project is

A personal homework deadline tracker built as a small Flask web app. Noah (a high school senior) currently tracks deadlines in an unstructured notes app and has missed assignments because of it. This app solves that: add assignments with a title, class name, and due date; see them sorted by due date so the most urgent is always first; get overdue items visually highlighted in red; mark them complete so they sink to a separate "Completed" section; and delete them when they're no longer needed. There is no database — assignments live in memory using the same in-memory + Flask pattern learned in this course. The project is built incrementally across 15 guided steps, with AI features (Claude API) planned for later steps.

## Tech stack

**Flask** (Python) for the backend and routing; **Jinja2** templates (bundled with Flask) for server-side rendering — no separate frontend framework. **pytest** for all tests. **Anthropic Python SDK** for Claude API integration when AI features are added. Flask was chosen because the project follows a course curriculum that uses it, and because server-side rendering keeps the stack minimal and easy to reason about end-to-end without a build step.

## Run commands

```bash
python app.py          # start dev server
pytest                 # run full test suite
```

## Assignment dict shape

Every assignment is a plain Python dict:

```python
{"title": "...", "class_name": "...", "due_date": "YYYY-MM-DD", "done": False}
```

Due dates are ISO 8601 strings so lexicographic comparison (`<`, `>`) gives correct chronological order.

## Conventions

- Use the `create_app()` application factory pattern; keep `app.assignments` as an in-memory list on the app object.
- Use type hints on all function signatures.
- Keep functions small and single-purpose; prefer extracting date/sort/filter logic into standalone functions that can be unit-tested in `tests/test_logic.py`.
- Validate all user input at the POST handler boundary; re-render the form (not a redirect) on validation failure, preserving already-typed values.
- Templates live in `templates/`; static assets in `static/`. No inline styles — use a CSS class.
- Use `date.today().isoformat()` (not `datetime.now()`) for today's date comparisons.
- No global state outside of what Flask's `create_app()` explicitly initializes.
- No new `pip` packages without asking first.

## Things Claude must not do

- **Do not modify tests to make them pass.** Fix the implementation instead.
- **Do not add new dependencies** (pip packages, JS libraries, etc.) without explicit approval.
- **Do not introduce a database or ORM** — assignments live in `app.assignments` (in-memory list) unless the user explicitly asks to add persistence.
- **Do not add authentication, login, or session handling** unless asked.
- **Do not generate or auto-run destructive commands** (dropping data, `git reset --hard`, etc.) without user confirmation.
- **Do not add comments that just restate what the code does** — only comment when the *why* is non-obvious.
