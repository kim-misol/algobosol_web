import streamlit as st

st.set_page_config(page_title="크레온 | 알고보솔", layout="wide")

# 세부 기능 선택 (서브페이지) - 계정 연결, 누적 투자 손익, 거래내역
sub_page = st.selectbox(
    "세부 기능 선택", ["계정 연결 및 보유 자산 확인", "누적 투자 손익", "거래내역"]
)

if sub_page == "계정 연결 및 보유 자산 확인":
    st.header("계정 연결하기")
    st.info("여기에 계정 연결 로직 및 보유 자산 표시 코드를 추가합니다.")
    # 예시: API 키 입력, 계정 연결 버튼, 보유 자산 테이블 등
elif sub_page == "누적 투자 손익":
    st.header("누적 투자 손익")
    st.info("누적 투자 손익 계산 및 결과 표시 로직을 구현합니다.")
elif sub_page == "거래내역":
    st.header("거래내역")
    st.info("거래내역을 불러와서 표시하는 로직을 구현합니다.")
