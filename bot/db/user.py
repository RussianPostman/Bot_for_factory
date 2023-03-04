from sqlalchemy import Column, VARCHAR, select, BigInteger
from bot.db.base import BaseModel

from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import selectinload


class User(BaseModel):
    """Класс пользователя"""
    __tablename__ = 'users'

    user_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)
    name = Column(VARCHAR(100), unique=False, nullable=True)
    role = Column(VARCHAR(50), unique=False)

    def __str__(self) -> int:
        return f'User: {self.name} - {self.role}'

    def __repr__(self):
        return self.__str__()


async def get_user(user_id: int, session_maker: sessionmaker) -> User:
    """
    Получить пользователя по его id
    :param user_id:
    :param session_maker:
    :return:
    """
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User).options(
                    selectinload(User.posts)).filter(User.user_id == user_id)
            )
            return result.scalars().one()


async def create_user(
        user_id: int,
        username: str,
        role: str,
        session_maker:
        sessionmaker
        ) -> None:
    async with session_maker() as session:
        async with session.begin():
            user = User(
                user_id=user_id,
                username=username,
                role=role
            )
            try:
                session.add(user)
            except ProgrammingError:
                # TODO: add log
                pass


async def is_user_exists(user_id: int, session_maker: sessionmaker) -> bool:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(
                select(User).where(User.user_id == user_id)
            )
            result = sql_res.first()
            return bool(result)
