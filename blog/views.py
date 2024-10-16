from flask import Blueprint, render_template
from app import db
from blog.forms import PostForm
from models import Post
from sqlalchemy import desc
from flask_login import current_user,login_required

blog_blueprint = Blueprint('blog', __name__, template_folder='templates')

@blog_blueprint.route('/blog')
@login_required
def blog():
    posts = Post.query.order_by(desc('id')).all()
    return render_template('blog/blog.html', posts=posts)


@blog_blueprint.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post(username=current_user.username, title=form.title.data, body=form.body.data)

        db.session.add(new_post)
        db.session.commit()



    return render_template('blog/create.html', form=form)



@blog_blueprint.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = Post.query.filter_by(id=id).first()



    form = PostForm()

    if form.validate_on_submit():
        post.update_post(form.title.data, form.body.data)
        return blog()

        # set update form with title and body of post object
    form.title.data = post.title
    form.body.data = post.body

    return render_template('blog/update.html', form=form)

@blog_blueprint.route('/<int:id>/delete')
@login_required
def delete(id):
    Post.query.filter_by(id=id).delete()
    db.session.commit()

    return blog()

@blog_blueprint.route('/filterposts')
@login_required
def filterposts():
    posts = Post.query.filter_by(username = current_user.username).order_by(desc('id'))

    return render_template('blog/blog.html', posts=posts)