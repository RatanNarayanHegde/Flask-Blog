from flask import Blueprint

users = Blueprint('users',__name__)

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
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Check Username and password ','danger')
    return render_template('login.html',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))