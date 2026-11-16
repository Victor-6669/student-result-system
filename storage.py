"""storage.py - Load and save student data as JSON."""

import json
import os

from student import Student

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "students.json")


def load_students(path=DATA_FILE):
    """Load students from a JSON file.

    Returns a dictionary of {student_id: Student}.
    If the file does not exist yet (first run) or is damaged, returns {}.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            raw_data = json.load(file)
    except FileNotFoundError:
        # First time the program runs - nothing saved yet, so start empty.
        return {}
    except json.JSONDecodeError:
        print("Warning: data file is damaged. Starting with an empty list.")
        return {}
    else:
        # Only runs if the file was read without errors.
        students = {}
        for item in raw_data:
            student = Student.from_dict(item)
            students[student.student_id] = student
        return students


def save_students(students, path=DATA_FILE):
    """Save all students to a JSON file.

    Writes to a temporary file first, then swaps it in, so a crash
    half-way through never leaves a broken data file behind.
    """
    temp_path = path + ".tmp"
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump([s.to_dict() for s in students.values()], file, indent=4)
        os.replace(temp_path, path)
    except OSError as error:
        print(f"Error: could not save data ({error}).")
        return False
    else:
        return True
    finally:
        # Always clean up the temp file if something went wrong.
        if os.path.exists(temp_path):
            os.remove(temp_path)
