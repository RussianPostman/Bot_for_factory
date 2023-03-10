from sqlalchemy import Column, VARCHAR, select, BigInteger, Table, \
    ForeignKey, String, delete
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.engine.result import ScalarResult

from bot.db.base import BaseModel


association_table = Table(
    "association_table",
    BaseModel.metadata,
    Column("user_id", ForeignKey("users.user_id")),
    Column("role_id", ForeignKey("roles.id")),
)


class User(BaseModel):
    """Класс пользователя"""
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(100))
    roles: Mapped[list['Role']] = relationship(
        secondary=association_table, back_populates="users"
    )

    def __str__(self) -> int:
        return f'User: {self.name}'

    def __repr__(self):
        return self.__str__()


class Role(BaseModel):
    """Класс ролей пользователей"""
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column(String(100))
    users: Mapped[list[User]] = relationship(
        secondary=association_table, back_populates="roles"
    )

    def __str__(self) -> int:
        return f'Role: {self.name}'

    def __repr__(self):
        return self.__str__()


async def get_user(user_id: int, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(User).where(User.user_id  == user_id)
            )
            return sql_res.first()


async def get_list_users(session_maker: sessionmaker) -> list[User]:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(User)
            )
            result = sql_res.all()
            print(result)
            return result


async def create_user_admin(
        user_id: int,
        username: str,
        session_maker: sessionmaker
        ) -> None:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(Role).where(Role.name == 'Администратор')
            )
            role = sql_res.first()
            user = User(
                user_id=int(user_id),
                name=username,
            )
            print(type(role))
            user.roles.append(role)
            session.add(user)


async def create_user_worker(
        user_id: int,
        username: str,
        session_maker: sessionmaker
        ) -> None:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(Role).where(Role.name != 'Администратор')
            )
            roles = sql_res.all()
            user = User(
                user_id=user_id,
                name=username,
            )
            for role in roles:
                user.roles.append(role)
            session.add(user)


async def delete_user(
        user_id: int,
        session_maker: sessionmaker
        ):
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(User)
                .options(selectinload(User.roles))
                .where(User.user_id == user_id)
            )
            result: User = sql_res.first()
            result.roles.clear()

    async with session_maker() as session:
        async with session.begin():
            await session.execute(
                delete(User).where(User.user_id == user_id)
            )


async def is_user_exists(user_id: int, session_maker: sessionmaker) -> bool:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(
                select(User).where(User.user_id == user_id)
            )
            result = sql_res.first()
            return bool(result)


async def is_user_admin(user_id: int, session_maker: sessionmaker) -> bool:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(
                select(User)
                .where(
                    (User.user_id == user_id) &
                    (User.roles.any(Role.name == 'Администратор'))
                )
            )
            result = sql_res.first()
            return bool(result)


async def get_user_roles(user_id: int, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(Role.name)
                .where(Role.users.any(User.user_id == user_id))
            )
            return sql_res.all()


async def create_role(
        name: str,
        session_maker: sessionmaker
        ) -> None:
    async with session_maker() as session:
        async with session.begin():
            user = Role(name=name)
            session.add(user)


async def get_roles_list(session_maker: sessionmaker) -> ScalarResult:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.scalars(
                select(Role.name)
            )
            return sql_res.all()
