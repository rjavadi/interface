from flask import Flask, render_template, request, \
    redirect, url_for, flash
from flask_login import LoginManager, login_required, current_user, login_user, logout_user

import utils
from extension import db
from models import User, Annotation, GiftCard

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
    # if current_user.is_authenticated:
    #     logout_user()
    return render_template('main.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = request.form
    if request.method == "POST":
        user = User.query.filter_by(username=form['username']).first()
        if user is None or not user.check_password("[%J^3k8V"):
            flash('Invalid username')
            return render_template('login.html', message="Wrong username.")
        login_user(user, remember=False)
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

        user = User()
        user.username = utils.id_generator()
        user.set_password("[%J^3k8V")
        user.culture = user_form['culture']
        if user.culture == 'north american':
            user.language = 'english'
        elif user.culture == 'filipino':
            user.language = 'filipino'
        if user.culture == 'persian':
            user.language = 'persian'

        user.na_cult_level =  int(user_form['na_culture'])
        user.persian_cult_level = int(user_form['persian_culture'])
        user.filipino_cult_level = int(user_form['filipino_culture'])

        user.english_lang_level = int(user_form['english_lang'])
        user.persian_lang_level = int(user_form['persian_lang'])
        user.filipino_lang_level = int(user_form['filipino_lang'])

        culture_counter = User.query.filter_by(culture=user.culture).count()
        print("culture_counter = ", culture_counter)
        user.id = user.culture + '_%s' % culture_counter
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


    if request.method == "POST":  # if the request is post (i.e. new video annotated?)
        form = request.form

        annotation: Annotation = Annotation()
        # annotation.emotion = form.getlist('emotion')
        annotation.gender = form['gender']
        annotation.filename = form.get("token")
        user.add_video(form.get("token"))

        emotions = ','.join([ss for ss in form.getlist('emotion')])
        annotation.comment = form.get("comment")
        annotation.emotions = emotions

        annotation.confidence = form['confidence']
        annotation.annotator_culture = user.culture
        annotation.annotator_language = user.language
        annotation.annotator_individuality = user.individuality
        annotation.emoji = ','.join([ss for ss in form.getlist('emoji')])
        annotation.intensity = form['intensity']

        db.session.add(annotation)
        db.session.commit()
        vid = utils.get_random_video(user.culture, user.get_annotated_videos(), user.id)
        completed, all = utils.get_completed_videos(user.culture, user.get_annotated_videos())
        if vid == "FINISHED":
            user.finished = True
            gift_card_count = 2
            new_gift_cards = GiftCard.query.filter_by(used=False).limit(gift_card_count)
            user.add_gift_codes(new_gift_cards)
            db.session.commit()
            for card in new_gift_cards:
                card.used = True
                db.session.commit()
            return render_template('thankyou.html')

        return render_template('index.html', context={'video':vid, 'language': user.language, 'completed': completed, 'all_videos':all})
    # if method is GET:
    vid = utils.get_random_video(user.culture, user.get_annotated_videos(), user.id)
    completed, all = utils.get_completed_videos(user.culture, user.get_annotated_videos())
    if vid == "FINISHED" or user.withdraw == True:
        return render_template('thankyou.html')
    return render_template('index.html', context={'video':vid, 'language': user.language, 'completed': completed, 'all_videos':all})

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
    if request.method == "POST":  # if the request is post (ifrom thank you page)
        # print(request.form)
        err_msg = None
        code = request.form['code']
        if code is not None:
            user = User.query.filter_by(username=code).first()
            if user is None:
                err_msg = "Wrong code!"
                return render_template('thankyou.html', message=err_msg)
            return render_template('gift_cards.html', cards=user.get_gift_codes())

@app.route('/withdraw', methods=["GET", "POST"])
@login_required
def withdraw():
    if request.method == "GET":
        return render_template('withdraw.html')
    if request.method == "POST":  # if the request is post (i.e. new video annotated?)
        # print(request.form)
        err_msg = None

        code = request.form['code']
        if code is not None:
            user = User.query.filter_by(username=code).first()
            if user is None:
                err_msg = "Wrong code!"
                return render_template('withdraw.html', message=err_msg)
            user.withdraw = True
            completed, all = utils.get_completed_videos(user.culture, user.get_annotated_videos())
            gift_card_count = int((len(user.get_annotated_videos()) / all) * 2) # number of gift cards user should get.
            new_gift_cards = GiftCard.query.filter_by(used=False).limit(gift_card_count).all()
            user.add_gift_codes(new_gift_cards)
            db.session.commit()
            for card in new_gift_cards:
                card.used = True
                db.session.commit()

            return render_template('thankyou.html')

if __name__ == '__main__':
    app.debug = True
    for i in range(5):
        print(utils.id_generator(6))
    app.run(host='0.0.0.0', port=5000)


