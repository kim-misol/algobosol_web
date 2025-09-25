from __future__ import annotations
import pandas as pd
import streamlit as st

from utils import db
from utils.models import AnalysisUpdate
from utils.prices import price_service

st.set_page_config(page_title="기업분석 목록", page_icon="🗂️", layout="wide")
db.init()

st.title("🗂️ 기업분석 목록")

left, right = st.columns([1, 1])
with left:
    total_portfolio = st.number_input(
        "총 보유 금액(원) — 비중 계산용", min_value=0.0, value=0.0, step=10000.0
    )
with right:
    st.caption("표에서 직접 수정 후 **저장**을 누르면 DB에 반영됩니다.")

rows = db.list_all()
if not rows:
    st.info("등록된 분석이 없습니다. 상단 ‘기업분석 상세’에서 추가하세요.")
    st.stop()


def join_points(lst: list[str]) -> str:
    return " · ".join([x.strip() for x in lst if x.strip()])


data = []
for r in rows:
    cur = price_service.get_current_price(r.name)
    diff = ret = None
    if cur is not None and r.buy_price:
        diff = round(cur - r.buy_price, 2)
        ret = f"{round((diff / r.buy_price) * 100.0, 2)}%"
    weight = ""
    if r.sold:
        weight = "익절"
    elif total_portfolio and r.buy_price and r.qty:
        weight = f"{(r.buy_price * r.qty / total_portfolio) * 100:.2f}%"

    data.append(
        {
            "id": r.id,
            "날짜": r.date,
            "종목": r.name,
            "매수 의견 (익절 +30%)": r.buy_price,
            "투자 포인트": join_points(r.invest_points),
            "현재가": cur,
            "[현재가] [매수가]": (
                f"{cur} / {r.buy_price}" if (cur is not None and r.buy_price) else ""
            ),
            "[현재가 - 매수가]": diff if diff is not None else "",
            "수익률": ret or "",
            "수량": r.qty,
            "매입비중": weight,
            "매도완료": r.sold,
            "상세보기": f"/company_analysis?id={r.id}",
        }
    )

df = pd.DataFrame(data)

display_cols = [
    "날짜",
    "종목",
    "매수 의견 (익절 +30%)",
    "투자 포인트",
    "현재가",
    "[현재가] [매수가]",
    "[현재가 - 매수가]",
    "수익률",
    "수량",
    "매입비중",
    "매도완료",
    "상세보기",
]

edited = st.data_editor(
    df[["id"] + display_cols],
    use_container_width=True,
    num_rows="fixed",
    hide_index=True,
    column_config={
        "id": st.column_config.Column("id", disabled=True),
        "날짜": st.column_config.TextColumn("날짜 (YYYY-MM-DD)"),
        "종목": st.column_config.TextColumn("종목"),
        "매수 의견 (익절 +30%)": st.column_config.NumberColumn(
            "매수 의견 (익절 +30%)", step=10.0
        ),
        "투자 포인트": st.column_config.TextColumn("투자 포인트"),
        "현재가": st.column_config.NumberColumn("현재가", disabled=True),
        "[현재가] [매수가]": st.column_config.TextColumn(
            "[현재가] [매수가]", disabled=True
        ),
        "[현재가 - 매수가]": st.column_config.NumberColumn(
            "[현재가 - 매수가]", disabled=True
        ),
        "수익률": st.column_config.TextColumn("수익률", disabled=True),
        "수량": st.column_config.NumberColumn("수량", step=1.0),
        "매입비중": st.column_config.TextColumn("매입비중", disabled=True),
        "매도완료": st.column_config.CheckboxColumn("매도완료"),
        "상세보기": st.column_config.LinkColumn("상세보기", display_text="열기"),
    },
)

if st.button("💾 저장", type="primary"):
    payload = []
    for _, r in edited.iterrows():
        pts = [
            x.strip()
            for x in str(r["투자 포인트"] or "")
            .replace("·", "\n")
            .replace(",", "\n")
            .split("\n")
            if x.strip()
        ]
        payload.append(
            AnalysisUpdate(
                id=int(r["id"]),
                date=str(r["날짜"]).strip(),
                name=str(r["종목"]).strip(),
                buy_price=(
                    float(r["매수 의견 (익절 +30%)"])
                    if r["매수 의견 (익절 +30%)"] not in (None, "")
                    else None
                ),
                invest_points=pts,
                html="",  # 목록 페이지에서는 변경하지 않음
                pdf_path=None,  # 목록 페이지에서는 변경하지 않음
                qty=(float(r["수량"]) if r["수량"] not in (None, "") else None),
                sold=bool(r["매도완료"]),
            )
        )
    db.bulk_update(payload)
    st.success("저장 완료!")
