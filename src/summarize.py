"""
Counselor Co-Pilot AI Summarizer.

Takes one student record (a dict) and uses a free Hugging Face-hosted LLM
to generate a short, counselor-facing brief.

Design notes:
- We never send real PII. The demo uses synthetic data only.
- The prompt is structured to keep outputs actionable, not just descriptive.
- We constrain length and tone to keep it useful in a real workflow.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()  # loads HF_TOKEN from .env

HF_TOKEN = os.getenv("HF_TOKEN")

# Hugging Face Inference Providers endpoint (new, replaces old inference-api)
API_URL = "https://router.huggingface.co/v1/chat/completions"
MODEL_ID = MODEL_ID = "meta-llama/Llama-3.1-8B-Instruct:novita"


def build_prompt(student: dict) -> str:
    """Turn a student record into a structured prompt."""
    return f"""You are an assistant for a high school counselor. Given the student
data below, write a SHORT brief (max 5 sentences) that:
1. Summarizes where the student stands academically and behaviorally
2. Highlights ONE concern (if any) that needs attention
3. Suggests ONE concrete next conversation the counselor should have
4. Connects the student's career interest to a possible pathway action

Be direct, warm, and specific. Do NOT make up information that isn't given.

STUDENT DATA:
- Name: {student['first_name']} {student['last_name']}
- Grade: {student['grade']}
- Attendance: {student['attendance_pct']}%
- GPA: {student['gpa']}
- Behavior flags this quarter: {student['behavior_flags_this_quarter']}
- Career interest: {student['career_interest']}
- Current pathway: {student['pathway']}
- College application progress: {student['college_app_progress']}
- Days since last counselor meeting: {student['last_counselor_meeting_days_ago']}

Write the counselor brief now."""


def summarize_student(student: dict) -> str:
    """Call the LLM and return the generated brief."""
    if not HF_TOKEN:
        return "⚠️ No HF_TOKEN found. Please add it to your .env file."

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "user", "content": build_prompt(student)}
        ],
        "max_tokens": 300,
        "temperature": 0.4,
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.exceptions.HTTPError as e:
        return f"API error ({response.status_code}): {response.text}"
    except requests.exceptions.ConnectionError:
        return "🌐 Network error: cannot reach Hugging Face. Check your internet/VPN."
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    # Quick test with one student
    test_student = {
        "first_name": "Maria",
        "last_name": "Garcia",
        "grade": 11,
        "attendance_pct": 82.3,
        "gpa": 2.9,
        "behavior_flags_this_quarter": 1,
        "career_interest": "Nursing",
        "pathway": "Health Science",
        "college_app_progress": "Not started",
        "last_counselor_meeting_days_ago": 95,
    }
    print("Calling AI model... (may take 20s the first time)\n")
    print(summarize_student(test_student))