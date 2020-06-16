from flask import render_template,flash,redirect,url_for
from flaskBlog import app
from flaskBlog.forms import RegistrationForm, LoginForm
from flaskBlog.models import User,Post

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

    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Accout created for user {form.username.data}! ', 'success')
        return redirect(url_for('home'))
    return render_template('register.html',form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'ratanhegde08@gmail.com' and form.password.data== '123456':
            flash(f'Succesfully logged in ','success')
            return redirect(url_for('home'))
        else:
            flash(f'Check Username and password ','danger')
    return render_template('login.html',form=form)

