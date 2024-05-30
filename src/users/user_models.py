import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from database import Base

class UserModel(Base):
    __tablename__ = 'user'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, index=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)

