from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, BIGINT, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.models.base import Base, TableNameMixin, TimestampMixin
from datetime import date
from sqlalchemy import Date


class User(Base, TableNameMixin, TimestampMixin):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    city: Mapped[str | None] = mapped_column(String(250))
    login_wms: Mapped[str | None] = mapped_column(String(250))
    position: Mapped[str | None] = mapped_column(String(250))
    user_id: Mapped[str] = mapped_column(BIGINT, nullable=False, unique=True)
    sector: Mapped[str | None] = mapped_column(String(250))
    login: Mapped[str | None] = mapped_column(String(250))
    karma: Mapped[int] = mapped_column(Integer, default=0)
    phone: Mapped[str | None] = mapped_column(String(250))

    questions: Mapped[list["Question"]] = relationship("Question", back_populates="user")
    Task: Mapped[list["Task"]] = relationship("Task", back_populates="user")

    def __repr__(self):
        return f"<User id={self.id} name={self.name}>"


class Question(Base, TableNameMixin, TimestampMixin):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(String, nullable=False)
    question_ua: Mapped[str | None] = mapped_column(String)
    answer: Mapped[str | None] = mapped_column(String)
    # TODO: delete create_date
    create_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_city: Mapped[str | None] = mapped_column(String)
    user_sector: Mapped[str | None] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.user_id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="questions")

    def __repr__(self):
        return f"<Question id={self.id} question={self.question}>"


class Task(Base, TableNameMixin, TimestampMixin):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    message_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    chat_id: Mapped[int | None] = mapped_column(BIGINT)
    user_id: Mapped[int | None] = mapped_column(BIGINT, ForeignKey("users.user_id"))
    user_take_id: Mapped[int | None] = mapped_column(BIGINT)
    text: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str | None] = mapped_column(String)
    # TODO: delete create_date
    create_date: Mapped[datetime | None] = mapped_column(DateTime)
    take_date: Mapped[datetime | None] = mapped_column(DateTime)
    finish_date: Mapped[datetime | None] = mapped_column(DateTime)

    user: Mapped["User"] = relationship("User", back_populates="Task")

    def __repr__(self):
        return f"<Task id={self.id} message_id={self.message_id} text={self.text}>"


class PL_question(Base, TableNameMixin, TimestampMixin):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    price_nr: Mapped[str] = mapped_column(String, nullable=False) # Номер (ID) операції з ВМС
    operation_name: Mapped[str] = mapped_column(String, nullable=False) # Назва операції
    operation_type: Mapped[str] = mapped_column(String, nullable=False) # Тип операції
    operation_full_name: Mapped[str] = mapped_column(String, nullable=False) # Повна назва операції
    firm: Mapped[str] = mapped_column(String, nullable=False) # Власник
    answer: Mapped[int] = mapped_column(BIGINT) # Внесена значення (Загальна к-сть операцій)
    answer_with_coef: Mapped[int] = mapped_column(BIGINT, nullable=True) # Значення до якого застосовується коефіцієнт
    coefficient: Mapped[float] = mapped_column(Float(1), default=1.0) # Коефіцієнт (змінено з BIGINT на Float)
    price: Mapped[int] = mapped_column(BIGINT, nullable=True) # Ціна з ВМС
    is_checked: Mapped[bool] = mapped_column(Boolean, default=False) # Чи перевірено менеджером
    user_create: Mapped[str] = mapped_column(String, nullable=False) # Хто створив
    user_update: Mapped[str | None] = mapped_column(String, nullable=True) # Хто змінив
    date: Mapped["date"] = mapped_column(Date, nullable=False) # Дата операції

class PL_price(Base, TableNameMixin, TimestampMixin):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    price_op_name: Mapped[str] = mapped_column(String, nullable=False) # product_name
    price_op_nr: Mapped[str] = mapped_column(String, nullable=False) # info
    price_nr: Mapped[str] = mapped_column(String, nullable=False) # product_nr
    firm: Mapped[str] = mapped_column(String, nullable=False) # firm_nr
    price: Mapped[int] = mapped_column(BIGINT) # info_2
    user_create: Mapped[str] = mapped_column(String, nullable=False) # Береться з ВМС
    user_update: Mapped[str | None] = mapped_column(String, nullable=True) # Береться з ВМС
    date: Mapped["date"] = mapped_column(Date, nullable=False) # Дата останньої зміни ціни
    def __repr__(self):
        return f"<Question id={self.id} question={self.operation_name}>"