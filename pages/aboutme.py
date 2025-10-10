import streamlit as st
from datetime import date
import pandas as pd
import plotly.express as px

# ----------------------------
# 기본 설정
# ----------------------------
st.set_page_config(
    page_title="지원서 요약 | 김미솔",
    page_icon="🧑🏻‍💻",
    layout="wide",
)

# 상단 탭 생성 (네비게이션 바 역할)
tab_1, tab_2, tab_3 = "이력서", "경력 기술서", "현재 진행 중인 프로젝트"
tabs = st.tabs([tab_1, tab_2, tab_3])

with tabs[0]:
    st.header(tab_1)

with tabs[1]:
    st.header(tab_2)

with tabs[2]:
    st.header(tab_3)


# ----------------------------
# utils
# ----------------------------
def ym_duration(d1: date, d2: date):
    """기간을 'X년 Y개월'로 표기"""
    months = (d2.year - d1.year) * 12 + (d2.month - d1.month)
    years, months = divmod(months + (1 if d2.day >= d1.day else 0), 12)
    return f"{years}년 {months}개월"


def chip(text: str):
    return f"""<span class="chip">{text}</span>"""


def kv(key: str, val: str):
    return f"""
        <div class="kv">
            <div class="k">{key}</div>
            <div class="v">{val}</div>
        </div>
    """


# ----------------------------
# style
# ----------------------------
st.markdown(
    """
<style>
:root{
  --bg:#0e1117; --card:#161a22; --muted:#9aa4b2; --line:#232935; --acc:#3b82f6;
}
* { box-sizing: border-box; }
.block-container { padding-top: 1.2rem; }
h1,h2,h3 { margin: 0 0 .6rem 0; }
.small { color: var(--muted); font-size: .9rem; }
.row { display: grid; grid-template-columns: 1fr 1fr; gap: .9rem; }
.card {
  background: var(--card); border: 1px solid var(--line);
  border-radius: 14px; padding: 16px; margin-bottom: 12px;
}
.header {
  display: grid; grid-template-columns: 104px 1fr; gap: 16px; align-items: center;
  border-bottom: 1px solid var(--line); padding-bottom: 14px; margin-bottom: 10px;
}
.avatar { width: 104px; height: 104px; border-radius: 12px; object-fit: cover; }
.title { font-size: 1.35rem; font-weight: 700; }
.pills { display:flex; flex-wrap: wrap; gap: 6px; margin-top: 6px; }
.chip {
  display:inline-flex; align-items:center; gap:6px;
  padding: 4px 10px; border:1px solid var(--line); border-radius: 999px;
  background: rgba(255,255,255,.02); font-size:.85rem;
}
.kv { display:grid; grid-template-columns: 140px 1fr; gap: 8px; padding: 6px 0; }
.kv .k { color: var(--muted); }
.kv + .kv { border-top: 1px dashed var(--line); }
.grid-3 { display:grid; grid-template-columns: repeat(3,1fr); gap: 12px; }
.badge { padding:.15rem .5rem; border:1px solid var(--line); border-radius:6px; font-size:.8rem; color:var(--muted); }
.section h3 { font-size:1.05rem; margin-bottom:.4rem; }
hr.sep { border:none; border-top:1px solid var(--line); margin: 8px 0 4px; }
ul.clean { margin:.2rem 0 .2rem 1.1rem; }
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# data
# ----------------------------
profile = {
    "name_kr": "김미솔",
    "name_en": "Misol Kim",
    "birth": "1994.10.30 (만 30세)",
    "email": "misolkim94@gmail.com",
    "phone": "010-2381-0990",
    "apply_track": "경력 - 소프트웨어개발",
    "last_edu": (
        "Murdoch University (학사, Computer Science & Business Information System)"
    ),
    "total_exp_years": "5년",
    "desired_rank": "대리",
    "desired_pay": "5,500만원",
    "region": "서울",
    "address": "서울 강남구 남부순환로381길 25 울트라멤버스아파트 203호 (06274)",
    "hobby": "달리기",
    "skill": "영상편집",
    "empty_str": " ",
}

# timeline barchart data
timeline_rows = [
    # education
    dict(
        name="언남고등학교", start=date(2010, 3, 2), end=date(2013, 2, 28), cat="교육"
    ),
    dict(
        name="Murdoch University",
        start=date(2015, 10, 5),
        end=date(2018, 9, 7),
        cat="교육",
    ),
    # career
    dict(
        name="SAGE9 PTE LTD", start=date(2019, 1, 1), end=date(2020, 1, 1), cat="경력"
    ),
    dict(
        name="타임퍼센트",
        start=date(2020, 5, 25),
        end=date(2024, 3, 31),
        cat="경력",
    ),
    # overseas
    dict(
        name="싱가포르 (해외거주)",
        start=date(2015, 5, 18),
        end=date(2019, 12, 29),
        cat="해외경험",
    ),
]

languages = [
    ("영어", "회화 (상)"),
    ("중국어", "회화 (하)"),
]

education = [
    dict(
        school="Murdoch University (싱가폴) | 학사",
        period="2015.10.05 – 2018.09.07",
        major="Computer Science(주전공), Business Information System(복수전공)",
        gpa="학업성적 1.55 / 4.0점",
        courses=[
            "IT Professional Practice Project (3학점) – 82/100",
            "Advanced Business Analysis and Design (3학점) – 74/100",
            "Operating Systems and Systems Programming (3학점) – 66/100",
            "Business Intelligence Application Development (3학점) – Pass",
        ],
    ),
    dict(
        school="언남고등학교 (서울) | 졸업",
        period="2010.03.02 – 2013.02.28",
        major="인문계열",
        notes="",
    ),
]

careers = [
    dict(
        company="타임퍼센트",
        type="정규직",
        period="2020.05.25 – 2024.03.31 | 퇴사",
        summary="데이터/로보어드바이저/웹 서비스 개발 및 최적화",
    ),
    dict(
        company="SAGE9 PTE LTD",
        type="정규직",
        period="2018.11.01 – 2019.12.31 | 퇴사",
        summary="기업 웹사이트, ERP 시스템, 전자상거래 시스템 개발",
    ),
]

overseas = dict(
    title="싱가포르 (해외거주)", period="2015.05.18 – 2019.12.29", days=1687
)

# ----------------------------
# header
# ----------------------------
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    left, right = st.columns([1, 4], vertical_alignment="center")
    with left:
        st.image(
            "attachments/profile.png",
            caption=None,
            use_container_width=True,
        )
    with right:
        st.markdown(
            f"""
        <div class="title">{profile['name_kr']} <span class="small">({profile['name_en']})</span></div>
        <div class="small">생년월일 {profile['birth']}</div>
        <div class="pills">
            {chip('최종학력 ' + profile['last_edu'])}
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div class='pills' style='margin-top:6px'>"
            + chip("지원트랙 " + profile["apply_track"])
            + chip("총 경력 " + profile["total_exp_years"])
            + "</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='pills' style='margin-top:6px'>"
            + chip("Email: " + profile["email"])
            # + chip("휴대폰: " + profile["phone"])
            + "</div>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# timeline
# ----------------------------
with st.container():
    st.markdown('<div class="card section">', unsafe_allow_html=True)
    st.markdown("### 📈 타임라인")
    df = pd.DataFrame(timeline_rows)
    fig = px.timeline(
        df,
        x_start="start",
        x_end="end",
        y="cat",
        color="cat",
        text="name",
        hover_data={"name": True, "start": True, "end": True, "cat": False},
    )
    fig.update_yaxes(autorange="reversed")
    fig.update_traces(
        textposition="inside", insidetextanchor="middle", cliponaxis=False
    )
    fig.update_layout(height=300, margin=dict(l=0, r=0, t=20, b=10), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# 기본정보 / 입사정보 / 지원정보
# ----------------------------
c1, c2 = st.columns(2)
with c1:
    st.markdown('<div class="card section">', unsafe_allow_html=True)
    st.markdown("### 🧾 기본정보")
    st.markdown(
        kv("한글성명", profile["name_kr"])
        + kv("영문이름", profile["name_en"])
        + kv("생년월일", profile["birth"])
        + kv("Email", profile["email"]),
        # + kv("휴대폰", profile["phone"]),
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card section">', unsafe_allow_html=True)
    st.markdown("### 🏠 인적사항")
    st.markdown(
        kv("주소", profile["address"])
        + kv("취미", profile["hobby"])
        + kv("특기", profile["skill"]),
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card section">', unsafe_allow_html=True)
    st.markdown("### 💼 입사정보")
    st.markdown(
        kv("희망연봉", profile["desired_pay"])
        + kv("희망직위", profile["desired_rank"])
        + kv("입사 시 근무 가능 지역", profile["region"]),
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card section">', unsafe_allow_html=True)
    st.markdown("### 🪖 병역/취업우대")
    st.markdown(
        kv("보훈여부", "비대상") + kv("병역", "비대상") + kv("제대구분", "비대상"),
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# 경력 / 어학 / 해외경험
# ----------------------------
c3, c4 = st.columns(2)
with c3:
    st.markdown('<div class="card section">', unsafe_allow_html=True)
    st.markdown("### 🧑🏻‍💻 경력사항")
    for i, c in enumerate(careers, 1):
        st.markdown(
            f"**[{i}] {c['company']}** · {c['type']}  \n{c['period']}  \n{c['summary']}"
        )
        if i < len(careers):
            st.markdown("<hr class='sep'/>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c4:
    st.markdown('<div class="card section">', unsafe_allow_html=True)
    st.markdown("### 🌐 외국어활용능력")
    for lang, level in languages:
        st.markdown(f"- **{lang}** · {level}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card section">', unsafe_allow_html=True)
    st.markdown("### ✈️ 해외경험")
    st.markdown(
        f"**{overseas['title']}**  \n{overseas['period']} · 총 **{overseas['days']}일**"
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# 학력
# ----------------------------
st.markdown('<div class="card section">', unsafe_allow_html=True)
st.markdown("### 🎓 학력사항")
for edu in education:
    st.markdown(f"**{edu['school']}**  \n{edu['period']}  \n{edu['major']}")
    if "gpa" in edu and edu["gpa"]:
        st.markdown(f"- {edu['gpa']}")
    if "courses" in edu and edu["courses"]:
        with st.expander("주요 과목별 학점"):
            for c in edu["courses"]:
                st.markdown(f"- {c}")
    st.markdown("<hr class='sep'/>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# 원본 스크린샷 (참고)
# ----------------------------
# with st.expander("원본 스크린샷 미리보기"):
#     st.image(
#         "/mnt/data/스크린샷 2025-10-06 오후 10.08.00.png", use_container_width=True
#     )
#     st.image(
#         "/mnt/data/스크린샷 2025-10-06 오후 10.08.43.png", use_container_width=True
#     )
#     st.image(
#         "/mnt/data/스크린샷 2025-10-06 오후 10.09.02.png", use_container_width=True
#     )

# ----------------------------
# 푸터
# ----------------------------
st.caption("© 2025 Resume Preview • Streamlit")
