from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()
# engine = db.create_engine(Config.SQLALCHEMY_DATABASE_URI)