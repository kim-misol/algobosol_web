from __future__ import annotations
from uuid import uuid4
import datetime
import streamlit as st

from utils import db
from utils.config import SETTINGS
from utils.models import AnalysisCreate, AnalysisUpdate
from utils.pdf import pdf_iframe_b64

st.set_page_config(page_title="기업분석 상세", page_icon="📝", layout="wide")
db.init()

st.title("📝 기업분석 상세")

qid = st.query_params.get("id")
if isinstance(qid, list):
    qid = qid[0]
row = db.get_one(int(qid)) if qid else None

mode = st.segmented_control(
    "모드", options=["편집", "미리보기"], default="미리보기" if row else "편집"
)

if mode == "편집":
    with st.form("edit_form"):
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            date = st.text_input(
                "날짜 (YYYY-MM-DD)",
                value=row.date if row else datetime.date.today().isoformat(),
            )
        with c2:
            name = st.text_input("종목(제목)", value=row.name if row else "")
        with c3:
            buy_price = st.number_input(
                "매수 의견(매수가)",
                min_value=0.0,
                value=float(row.buy_price) if (row and row.buy_price) else 0.0,
                step=10.0,
            )

        default_points = (
            "\n".join(row.invest_points) if (row and row.invest_points) else ""
        )
        invest_points_text = st.text_area(
            "투자 포인트 (줄바꿈으로 구분)", value=default_points, height=120
        )

        st.markdown("#### 본문 (HTML/WYSIWYG)")
        html_value = row.html if row else ""
        try:
            from streamlit_quill import st_quill

            html_value = (
                st_quill(
                    html=html_value,
                    placeholder="여기에 작성하세요…",
                    key="quill",
                    toolbar=True,
                )
                or html_value
            )
        except Exception:
            html_value = st.text_area("HTML 본문", value=html_value, height=260)

        st.markdown("#### PDF 첨부")
        pdf_file = st.file_uploader("PDF 파일 업로드", type=["pdf"])

        qty = st.number_input(
            "수량(선택, 비중 계산용)",
            min_value=0.0,
            value=float(row.qty) if (row and row.qty) else 0.0,
            step=1.0,
        )
        sold = st.checkbox("매도 완료", value=bool(row.sold) if row else False)

        submitted = st.form_submit_button("💾 저장", type="primary")
        if submitted:
            pdf_path = row.pdf_path if row else None
            if pdf_file is not None:
                fname = f"{uuid4().hex}.pdf"
                dest = SETTINGS.attachments_dir / fname
                dest.write_bytes(pdf_file.read())
                pdf_path = str(dest)

            payload_common = dict(
                date=date.strip(),
                name=name.strip(),
                buy_price=float(buy_price) if buy_price else None,
                invest_points=[
                    x.strip() for x in invest_points_text.split("\n") if x.strip()
                ],
                html=html_value or "",
                pdf_path=pdf_path,
                qty=float(qty) if qty else None,
                sold=bool(sold),
            )

            if row:
                rid = db.upsert(AnalysisUpdate(id=row.id, **payload_common))
            else:
                rid = db.upsert(AnalysisCreate(**payload_common))

            st.query_params.update({"id": str(rid)})
            st.success("저장 완료!")

else:  # 미리보기
    if not row:
        st.info("새 글을 먼저 저장하세요.")
        st.stop()

    left, right = st.columns([1.2, 1])
    with left:
        st.subheader(f"📌 {row.name} / {row.date}")
        if row.invest_points:
            chips = " ".join(
                f"<span style='padding:.25rem .5rem;border:1px solid #ddd;border-radius:999px;margin-right:.35rem;font-size:.85rem'>{p}</span>"
                for p in row.invest_points
            )
            st.markdown(chips, unsafe_allow_html=True)
        st.divider()
        st.markdown(row.html or "_(본문이 없습니다)_", unsafe_allow_html=True)

    with right:
        st.subheader("첨부 PDF 미리보기")
        st.components.v1.html(
            pdf_iframe_b64(row.pdf_path, height=640), height=660, scrolling=True
        )

    st.page_link("pages/03_company_overview.py", label="◀ 목록으로", icon="🗂️")
    st.link_button(
        "편집 모드로", url=f"/pages/02_기업분석_상세.py?id={row.id}", type="secondary"
    )
