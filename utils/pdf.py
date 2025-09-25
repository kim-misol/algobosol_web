from __future__ import annotations
import base64
from pathlib import Path


def pdf_iframe_b64(pdf_path: str | None, height: int = 640) -> str:
    if not pdf_path:
        return "<div style='color:#999'>첨부된 PDF가 없습니다.</div>"
    p = Path(pdf_path)
    if not p.exists():
        return "<div style='color:#999'>PDF 파일을 찾을 수 없습니다.</div>"
    b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
    return f"""
    <iframe src="data:application/pdf;base64,{b64}"
            width="100%" height="{height}"
            style="border:1px solid #e5e5e5;border-radius:10px"></iframe>
    """
