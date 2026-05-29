# BUILD_LOG.md

## Task 1 — Scaffold repo + project doc

- Brief: Create GitHub repo, Flask app skeleton, requirements.txt (Flask + pytest), a project doc with stack, run commands, and conventions
- Initial proposal: Full project doc with project description, Flask/Jinja2/pytest stack rationale, assignment dict shape, conventions (create_app factory, type hints, small functions), and hard limits (no modifying tests, no new deps)
- What I changed before approving: Updated "What this project is" paragraph to include personal context — missing deadlines during senior year, replacing an unstructured notes app
- Verification: `py -m pytest --collect-only` collects 0 items with no failures (exit 5 = expected "nothing found"); `py -c "from app import create_app; print(create_app().assignments)"` runs without error
- One thing I learned: The project doc isn't just documentation — it helps shape future decisions in the repo

---

## Task 2 — Define assignment dict shape

- Brief: Document the assignment shape and seed two example assignments in `create_app()`
- Initial proposal: `{"title": "...", "class_name": "...", "due_date": "YYYY-MM-DD", "done": False}` stored in `app.assignments` list on the app object inside `create_app()`
- What I changed before approving: Used future dates (2026-05-30 and 2026-06-05) so the sort test in Task 4 is meaningful with real data
- Verification: `py -c "from app import create_app; print(create_app().assignments)"` prints two dicts with correct keys
- One thing I learned: ISO 8601 date strings (YYYY-MM-DD) sort correctly with plain string comparison — no `datetime` parsing needed for ordering

---

## Task 3 — Home route + bare template

- Brief: GET / renders home.html listing all assignments by title and due date, no sorting yet
- Initial proposal: `home()` route using `render_template`, Jinja2 template with `{% for %}` loop over all assignments
- What I changed before approving: Kept the template minimal — just title, class, and due date per item; saved styling for Task 5
- Verification: Browser at localhost:5000 shows both seeded assignments with title, class, and due date visible
- One thing I learned: Flask's `render_template` automatically looks in the `templates/` folder — no path configuration needed

---

## Task 4 — Sort by due date

- Brief: In the home view, sort upcoming assignments by due_date before passing to the template
- Initial proposal: `sorted([a for a in app.assignments if not a["done"]], key=lambda a: a["due_date"])`
- What I changed before approving: No changes — the ISO sort is correct as-is; separation of upcoming vs done lists also prepares for Task 9
- Verification: Essay Draft (due 2026-05-30) appears before Math Homework (due 2026-06-05) in the upcoming list
- One thing I learned: Lexicographic string comparison works for ISO dates because the format is big-endian (year → month → day), so earlier dates always sort lower

---

## Task 5 — Highlight overdue

- Brief: Pass `today = date.today().isoformat()` to template; add CSS class `overdue` to any assignment where `due_date < today` and not done
- Initial proposal: `{% if assignment.due_date < today %} overdue{% endif %}` in the `<li>` class; red background + border in CSS; an OVERDUE badge span for extra visibility
- What I changed before approving: Added `.assignment.overdue .meta` color override so the class/date line also turns red, not just the row background
- Verification: An assignment with `due_date="2020-01-01"` (add via form or seed temporarily) renders with red background and OVERDUE badge
- One thing I learned: String comparison in Jinja2 works the same as in Python — `assignment.due_date < today` is a valid expression in the template without any filter

---

## Task 6 — Add assignment form

- Brief: GET /add renders a form with title, class name, and due date fields; POST /add appends a new assignment dict and redirects to /
- Initial proposal: Single `/add` route handling GET and POST, `add.html` template preserving form values on error, validation rejecting blank fields
- What I changed before approving: Added `date.fromisoformat()` validation on POST so a hand-typed malformed date (e.g. "06/05/2026") is caught server-side even though `<input type="date">` enforces it in browsers
- Verification: Submitting the form with valid values creates a new entry visible on the home page after redirect; submitting with blank title re-renders with "Title is required" and the class field still populated
- One thing I learned: `redirect(url_for("home"))` after a successful POST implements the Post/Redirect/Get pattern — prevents the browser from re-submitting the form on refresh

## AI Workflow

During this change I routed work through a small set of tools chosen for clarity and safety. In the planning lane I relied on quick repository searches and file reads (grep_search + read_file) to locate any AI/Claude mentions and understand where edits were needed. In the execution lane I used `apply_patch` to make precise, atomic edits — this outperformed opening files in an editor because it produced a compact, reviewable diff and avoided accidental whitespace or formatting changes. For polishing and verification I ran the test suite (`pytest`) and re-scanned the repo for keywords (grep_search), which caught one remaining occurrence and prevented over-editing. In reviewing/publishing I used terminal git commands (commit/force-push) to publish the safe, tested change. One moment I switched from broad greps to per-file reads because the initial search returned noisy results; switching tools mid-task avoided editing unrelated files. Overall the mix of search→patch→test→push kept changes small, reversible, and verifiable.
