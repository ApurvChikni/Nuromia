from flask import Flask, render_template, request, redirect, session, url_for, flash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from flask_mail import Mail, Message
import secrets
import os
# from sqlalchemy import or_
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
basedir = os.path.abspath(os.path.dirname(__file__))
#for model integration 

import sys
import glob
import re
import pandas as pd
import numpy as np 
import tensorflow as tf
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'


# coding=utf-8


# physical_devices = tf.config.list_physical_devices('GPU')
# try:
#   tf.config.experimental.set_memory_grpowth(physical_devices[0], True)
# except:
#   # Invalid device or cannot modify virtual devices once initialized.
#   pass


# from tensorflow.compat.v1 import ConfigProto
# from tensorflow.compat.v1 import InteractiveSession

# config = ConfigProto()
# config.gpu_options.per_process_gpu_memory_fraction = 0.2
# config.gpu_options.allow_growth = True
# session = InteractiveSession(config=config)
# Keras
#for keras and model loading
# from keras.applications.vgg16 import preprocess_input
#from keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.applications.vgg19 import preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

from werkzeug.utils import secure_filename



# end of model intigreation

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'database.db')
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)
mail = Mail(app)
cmail ='neuromiacov@gmail.com'

# SQLALCHEMY_TRACK_MODIFICATIONS = False
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

model_path ='model_vgg19.h5'
model = load_model(model_path)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable = False)
    name = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(50), unique=True, nullable = False)
    contect = db.Column(db.Integer, unique= True)
    password = db.Column(db.String(80), nullable = False)
    result = db.Column(db.String(15), default="Null")
    status = db.Column(db.String(15), default="False")
    image_file = db.Column(db.String(20), default="avatar.svg", nullable = False)

    def get_pass_token(self, expires_sec = 1800):
        s_p = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s_p.dumps({'user_id': self.id}, salt='password').decode('utf-8')

    @staticmethod
    def verify_pass_token(token):
        s_p = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s_p.loads(token, salt='password')['user_id']
        except:
            return None
        return User.query.get(user_id)


    # def get_email_token(self, expires_sec = 1800):
    #     s_e = Serializer(app.config['SECRET_KEY'], expires_sec)
    #     return s_e.dumps({'email': self.email}, salt ='email').decode('utf-8')


    # @staticmethod
    # def verify_email_token(token):
    #     s_e = Serializer(app.config['SECRET_KEY'])
    #     try:
    #         email = s_e.loads(token, salt='email')['email']
    #     except:
    #         return None
    #     return User.query.get(email)


    def __repr__(self):
        return f"User('{self.username}', '{self.name}', '{self.email}', '{self.contect}', '{self.result}', '{self.image_file}')"

class Conn(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(50))
    subject = db.Column(db.String(200))
    mess = db.Column(db.String(1500))

db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    title = 'About'
    return render_template('aboutp.html', title= title)

@app.route('/prevantion')
def prevantion():
    title = 'Prevantion'
    return render_template('prevantion.html', title= title)

@app.route("/team")
def team():
    return render_template('team.html')

@app.route('/contect',  methods=['GET', 'POST'])
def contect():
    title = 'Contact Us'
    return render_template('contect.html', title = title)

@app.route('/result',  methods=['GET', 'POST'])
@login_required
def result():
    return render_template('result.html', name = current_user.username)

@app.route('/profile')
@login_required
def profile():
    image_file = url_for('static', filename='img/profile_pics/' + current_user.image_file)
    return render_template('profile.html', name_p = current_user.name, uname_p = current_user.username, email_p = current_user.email, contect_p = current_user.contect, result_p = current_user.result, image_file = image_file)

@app.route('/eprofile')
@login_required
def eprofile():
    image_file = url_for('static', filename='img/profile_pics/' + current_user.image_file)
    return render_template('eprofile.html', image_file = image_file)
    # , name_p = current_user.name, uname_p = current_user.username, email_p = current_user.email, contect_p = current_user.contect, result_p = current_user.result)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/reg')
def reg():
    return render_template('reg.html')



# no need

# @app.route('/Register', methods=['GET', 'POST'])
# def register():
#     # form = RegisterForm()
#     return render_template('register.html')
#  no need
@app.route('/contactval',  methods=['GET', 'POST'])
def contactval():
    username_ = request.form.get('name')
    # user_=username_.split(' ')
    email_=  request.form.get('email')
    subject_ = request.form.get('subject')
    message_ = request.form.get('message')
    cmail='neuromiacov@gmail.com'
    msg = Message(subject_ , sender=cmail, recipients=[email_])
    msg.body="""
    Thanks for being awesome!

    We have received your message and would like to thank you for writing to us.
    If your inquiry is urgent, please use the telephone number listed below to 
    talk to one of our staff members. 

    Otherwise, we will reply by email as soon as possible.

    While we do our best to answer your queries quickly, it may take about 10 hours
    to receive a response from us during peak hours.

    Thank you for getting in touch!
    Talk to you soon, Nuromia.

    Have a great day!"""
        
    mail.send(msg)
    tous = Message('Feed Back Message from Site', sender=cmail, recipients=[cmail])
    tous.body = """
        Mail is sent by {}
        email: {}
        subject: {} 
        Message:{} """.format(username_, email_, subject_, message_)
    try:
        mail.send(tous)
        new_conn = Conn(name= username_,email= email_, subject= subject_ , mess= message_)
        db.session.add(new_conn)
        db.session.commit()
        flash('Your message has been sent. Thank you!', 'success')
    except:
        flash('Your message has not been sent. Please try again')
    return redirect(url_for('contect'))





def send_ver(email,token):
    # mail = Mail(app)
    msg = Message('Account Verification', sender='apuu1306200@gmail.com', recipients=[email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('loginvalidation_val', token=token, _external=True)}

This link is valid till 30 minuts.

If you did not make this request then simply ignore this email and no changes will be made.
''' 
    # print(msg.body)
    mail.send(msg)

@app.route('/verification/<token>',  methods=['GET', 'POST'])
def loginvalidation_val(token):
    # print(verify_email_token(token))
    # user = User.verify_email_token(token)
    try:
        email = s.loads(token, salt='email', max_age=1800)
    except (SignatureExpired, BadTimeSignature):
        flash('That is an invalid or expired token if it is expired genrate a new verification link', 'warning')
        # send_ver(user)
        return redirect(url_for('login'))
    # print(user)
    # if user is None:
    #     flash('That is an invalid or expired token new token is sent on your mail', 'warning')
    #     # send_ver(user)
    #     return redirect(url_for('login'))
    user_e = User.query.filter_by(email = email).first()
    user_e.status= str(True)
    db.session.commit()
    flash('Your account is verified please login.','success')
    return redirect(url_for('login'))

@app.route('/resend_link')
def resend_link():
    return render_template('resend_link.html')


@app.route('/val_resend_link',  methods=['GET', 'POST'])
def val_resend_link():
    if current_user.is_authenticated:
        session['logged_in'] = False
        session.pop('uname', None)
        logout_user()
        return redirect(url_for('home'))    
    email_=  request.form.get('email')
    user_e = User.query.filter_by(email = email_).first()
    if user_e is None:
        flash("There is no account with that email. You must register first", 'danger')
        return redirect(url_for('reg'))
    elif user_e.status == str(True):
        flash('Your account is already verified Please login','primary')
        return redirect(url_for('login'))
    token = s.dumps(email_, salt='email')
    send_ver(email_,token)
    flash('New verification link is sent to your email please verify your account within 30 minuts.','primary')
    return redirect(url_for('login'))

@app.route('/loginvalidation',  methods=['GET', 'POST'])
def loginvalidation():
    if current_user.is_authenticated:
        session['logged_in'] = False
        session.pop('uname', None)
        logout_user()
        return redirect(url_for('home'))
    username1 = request.form.get('email')
    user = User.query.filter_by(email = username1).first()
    # user = User.query.filter_by(username = request.form.get('uname')).first()
    if user is None:
        flash("There is no account with that email. You must register first", 'danger')
        return redirect(url_for('reg'))
    elif user.status ==str(False):
        flash('Please verfiy your email first','warning')
        return redirect(url_for('login'))
    if user:
        if check_password_hash(user.password, request.form.get('password')):
            # name = "hell"
            session['logged_in'] = True
            login_user(user, remember=True)
            session['uname'] = current_user.username
            return redirect(url_for('home'))
    flash("Invalid user id or password",'warning')        
    return redirect(url_for('login'))

@app.route('/Registervalidation', methods=['GET', 'POST'])
def Rvalidation():
    if current_user.is_authenticated:
        session['logged_in'] = False
        session.pop('uname', None)
        logout_user()
        return redirect(url_for('home'))
    username_ = request.form.get('uname')
    email_=  request.form.get('uemail')
    contect_ = request.form.get('ucontect')
    name_ = request.form.get('uname_')
    e=0
    # password=  request.form.get('upassword')
    # try:
    #     new_user = User(username= request.form.get('uname'), email= request.form.get('uemail'), password= request.form.get('upassword'))
    # except:
    #     flash("username or email or password is already in use.")

    user = User.query.filter_by(username = username_).first()
    user_e = User.query.filter_by(email = email_).first()
    user_c = User.query.filter_by(contect = contect_).first()
    if user:
        flash("That Userid is taken. Please choose a diffrent Userid.",'warning')
        e = 1
    if user_e:
        flash("That Email is taken. Please choose a diffrent Email.",'warning')
        e=2
    if user_c:
        flash("That Contact is taken. Please choose a diffrent Contact.",'warning')
        e=3
    if True:
        # flash(e)
        if e != 0:
            return redirect(url_for('reg'))
        if e==0:
            token = s.dumps(email_, salt='email')
            hashed_password = generate_password_hash(request.form.get('upassword'), method='sha256')
            new_user = User(username= request.form.get('uname'), name= name_, email= request.form.get('uemail'), contect= contect_, password= hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('You have successfully registered and verification link is sent on your mail', 'success')
            # user_ev = User.query.filter_by(email = email_).first()
            send_ver(email_,token)
            # return ("username is {} email is {} and password is {}".format(username, email, password))
            return redirect(url_for('login'))
            
    # user = User.query.filter_by(email = username1).first()
    # user = User.query.filter(or_(User.email == email_, User.username == username_)).first()
    # if user:
    #     flash('Email address or user name already exists')
    #     return redirect(url_for('reg'))

    # hashed_password = generate_password_hash(request.form.get('upassword'), method='sha256')
    # new_user = User(username= request.form.get('uname'), name= name_, email= request.form.get('uemail'), contect= contect_, password= hashed_password)
    
    # db.session.add(new_user)
    # db.session.commit()
    # flash('You have successfully registered', 'success')
    # # return ("username is {} email is {} and password is {}".format(username, email, password))
    # return redirect(url_for('login'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img/profile_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}


@app.route('/profilevalidation', methods = ['GET', 'POST'])
def profilevalidation():
    username_p = request.form.get('puserid')
    email_p=  request.form.get('pemail')
    contect_p = str(request.form.get('pcotact'))
    name_p = request.form.get('pusername')
    # e = False
    # ui =False
    # co = False
    error = 0
    # flash(username_p)/
    # flash(current_user.username)
    # current_user.contect = "1"
    # db.session.commit()
    if (username_p != current_user.username):
        # flash( current_user.username)
        # flash( username_p)
        # print(username_p, current_user.username)
        # user = User.query.filter_by(email = username1).first()
        user = User.query.filter_by(username = username_p).first()
        if user:
            flash("That Userid is taken. Please choose a diffrent Userid.",'danger')
            error = 1
            # break
    if (email_p != current_user.email):
        user_e = User.query.filter_by(email = email_p).first()
        if user_e:
            flash("That Email is taken. Please choose a diffrent Email.",'danger')
            # raise ValidationError
            e= True
            error = 2
            # break
    if (contect_p != str(current_user.contect)):
        user_c = User.query.filter_by(contect = contect_p).first()
        if user_c:
            flash("That Contact is taken. Please choose a diffrent Contact.",'danger')
            error = 3
            # break
    if request.method == 'POST':
        file = request.files['file_1']
        if file and allowed_file(file.filename):
            picture_file = save_picture(file)
            current_user.image_file = picture_file
            db.session.commit()
            flash('Profile picture has been updated','success')
            if (username_p == current_user.username) and (email_p == current_user.email) and (contect_p == str(current_user.contect)) and (name_p== current_user.name):
                error = 6
            
        elif((file.filename != '') and (not allowed_file(file.filename))):
            error = 4
            flash('Please select .jpeg or .jpg or .png files..', 'primary')  
    if((username_p == current_user.username) and (email_p == current_user.email) and (contect_p
     == str(current_user.contect)) and (name_p== current_user.name) and ( request.files['file_1'].filename == '')):
        error = 5
        flash("Please change data in fields or upload files", "primary")
    if(True):
        # flash(error)
        if error == 0 :
            current_user.name = name_p
            current_user.username = username_p
            current_user.email = email_p
            current_user.contect = str(contect_p)
            db.session.commit()
            flash(" Your account has been updated! ", 'success')
        return redirect(url_for('eprofile'))
    # user = User.query.filter_by(username = username_p).first()
    # user_e = User.query.filter_by(email = email_p).first()
    # user_c = User.query.filter_by(contect = contect_p).first()
    # if user:
    #     flash("That userid is taken. Please choose a diffrent userid.")
    # if user_e:
    #     flash("That email is taken. Please choose a diffrent userid.")
    # if user_c:
    #     flash("That contact is taken. Please choose a diffrent userid.")
    # return redirect(url_for('eprofile'))

def send_mail(user):
    # mail = Mail(app)
    token = user.get_pass_token()
    msg = Message('Password Reset Request', sender='neuromiacov@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

This link is valid till 30 minuts.

If you did not make this request then simply ignore this email and no changes will be made.
''' 
    print(msg.body)
    mail.send(msg)

@app.route('/reset')
def reset():
    return render_template("sendmail_.html")


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        session['logged_in'] = False
        session.pop('uname', None)
        logout_user()
        return redirect(url_for('home'))
    email_m=  request.form.get('email')
    user_e = User.query.filter_by(email = email_m).first()
    if user_e is None:
        flash("There is no account with that email. You must register first", 'danger')
        # return render_template('sendmail_.html')
        return redirect(url_for('reset'))
    send_mail(user_e)
    session['pass_token'] = True
    flash('An email has been sent with instructions to reset your password.', 'primary')

    return redirect(url_for('login'))


@app.route('/reset/<token>',methods=['GET', 'POST'])
def reset_pass(token):
    user = User.verify_pass_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset'))
    # password = request.form.get('upassword')
    hashed_password = generate_password_hash(request.form.get('upassword'), method='sha256') 
    user.password = hashed_password
    db.session.commit()
    flash('Your password has been updated! You are now able to log in','success')
    session['pass_token'] = False
    return redirect(url_for('login'))
    # return render_template('resetpass.html', form = FlaskForm)

    # return render_template("resetpass.html")


@app.route('/resetpass/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        session['logged_in'] = False
        session.pop('uname', None)
        logout_user()
        return redirect(url_for('home'))
    if (session['pass_token'] == False):
        flash('This token is used please genrate new token to reset password!','danger')
        return redirect(url_for('reset'))

    return render_template('resetpass.html', token = token) 
    



def predict(img_path, model):
    # print(img_path)
    img = image.load_img(img_path, target_size =(224, 224))
    x = image.img_to_array(img)

    x = x/225
    x = np.expand_dims(x, axis=0)

    preds_1 = model.predict(x)
    print(preds_1)
    preds=np.argmax(preds_1, axis=1)
    if preds==0:
        per = (preds_1[0][0])*100
        preds="Person is normal  {:0.2f}%".format(per)
        ind = "Negative"
        
    elif preds==1:
        per = (preds_1[0][1])*100
        preds="Person have pneumonia  {:0.2f}%".format(per)
        ind = "Positive"
    else:
        print('error')
    # preds = "Person is normal  100%"
    # ind = "Negative"
    return preds, ind




@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file_1']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds, flag= predict(file_path, model)
        result_1=preds
        user_2 = User.query.filter_by(username = current_user.username).first()
        user_2.result = flag
        db.session.commit()
        return result_1
    return None







@app.route('/logout')
@login_required
def logout():
    session['logged_in'] = False
    [session.pop(key) for key in list(session.keys())]
    logout_user()
    return redirect('/')



if __name__=="__main__":
    app.run(debug=True)
