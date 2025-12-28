from datetime import datetime, timezone
from factory import db
from pydantic import BaseModel, ConfigDict
from typing import Optional
from utils.models import OrmBase
from werkzeug.security import check_password_hash, generate_password_hash
from models.role import Role, RoleResponse
from sqlalchemy import select

class User(db.Model):
   __tablename__ = "User"

   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(64), unique=True, nullable=False, index=True)
   password_hash = db.Column(db.String(64), index=True)
   email = db.Column(db.String(128), unique=True, nullable=False, index=True)
   birthdate = db.Column(db.DateTime)
   created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

   posts = db.relationship("Post", back_populates="author", lazy="dynamic")

   role_id = db.Column(db.Integer, db.ForeignKey("role.id"))

   role = db.relationship("Role", back_populates="users")

   def __init__(self, **kwargs):
      super(User, self).__init__(**kwargs)
      if self.role is None:
         self.role = db.session.scalars(select(Role).filter_by(name="user")).first()

   def __repr__(self) -> str:
      return f"User {self.username}"

   @property
   def password(self):
      raise AttributeError("Password is not a readable attribute")
   
   @password.setter
   def password(self, password):
      self.password_hash = generate_password_hash(password)

   def verify_password(self, password):
      return check_password_hash(self.password_hash, password)

class UserEdit(BaseModel):
   username: str
   email: str
   birthdate: Optional[datetime]

#esquema para rotas post e put(criar e alterar usuário) respectivamente
class UserCreate(UserEdit):
   password: str

class UserResponse(OrmBase):
   username: str
   email: str
   birthdate: Optional[datetime]
   created_at: datetime
   role: RoleResponse

class UserResponseList(BaseModel):
   users: list[UserResponse]

class UserResponseSimple(OrmBase):
    username: str 