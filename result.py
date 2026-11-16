"""results.py - Score calculation, grading, sorting and class statistics."""

# Every student must have a score for each of these (at least five subjects).
SUBJECTS = ["Mathematics", "English", "Physics", "Chemistry", "Biology"]

# (minimum average, grade) - checked from the top down.
GRADE_SCALE = [
    (70, "A"),
    (60, "B"),
    (50, "C"),
    (40, "D"),
]


def calculate_total(scores):
    """Return the sum of all scores in a {subject: score} dictionary."""
    return sum(scores.values())


def calculate_average(scores):
    """Return the average score (0.0 if there are no scores)."""
    if not scores:
        return 0.0
    return calculate_total(scores) / len(scores)


def assign_grade(average):
    """Turn an average score into a letter grade."""
    for minimum, grade in GRADE_SCALE:
        if average >= minimum:
            return grade
    return "F"


def has_complete_results(student):
    """True if the student has a score for every subject in SUBJECTS."""
    return all(subject in student.scores for subject in SUBJECTS)


def sort_by_average(students):
    """Return a list of students sorted from highest to lowest average."""
    return sorted(
        students,
        key=lambda s: calculate_average(s.scores),
        reverse=True,
    )


def sort_by_name(students):
    """Return a list of students sorted A-Z by name."""
    return sorted(students, key=lambda s: s.name.lower())


def class_statistics(students):
    """Work out class statistics from students that have complete results.

    Returns a dictionary, or None if no student has complete results yet.
    """
    graded = [s for s in students if has_complete_results(s)]
    if not graded:
        return None

    averages = [calculate_average(s.scores) for s in graded]
    top_student = max(graded, key=lambda s: calculate_average(s.scores))
    bottom_student = min(graded, key=lambda s: calculate_average(s.scores))

    # Highest and lowest single subject score across the whole class.
    all_scores = []  # list of (score, subject, student name) tuples
    for s in graded:
        for subject, score in s.scores.items():
            all_scores.append((score, subject, s.name))

    return {
        "count": len(graded),
        "class_average": sum(averages) / len(averages),
        "top_student": top_student,
        "top_average": calculate_average(top_student.scores),
        "bottom_student": bottom_student,
        "bottom_average": calculate_average(bottom_student.scores),
        "highest_score": max(all_scores),
        "lowest_score": min(all_scores),
    }
