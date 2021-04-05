from extension import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String, index=True, unique=True)
    annotated_videos = db.Column(db.String)
    password = db.Column(db.String)
    culture = db.Column(db.String)
    language = db.Column(db.String)
    individuality = db.Column(db.Integer)
    withdraw = db.Column(db.Boolean, default=False)
    gift_codes = db.Column(db.String)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        entered_password = generate_password_hash(
            password,
            method='sha256'
        )
        print('entered_password: ', entered_password)
        return check_password_hash(self.password, password)

    def get_annotated_videos(self):
        if self.annotated_videos is not None:
            return [x for x in self.annotated_videos.split(';')]
        return []

    def add_video(self, video_name):
        if self.annotated_videos in [None, '']:
            self.annotated_videos = video_name
        else:
            self.annotated_videos += ';%s' % video_name


    #TODO: the size shouldn't be more than 4
    def add_gift_code(self, code):
        if self.gift_codes in [None, '']:
            self.gift_codes = code
        else:
            self.gift_codes += ';%s' % code

    def add_gift_codes(self, gift_card_list):
        for c in gift_card_list:
            self.add_gift_code(c.code)

    def get_gift_codes(self):
        if self.gift_codes is not None:
            return [x for x in self.gift_codes.split(';')]
        return []

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Annotation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    filename = db.Column(db.String, nullable=False)
    video_culture = db.Column(db.String)
    emotion = db.Column(db.String)
    gender = db.Column(db.String)
    confidence = db.Column(db.Integer)
    anger_score = db.Column(db.Integer)
    contempt_score = db.Column(db.Integer)
    disgust_score = db.Column(db.Integer)
    annoyed_score = db.Column(db.Integer)
    social_signals = db.Column(db.String, default='')
    annotator_culture = db.Column(db.String)
    annotator_language = db.Column(db.String)
    annotator_individuality = db.Column(db.Integer)

    def __repr__(self):
        return '<Annotation {} {}>'.format(self.emotion, self.filename)


class GiftCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    used = db.Column(db.Boolean, default=False)