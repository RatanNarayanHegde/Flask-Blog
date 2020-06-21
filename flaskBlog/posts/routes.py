from flask import render_template,flash,redirect,url_for,request,abort, Blueprint
from flask_login import current_user, login_required
from flaskBlog import db
from flaskBlog.models import Post
from flaskBlog.posts.forms import PostForm



posts = Blueprint('posts',__name__)



@posts.route("/post/new",methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit() :
        post = Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post has been created','success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html',title='New Post',form=form,legend='New Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title,post=post)

@posts.route("/post/<int:post_id>/update",methods=['GET','POST'])
@login_required
def update_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if current_user.id != post.author.id :
        abort(403)
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated','success')
        return redirect(url_for('posts.post',post_id=post.id))

    elif request.method == 'GET':
        form.content.data = post.content
        form.title.data = post.title

    return render_template('create_post.html',title='Update Post',legend='Update Post',form=form)


@posts.route("/post/<int:post_id>/delete",methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.id != post.author.id :
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been deleted','success')
    return redirect(url_for('main.home'))
    
