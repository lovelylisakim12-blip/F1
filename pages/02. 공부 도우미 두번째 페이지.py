import streamlit as st
import time
import matplotlib.pyplot as plt

# 기본 설정
st.set_page_config(page_title="학생용 공부 도우미", page_icon="📚")

# session_state 초기화
if "planner" not in st.session_state:
    st.session_state.planner = []

if "tasks" not in st.session_state:
    st.session_state.tasks = {}

# ---------------- 사이드바 ----------------
st.sidebar.title("📌 메뉴")
page = st.sidebar.radio(
    "이동할 페이지를 선택하세요",
    ["홈", "결과 한눈에 보기", "오늘의 공부 플래너", "과목별 공부 타이머", "성취 기록"]
)

# ---------------- 홈 ----------------
if page == "홈":
    st.title("📚 학생용 공부 도우미")
    st.write("""
    이 웹사이트는 학생들이  
    **공부 계획 → 실행 → 결과 확인**을 한 번에 할 수 있도록 만든 사이트입니다.
    """)

    st.subheader("✨ 기능 소개")
    st.markdown("""
    - 오늘의 공부 계획 작성  
    - 과목별 공부 타이머  
    - 그래프로 보는 공부 결과  
    - 체크리스트 성취 기록  
    """)

    st.info("왼쪽 메뉴에서 기능을 선택해 주세요!")

# ---------------- 결과 한눈에 보기 (2번째 페이지) ----------------
elif page == "결과 한눈에 보기":
    st.title("📊 오늘의 공부 결과 요약")

    total_plans = len(st.session_state.planner)
    total_tasks = len(st.session_state.tasks)
    completed = sum(st.session_state.tasks.values())
    remaining = total_tasks - completed

    # 숫자 요약
    col1, col2, col3 = st.columns(3)
    col1.metric("📌 계획한 공부", total_plans)
    col2.metric("✅ 완료", completed)
    col3.metric("⏳ 남은 공부", remaining)

    st.divider()

    # 완료 / 미완료 비율
    if total_tasks > 0:
        st.subheader("✅ 공부 완료 비율")

        fig1, ax1 = plt.subplots()
        ax1.pie(
            [completed, remaining],
            labels=["완료", "미완료"],
            autopct="%1.1f%%",
            startangle=90
        )
        ax1.axis("equal")
        st.pyplot(fig1)
    else:
        st.info("아직 성취 기록이 없습니다.")

    st.divider()

    # 과목 분포 그래프
    if total_plans > 0:
        st.subheader("📚 공부 과목 분포")

        subjects = ["국어", "수학", "영어", "과학", "사회", "기타"]
        subject_count = {s: 0 for s in subjects}

        for plan in st.session_state.planner:
            for s in subjects:
                if s in plan:
                    subject_count[s] += 1

        fig2, ax2 = plt.subplots()
        ax2.bar(subject_count.keys(), subject_count.values())
        ax2.set_ylabel("공부 개수")
        ax2.set_xlabel("과목")
        st.pyplot(fig2)
    else:
        st.info("아직 공부 계획이 없습니다.")

# ---------------- 공부 플래너 ----------------
elif page == "오늘의 공부 플래너":
    st.title("📅 오늘의 공부 플래너")

    new_plan = st.text_input("오늘 할 공부를 입력하세요")

    if st.button("추가하기"):
        if new_plan:
            st.session_state.planner.append(new_plan)

    st.subheader("📝 오늘의 할 일")
    if not st.session_state.planner:
        st.write("아직 계획이 없습니다.")
    else:
        for i, plan in enumerate(st.session_state.planner, 1):
            st.write(f"{i}. {plan}")

# ---------------- 공부 타이머 ----------------
elif page == "과목별 공부 타이머":
    st.title("⏱ 과목별 공부 타이머")

    subject = st.selectbox(
        "공부할 과목 선택",
        ["국어", "수학", "영어", "과학", "사회", "기타"]
    )

    minutes = st.number_input("공부 시간 (분)", 1, 180, 30)

    if st.button("공부 시작"):
        st.success(f"{subject} 공부 시작! 💪")
        seconds = minutes * 60
        timer = st.empty()

        while seconds > 0:
            m, s = divmod(seconds, 60)
            timer.info(f"⏳ 남은 시간 {m:02d}:{s:02d}")
            time.sleep(1)
            seconds -= 1

        st.balloons()
        st.success("🎉 공부 완료!")

# ---------------- 성취 기록 ----------------
elif page == "성취 기록":
    st.title("✅ 성취 기록 체크리스트")

    task = st.text_input("기록할 공부 입력")

    if st.button("기록 추가"):
        if task:
            st.session_state.tasks[task] = False

    if not st.session_state.tasks:
        st.write("아직 기록된 공부가 없습니다.")
    else:
        for t in st.session_state.tasks:
            st.session_state.tasks[t] = st.checkbox(
                t, st.session_state.tasks[t]
            )
