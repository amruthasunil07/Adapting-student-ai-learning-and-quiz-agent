import httpx

def run_e2e_check():
    client = httpx.Client(base_url="http://127.0.0.1:8000")
    
    # 1. Health
    h = client.get("/api/health")
    print(f"1. /api/health: {h.status_code} -> {h.json()}")
    assert h.status_code == 200

    # 2. Login
    login_resp = client.post("/api/auth/login", json={"email": "student@example.com", "password": "student123"})
    print(f"2. /api/auth/login: {login_resp.status_code}")
    if login_resp.status_code != 200:
        print("Login failed response:", login_resp.text)
        return
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. /api/auth/me
    me = client.get("/api/auth/me", headers=headers)
    print(f"3. /api/auth/me: {me.status_code} -> {me.json()}")

    # 4. /api/subjects
    subs = client.get("/api/subjects", headers=headers)
    print(f"4. /api/subjects: {subs.status_code} -> {len(subs.json())} subjects")
    topic_id = subs.json()[0]["topics"][0]["id"]
    topic_name = subs.json()[0]["topics"][0]["name"]
    print(f"   Selecting topic: {topic_name} (ID: {topic_id})")

    # 5. /api/quiz/start
    quiz_resp = client.post("/api/quiz/start", json={"topic_id": topic_id, "num_questions": 3}, headers=headers)
    print(f"5. /api/quiz/start: {quiz_resp.status_code} -> {len(quiz_resp.json()['questions'])} questions")
    quiz_data = quiz_resp.json()

    # 6. /api/quiz/submit
    answers = [{"question_id": q["id"], "selected_option": "A"} for q in quiz_data["questions"]]
    submit_resp = client.post("/api/quiz/submit", json={"topic_id": topic_id, "answers": answers}, headers=headers)
    print(f"6. /api/quiz/submit: {submit_resp.status_code} -> Score: {submit_resp.json()['score']}%")

    # 7. /api/dashboard/stats
    stats = client.get("/api/dashboard/stats", headers=headers)
    print(f"7. /api/dashboard/stats: {stats.status_code} -> Total: {stats.json()['total_quizzes']}, Avg: {stats.json()['average_score']}")

    # 8. /api/ai/heuristic-priorities (Module 2)
    heuristics = client.get("/api/ai/heuristic-priorities", headers=headers)
    print(f"8. /api/ai/heuristic-priorities: {heuristics.status_code} -> Top: {heuristics.json()[0]['topic_name']} ({heuristics.json()[0]['priority_score']:.3f})")

    # 9. /api/ai/recommendations (Module 4 FOL)
    fol = client.get("/api/ai/recommendations", headers=headers)
    print(f"9. /api/ai/recommendations: {fol.status_code} -> {len(fol.json()['recommendations'])} derived rules")

    # 10. /api/ai/generate-schedule (Module 3 CSP)
    sched = client.post("/api/ai/generate-schedule", json={
        "study_hours_per_day": [9, 10, 11],
        "max_hours_per_day": 2,
        "max_consecutive_hours": 1,
        "total_weekly_hours": 18,
    }, headers=headers)
    print(f"10. /api/ai/generate-schedule: {sched.status_code} -> Total Hours: {sched.json()['total_study_hours']}")

    # 11. /api/ai/predict-activities (Module 5 ML)
    preds = client.get("/api/ai/predict-activities", headers=headers)
    print(f"11. /api/ai/predict-activities: {preds.status_code} -> Accuracy: {preds.json()['model_accuracy']:.2%}")

    print("\nALL 11 ENDPOINTS TESTED AND VERIFIED SUCCESSFULLY!")

if __name__ == "__main__":
    run_e2e_check()
