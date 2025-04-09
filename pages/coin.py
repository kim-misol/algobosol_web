import os
import pyupbit
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # .env 파일의 변수 로드

ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

st.set_page_config(page_title="업비트 | 알고보솔", layout="wide")

if SECRET_KEY and ACCESS_KEY:
    access_key = ACCESS_KEY
    secret_key = SECRET_KEY
else:
    # API 키 입력 영역은 계정 연동이 되지 않았을 때만 표시
    st.markdown("업비트 Open API 키를 입력해주세요.")
    access_key = st.text_input("Access Key", type="password")
    secret_key = st.text_input("Secret Key", type="password")

# 상단 탭 생성 (네비게이션 바 역할)
tabs = st.tabs(["계정 연동", "누적 투자 손익", "거래내역"])

with tabs[0]:
    st.header("업비트 계정 연동")

    if access_key and secret_key:
        try:
            upbit = pyupbit.Upbit(access_key, secret_key)
            balances = upbit.get_balances()

            st.success("✅ 계정 연동 성공!")
            df = pd.DataFrame(balances)
            st.dataframe(df)

        except Exception as e:
            st.error(f"❌ 계정 연동 실패: {str(e)}, 업비트 API 키를 확인해주세요.")


with tabs[1]:
    st.header("누적 투자 손익")

with tabs[2]:
    st.header("거래내역")
