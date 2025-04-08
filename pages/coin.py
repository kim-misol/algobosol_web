import streamlit as st

st.set_page_config(page_title="업비트 | 알고보솔", layout="wide")

# API 키 입력 영역은 계정 연동이 되지 않았을 때만 표시
st.markdown("업비트 Open API 키를 입력해주세요.")

access_key = st.text_input("Access Key", type="password")
secret_key = st.text_input("Secret Key", type="password")

# 상단 탭 생성 (네비게이션 바 역할)
tabs = st.tabs(["계정 연동", "누적 투자 손익", "거래내역"])

with tabs[0]:
    st.header("업비트 계정 연동")
    # 예: 업비트 API를 통해 계정 연결 및 정보 표시 등
    import pyupbit
    import pandas as pd

    if access_key and secret_key:
        try:
            upbit = pyupbit.Upbit(access_key, secret_key)
            balances = upbit.get_balances()

            st.success("✅ 계정 연동 성공!")
            df = pd.DataFrame(balances)
            st.dataframe(df)

        except Exception as e:
            st.error(f"❌ 계정 연동 실패: {str(e)}")


with tabs[1]:
    st.header("누적 투자 손익")

with tabs[2]:
    st.header("거래내역")
