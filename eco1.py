import streamlit as st
from datetime import date
import pandas as pd
import altair as alt

st.title("에코루틴 🌱")
st.write("성수고를 위한 친환경 루틴 관리 앱")

# 날짜
today = date.today()

# 루틴 저장용 세션 상태
if "routine_list" not in st.session_state:
    st.session_state.routine_list = []

# ✅ 추천 루틴 리스트
recommended_routines = [
    "텀블러 사용하기",
    "분리수거 제대로 하기",
    "잔반 남기지 않기",
    "대중교통 이용하기",
    "불필요한 플러그 뽑기"
]

st.subheader("🌿 오늘 실천한 친환경 루틴을 체크해보세요!")

# 체크박스 → 루틴 저장
for routine in recommended_routines:
    checked = st.checkbox(routine, key=routine)
    # 이미 저장 안 되어 있고, 체크됐으면 저장
    if checked and (today, routine) not in st.session_state.routine_list:
        st.session_state.routine_list.append((today, routine))
        st.success(f"🎉 '{routine}' 실천 완료!")
        st.image("https://cdn-icons-png.flaticon.com/512/427/427735.png", width=200)

# ✅ 오늘의 루틴 표시
st.subheader(f"📅 {today}의 루틴 기록")
has_today = False
for d, r in st.session_state.routine_list:
    if d == today:
        st.write(f"✅ {r}")
        has_today = True
if not has_today:
    st.write("아직 체크한 루틴이 없어요!")

# ✅ 루틴 실천 그래프
st.subheader("📊 나의 실천 그래프")
if st.session_state.routine_list:
    df = pd.DataFrame(st.session_state.routine_list, columns=["날짜", "루틴"])
    count_by_day = df.groupby("날짜").count().reset_index()
    count_by_day.columns = ["날짜", "루틴 수"]
    chart = alt.Chart(count_by_day).mark_bar().encode(
        x="날짜:T",
        y="루틴 수:Q",
        tooltip=["날짜:T", "루틴 수:Q"]
    ).properties(width=600, height=400)
    st.altair_chart(chart)
else:
    st.info("아직 실천 기록이 없어요. 먼저 루틴을 완료해보세요!")


from datetime import datetime, timedelta

# 날짜만 뽑아서 정렬된 set으로 저장
dates = sorted({d for d, _ in st.session_state.routine_list})
continuous_days = 1 if dates else 0

# 연속 날짜 계산
for i in range(len(dates) - 1, 0, -1):
    today = dates[i]
    yesterday = dates[i - 1]
    if (today - yesterday).days == 1:
        continuous_days += 1
    else:
        break  # 연속 아님 → 중단

# 보상 출력
st.subheader("🔥 연속 실천 기록")
if continuous_days >= 3:
    st.success(f"🎉 {continuous_days}일 연속 실천 중입니다! 대단해요 🌟")
    st.balloons()  # 풍선 효과
    if continuous_days >= 7:
        st.info("🏆 칭호: 환경 영웅")
    elif continuous_days >= 5:
        st.info("🥈 칭호: 초록 수호자")
    else:
        st.info("🌱 칭호: 작은 실천가")
elif continuous_days == 2:
    st.info("내일도 하면 3일 연속! 힘내요 💪")
elif continuous_days == 1:
    st.write("오늘부터 실천 시작! 내일 또 도전해요 💚")
else:
    st.write("아직 실천 기록이 없어요. 첫 걸음을 시작해볼까요?")


st.subheader("📚 환경 지식 카드 게시판")


# 게시글 저장 리스트 초기화
if "eco_posts" not in st.session_state:
    st.session_state.eco_posts = [
        {"title": "성수고 급식 잔반은 어디로 갈까?", "content": "예시 환경 카드입니다."},
        {"title": "분리수거 꿀팁", "content": "종이팩과 일반 종이는 분리해서 버려야 해요! 특히 테이프, 스테이플러는 제거해주세요."}
    ]

# 글 입력
with st.expander("➕ 지식 카드 새로 등록하기"):
    new_title = st.text_input("제목", key="post_title")
    new_content = st.text_area("내용", key="post_content")
    if st.button("게시하기"):
        if new_title and new_content:
            st.session_state.eco_posts.insert(0, {"title": new_title, "content": new_content})
            st.success("게시글이 등록되었어요!")
        else:
            st.warning("제목과 내용을 모두 입력해 주세요!")

# 카드 형식으로 게시글 보여주기
for post in st.session_state.eco_posts:
    with st.expander("📌 " + post["title"]):
        st.write(post["content"])
st.subheader("👥 친구 루틴 기능")


# 사용자 이름 설정
if "my_name" not in st.session_state:
    st.session_state.my_name = ""

st.session_state.my_name = st.text_input("내 이름 (닉네임)", value=st.session_state.my_name)

# 사용자별 루틴 저장 구조 초기화
if "user_routines" not in st.session_state:
    st.session_state.user_routines = {}

# 현재 사용자 루틴 등록
if st.session_state.my_name:
    if st.session_state.my_name not in st.session_state.user_routines:
        st.session_state.user_routines[st.session_state.my_name] = st.session_state.routine_list
    else:
        st.session_state.user_routines[st.session_state.my_name] = st.session_state.routine_list

# 친구 목록 초기화
if "friend_list" not in st.session_state:
    st.session_state.friend_list = []

# 친구 추가
friend_name = st.text_input("친구 이름 입력 (닉네임)")
if st.button("➕ 친구 추가"):
    if friend_name and friend_name not in st.session_state.friend_list:
        st.session_state.friend_list.append(friend_name)
        st.success(f"{friend_name}님을 친구로 추가했어요!")
    elif friend_name in st.session_state.friend_list:
        st.info(f"{friend_name}님은 이미 친구예요.")

# 친구 루틴 보기
if st.session_state.friend_list:
    st.subheader("👀 친구의 루틴 보기")
    for friend in st.session_state.friend_list:
        st.markdown(f"**{friend}님의 루틴 목록**")
        routines = st.session_state.user_routines.get(friend, [])
        today_routines = [r for d, r in routines if d == today]
        if today_routines:
            for r in today_routines:
                st.write(f"✅ {r}")
                if st.button(f"따라하기: {r}", key=f"{friend}_{r}"):
                    if (today, r) not in st.session_state.routine_list:
                        st.session_state.routine_list.append((today, r))
                        st.success(f"{r} 따라하기 완료!")
        else:
            st.write("오늘 실천한 루틴이 아직 없어요.")
