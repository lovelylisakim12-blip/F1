import streamlit as st

st.title("📊 오늘의 공부 결과 한눈에 보기")

# session_state 안전 처리
planner = st.session_state.get("planner", [])
tasks = st.session_state.get("tasks", {})

total_plans = len(planner)
total_tasks = len(tasks)
completed = sum(tasks.values()) if tasks else 0
remaining = total_tasks - completed

# ---------------- 숫자 요약 ----------------
col1, col2, col3 = st.columns(3)
col1.metric("📌 계획한 공부", total_plans)
col2.metric("✅ 완료", completed)
col3.metric("⏳ 남은 공부", remaining)

st.divider()

# ---------------- 완료율 ----------------
st.subheader("✅ 공부 완료율")

if total_tasks > 0:
    completion_rate = int((completed / total_tasks) * 100)
    st.progress(completion_rate)
    st.write(f"**달성률: {completion_rate}%**")
else:
    st.info("아직 성취 기록이 없습니다.")

st.divider()

# ---------------- 과목 분포 ----------------
st.subheader("📚 공부 과목 분포")

subjects = ["국어", "수학", "영어", "과학", "사회", "기타"]
subject_count = {s: 0 for s in subjects}

for plan in planner:
    for s in subjects:
        if s in plan:
            subject_count[s] += 1

if sum(subject_count.values()) > 0:
    st.bar_chart(subject_count)
else:
    st.info("아직 공부 계획이 없습니다.")
