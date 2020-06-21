from flask import render_template,flash,redirect,url_for,request, Blueprint
from flaskBlog import db, bcrpyt
from flaskBlog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPassword
from flaskBlog.models import User,Post
from flask_login import login_user,current_user,logout_user,login_required
from flaskBlog.users.utils import save_picture, send_reset_email



users = Blueprint('users',__name__)

@users.route("/register" , methods=['GET','POST'])
def register():
    if current_user.is_authenticated :
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrpyt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username= form.username.data , email=form.email.data , password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account successfully created You can now login', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html',form=form)

@users.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated :
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrpyt.check_password_hash(user.password,form.password.data):
            login_user(user, form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Check Username and password ','danger')
    return render_template('login.html',form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))



@users.route("/account",methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_fn = save_picture(form.picture.data)
            current_user.image_file= picture_fn
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated Successfully','success')
    elif request.method=='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='profile_pics/'+ current_user.image_file)
    return render_template('account.html',title='Account',image_file=image_file, form=form)




@users.route("/user/<string:username>")
def user_posts(username):
    page_no = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts= Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page_no,per_page=5)
    image_file = url_for('static',filename='profile_pics/'+ user.image_file)
    return render_template('user_posts.html', posts=posts,user=user,image_file=image_file)



@users.route("/reset_password",methods=['GET','POST'])
def reset_password():
    if current_user.is_authenticated :
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Am email with instructions has been sent to your email.Please check','info')
        return redirect(url_for('users.login'))

    return render_template('reset_request.html',title='Reset Password',form=form)

@users.route("/reset_password/<string:token>",methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated :
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('The token is invalid or expired','warning')
        return redirect(url_for('users.reset_password'))
    form = ResetPassword()
    if form.validate_on_submit():
        hashed_password = bcrpyt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your Password has been changed. You can now login', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',title='Reset password',form=form)