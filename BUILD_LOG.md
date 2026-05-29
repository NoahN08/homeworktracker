# BUILD_LOG.md

## Task 1 — Scaffold repo + CLAUDE.md

- Brief: Create GitHub repo, Flask app skeleton, requirements.txt (Flask + pytest), CLAUDE.md with stack, run commands, and conventions
- What Claude proposed: Full CLAUDE.md with project description, Flask/Jinja2/pytest stack rationale, assignment dict shape, conventions (create_app factory, type hints, small functions), and hard limits (no modifying tests, no new deps)
- What I changed before approving: Updated "What this project is" paragraph to include personal context — missing deadlines during senior year, replacing an unstructured notes app
- Verification: `py -m pytest --collect-only` collects 0 items with no failures (exit 5 = expected "nothing found"); `py -c "from app import create_app; print(create_app().assignments)"` runs without error
- One thing I learned: CLAUDE.md isn't just documentation — it's the rules file that shapes every future Claude response in the repo

---

## Task 2 — Define assignment dict shape

- Brief: Document the assignment shape and seed two example assignments in `create_app()`
- What Claude proposed: `{"title": "...", "class_name": "...", "due_date": "YYYY-MM-DD", "done": False}` stored in `app.assignments` list on the app object inside `create_app()`
- What I changed before approving: Used future dates (2026-05-30 and 2026-06-05) so the sort test in Task 4 is meaningful with real data
- Verification: `py -c "from app import create_app; print(create_app().assignments)"` prints two dicts with correct keys
- One thing I learned: ISO 8601 date strings (YYYY-MM-DD) sort correctly with plain string comparison — no `datetime` parsing needed for ordering

---

## Task 3 — Home route + bare template

- Brief: GET / renders home.html listing all assignments by title and due date, no sorting yet
- What Claude proposed: `home()` route using `render_template`, Jinja2 template with `{% for %}` loop over all assignments
- What I changed before approving: Kept the template minimal — just title, class, and due date per item; saved styling for Task 5
- Verification: Browser at localhost:5000 shows both seeded assignments with title, class, and due date visible
- One thing I learned: Flask's `render_template` automatically looks in the `templates/` folder — no path configuration needed

---

## Task 4 — Sort by due date

- Brief: In the home view, sort upcoming assignments by due_date before passing to the template
- What Claude proposed: `sorted([a for a in app.assignments if not a["done"]], key=lambda a: a["due_date"])`
- What I changed before approving: No changes — the ISO sort is correct as-is; separation of upcoming vs done lists also prepares for Task 9
- Verification: Essay Draft (due 2026-05-30) appears before Math Homework (due 2026-06-05) in the upcoming list
- One thing I learned: Lexicographic string comparison works for ISO dates because the format is big-endian (year → month → day), so earlier dates always sort lower

---

## Task 5 — Highlight overdue

- Brief: Pass `today = date.today().isoformat()` to template; add CSS class `overdue` to any assignment where `due_date < today` and not done
- What Claude proposed: `{% if assignment.due_date < today %} overdue{% endif %}` in the `<li>` class; red background + border in CSS; an OVERDUE badge span for extra visibility
- What I changed before approving: Added `.assignment.overdue .meta` color override so the class/date line also turns red, not just the row background
- Verification: An assignment with `due_date="2020-01-01"` (add via form or seed temporarily) renders with red background and OVERDUE badge
- One thing I learned: String comparison in Jinja2 works the same as in Python — `assignment.due_date < today` is a valid expression in the template without any filter

---

## Task 6 — Add assignment form

- Brief: GET /add renders a form with title, class name, and due date fields; POST /add appends a new assignment dict and redirects to /
- What Claude proposed: Single `/add` route handling GET and POST, `add.html` template preserving form values on error, validation rejecting blank fields
- What I changed before approving: Added `date.fromisoformat()` validation on POST so a hand-typed malformed date (e.g. "06/05/2026") is caught server-side even though `<input type="date">` enforces it in browsers
- Verification: Submitting the form with valid values creates a new entry visible on the home page after redirect; submitting with blank title re-renders with "Title is required" and the class field still populated
- One thing I learned: `redirect(url_for("home"))` after a successful POST implements the Post/Redirect/Get pattern — prevents the browser from re-submitting the form on refresh
