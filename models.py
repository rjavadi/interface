from extension import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True, unique=True)
    annotated_videos = db.Column(db.String, default='')
    password = db.Column(db.String)
    culture = db.Column(db.String)
    nationality = db.Column(db.String)
    language = db.Column(db.String)
    individuality = db.Column(db.Integer)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def get_annotated_videos(self):
        return [x for x in self.annotated_videos.split(';')]

    def add_video(self, video_name):
        self.annotated_videos += ';%s' % video_name

    def __repr__(self):
        return '<User {}>'.format(self.username)