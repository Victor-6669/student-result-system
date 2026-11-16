"""student.py - The Student class, input validation and search helpers."""

import re
from datetime import datetime, date

# Regular expression: "STU" followed by at least 3 digits, e.g. STU001
ID_PATTERN = re.compile(r"^STU\d{3,}$")
VALID_GENDERS = ("M", "F")


def is_valid_id(student_id):
    """Return True if the ID looks like STU001, STU1234, etc."""
    return bool(ID_PATTERN.match(student_id))


def is_valid_dob(text):
    """Return True if text is a real past date written as YYYY-MM-DD."""
    try:
        dob = datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return False
    return dob < date.today()


class Student:
    """Represents one student and the scores recorded for them."""

    def __init__(self, student_id, name, class_name, gender, dob,
                 scores=None, result_date=None):
        self.student_id = student_id
        self.name = name
        self.class_name = class_name
        self.gender = gender
        self.dob = dob
        self.scores = scores if scores is not None else {}  # {subject: score}
        self.result_date = result_date  # when the scores were last entered

    def set_score(self, subject, score):
        """Add or update a subject score (must be 0-100) and stamp the date."""
        score = float(score)  # may raise ValueError if not a number
        if not 0 <= score <= 100:
            raise ValueError("Score must be between 0 and 100.")
        self.scores[subject] = score
        self.result_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self):
        """Convert to a plain dictionary so it can be saved as JSON."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "class_name": self.class_name,
            "gender": self.gender,
            "dob": self.dob,
            "scores": self.scores,
            "result_date": self.result_date,
        }

    @classmethod
    def from_dict(cls, data):
        """Build a Student back from a dictionary loaded from JSON."""
        return cls(
            data["student_id"],
            data["name"],
            data["class_name"],
            data["gender"],
            data["dob"],
            data.get("scores", {}),
            data.get("result_date"),
        )

    def __str__(self):
        return f"{self.student_id} - {self.name} ({self.class_name})"


def search_students(students, query):
    """Find students by exact ID or by part of the name (case-insensitive).

    `students` is a dictionary of {student_id: Student}.
    Returns a list of matching Student objects.
    """
    query = query.strip().lower()
    matches = []
    for student in students.values():
        if query == student.student_id.lower() or query in student.name.lower():
            matches.append(student)
    return matches
