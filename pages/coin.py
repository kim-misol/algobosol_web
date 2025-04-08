import streamlit as st

st.set_page_config(page_title="업비트 | 알고보솔", layout="wide")

# 상단 탭 생성 (네비게이션 바 역할)
tabs = st.tabs(["계정 연결", "누적 투자 손익", "거래내역"])

with tabs[0]:
    st.header("계정 연결")
    # 예: 업비트 API를 통해 계정 연결 및 정보 표시 등

with tabs[1]:
    st.header("누적 투자 손익")

with tabs[2]:
    st.header("거래내역")
