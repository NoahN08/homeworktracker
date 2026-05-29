from flask import Flask, render_template, request, redirect, url_for
from datetime import date


def create_app():
    app = Flask(__name__)

    # Task 2: seeded assignments (one due soon, one due later for sort testing)
    app.assignments = [
        {"title": "Math Homework", "class_name": "Calculus", "due_date": "2026-06-05", "done": False},
        {"title": "Essay Draft", "class_name": "English", "due_date": "2026-05-30", "done": False},
    ]

    @app.route("/")
    def home():
        today = date.today().isoformat()
        # Task 4: sort upcoming by due_date (ISO strings sort lexicographically)
        upcoming = sorted(
            [a for a in app.assignments if not a["done"]],
            key=lambda a: a["due_date"],
        )
        done = [a for a in app.assignments if a["done"]]
        return render_template("home.html", upcoming=upcoming, done=done, today=today)

    @app.route("/add", methods=["GET", "POST"])
    def add():
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            class_name = request.form.get("class_name", "").strip()
            due_date = request.form.get("due_date", "").strip()

            errors = {}
            if not title:
                errors["title"] = "Title is required"
            if not class_name:
                errors["class_name"] = "Class name is required"
            if not due_date:
                errors["due_date"] = "Due date is required"
            else:
                try:
                    date.fromisoformat(due_date)
                except ValueError:
                    errors["due_date"] = "Due date must be YYYY-MM-DD"

            if errors:
                return render_template(
                    "add.html",
                    errors=errors,
                    title=title,
                    class_name=class_name,
                    due_date=due_date,
                )

            app.assignments.append(
                {"title": title, "class_name": class_name, "due_date": due_date, "done": False}
            )
            return redirect(url_for("home"))

        return render_template("add.html", errors={}, title="", class_name="", due_date="")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
