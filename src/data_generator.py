"""
Synthetic student data generator.

We never use real student data. This generator produces realistic-looking
records that mirror the shape of typical K-12 student information so we
can demo the Counselor Co-Pilot safely.
"""

import random
import pandas as pd
from pathlib import Path

random.seed(42)  # makes results repeatable

FIRST_NAMES = ["Maria", "Aiden", "Sofia", "Jamal", "Priya", "Diego",
               "Zara", "Noah", "Aaliyah", "Lucas", "Isabella", "Mateo",
               "Amara", "Ethan", "Layla"]
LAST_NAMES = ["Garcia", "Smith", "Patel", "Johnson", "Nguyen", "Lopez",
              "Brown", "Khan", "Davis", "Martinez"]
GRADES = [9, 10, 11, 12]
CAREER_INTERESTS = [
    "Nursing", "Software Engineering", "Business / Entrepreneurship",
    "Education", "Mechanical Engineering", "Healthcare (general)",
    "Law / Criminal Justice", "Skilled Trades", "Undecided"
]
PATHWAYS = [
    "Health Science", "STEM", "Business & Finance",
    "Arts & Humanities", "Skilled Trades", "None yet"
]


def make_student(student_id: int) -> dict:
    """Generate one synthetic student record."""
    attendance = round(random.uniform(70, 99), 1)
    gpa = round(random.uniform(1.8, 4.0), 2)
    behavior_flags = random.choice([0, 0, 0, 1, 2])  # mostly zero
    college_app_progress = random.choice(
        ["Not started", "In progress", "Submitted", "Multiple submitted"]
    )

    return {
        "student_id": f"S{1000 + student_id}",
        "first_name": random.choice(FIRST_NAMES),
        "last_name": random.choice(LAST_NAMES),
        "grade": random.choice(GRADES),
        "attendance_pct": attendance,
        "gpa": gpa,
        "behavior_flags_this_quarter": behavior_flags,
        "career_interest": random.choice(CAREER_INTERESTS),
        "pathway": random.choice(PATHWAYS),
        "college_app_progress": college_app_progress,
        "last_counselor_meeting_days_ago": random.randint(3, 180),
    }


def generate_dataset(n: int = 50) -> pd.DataFrame:
    """Generate a DataFrame of n synthetic students."""
    students = [make_student(i) for i in range(n)]
    return pd.DataFrame(students)


if __name__ == "__main__":
    df = generate_dataset(50)
    out_path = Path(__file__).parent.parent / "data" / "sample_students.csv"
    df.to_csv(out_path, index=False)
    print(f"✅ Generated {len(df)} synthetic students → {out_path}")