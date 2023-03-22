from .base import BaseModel

from sqlalchemy import String, delete, select, update, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, mapped_column, Mapped,\
    selectinload


class Category(BaseModel):
    """
    Категории продуктов
    args:
        name: Mapped[str]
        products: Mapped[list["Product"]]
    """
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    products: Mapped[list["Product"]] = relationship(back_populates="category")

    def __str__(self) -> int:
        return f'Категория: {self.name}'


class Product(BaseModel):
    """
    Класс продуктов производства
    args:
        name: Mapped[str] = mapped_column(String(100))
        turner: Mapped[int]
        caster: Mapped[int]
        miller: Mapped[int]
        packaging: Mapped[int]
        category: Mapped["Category"] = relationship(back_populates="products")
    """
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(60))
    turner: Mapped[float]
    caster: Mapped[float]
    miller: Mapped[float]
    packaging: Mapped[float]
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    category: Mapped["Category"] = relationship(back_populates="products")

    def __str__(self) -> int:
        return f'Продукт: {self.name}'


async def get_сategory_list(
        session_maker: sessionmaker
        ) -> list[Category.name]:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(Category.name)
            )
            return sql_res.all()


async def create_category(
        name: str,
        session_maker: sessionmaker
        ) -> None:
    async with session_maker() as session:
        async with session.begin():
            category = Category(
                name=name
            )
            session.add(category)


async def get_product(
        session_maker: sessionmaker,
        cat_name: str,
        prod_name: str
        ) -> Product:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(Product)
                .where(
                    (Product.category.has(Category.name == cat_name)) &
                    (Product.name == prod_name)
                )
            )
            return sql_res.first()


async def get_products_list(
        session_maker: sessionmaker,
        cat_name: str
        ) -> list[Product]:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(Product)
                .where(Product.category.has(Category.name == cat_name))
            )
            return sql_res.all()


async def get_products_names_list(
        session_maker: sessionmaker,
        cat_name: str
        ) -> list[Product.name]:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(Product.name)
                .where(Product.category.has(Category.name == cat_name))
            )
            return sql_res.all()


async def create_product(
        product_data: list[str],
        cat_name: str,
        session_maker: sessionmaker
        ) -> None:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(Category)
                .options(selectinload(Category.products))
                .where(Category.name == cat_name)
            )
            category: Category = sql_res.first()
            product = Product(
                name=product_data[0],
                turner=float(product_data[1]),
                caster=float(product_data[2]),
                miller=float(product_data[3]),
                packaging=float(product_data[4])
            )
            category.products.append(product)
            session.add(product)
            session.add(category)


async def update_product(
        product_data: list[str],
        cat_name: str,
        session_maker: sessionmaker
        ) -> None:
    async with session_maker() as session:
        async with session.begin():
            await session.execute(
                update(Product)
                .where((Product.category.has(Category.name == cat_name)) &
                       (Product.name == product_data[0]))
                .values(
                    name=product_data[0],
                    turner=float(product_data[1]),
                    caster=float(product_data[2]),
                    miller=float(product_data[3]),
                    packaging=float(product_data[4])
                )
            )
            print('удалили продукт ' + product_data[0])


async def delete_product(
        product_data: list[str],
        cat_name: str,
        session_maker: sessionmaker
        ) -> None:
    async with session_maker() as session:
        async with session.begin():
            await session.execute(
                delete(Product)
                .where((Product.category.has(Category.name == cat_name)) &
                       (Product.name == product_data[0]))
            )
            print('удалили продукт ' + product_data[0])
