import streamlit as st
import time

# 기본 설정
st.set_page_config(page_title="학생용 공부 도우미", page_icon="📚")

# session_state 초기화
if "planner" not in st.session_state:
    st.session_state.planner = []

if "tasks" not in st.session_state:
    st.session_state.tasks = {}

# 사이드바 페이지 선택
st.sidebar.title("📌 메뉴")
page = st.sidebar.radio(
    "이동할 페이지를 선택하세요",
    ["홈", "오늘의 공부 플래너", "과목별 공부 타이머", "성취 기록"]
)

# ---------------- 홈 ----------------
if page == "홈":
    st.title("📚 학생용 공부 도우미")
    st.write("""
    이 웹사이트는 **학생들이 스스로 공부를 계획하고,  
    시간을 관리하고, 성취를 기록**할 수 있도록 도와줍니다.
    """)

    st.subheader("✨ 주요 기능")
    st.markdown("""
    - 오늘의 공부 계획 작성  
    - 과목별 공부 타이머  
    - 체크리스트로 성취 기록  
    """)

    st.info("왼쪽 메뉴에서 기능을 선택해 주세요!")

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
        "공부할 과목을 선택하세요",
        ["국어", "수학", "영어", "과학", "사회", "기타"]
    )

    minutes = st.number_input(
        "공부 시간 (분)",
        min_value=1,
        max_value=180,
        value=30
    )

    if st.button("공부 시작"):
        st.success(f"{subject} 공부 시작! 집중하세요 💪")
        seconds = minutes * 60

        timer_placeholder = st.empty()

        while seconds > 0:
            mins, secs = divmod(seconds, 60)
            timer_placeholder.info(f"⏳ 남은 시간: {mins:02d}:{secs:02d}")
            time.sleep(1)
            seconds -= 1

        st.balloons()
        st.success("🎉 공부 완료!")

# ---------------- 성취 기록 ----------------
elif page == "성취 기록":
    st.title("✅ 성취 기록 체크리스트")

    task = st.text_input("기록할 공부를 입력하세요")

    if st.button("기록 추가"):
        if task:
            st.session_state.tasks[task] = False

    if not st.session_state.tasks:
        st.write("아직 기록된 공부가 없습니다.")
    else:
        for t in list(st.session_state.tasks.keys()):
            st.session_state.tasks[t] = st.checkbox(
                t, st.session_state.tasks[t]
            )

    completed = sum(st.session_state.tasks.values())
    total = len(st.session_state.tasks)

    if total > 0:
        st.info(f"완료한 공부: {completed} / {total}")
