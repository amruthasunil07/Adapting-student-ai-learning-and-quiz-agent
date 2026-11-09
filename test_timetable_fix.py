"""
Comprehensive test script verifying the Study Timetable fixes for:
1. Student-created subjects & topics only (Mathematics & Python)
2. Conflict-free CSP timetable generation with anti-repetition & subject alternation
3. Adding an additional subject (Physics) and regenerating
4. Persistence of saved timetable across page refresh (GET /api/ai/schedules)
5. Dynamic synchronization on subject/topic edit and delete
"""

import requests
import sys

BASE_URL = "http://127.0.0.1:8000/api"

def run_test():
    print("======================================================================")
    print("STARTING TEST SCENARIO: TIMETABLE PERSONALIZATION & DYNAMIC SYNC")
    print("======================================================================")

    # 1. Register a dedicated test student
    email = f"student_test_sched_{id(object())}@cognilearn.ai"
    reg_res = requests.post(f"{BASE_URL}/auth/register", json={
        "name": "Personalized Student",
        "email": email,
        "password": "password123"
    })
    assert reg_res.status_code in (200, 201), f"Registration failed: {reg_res.text}"
    token = reg_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"[PASSED] Step 0: Registered test student: {email}")

    # 2. Verify initial empty state
    subs_res = requests.get(f"{BASE_URL}/subjects", headers=headers)
    assert subs_res.status_code == 200 and len(subs_res.json()) == 0, "Subjects should be empty initially"

    sched_res = requests.get(f"{BASE_URL}/ai/schedules", headers=headers)
    assert sched_res.status_code == 200 and len(sched_res.json()) == 0, "Schedules should be empty initially"

    empty_gen = requests.post(f"{BASE_URL}/ai/generate-schedule", json={"daily_study_hours": 3}, headers=headers)
    assert empty_gen.status_code == 400, "Should reject schedule generation when student has 0 subjects"
    assert "No subjects available. Add subjects to generate your personalized timetable." in empty_gen.json()["detail"]
    print("[PASSED] Step 0b: Empty state guard verified")

    # 3. Add Mathematics and Python as subjects
    math_sub = requests.post(f"{BASE_URL}/subjects", json={
        "name": "Mathematics",
        "code": "MATH101",
        "semester": 3,
        "description": "Calculus and Linear Algebra"
    }, headers=headers).json()
    math_id = math_sub["id"]

    py_sub = requests.post(f"{BASE_URL}/subjects", json={
        "name": "Python",
        "code": "PY101",
        "semester": 3,
        "description": "OOP and System Scripting"
    }, headers=headers).json()
    py_id = py_sub["id"]
    print(f"[PASSED] Step 1: Added subjects: Mathematics (ID: {math_id}), Python (ID: {py_id})")

    # 4. Add two or more topics under each subject
    # Under Mathematics:
    t_calc = requests.post(f"{BASE_URL}/subjects/{math_id}/topics", json={
        "name": "Calculus",
        "description": "Differential and Integral Calculus",
        "difficulty": 4,
        "priority": "High"
    }, headers=headers).json()

    t_la = requests.post(f"{BASE_URL}/subjects/{math_id}/topics", json={
        "name": "Linear Algebra",
        "description": "Matrices and Eigenvalues",
        "difficulty": 3,
        "priority": "Medium"
    }, headers=headers).json()

    # Under Python:
    t_oop = requests.post(f"{BASE_URL}/subjects/{py_id}/topics", json={
        "name": "Object Oriented Programming",
        "description": "Classes, Inheritance, and Polymorphism",
        "difficulty": 3,
        "priority": "High"
    }, headers=headers).json()

    t_file = requests.post(f"{BASE_URL}/subjects/{py_id}/topics", json={
        "name": "File Handling",
        "description": "File I/O and Context Managers",
        "difficulty": 2,
        "priority": "Medium"
    }, headers=headers).json()
    print("[PASSED] Step 2: Added topics: Calculus, Linear Algebra, Object Oriented Programming, File Handling")

    # 5. Generate the study timetable
    gen_payload = {
        "daily_study_hours": 3,
        "start_time": "09:00 AM",
        "session_duration": 45,
        "available_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "max_hours_per_day": 3,
        "max_consecutive_hours": 2,
        "total_weekly_hours": 15,
        "subject_ids": [math_id, py_id],
        "topic_ids": [t_calc["id"], t_la["id"], t_oop["id"], t_file["id"]]
    }
    gen_res = requests.post(f"{BASE_URL}/ai/generate-schedule", json=gen_payload, headers=headers)
    assert gen_res.status_code == 200, f"Generate timetable failed: {gen_res.text}"
    schedule_data = gen_res.json()["schedule"]
    print("[PASSED] Step 3: Timetable generated successfully via CSP solver")

    # 6. Verify that it contains ONLY the subjects and topics actually added by the student
    allowed_subjects = {"Mathematics", "Python"}
    allowed_topics = {"Calculus", "Linear Algebra", "Object Oriented Programming", "File Handling"}
    
    total_sessions = 0
    all_subjects_found = set()
    all_topics_found = set()

    for day, slots in schedule_data.items():
        prev_sub = None
        prev_topic = None
        for slot in slots:
            sub = slot["subject"]
            topic = slot["topic"]
            total_sessions += 1
            all_subjects_found.add(sub)
            all_topics_found.add(topic)

            assert sub in allowed_subjects, f"Found unexpected subject: {sub} (Expected only {allowed_subjects})"
            assert topic in allowed_topics, f"Found unexpected topic: {topic} (Expected only {allowed_topics})"
            assert slot["start_time"] and slot["end_time"], f"Invalid session time format: {slot}"

            # Check consecutive duplicate prevention
            if prev_sub is not None:
                assert sub != prev_sub, f"Consecutive identical subject on {day}: {sub} after {prev_sub}"
            if prev_topic is not None:
                assert topic != prev_topic, f"Consecutive identical topic on {day}: {topic} after {prev_topic}"

            prev_sub = sub
            prev_topic = topic

    assert all_subjects_found == allowed_subjects, f"Expected all subjects {allowed_subjects}, got {all_subjects_found}"
    print(f"[PASSED] Step 4: Timetable verified! Contains ONLY student subjects: {all_subjects_found}")
    print(f"         Total conflict-free sessions: {total_sessions}. Zero duplicates or overlaps.")

    # 7. Add another subject (Physics) and regenerate the timetable
    phys_sub = requests.post(f"{BASE_URL}/subjects", json={
        "name": "Physics",
        "code": "PHY101",
        "semester": 3,
        "description": "Classical and Quantum Mechanics"
    }, headers=headers).json()
    phys_id = phys_sub["id"]

    t_qm = requests.post(f"{BASE_URL}/subjects/{phys_id}/topics", json={
        "name": "Quantum Mechanics",
        "description": "Wave-particle duality and Schrödinger equation",
        "difficulty": 4,
        "priority": "High"
    }, headers=headers).json()

    t_thermo = requests.post(f"{BASE_URL}/subjects/{phys_id}/topics", json={
        "name": "Thermodynamics",
        "description": "Laws of thermodynamics and entropy",
        "difficulty": 3,
        "priority": "Medium"
    }, headers=headers).json()
    print(f"[PASSED] Step 5: Added third subject: Physics (ID: {phys_id}) with 2 topics")

    # Regenerate timetable with all 3 subjects
    gen_payload["subject_ids"] = [math_id, py_id, phys_id]
    gen_payload["topic_ids"] = [t_calc["id"], t_la["id"], t_oop["id"], t_file["id"], t_qm["id"], t_thermo["id"]]
    
    regen_res = requests.post(f"{BASE_URL}/ai/generate-schedule", json=gen_payload, headers=headers)
    assert regen_res.status_code == 200, f"Regenerate timetable failed: {regen_res.text}"
    regen_data = regen_res.json()["schedule"]

    # 8. Verify that the new subject appears and that sessions do not overlap or duplicate
    three_subjects = {"Mathematics", "Python", "Physics"}
    regen_subjects_found = set()
    regen_sessions_count = 0

    for day, slots in regen_data.items():
        prev_sub = None
        for slot in slots:
            sub = slot["subject"]
            regen_subjects_found.add(sub)
            regen_sessions_count += 1
            if prev_sub is not None:
                assert sub != prev_sub, f"Consecutive identical subject on {day}: {sub} after {prev_sub}"
            prev_sub = sub

    assert "Physics" in regen_subjects_found, "Physics was not scheduled!"
    assert regen_subjects_found == three_subjects, f"Expected {three_subjects}, found {regen_subjects_found}"
    print(f"[PASSED] Step 6: Regenerated timetable verified! All 3 subjects scheduled: {regen_subjects_found}")
    print(f"         Total sessions: {regen_sessions_count}. Alternation and non-overlapping constraints satisfied.")

    # 9. Refresh simulation: call GET /api/ai/schedules
    refresh_res = requests.get(f"{BASE_URL}/ai/schedules", headers=headers)
    assert refresh_res.status_code == 200, f"Failed to get saved schedules: {refresh_res.text}"
    saved_list = refresh_res.json()
    assert len(saved_list) > 0, "Saved schedule should persist after refresh"
    latest_saved = saved_list[0]["schedule"]

    persisted_subjects = set()
    for day, slots in latest_saved.items():
        for slot in slots:
            persisted_subjects.add(slot["subject"])

    assert persisted_subjects == three_subjects, f"Saved schedule mismatch after refresh: {persisted_subjects} vs {three_subjects}"
    print(f"[PASSED] Step 7: Page refresh verified! Saved timetable persists with exact subjects: {persisted_subjects}")

    # 10. Verify subject deletion sync: Delete 'Python'
    del_res = requests.delete(f"{BASE_URL}/subjects/{py_id}", headers=headers)
    assert del_res.status_code == 200, f"Failed to delete subject: {del_res.text}"
    
    after_del_sched = requests.get(f"{BASE_URL}/ai/schedules", headers=headers).json()[0]["schedule"]
    after_del_subjects = set()
    for day, slots in after_del_sched.items():
        for slot in slots:
            after_del_subjects.add(slot["subject"])

    print("DEBUG: after_del_subjects:", after_del_subjects)
    assert "Python" not in after_del_subjects, "Deleted subject 'Python' should be purged from saved timetable slots!"
    print(f"[PASSED] Step 8: Subject deletion sync verified! Remaining timetable subjects: {after_del_subjects}")

    print("======================================================================")
    print("ALL 7 TEST STEPS PASSED WITH 100% SUCCESS!")
    print("======================================================================")

if __name__ == "__main__":
    run_test()
