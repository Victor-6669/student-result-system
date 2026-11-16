"""reports.py - Build and save text reports."""

import os
from datetime import datetime

import results
from storage import BASE_DIR

REPORTS_DIR = os.path.join(BASE_DIR, "reports")
LINE = "=" * 60
THIN = "-" * 60


def format_report_card(student):
    """Return a printable report card for one student."""
    lines = [
        LINE,
        "STUDENT REPORT CARD".center(60),
        LINE,
        f"ID: {student.student_id}    Name: {student.name}",
        f"Class: {student.class_name}    Gender: {student.gender}    "
        f"DOB: {student.dob}",
        THIN,
        f"{'Subject':<25}{'Score':>10}",
        THIN,
    ]
    for subject in results.SUBJECTS:
        if subject in student.scores:
            lines.append(f"{subject:<25}{student.scores[subject]:>10.1f}")
        else:
            lines.append(f"{subject:<25}{'--':>10}")
    # Any extra subjects beyond the standard list
    for subject, score in student.scores.items():
        if subject not in results.SUBJECTS:
            lines.append(f"{subject:<25}{score:>10.1f}")

    lines.append(THIN)
    if student.scores:
        total = results.calculate_total(student.scores)
        average = results.calculate_average(student.scores)
        out_of = len(student.scores) * 100
        lines.append(f"Total:   {total:.1f} / {out_of}")
        lines.append(f"Average: {average:.2f}")
        lines.append(f"Grade:   {results.assign_grade(average)}")
        if not results.has_complete_results(student):
            lines.append("(Note: some subject scores are still missing)")
        lines.append(f"Result entered: {student.result_date}")
    else:
        lines.append("No scores recorded yet.")
    lines.append(LINE)
    return "\n".join(lines)


def format_student_list(students):
    """Return a table of students (no scores)."""
    if not students:
        return "No students found."
    lines = [
        f"{'ID':<10}{'Name':<25}{'Class':<8}{'Gender':<8}{'DOB':<12}",
        THIN,
    ]
    for s in students:
        lines.append(
            f"{s.student_id:<10}{s.name:<25}{s.class_name:<8}"
            f"{s.gender:<8}{s.dob:<12}"
        )
    return "\n".join(lines)


def format_results_table(students):
    """Return a table of students with total, average and grade."""
    if not students:
        return "No students found."
    lines = [
        f"{'ID':<10}{'Name':<25}{'Total':>8}{'Average':>10}{'Grade':>7}",
        THIN,
    ]
    for s in students:
        if s.scores:
            total = results.calculate_total(s.scores)
            average = results.calculate_average(s.scores)
            grade = results.assign_grade(average)
            lines.append(
                f"{s.student_id:<10}{s.name:<25}{total:>8.1f}"
                f"{average:>10.2f}{grade:>7}"
            )
        else:
            lines.append(
                f"{s.student_id:<10}{s.name:<25}{'--':>8}{'--':>10}{'--':>7}"
            )
    return "\n".join(lines)


def format_statistics(stats):
    """Return class statistics as text."""
    if stats is None:
        return "No complete results yet, so there are no statistics."
    high_score, high_subject, high_name = stats["highest_score"]
    low_score, low_subject, low_name = stats["lowest_score"]
    lines = [
        f"Students with complete results: {stats['count']}",
        f"Class average: {stats['class_average']:.2f}",
        f"Top student:    {stats['top_student'].name} "
        f"({stats['top_average']:.2f})",
        f"Lowest student: {stats['bottom_student'].name} "
        f"({stats['bottom_average']:.2f})",
        f"Highest score:  {high_score:.1f} - {high_name} ({high_subject})",
        f"Lowest score:   {low_score:.1f} - {low_name} ({low_subject})",
    ]
    return "\n".join(lines)


def build_full_report(students):
    """Build the full class report (ranked table + statistics)."""
    ranked = results.sort_by_average(students)
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    parts = [
        LINE,
        "CLASS RESULT REPORT".center(60),
        f"Generated: {generated}".center(60),
        LINE,
        format_results_table(ranked),
        THIN,
        "CLASS STATISTICS",
        THIN,
        format_statistics(results.class_statistics(students)),
        LINE,
    ]
    return "\n".join(parts)


def save_report(text):
    """Save report text to a timestamped file in the reports folder.

    Returns the file path, or None if saving failed.
    """
    try:
        os.makedirs(REPORTS_DIR, exist_ok=True)
        filename = datetime.now().strftime("report_%Y%m%d_%H%M%S.txt")
        path = os.path.join(REPORTS_DIR, filename)
        with open(path, "w", encoding="utf-8") as file:
            file.write(text + "\n")
    except OSError as error:
        print(f"Error: could not save report ({error}).")
        return None
    return path
