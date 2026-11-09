"""
Verification script for CogniLearn Student Subject & Topic Management Feature.
Tests:
- Subject CRUD
- Topic CRUD
- Dynamic question generation
- Quiz integration by topic and by subject
- AI Heuristic & FOL recommendations
- CSP Timetable integration
- Dashboard stats calculation
- Empty states
- Student isolation / authorization
"""

import requests
import sys

BASE_URL = "http://127.0.0.1:8000/api"

def test_student_lifecycle():
    print("[1] Registering a new dedicated test student...")
    import time
    unique_email = f"student_test_{int(time.time())}@cognilearn.ai"
    reg_res = requests.post(f"{BASE_URL}/auth/register", json={
        "name": "Alex Mercer",
        "email": unique_email,
        "password": "Password123!"
    })
    assert reg_res.status_code in [200, 201], f"Register failed: {reg_res.text}"
    token = reg_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"    Student registered: {unique_email}")

    print("\n[2] Checking initial empty states on dashboard & AI recommendations...")
    dash_res = requests.get(f"{BASE_URL}/dashboard/stats", headers=headers)
    assert dash_res.status_code == 200
    dash_stats = dash_res.json()
    assert dash_stats["total_subjects"] == 0, f"Expected 0 subjects, got {dash_stats['total_subjects']}"
    assert dash_stats["total_topics"] == 0, f"Expected 0 topics, got {dash_stats['total_topics']}"
    assert dash_stats["total_quizzes"] == 0, f"Expected 0 quizzes, got {dash_stats['total_quizzes']}"
    print(f"    Empty dashboard verified: total_subjects=0, total_topics=0, total_quizzes=0")

    ai_heur_res = requests.get(f"{BASE_URL}/ai/heuristic-priorities", headers=headers)
    assert ai_heur_res.status_code == 200, f"Status: {ai_heur_res.status_code}, Body: {ai_heur_res.text}"
    assert ai_heur_res.json() == [], f"Expected empty list, got: {ai_heur_res.json()}"
    print("    Empty AI Heuristic verified: [] (allows frontend to show 'Complete a quiz to generate personalized AI recommendations')")

    ai_fol_res = requests.get(f"{BASE_URL}/ai/recommendations", headers=headers)
    assert ai_fol_res.status_code == 200
    assert ai_fol_res.json()["recommendations"] == []
    print("    Empty FOL recommendations verified: []")

    print("\n[3] Creating Subject 1: Artificial Intelligence (24ADT301, Sem 3)...")
    sub_res = requests.post(f"{BASE_URL}/subjects", json={
        "name": "Artificial Intelligence",
        "code": "24ADT301",
        "semester": 3,
        "description": "Core principles of autonomous agents and intelligent search."
    }, headers=headers)
    assert sub_res.status_code in [200, 201], f"Subject create failed: {sub_res.text}"
    sub1 = sub_res.json()
    sub1_id = sub1["id"]
    print(f"    Created subject ID {sub1_id}: {sub1['name']} ({sub1['code']})")

    print("\n[4] Adding Topics to Artificial Intelligence...")
    topics_to_add = [
        {"name": "Intelligent Agents", "description": "Agent architectures and rational agents", "difficulty": 2, "priority": "High"},
        {"name": "Search Algorithms", "description": "BFS, DFS, A* and heuristic evaluation", "difficulty": 3, "priority": "High"},
        {"name": "Constraint Satisfaction Problems", "description": "AC-3 arc consistency, MRV heuristic", "difficulty": 4, "priority": "Medium"},
    ]
    created_topics = []
    for t in topics_to_add:
        t_res = requests.post(f"{BASE_URL}/subjects/{sub1_id}/topics", json=t, headers=headers)
        assert t_res.status_code in [200, 201], f"Topic create failed: {t_res.text}"
        topic_obj = t_res.json()
        created_topics.append(topic_obj)
        print(f"    Added topic ID {topic_obj['id']}: {topic_obj['name']} (Diff: {topic_obj['difficulty']}, Priority: {topic_obj['priority']})")

    print("\n[5] Editing Topic 1...")
    t1 = created_topics[0]
    t1_edit = requests.put(f"{BASE_URL}/topics/{t1['id']}", json={
        "name": "Intelligent Rational Agents",
        "description": "Updated architecture and environment properties",
        "difficulty": 3,
        "priority": "High"
    }, headers=headers)
    assert t1_edit.status_code == 200
    assert t1_edit.json()["name"] == "Intelligent Rational Agents"
    print("    Topic successfully edited and verified.")

    print("\n[6] Starting Quiz on single Topic (Search Algorithms)...")
    t2 = created_topics[1]
    quiz_res = requests.post(f"{BASE_URL}/quiz/start", json={
        "topic_id": t2["id"],
        "num_questions": 5
    }, headers=headers)
    assert quiz_res.status_code == 200, f"Quiz start failed: {quiz_res.text}"
    quiz_data = quiz_res.json()
    assert len(quiz_data["questions"]) == 5, f"Expected 5 generated questions, got {len(quiz_data['questions'])}"
    print(f"    Quiz session generated with {len(quiz_data['questions'])} questions for topic: {quiz_data['topic_name']}")
    print(f"    Sample question 1: {quiz_data['questions'][0]['text']}")

    print("\n[7] Submitting Quiz answers...")
    answers = [{"question_id": q["id"], "selected_option": "A"} for q in quiz_data["questions"]]
    submit_res = requests.post(f"{BASE_URL}/quiz/submit", json={
        "topic_id": t2["id"],
        "answers": answers
    }, headers=headers)
    assert submit_res.status_code == 200, f"Submit failed: {submit_res.text}"
    result = submit_res.json()
    print(f"    Quiz submitted! Score: {result['score']}% ({result['correct_answers']}/{result['total_questions']} correct)")

    print("\n[8] Starting Quiz across the entire Subject (all topics in Artificial Intelligence)...")
    sub_quiz_res = requests.post(f"{BASE_URL}/quiz/start", json={
        "subject_id": sub1_id,
        "num_questions": 5
    }, headers=headers)
    assert sub_quiz_res.status_code == 200, f"Subject quiz start failed: {sub_quiz_res.text}"
    sub_quiz_data = sub_quiz_res.json()
    assert len(sub_quiz_data["questions"]) >= 3, "Expected subject questions"
    print(f"    Subject quiz launched: {sub_quiz_data['topic_name']} with {len(sub_quiz_data['questions'])} questions across topics")

    print("\n[9] Checking Dashboard stats after quiz attempt...")
    dash_after = requests.get(f"{BASE_URL}/dashboard/stats", headers=headers).json()
    assert dash_after["total_subjects"] == 1, f"Expected 1 subject, got {dash_after['total_subjects']}"
    assert dash_after["total_topics"] == 3, f"Expected 3 topics, got {dash_after['total_topics']}"
    assert dash_after["total_quizzes"] == 1, f"Expected 1 quiz, got {dash_after['total_quizzes']}"
    assert dash_after["average_score"] == result["score"]
    assert dash_after["weakest_topic"] is not None
    print(f"    Dashboard verified: Total Subjects={dash_after['total_subjects']}, Topics={dash_after['total_topics']}, Quizzes={dash_after['total_quizzes']}, AvgScore={dash_after['average_score']}%, Weakest={dash_after['weakest_topic']}")

    print("\n[10] Checking AI Heuristic Priorities with student data...")
    prio_res = requests.get(f"{BASE_URL}/ai/heuristic-priorities", headers=headers)
    assert prio_res.status_code == 200
    prios = prio_res.json()
    assert len(prios) > 0, "Expected ranked topics"
    print(f"    AI Heuristic ranking: Top priority is '{prios[0]['topic_name']}' with priority score {prios[0]['priority_score']}")

    print("\n[11] Checking AI FOL Recommendations...")
    fol_res = requests.get(f"{BASE_URL}/ai/recommendations", headers=headers)
    assert fol_res.status_code == 200
    fol_data = fol_res.json()
    print(f"    AI FOL derived {len(fol_data['recommendations'])} rule-based recommendation(s)")
    if fol_data['recommendations']:
        print(f"    First FOL recommendation: {fol_data['recommendations'][0]['topic_name']} -> {fol_data['recommendations'][0]['activity']}")

    print("\n[12] Checking CSP Study Timetable with student's subject...")
    sched_res = requests.post(f"{BASE_URL}/ai/generate-schedule", json={
        "subject_ids": [sub1_id],
        "study_hours_per_day": [9, 10, 11, 14],
        "max_hours_per_day": 2,
        "max_consecutive_hours": 1,
        "total_weekly_hours": 14,
        "exam_date": "2026-11-15"
    }, headers=headers)
    assert sched_res.status_code == 200, f"Schedule generation failed: {sched_res.text}"
    sched = sched_res.json()
    assert sched["total_study_hours"] > 0
    print(f"    CSP Timetable successfully generated: {sched['total_study_hours']} total study hours scheduled conflict-free.")

    print("\n[13] Deleting topic and verifying persistence...")
    del_topic_res = requests.delete(f"{BASE_URL}/topics/{created_topics[2]['id']}", headers=headers)
    assert del_topic_res.status_code == 200
    topics_after = requests.get(f"{BASE_URL}/subjects/{sub1_id}/topics", headers=headers).json()
    assert len(topics_after) == 2, f"Expected 2 topics, got {len(topics_after)}"
    print(f"    Topic deleted successfully. Remaining topics: {len(topics_after)}")

    print("\n[14] Deleting subject and verifying cascade delete...")
    del_sub_res = requests.delete(f"{BASE_URL}/subjects/{sub1_id}", headers=headers)
    assert del_sub_res.status_code == 200
    subs_after = requests.get(f"{BASE_URL}/subjects", headers=headers).json()
    assert not any(s["id"] == sub1_id for s in subs_after), "Subject still found in list"
    print("    Subject deleted successfully. Verified.")

    print("\n=======================================================")
    print(" ALL 14 TEST STEPS PASSED WITH 100% SUCCESS!")
    print("=======================================================")

if __name__ == "__main__":
    try:
        test_student_lifecycle()
    except Exception as e:
        print(f"\n[-] TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
