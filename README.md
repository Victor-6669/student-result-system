# Student Result Management System

A menu-driven Python program that lets a school register students, record
subject scores, calculate totals/averages/grades, and generate reports.
Built for the New Horizon *Introduction to Python Programming* project.

## Features

- **Student management:** add, view, search (by ID or name), update, delete
- **Results:** record scores for 5 subjects, update scores, report card per student
- **Grading:** total, average and letter grade (A-F)
- **Reports:** ranked class list (by average or name), class statistics, save a text report
- **Persistence:** all data is saved to `data/students.json` and loaded on start-up

## Requirements

- Python 3.8 or newer (standard library only, nothing to install)

## How to run

```bash
git clone <your-repo-url>
cd student-result-system
python main.py
```

On the first run there is no data file, so the program starts empty and
creates `data/students.json` automatically.

## Project structure

```
student-result-system/
├── main.py        # Entry point and main menu
├── student.py     # Student class, validation (regex), search
├── results.py     # Totals, averages, grading, sorting, statistics
├── storage.py     # Load/save JSON data
├── reports.py     # Report card, tables and text report export
├── data/
│   └── students.json   # Created automatically
└── reports/            # Saved text reports appear here
```

## Grading scale

| Average | Grade |
|---------|-------|
| 70+     | A     |
| 60-69   | B     |
| 50-59   | C     |
| 40-49   | D     |
| Below 40| F     |

## Subjects

Mathematics, English, Physics, Chemistry, Biology
(change the `SUBJECTS` list in `results.py` to use different ones).

## Python concepts used

- Variables, data types and type conversion (`float()` on score input)
- Flow control: `if/elif/else`, `for` and `while` loops
- Lists, tuples and dictionaries (students stored in a dict keyed by ID)
- Functions with parameters and return values
- Sorting with `sorted()` and `lambda` keys
- Exception handling: `try / except / else / finally`
- File handling with JSON
- Modules: code split across multiple `.py` files
- Object-Oriented Programming: the `Student` class
- Dates and times: `datetime` records when results were entered
- Standard library: `os`, `json`, `re`, `datetime`
- Regular expressions to validate student IDs (`STU001` format)
