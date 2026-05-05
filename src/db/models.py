from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import *

class Base(DeclarativeBase):
    pass

class Player(Base):
    __tablename__ = "Player"
    
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user : Mapped[str] = mapped_column("username", String(25), unique=True)
    hash_password : Mapped[str] = mapped_column("senha_hash")
    elo : Mapped[int] = mapped_column(default=100)
    matches : Mapped[int] = mapped_column("partidas", default=0)

class Queue(Base):
    __tablename__ = "Queue"

    id : Mapped[int] = mapped_column(primary_key=True, autoincrement= True)
    player_id : Mapped[int] = mapped_column(ForeignKey("Player.id"))
    joinedAt : Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    