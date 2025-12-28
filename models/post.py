from datetime import datetime, timezone
from factory import db
from pydantic import BaseModel
from utils.models import OrmBase
from models.user import UserResponseSimple

class Post(db.Model):
   __tablename__ = "post"
   id = db.Column(db.Integer, primary_key=True)
   text = db.Column(db.UnicodeText)
   created_at = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc))

   author_id = db.Column(db.Integer, db.ForeignKey("User.id"))

   author = db.relationship("User", back_populates="posts")

   def __repr__(self) -> str:
      return f"<Post {self.id}"
   
class PostCreate(BaseModel):
   text: str

class PostResponse(OrmBase):
   text: str
   created: datetime
   author: UserResponseSimple

class PostResponseList(BaseModel):
   page: int
   pages: int
   total: int
   posts: list[PostResponse]