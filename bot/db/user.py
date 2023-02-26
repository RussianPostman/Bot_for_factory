from sqlalchemy import Column, Integer, VARCHAR
from .base import BaseModel


class User(BaseModel):
    """Класс пользователя"""
    __tablename__ = 'users'

    user_id = Column(Integer, unique=True, nullable=False, primary_key=True)

    name = Column(VARCHAR(100), unique=False, nullable=True)

    role = Column(VARCHAR(50), unique=False)


def __str__(self) -> int:
    return f'User: {self.name} - {self.role}'
