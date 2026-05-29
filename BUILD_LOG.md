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

## Reflection

Using tools helps me work much faster. I can find things quickly with tools like searching through files and reading parts of files. This way I can locate everything I need in seconds.

* I can make changes with tools like apply_patch.

* This helps me make changes without messing up parts of the code.

* I can see how my changes affect the code and save them in a commit.

I run tests frequently to get feedback away.

For example I make a change to a document run the tests and immediately see if I broke anything.

These quick steps. Search, make a change, test. Help me finish tasks fast.

I can find things make changes and verify them in one session.

Without these tools I could still do the work. It would take longer and I wouldn't be as confident.

Sometimes I have to make decisions about automated wording.

If its not clear I do it manually.

For example there's a file and some references that need a careful look.

I don't want to remove information so I read the files and make changes that keep the meaning but remove AI-related phrases.

I also don't touch tests. Add new dependencies.

Those are areas where a tool might suggest changes. I only fix the implementation.

This task showed me I make choices when I'm in a hurry.

I prefer reversible changes and frequent tests.

It also showed me some gaps.

I have to be careful with commit history and rely on tests to work correctly.

I should learn more about git workflows and lightweight UI tests.

This way I can check UI changes and refactor documents or templates.

On the day I'll run the projects tests and some searches to see what needs attention.

Then I'll look at the relevant documents.

My plan is to:

1. Run tests

2. Search for what I'm about to change

3. Make a change

4. Run tests again

I'll document any AI-assisted steps, in PR descriptions. Keep changes small and reviewable.

The first thing I'll do is clone the repo run the tests and create a branch with a one-line improvement.

This way I can confirm that CI and the teams review process work smoothly.

Replace the essay with this

During this change I routed work through a small set of tools chosen for clarity and safety. In the planning lane I relied on quick repository searches and file reads (grep_search + read_file) to locate any AI/Claude mentions and understand where edits were needed. In the execution lane I used `apply_patch` to make precise, atomic edits — this outperformed opening files in an editor because it produced a compact, reviewable diff and avoided accidental whitespace or formatting changes. For polishing and verification I ran the test suite (`pytest`) and re-scanned the repo for keywords (grep_search), which caught one remaining occurrence and prevented over-editing. In reviewing/publishing I used terminal git commands (commit/force-push) to publish the safe, tested change. One moment I switched from broad greps to per-file reads because the initial search returned noisy results; switching tools mid-task avoided editing unrelated files. Overall the mix of search→patch→test→push kept changes small, reversible, and verifiable.
