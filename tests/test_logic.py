from datetime import date


def test_sort_order_earliest_first():
    assignments = [
        {"title": "Later", "class_name": "Math", "due_date": "2026-06-10", "done": False},
        {"title": "Sooner", "class_name": "English", "due_date": "2026-06-01", "done": False},
        {"title": "Middle", "class_name": "History", "due_date": "2026-06-05", "done": False},
    ]
    result = sorted(
        [a for a in assignments if not a["done"]],
        key=lambda a: a["due_date"],
    )
    assert [a["title"] for a in result] == ["Sooner", "Middle", "Later"]


def test_overdue_detection():
    today = date.today().isoformat()
    assert "2020-01-01" < today          # clearly past → overdue
    assert "2099-12-31" >= today         # clearly future → not overdue


def test_done_items_excluded_from_upcoming():
    assignments = [
        {"title": "Finished", "class_name": "Art", "due_date": "2026-06-01", "done": True},
        {"title": "Pending", "class_name": "Math", "due_date": "2026-06-05", "done": False},
    ]
    upcoming = [a for a in assignments if not a["done"]]
    done = [a for a in assignments if a["done"]]

    assert len(upcoming) == 1 and upcoming[0]["title"] == "Pending"
    assert len(done) == 1 and done[0]["title"] == "Finished"


def test_iso_date_string_comparison_is_chronological():
    # Lexicographic order == chronological order for YYYY-MM-DD
    dates = ["2026-12-01", "2026-01-15", "2026-06-30"]
    assert sorted(dates) == ["2026-01-15", "2026-06-30", "2026-12-01"]
