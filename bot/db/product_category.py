from .base import BaseModel

from sqlalchemy import Column, Integer, VARCHAR, String, select, ForeignKey
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker, relationship, mapped_column, Mapped


class Category(BaseModel):
    """Категории продуктов"""
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    products: Mapped[list["Product"]] = relationship(back_populates="category")

    def __str__(self) -> int:
        return f'Категория: {self.name}'


class Product(BaseModel):
    """Класс продуктов производства"""
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(100))
    turner: Mapped[int]
    caster: Mapped[int]
    miller: Mapped[int]
    packaging: Mapped[int]
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    category: Mapped["Category"] = relationship(back_populates="products")

    def __str__(self) -> int:
        return f'Продукт: {self.name}'


async def create_category(
        name: str,
        session_maker: sessionmaker
        ) -> None:
    async with session_maker() as session:
        async with session.begin():
            user = Category(
                name=name
            )
            session.add(user)
