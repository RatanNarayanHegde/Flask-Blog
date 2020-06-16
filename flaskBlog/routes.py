from flask import render_template,flash,redirect,url_for
from flaskBlog import app, db, bcrpyt
from flaskBlog.forms import RegistrationForm, LoginForm
from flaskBlog.models import User,Post
from flask_login import login_user,current_user,logout_user

posts = [
    {
        'author': 'Ratan Hegde',
        'title': 'Blog Post 1',
        'content': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Natus, mollitia?',
        'date_pub': 'June 14 2020'
    },
    {
        'author': 'Shubham Kumtole',
        'title': 'Blog Post 2',
        'content': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Natus, mollitia?',
        'date_pub': 'June 13 2020'
    }
]


@app.route("/")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register" , methods=['GET','POST'])
def register():
    if current_user.is_authenticated :
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrpyt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username= form.username.data , email=form.email.data , password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account successfully created You can now login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated :
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrpyt.check_password_hash(user.password,form.password.data):
            login_user(user, form.remember.data)
            return redirect(url_for('home'))
        else:
            flash(f'Check Username and password ','danger')
    return render_template('login.html',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))