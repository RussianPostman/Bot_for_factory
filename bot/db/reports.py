from .base import BaseModel

from sqlalchemy import BigInteger, String, delete, select, update, ForeignKey
from sqlalchemy.orm import sessionmaker, mapped_column, Mapped


class Report(BaseModel):
    """
    Отчёты о авполненной работе
    Аргументы:
        id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
        username: Mapped[str] - имя рабочего
        product: Mapped[str]
        deta: Mapped[str] - дата отправки
        count: Mapped[int] - количество
        prise: Mapped[int] - цена за шт
        salary: Mapped[int] - оклад
        comment: Mapped[str] - комментарий
        amount: Mapped[int] - итоговая сумма
        marriage: Mapped[int] - количество брака
    """
    __tablename__ = 'reports'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str]
    product: Mapped[str]
    deta: Mapped[str]
    count: Mapped[int]
    prise: Mapped[int]
    salary: Mapped[int]
    comment: Mapped[str]
    amount: Mapped[int]
    marriage: Mapped[int]

    def __str__(self) -> int:
        return f'Категория: {self.username}-{self.deta}-{self.deta}'


async def create_report(
        data: dict,
        session_maker: sessionmaker
        ) -> None:
    async with session_maker() as session:
        async with session.begin():
            report = Report(**data)
            session.add(report)