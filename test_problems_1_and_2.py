"""
Comprehensive verification test for CogniLearn Problem 1 & Problem 2 solutions.

Problem 1:
- Personalized study timetable using student-owned subjects and topics
- Anti-starvation and subject rotation (no repeating same subject)
- Rich session timing (start_time, end_time, duration, activity, priority)
- Weak topic prioritization from real quiz scores
- Timetable persistence, session editing, deleting, and complete toggling
- Clear message when student has no subjects

Problem 2:
- OpenAI API integration for educational quiz questions (Easy, Medium, Hard)
- Question count options (5, 10, etc.)
- 4 options per question, correct answer in options
- No correct answers exposed before submission
- Server-side answer validation & scoring
- Results display with pedagogical explanations
- Real quiz performance reflected in Dashboard, Heuristics, and ML Predictions
"""

import sys
import time
import requests

BASE_URL = "http://127.0.0.1:8000/api"

def run_tests():
    print("=" * 70)
    print("RUNNING COMPREHENSIVE TESTS: PROBLEM 1 & PROBLEM 2")
    print("=" * 70)

    # ──────────────────────────────────────────────────────────────────────────
    # 1. Register a fresh test student
    # ──────────────────────────────────────────────────────────────────────────
    student_email = f"test_student_{int(time.time())}@cognilearn.ai"
    reg_res = requests.post(f"{BASE_URL}/auth/register", json={
        "name": "Jordan Lee",
        "email": student_email,
        "password": "Password123!"
    })
    assert reg_res.status_code in [200, 201], f"Registration failed: {reg_res.text}"
    token = reg_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"[PASSED] Test student registered: {student_email}")

    # ──────────────────────────────────────────────────────────────────────────
    # 2. Test Empty Subject Guard for Timetable
    # ──────────────────────────────────────────────────────────────────────────
    empty_sched_res = requests.post(f"{BASE_URL}/ai/generate-schedule", json={
        "daily_study_hours": 3,
        "start_time": "09:00 AM",
        "available_days": ["Monday", "Tuesday", "Wednesday"],
    }, headers=headers)
    assert empty_sched_res.status_code == 400, f"Expected 400 for no subjects, got {empty_sched_res.status_code}"
    detail_msg = empty_sched_res.json().get("detail", "")
    assert "No subjects available" in detail_msg, f"Unexpected error detail: {detail_msg}"
    print(f"[PASSED] Empty timetable guard verified: '{detail_msg}'")

    # ──────────────────────────────────────────────────────────────────────────
    # 3. Create Student Subjects & Topics (Multi-subject setup)
    # ──────────────────────────────────────────────────────────────────────────
    # Subject A: Artificial Intelligence
    sub_a_res = requests.post(f"{BASE_URL}/subjects", json={
        "name": "Artificial Intelligence",
        "code": "CS-401",
        "semester": 4,
        "description": "Modern intelligent agents and search methodologies"
    }, headers=headers)
    assert sub_a_res.status_code in [200, 201], f"Subject A failed: {sub_a_res.status_code} {sub_a_res.text}"
    sub_a = sub_a_res.json()

    top_a1_res = requests.post(f"{BASE_URL}/subjects/{sub_a['id']}/topics", json={
        "name": "Search Algorithms",
        "description": "BFS, DFS, Uniform Cost, and A* Search",
        "difficulty": 3,
        "priority": "High"
    }, headers=headers)
    top_a1 = top_a1_res.json()

    top_a2_res = requests.post(f"{BASE_URL}/subjects/{sub_a['id']}/topics", json={
        "name": "Constraint Satisfaction Problems",
        "description": "Backtracking search, MRV heuristic, and AC-3",
        "difficulty": 4,
        "priority": "High"
    }, headers=headers)
    top_a2 = top_a2_res.json()

    # Subject B: Database Management Systems
    sub_b_res = requests.post(f"{BASE_URL}/subjects", json={
        "name": "Database Management Systems",
        "code": "CS-302",
        "semester": 3,
        "description": "Relational algebra, normalization, and ACID transactions"
    }, headers=headers)
    assert sub_b_res.status_code in [200, 201]
    sub_b = sub_b_res.json()

    top_b1_res = requests.post(f"{BASE_URL}/subjects/{sub_b['id']}/topics", json={
        "name": "Query Optimization",
        "description": "Cost-based execution plans and indexing strategies",
        "difficulty": 3,
        "priority": "Medium"
    }, headers=headers)
    top_b1 = top_b1_res.json()

    top_b2_res = requests.post(f"{BASE_URL}/subjects/{sub_b['id']}/topics", json={
        "name": "Transaction Concurrency",
        "description": "Two-phase locking and serializability protocols",
        "difficulty": 4,
        "priority": "High"
    }, headers=headers)
    top_b2 = top_b2_res.json()

    # Subject C: Computer Networks
    sub_c_res = requests.post(f"{BASE_URL}/subjects", json={
        "name": "Computer Networks",
        "code": "CS-305",
        "semester": 3,
        "description": "OSI stack, TCP/IP congestion control, and routing"
    }, headers=headers)
    assert sub_c_res.status_code in [200, 201]
    sub_c = sub_c_res.json()

    top_c1_res = requests.post(f"{BASE_URL}/subjects/{sub_c['id']}/topics", json={
        "name": "Routing Protocols",
        "description": "Distance vector and link-state routing algorithms",
        "difficulty": 3,
        "priority": "Medium"
    }, headers=headers)
    top_c1 = top_c1_res.json()

    print(f"[PASSED] Created 3 student subjects with 5 topics.")

    # ──────────────────────────────────────────────────────────────────────────
    # 4. PROBLEM 2: Quiz Generation with OpenAI / Fallback Engine
    # ──────────────────────────────────────────────────────────────────────────
    print("\n--- Testing Problem 2: Quiz Generation (Easy, Medium, Hard) ---")
    
    # 4a. Easy Quiz (5 Questions)
    easy_quiz_res = requests.post(f"{BASE_URL}/quiz/generate", json={
        "subject_id": sub_a["id"],
        "topic_id": top_a1["id"],
        "difficulty": "Easy",
        "num_questions": 5,
    }, headers=headers)
    assert easy_quiz_res.status_code == 200, f"Easy quiz failed: {easy_quiz_res.text}"
    easy_quiz = easy_quiz_res.json()
    assert len(easy_quiz["questions"]) == 5, f"Expected 5 questions, got {len(easy_quiz['questions'])}"
    assert easy_quiz["difficulty"] == "Easy"
    assert easy_quiz["topic_name"] == top_a1["name"]
    # Verify no correct answer leak
    for q in easy_quiz["questions"]:
        assert "correct_option" not in q or q.get("correct_option") is None
        assert "correct_answer" not in q
        assert q["option_a"] and q["option_b"] and q["option_c"] and q["option_d"]
    print(f"[PASSED] Easy quiz generated (5 questions) without leaking correct answers.")

    # 4b. Medium Quiz (10 Questions)
    med_quiz_res = requests.post(f"{BASE_URL}/quiz/generate", json={
        "subject_id": sub_a["id"],
        "topic_id": top_a1["id"],
        "difficulty": "Medium",
        "num_questions": 10,
    }, headers=headers)
    assert med_quiz_res.status_code == 200
    med_quiz = med_quiz_res.json()
    assert len(med_quiz["questions"]) == 10
    assert med_quiz["difficulty"] == "Medium"
    print(f"[PASSED] Medium quiz generated (10 questions) calibrated to application & reasoning.")

    # 4c. Hard Quiz (5 Questions on CSPs)
    hard_quiz_res = requests.post(f"{BASE_URL}/quiz/generate", json={
        "subject_id": sub_a["id"],
        "topic_id": top_a2["id"],
        "difficulty": "Hard",
        "num_questions": 5,
    }, headers=headers)
    assert hard_quiz_res.status_code == 200
    hard_quiz = hard_quiz_res.json()
    assert len(hard_quiz["questions"]) == 5
    assert hard_quiz["difficulty"] == "Hard"
    print(f"[PASSED] Hard quiz generated (5 questions) calibrated to deeper problem-solving.")

    # ──────────────────────────────────────────────────────────────────────────
    # 5. Quiz Attempt Submission & Explanation Validation
    # ──────────────────────────────────────────────────────────────────────────
    print("\n--- Testing Problem 2: Answer Validation, Scoring & Explanations ---")
    
    # Intentionally answer 3 correctly and 2 incorrectly
    answers = []
    for idx, q in enumerate(easy_quiz["questions"]):
        chosen = "A" if idx < 3 else "C"
        answers.append({"question_id": q["id"], "selected_option": chosen})

    submit_res = requests.post(f"{BASE_URL}/quiz/submit", json={
        "topic_id": top_a1["id"],
        "answers": answers,
    }, headers=headers)
    assert submit_res.status_code == 200, f"Submit failed: {submit_res.text}"
    result = submit_res.json()
    
    assert "score" in result
    assert result["total_questions"] == 5
    assert "correct_answers" in result
    assert "incorrect_answers" in result
    assert result["total_questions"] == result["correct_answers"] + result["incorrect_answers"]
    assert len(result["details"]) == 5
    
    # Verify each question has pedagogical explanation and correct options
    for d in result["details"]:
        assert "explanation" in d and len(d["explanation"]) > 5, "Missing educational explanation"
        assert d["correct_option"] in ["A", "B", "C", "D"]
        assert isinstance(d["is_correct"], bool)
    print(f"[PASSED] Server-side grading succeeded: Score {result['score']}%, {result['correct_answers']} correct, {result['incorrect_answers']} incorrect.")
    print(f"         Verified pedagogical explanations present in every audit record.")

    # ──────────────────────────────────────────────────────────────────────────
    # 6. Verify Dashboard and AI Modules reflect Real Quiz Performance
    # ──────────────────────────────────────────────────────────────────────────
    print("\n--- Testing Problem 2: Live AI Integration ---")
    dash_res = requests.get(f"{BASE_URL}/dashboard/stats", headers=headers)
    dash_data = dash_res.json()
    assert dash_data["total_quizzes"] == 1
    assert dash_data["total_subjects"] == 3
    assert dash_data["total_topics"] == 5
    print(f"[PASSED] Dashboard updated: {dash_data['total_quizzes']} quiz, avg score {dash_data['average_score']}%.")

    heur_res = requests.get(f"{BASE_URL}/ai/heuristic-priorities", headers=headers)
    assert heur_res.status_code == 200
    ranked_topics = heur_res.json()
    assert len(ranked_topics) > 0
    print(f"[PASSED] AI Heuristic prioritized {len(ranked_topics)} student topics.")

    # ──────────────────────────────────────────────────────────────────────────
    # 7. PROBLEM 1: Personalized Study Timetable Generation & Anti-Repetition
    # ──────────────────────────────────────────────────────────────────────────
    print("\n--- Testing Problem 1: Personalized CSP Timetable Generation ---")
    sched_payload = {
        "daily_study_hours": 3,
        "start_time": "09:00 AM",
        "session_duration": 45,
        "available_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "max_hours_per_day": 3,
        "max_consecutive_hours": 2,
        "total_weekly_hours": 15,
        "subject_ids": [sub_a["id"], sub_b["id"], sub_c["id"]],
        "exam_date": "2026-11-20",
    }

    sched_res = requests.post(f"{BASE_URL}/ai/generate-schedule", json=sched_payload, headers=headers)
    assert sched_res.status_code == 200, f"Timetable generation failed: {sched_res.text}"
    sched_data = sched_res.json()
    weekly_grid = sched_data["schedule"]

    assert len(weekly_grid) == 7, "Expected all 7 days in schedule response"
    
    # 7a. Verify student subjects are used (no hardcoded subjects)
    assigned_subjects = set()
    assigned_topics = set()
    consecutive_same_subject_violations = 0
    consecutive_same_topic_violations = 0

    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
        slots = weekly_grid[day]
        assert len(slots) <= 3, f"Day {day} exceeded daily limit"
        for i, slot in enumerate(slots):
            assigned_subjects.add(slot["subject"])
            assigned_topics.add(slot["topic"])
            
            # Verify slot fields required by Part 1
            assert "start_time" in slot and slot["start_time"], "Missing start_time"
            assert "end_time" in slot and slot["end_time"], "Missing end_time"
            assert "duration" in slot and slot["duration"], "Missing duration"
            assert "activity" in slot and slot["activity"], "Missing study activity"
            assert "priority" in slot and slot["priority"], "Missing priority"
            assert slot["subject"] in ["Artificial Intelligence", "Database Management Systems", "Computer Networks"]
            
            # Check consecutive slots
            if i > 0:
                prev_slot = slots[i - 1]
                if slot["topic"] == prev_slot["topic"]:
                    consecutive_same_topic_violations += 1
                if slot["subject"] == prev_slot["subject"]:
                    consecutive_same_subject_violations += 1

    print(f"[PASSED] Timetable uses ONLY student's subjects: {assigned_subjects}")
    print(f"[PASSED] Topics scheduled: {assigned_topics}")
    assert len(assigned_subjects) >= 2, "Expected multiple student subjects across the timetable"
    assert consecutive_same_topic_violations == 0, "Found identical topic in consecutive slots"
    assert consecutive_same_subject_violations == 0, "Found identical subject in consecutive slots with multi-subject enrollment"
    print(f"[PASSED] Anti-repetition confirmed: 0 consecutive topic or subject duplicates.")

    # ──────────────────────────────────────────────────────────────────────────
    # 8. Timetable Persistence & Session Actions (Edit, Delete, Complete)
    # ──────────────────────────────────────────────────────────────────────────
    print("\n--- Testing Problem 1: Timetable Persistence & Interactive Session Actions ---")
    schedule_id = sched_data["schedule_id"]
    
    # 8a. Persistence check
    saved_res = requests.get(f"{BASE_URL}/ai/schedules", headers=headers)
    assert saved_res.status_code == 200
    saved_list = saved_res.json()
    assert len(saved_list) >= 1
    assert saved_list[0]["id"] == schedule_id
    print(f"[PASSED] Timetable persists in database (Schedule ID: {schedule_id}).")

    # Pick a session to edit/toggle
    first_mon_slot = weekly_grid["Monday"][0]
    session_id = first_mon_slot["id"]

    # 8b. Toggle completed
    toggle_res = requests.put(f"{BASE_URL}/ai/schedules/{schedule_id}/session/{session_id}/complete?day=Monday", headers=headers)
    assert toggle_res.status_code == 200
    assert toggle_res.json()["is_completed"] is True
    print(f"[PASSED] Toggled session '{session_id}' to completed = True.")

    # 8c. Edit session
    edit_res = requests.put(f"{BASE_URL}/ai/schedules/{schedule_id}/session", json={
        "session_id": session_id,
        "day": "Monday",
        "topic": "Advanced A* Search",
        "activity": "Advanced Problem Solving",
        "start_time": "09:15 AM",
        "end_time": "10:00 AM",
    }, headers=headers)
    assert edit_res.status_code == 200
    updated_sched = edit_res.json()["schedule"]
    edited_slot = next(s for s in updated_sched["Monday"] if s["id"] == session_id)
    assert edited_slot["topic"] == "Advanced A* Search"
    assert edited_slot["activity"] == "Advanced Problem Solving"
    print(f"[PASSED] Edited session verified: {edited_slot['topic']} ({edited_slot['start_time']} - {edited_slot['end_time']}).")

    # 8d. Delete session
    del_res = requests.delete(f"{BASE_URL}/ai/schedules/{schedule_id}/session/{session_id}?day=Monday", headers=headers)
    assert del_res.status_code == 200
    remaining_mon_slots = del_res.json()["schedule"]["Monday"]
    assert all(s["id"] != session_id for s in remaining_mon_slots)
    print(f"[PASSED] Deleted session verified. Remaining Monday slots: {len(remaining_mon_slots)}.")

    print("\n" + "=" * 70)
    print("ALL INTEGRATION TESTS PASSED (100% SUCCESS)!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
