import matplotlib.pyplot as plt

elif page == "결과 한눈에 보기":
    st.title("📊 오늘의 공부 결과 요약")

    # 데이터 준비
    total_plans = len(st.session_state.planner)
    total_tasks = len(st.session_state.tasks)
    completed_tasks = sum(st.session_state.tasks.values())
    incomplete_tasks = total_tasks - completed_tasks

    # -------- 숫자 요약 --------
    col1, col2, col3 = st.columns(3)
    col1.metric("📌 계획한 공부", total_plans)
    col2.metric("✅ 완료", completed_tasks)
    col3.metric("⏳ 남은 공부", incomplete_tasks)

    st.divider()

    # -------- 완료 / 미완료 파이 차트 --------
    if total_tasks > 0:
        st.subheader("✅ 공부 완료 비율")

        fig1, ax1 = plt.subplots()
        ax1.pie(
            [completed_tasks, incomplete_tasks],
            labels=["완료", "미완료"],
            autopct="%1.1f%%",
            startangle=90
        )
        ax1.axis("equal")
        st.pyplot(fig1)
    else:
        st.info("아직 성취 기록이 없습니다.")

    st.divider()

    # -------- 과목 분포 그래프 (플래너 기반) --------
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
        ax2.set_ylabel("개수")
        ax2.set_xlabel("과목")
        st.pyplot(fig2)
    else:
        st.info("아직 공부 계획이 없습니다.")
      
