"""main.py - Entry point and menu for the Student Result Management System."""

import reports
import results
import storage
from student import (
    Student,
    VALID_GENDERS,
    is_valid_dob,
    is_valid_id,
    search_students,
)

MENU = """
========== STUDENT RESULT MANAGEMENT SYSTEM ==========
 1. Add student              7. Update a score
 2. View all students        8. Show report card
 3. Search student           9. Class results (sorted)
 4. Update student info     10. Class statistics
 5. Delete student          11. Save text report to file
 6. Record scores            0. Exit
======================================================"""


# ---------- input helpers ----------

def ask(prompt, validator=None, error="Invalid input, try again."):
    """Keep asking until the person types a non-empty, valid answer."""
    while True:
        value = input(prompt).strip()
        if not value:
            print("This field cannot be empty.")
        elif validator is None or validator(value):
            return value
        else:
            print(error)


def ask_optional(prompt, validator=None, error="Invalid input, try again."):
    """Like ask(), but pressing Enter returns None (keep the old value)."""
    while True:
        value = input(prompt).strip()
        if not value:
            return None
        if validator is None or validator(value):
            return value
        print(error)


def ask_score(student, subject):
    """Ask for a score until a valid number from 0 to 100 is entered."""
    while True:
        raw = input(f"  {subject} score (0-100): ").strip()
        try:
            student.set_score(subject, raw)
        except ValueError as error:
            # float() failures and out-of-range scores both end up here.
            print(f"  Invalid: {error}" if "between" in str(error)
                  else "  Invalid: please enter a number.")
        else:
            return


def pick_student(students):
    """Ask for a student ID and return that Student (or None)."""
    student_id = input("Enter student ID: ").strip().upper()
    student = students.get(student_id)
    if student is None:
        print("No student with that ID.")
    return student


def save(students):
    """Save data after every change so nothing is lost."""
    storage.save_students(students)


# ---------- menu actions ----------

def add_student(students):
    print("\n--- Add New Student ---")
    student_id = ask(
        "Student ID (e.g. STU001): ",
        lambda v: is_valid_id(v.upper()),
        "ID must look like STU001 (STU followed by 3+ digits).",
    ).upper()
    if student_id in students:
        print("That ID already exists.")
        return
    name = ask("Full name: ").title()
    class_name = ask("Class/Form (e.g. SS2): ").upper()
    gender = ask(
        "Gender (M/F): ",
        lambda v: v.upper() in VALID_GENDERS,
        "Please enter M or F.",
    ).upper()
    dob = ask(
        "Date of birth (YYYY-MM-DD): ",
        is_valid_dob,
        "Enter a real past date like 2009-04-23.",
    )
    students[student_id] = Student(student_id, name, class_name, gender, dob)
    save(students)
    print(f"Student {name} added.")


def view_all(students):
    print("\n--- All Students ---")
    print(reports.format_student_list(results.sort_by_name(students.values())))


def search(students):
    print("\n--- Search Student ---")
    query = ask("Enter student ID or name: ")
    matches = search_students(students, query)
    print(reports.format_student_list(matches))


def update_student(students):
    print("\n--- Update Student Info (press Enter to keep current value) ---")
    student = pick_student(students)
    if student is None:
        return
    name = ask_optional(f"Full name [{student.name}]: ")
    class_name = ask_optional(f"Class/Form [{student.class_name}]: ")
    gender = ask_optional(
        f"Gender [{student.gender}]: ",
        lambda v: v.upper() in VALID_GENDERS,
        "Please enter M or F.",
    )
    dob = ask_optional(
        f"Date of birth [{student.dob}]: ",
        is_valid_dob,
        "Enter a real past date like 2009-04-23.",
    )
    if name:
        student.name = name.title()
    if class_name:
        student.class_name = class_name.upper()
    if gender:
        student.gender = gender.upper()
    if dob:
        student.dob = dob
    save(students)
    print("Student updated.")


def delete_student(students):
    print("\n--- Delete Student ---")
    student = pick_student(students)
    if student is None:
        return
    confirm = input(f"Delete {student}? (y/n): ").strip().lower()
    if confirm == "y":
        del students[student.student_id]
        save(students)
        print("Student deleted.")
    else:
        print("Cancelled.")


def record_scores(students):
    print("\n--- Record Scores ---")
    student = pick_student(students)
    if student is None:
        return
    if results.has_complete_results(student):
        print("This student already has all scores. Use option 7 to update.")
        return
    print(f"Enter scores for {student.name}:")
    for subject in results.SUBJECTS:
        if subject not in student.scores:
            ask_score(student, subject)
    save(students)
    print("Scores saved.")


def update_score(students):
    print("\n--- Update a Score ---")
    student = pick_student(students)
    if student is None:
        return
    if not student.scores:
        print("No scores yet. Use option 6 first.")
        return
    print("Subjects:", ", ".join(student.scores))
    subject = ask(
        "Subject to update: ",
        lambda v: v.title() in student.scores,
        "That subject is not recorded for this student.",
    ).title()
    ask_score(student, subject)
    save(students)
    print("Score updated.")


def show_report_card(students):
    print("\n--- Report Card ---")
    student = pick_student(students)
    if student is not None:
        print(reports.format_report_card(student))


def class_results(students):
    print("\n--- Class Results ---")
    choice = ask(
        "Sort by (1) average, highest first or (2) name: ",
        lambda v: v in ("1", "2"),
        "Please enter 1 or 2.",
    )
    if choice == "1":
        ordered = results.sort_by_average(students.values())
    else:
        ordered = results.sort_by_name(students.values())
    print(reports.format_results_table(ordered))


def class_statistics(students):
    print("\n--- Class Statistics ---")
    stats = results.class_statistics(students.values())
    print(reports.format_statistics(stats))


def save_text_report(students):
    print("\n--- Save Text Report ---")
    if not students:
        print("No students to report on.")
        return
    path = reports.save_report(reports.build_full_report(students.values()))
    if path:
        print(f"Report saved to: {path}")


# ---------- program loop ----------

ACTIONS = {
    "1": add_student,
    "2": view_all,
    "3": search,
    "4": update_student,
    "5": delete_student,
    "6": record_scores,
    "7": update_score,
    "8": show_report_card,
    "9": class_results,
    "10": class_statistics,
    "11": save_text_report,
}


def main():
    students = storage.load_students()
    print(f"Loaded {len(students)} student(s).")
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            save(students)
            print("Data saved. Goodbye!")
            break
        action = ACTIONS.get(choice)
        if action is None:
            print("Invalid option, please choose from the menu.")
        else:
            action(students)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram closed.")
