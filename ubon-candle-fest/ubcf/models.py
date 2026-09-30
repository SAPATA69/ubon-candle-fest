from typing import List
from flask_login import UserMixin
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ubcf import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class Role(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    users: Mapped[List["User"]] = relationship(back_populates="role")

    def __repr__(self):
        return f"<Role: {self.name}>"


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        String(25), unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    # แก้ไข ForeignKey ให้ใช้ String ชี้ไปที่ 'role.id'
    role_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("role.id"), default=2
    )

    candles: Mapped[List["Candle"]] = relationship(back_populates="user")
    role: Mapped[Role] = relationship(back_populates="users")

    def __repr__(self):
        return f"<User: {self.username}>"


class Temple(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    candles: Mapped[List["Candle"]] = relationship(back_populates="temple")

    def __repr__(self):
        return f"<Temple: {self.name}>"


class Candle(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    temple_id: Mapped[int] = mapped_column(Integer, ForeignKey("temple.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

    user: Mapped[User] = relationship(back_populates="candles")
    temple: Mapped[Temple] = relationship(back_populates="candles")

    def __repr__(self):
        return f"<Candle: {self.name}>"