from flask import Flask, render_template, request, \
    redirect, url_for, flash
from flask_login import LoginManager, login_required, current_user, login_user, logout_user

import utils
from extension import db
from models import User, Annotation, DrawEmail

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
        print(current_user)
    form = request.form
    if request.method == "POST":
        # print("PASSWORD: ", form['password'])
        user = User.query.filter_by(username=form['username']).first()
        if user is None or not user.check_password("[%J^3k8V"):
            flash('Invalid username')
            return render_template('login.html', message="Wrong username.")
        login_user(user, remember=True)
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/register', methods=["GET", "POST"])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == "POST":
        return render_template('register.html')
    return render_template('register.html')


@app.route('/create_user', methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        user_form = request.form

        IDV = user_form['IDV']

        print(user_form['na_culture'])
        print(user_form['persian_culture'])
        print(user_form['filipino_culture'])
        print(user_form['filipino_lang'])
        # username = user_form['username']
        # password = user_form['password']

        user = User()

        user.username = utils.id_generator()
        user.set_password("[%J^3k8V")
        if int(user_form['na_culture']) > int(user_form['persian_culture']) and int(user_form['na_culture']) > int(user_form['filipino_culture']):
            user.culture = 'north american'
        elif int(user_form['persian_culture']) > int(user_form['filipino_culture']):
            user.culture = 'persian'
        elif int(user_form['persian_culture']) < int(user_form['filipino_culture']):
            user.culture = 'filipino'

        if int(user_form['english_lang']) > int(user_form['persian_lang']) and int(user_form['english_lang']) > int(user_form['filipino_lang']):
            user.language = 'english'
        elif int(user_form['persian_lang']) > int(user_form['filipino_lang']):
            user.language = 'persian'
        elif int(user_form['persian_lang']) < int(user_form['filipino_lang']):
            user.language = 'filipino'

        user.individuality = IDV
        db.session.add(user)
        db.session.commit()
        print("User %s created :)" % user.username)
        return render_template('show_code.html', user_code=user.username)

# @app.route('/code', methods=["GET"])



@app.route('/index', methods=["GET", "POST"])
@login_required
def index():
    user: User = current_user
    facial_exprssions_translations = None
    # setting translations for social signals
    if user.language == 'english':
        facial_exprssions_translations = utils.english_fe
    elif user.language == 'persian':
        facial_exprssions_translations = utils.persian_fe
    elif user.language == 'filipino':
        facial_exprssions_translations = utils.filipino_fe

    if request.method == "POST":  # if the request is post (i.e. new video annotated?)
        # print(request.form)
        form = request.form



        annotation: Annotation = Annotation()
        annotation.emotion = form['emotion']
        annotation.anger_score = form['anger']
        annotation.contempt_score = form['contempt']
        annotation.disgust_score = form['disgust']
        annotation.annoyed_score = form['annoyed']
        annotation.gender = form['gender']
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
        annotation.social_signals = social_signals


        db.session.add(annotation)
        db.session.commit()
        vid = utils.get_random_video(user.culture, user.get_annotated_videos())
        completed = utils.get_completed_videos(user.culture, user.get_annotated_videos())
        if vid == "FINISHED":
            return render_template('thankyou.html')
        print("Annotation %s created :)" % annotation)

        return render_template('index.html', context={'video':vid, 'language': user.language, 'completed': completed,
                                                      'expressions': facial_exprssions_translations})

    vid = utils.get_random_video(user.culture, user.get_annotated_videos())
    completed = utils.get_completed_videos(user.culture, user.get_annotated_videos())
    if vid == "FINISHED":
        return render_template('thankyou.html')
    return render_template('index.html', context={'video':vid, 'language': user.language, 'completed': completed,
                                                  'expressions': facial_exprssions_translations})

@app.route("/consent_form")
def consent_form():
    return render_template('consent_form.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None

@app.route('/gift_codes', methods=["GET", "POST"])
@login_required
def gift_codes():
    if request.method == "GET":
        return render_template('thankyou.html')
    if request.method == "POST":  # if the request is post (i.e. new video annotated?)
        # print(request.form)
        err_msg = None
        code = request.form['code']
        if code is not None:
            user = User.query.get(code)
            if user is None:
                err_msg = "Wrong code!"
        return render_template('thankyou.html', message=err_msg)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
