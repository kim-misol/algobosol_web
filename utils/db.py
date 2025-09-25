from __future__ import annotations
from datetime import datetime
from typing import Iterable, List, Optional

from sqlalchemy import (
    JSON,
    Boolean,
    Float,
    Integer,
    String,
    Text,
    create_engine,
    select,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from utils.config import SETTINGS
from utils.models import AnalysisCreate, AnalysisRead, AnalysisUpdate

# Engine/Session (캐시)
_engine = None
_Session = None


def _get_engine():
    global _engine, _Session
    if _engine is None:
        _engine = create_engine(f"sqlite+pysqlite:///{SETTINGS.db_path}", future=True)
        _Session = sessionmaker(_engine, expire_on_commit=False, future=True)
    return _engine, _Session


class Base(DeclarativeBase):
    pass


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[str] = mapped_column(String(10), index=True)  # YYYY-MM-DD
    name: Mapped[str] = mapped_column(String(200), index=True)
    buy_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    invest_points: Mapped[list] = mapped_column(JSON, default=list)  # JSON 배열
    html: Mapped[str] = mapped_column(Text, default="")
    pdf_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    qty: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    sold: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[str] = mapped_column(String(32))
    updated_at: Mapped[str] = mapped_column(String(32))


def init() -> None:
    engine, _ = _get_engine()
    Base.metadata.create_all(engine)


def _now() -> str:
    return datetime.utcnow().isoformat(timespec="seconds")


def to_read(m: Analysis) -> AnalysisRead:
    return AnalysisRead(
        id=m.id,
        date=m.date,
        name=m.name,
        buy_price=m.buy_price,
        invest_points=m.invest_points or [],
        html=m.html,
        pdf_path=m.pdf_path,
        qty=m.qty,
        sold=m.sold,
    )


def upsert(payload: AnalysisCreate | AnalysisUpdate) -> int:
    _, Session = _get_engine()
    with Session.begin() as s:
        if isinstance(payload, AnalysisUpdate):
            m = s.get(Analysis, payload.id)
            if not m:
                raise ValueError("row not found")
        else:
            m = Analysis(created_at=_now(), updated_at=_now())
            s.add(m)

        m.date = payload.date
        m.name = payload.name
        m.buy_price = payload.buy_price
        m.invest_points = payload.invest_points
        m.html = payload.html
        m.pdf_path = payload.pdf_path
        m.qty = payload.qty
        m.sold = payload.sold
        m.updated_at = _now()
        s.flush()
        return m.id


def get_one(id_: int) -> Optional[AnalysisRead]:
    _, Session = _get_engine()
    with Session() as s:
        m = s.get(Analysis, id_)
        return to_read(m) if m else None


def list_all() -> List[AnalysisRead]:
    _, Session = _get_engine()
    with Session() as s:
        rows = s.scalars(
            select(Analysis).order_by(Analysis.date.desc(), Analysis.id.desc())
        ).all()
        return [to_read(m) for m in rows]


def bulk_update(rows: Iterable[AnalysisUpdate]) -> None:
    _, Session = _get_engine()
    with Session.begin() as s:
        for r in rows:
            m = s.get(Analysis, r.id)
            if not m:
                continue
            m.date = r.date
            m.name = r.name
            m.buy_price = r.buy_price
            m.invest_points = r.invest_points
            m.qty = r.qty
            m.sold = r.sold
            m.updated_at = _now()
