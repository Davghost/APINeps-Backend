from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from spectree import SpecTree, SecurityScheme
from config import Config
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()

jwt = JWTManager()
api = SpecTree(
   "flask",
   title="Mini Feed API",
   version="v.1.0",
   path="docs",
   security_schemes=[
      SecurityScheme(
         name="api_key",
         data={"type": "apiKey", "name": "Authorization", "in": "header"},
      )
   ],
   security={"api_key": []},
)

def create_app():
   app = Flask(__name__)

   app.config.from_object(Config)
   jwt.init_app(app)

   db.init_app(app)

   from models import User, Post, Role
   migrate.init_app(app, db)

   @jwt.user_lookup_loader
   def user_load(header, data):
      current_user = db.session.scalars(
         select(User).filter_by(username=data["sub"])
      ).first()
      return current_user

   from controller import user_controller, auth_controller, posts_controller
   app.register_blueprint(user_controller)
   app.register_blueprint(auth_controller)
   app.register_blueprint(posts_controller)

   #api deve ser registrada após registro de todos blueprints
   api.register(app)

   return app