from flask import Flask, render_template, request, \
    redirect, url_for, flash
import pandas as pd
import csv
from collections import defaultdict
import random
from models import User, Annotation, DrawEmail
from config import Config
from extension import db
import utils
from flask_login import LoginManager, login_url, login_required, current_user, login_user, logout_user

## Setting up app essentials
app = Flask(__name__, static_folder='./static')
app.config.from_object('config.Config')
# db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
db.init_app(app)
with app.app_context():
    db.create_all()
# db.create_all()


@app.route('/', methods=["GET", "POST"])
def initial():
    # TODO: remove these lines
    if current_user.is_authenticated:
        logout_user()
    return render_template('main.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = request.form
    if request.method == "POST":
        print("PASSWORD: ", form['password'])
        user = User.query.filter_by(username=form['username']).first()
        if user is None or not user.check_password(form['password']):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=True)
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/register', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        print("here")
        return render_template('register.html')
    return render_template('register.html')


@app.route('/create_user', methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        user_form = request.form
        # cult = user_form['culture']
        # IDV = user_form['IDV']
        # nat = user_form['country']
        # lang = user_form['language']
        print(user_form['na_culture'])
        print(user_form['persian_culture'])
        print(user_form['filipino_culture'])
        print(user_form['filipino_lang'])
        username = user_form['username']
        password = user_form['password']
        rvs_1 = user_form['rvs_1']
        rvs_2 = user_form['rvs_1']
        rvs_3 = user_form['rvs_3']
        rvs_4 = user_form['rvs_4']
        rvs_5 = user_form['rvs_5']
        rvs_6 = user_form['rvs_6']
        rvs_7 = user_form['rvs_7']
        rvs_8 = user_form['rvs_8']
        rvs_9 = user_form['rvs_9']
        rvs_10 = user_form['rvs_10']
        rvs_11 = user_form['rvs_11']
        rvs_12 = user_form['rvs_12']
        rvs_13 = user_form['rvs_13']
        rvs_14 = user_form['rvs_14']
        rvs_15 = user_form['rvs_15']
        rvs_16 = user_form['rvs_16']
        rvs_17 = user_form['rvs_17']
        rvs_18 = user_form['rvs_18']

        consent_confirm = user_form['consent']

        user = User()
        user.username = username
        user.set_password(password)
        if int(user_form['na_culture']) > int(user_form['persian_culture']) & int(user_form['na_culture']) > int(user_form['filipino_culture']):
            user.culture = 'north american'
        elif int(user_form['persian_culture']) > int(user_form['filipino_culture']):
            user.culture = 'persian'
        elif int(user_form['persian_culture']) < int(user_form['filipino_culture']):
            user.culture = 'filipino'

        if int(user_form['english_lang']) > int(user_form['persian_lang']) & int(user_form['english_lang']) > int(user_form['filipino_lang']):
            user.language = 'english'
        elif int(user_form['persian_lang']) > int(user_form['filipino_lang']):
            user.language = 'persian'
        elif int(user_form['persian_lang']) < int(user_form['filipino_lang']):
            user.language = 'filipino'
        # user.culture = cult
        # user.individuality = IDV
        # user.language = lang
        # user.nationality = nat
        # user.rvs_1 = rvs_1
        # user.rvs_2 = rvs_2
        # user.rvs_3 = rvs_3
        db.session.add(user)
        db.session.commit()
        print("User %s created :)" % username)
        return redirect(url_for('login'))


@app.route('/index', methods=["GET", "POST"])
@login_required
def index():
    user: User = current_user
    if request.method == "POST":  # if the request is post (i.e. new video annotated?)
        # print(request.form)
        form = request.form


        annotation: Annotation = Annotation()
        annotation.emotion = form['emotion']
        annotation.anger_score = form['anger']
        annotation.contempt_score = form['contempt']
        annotation.disgust_score = form['disgust']
        annotation.annoyed_score = form['annoyed']
        annotation.filename = form.get("token")
        user.add_video(form.get("token"))

        social_signals = ','.join([ss for ss in form.getlist('socialsignal')])
        extra_ss = form.get("extra")
        ## TODO: should be tested
        if len(extra_ss) > 0:
            social_signals += ',%s' % extra_ss
        annotation.confidence = form['confidence']
        annotation.annotator_culture = user.culture
        annotation.annotator_language = user.language
        annotation.annotator_individuality = user.individuality
        annotation.annotator_nationality = user.nationality
        annotation.social_signals = social_signals

        db.session.add(annotation)
        db.session.commit()
        vid = utils.get_random_video(user.culture, user.get_annotated_videos())
        if vid == "FINISHED":
            return render_template('thankyou.html')
        print("Annotation %s created :)" % annotation)



        return render_template('index.html', video=vid)

    vid = utils.get_random_video(user.culture, user.get_annotated_videos())
    if vid == "FINISHED":
        return render_template('thankyou.html')
    return render_template('index.html', video=vid)



@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None

@app.route('/enter_draw', methods=["GET", "POST"])
@login_required
def enter_draw():
    if request.method == "POST":  # if the request is post (i.e. new video annotated?)
        # print(request.form)
        email = request.form['email']
        draw = DrawEmail()
        draw.email = email
        db.session.add(draw)
        db.session.commit()
        # TODO: return this page with a message that shows the user has entered email successfully.
        return render_template('thankyou.html', message="You have successfully submitted your email!")

if __name__ == '__main__':
    app.debug = True
    print("SECRET_KEY:    ", app.config['SECRET_KEY'])
    app.run(host='0.0.0.0', port=5000)
