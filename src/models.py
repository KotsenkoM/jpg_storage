from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Picture(Base):
    """Модель для изображений"""

    __tablename__ = 'pictures'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(256), unique=True)
    size: Mapped[int]

    def __repr__(self) -> str:
        """Название изображения"""

        return f'Picture | {self.name}'


UniqueConstraint('name', name='unique_name_constraint')
