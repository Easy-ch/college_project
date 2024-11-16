from pydantic import BaseModel,ConfigDict
from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

class User(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: Mapped[int]
    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str]
    
    is_user: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_student: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_teacher: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_super_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)

