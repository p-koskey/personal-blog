from flask import render_template,request,redirect,url_for,abort,flash
from ..models import User,Post,Comments, Subscribers
from . import main
from .forms import PostForm, UpdateProfile,CommentForm, CommentForm2,SubscribeForm
from flask_login import login_required,current_user
from .. import db,photos
from flask_mail import Message
from .. import mail
from ..requests import get_quotes
from sqlalchemy import asc,desc

@main.route('/', methods = ['GET','POST'])
def index():
    posts = Post.get_all_posts()
    quote = get_quotes()
    subscribe_form = SubscribeForm()
    recent = Post.query.order_by(desc(Post.posted)).limit(3).all()

    if subscribe_form.validate_on_submit():
        semail = subscribe_form.email.data
        new_email = Subscribers(semail = email)

        new_email.save_email()

        msg = Message(subject="Tech Blog Subscriber", sender="testingemailpk6@gmail.com", recipients=[semail])
        msg.body = f"Hello, Thank you for subscribing to Tech blog, welcome to the family. You will be notified of new emails Please enjoy."
        mail.send(msg)
        flash("Subscribed sucessfully")
   
    return render_template('index.html', subscribe_form=subscribe_form, posts=posts, quote =quote, recent=recent)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/post/new/', methods = ['GET','POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        post_title = form.post_title.data
        post_content = form.post_content.data
    
        # Updated osth instance
        new_post = Post(title=post_title, content=post_content, user_id = current_user.id)

        # save review method
        new_post.save_post()
        return redirect(url_for('.index' ))

    title = 'New Post'
    return render_template('newpost.html',title = title,action="Add", post_form=form, )

@main.route('/post/delete/<int:post_id>/',methods=['GET'])
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    db.session.delete(post)
    db.session.commit()
    #flash('Page was deleted successfully', 'success')
    return redirect(url_for('main.index'))

@main.route('/post/update/<int:post_id>/',methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    form =PostForm()
    if form.validate_on_submit():
        post.title = form.post_title.data
        post.content = form.post_content.data
        db.session.commit()
        flash('Post updated successfully!')
        return redirect (url_for('.index') )

    else:
        title = 'Edit Post'
        return render_template('newpost.html',title = title, post = post, post_form=form,action="Edit" )
  
@main.route('/user/<uname>/posts')
@login_required
def view_my_posts(uname):
    user = User.query.filter_by(username=uname).first()
    posts = Post.query.filter_by(user_id = user.id).all()    
    
    return render_template("profile/myposts.html", user=user,posts=posts)

@main.route('/post/edit/<post_id>', methods=['GET'])
def edit_post(post_id):
    comment_form = CommentForm()
    user_form = CommentForm2()
    post = Post.query.filter_by(id=post_id).first()
    user = User.query.filter_by(id=post.user_id)
    comments = Comments.get_comments(post_id)
    return render_template('profile/editpost.html', post=post, comments=comments, post_id=post.id, comment_form = comment_form, user_form=user_form, user =user)
 
@main.route('/post/view/<post_id>', methods=['POST'])
def post_comment(post_id):
   

    post = Post.query.filter_by(id=post_id).first()
    
    comments = Comments.get_comments(post_id)
    comment_form = CommentForm()
    user_form = CommentForm2()

    if comment_form.validate_on_submit() or user_form.validate_on_submit():
        if current_user.is_authenticated:
            name = current_user.username        
            comment = comment_form.description.data
        else:  
            name = user_form.name.data
            comment = user_form.description.data

        new_comment = Comments( name = name , comments=comment, post_id = post_id)

        new_comment.save_comment()

        return redirect(request.referrer)

@main.route('/post/view/<post_id>', methods=['GET'])
def view_post(post_id):
    comment_form = CommentForm()
    user_form = CommentForm2()
    post = Post.query.filter_by(id=post_id).first()
    user = User.query.filter_by(id=post.user_id)
    comments = Comments.get_comments(post_id)
    return render_template('post.html', post=post, comments=comments, post_id=post.id, comment_form = comment_form, user_form=user_form, user =user)

@main.route('/post/<int:comment_id>/delete')
@login_required
def delete_comment(comment_id):
    
    comment = Comments.query.filter_by(id=comment_id).first_or_404()
    db.session.delete(comment)
    db.session.commit()
    
    return redirect(request.referrer)


    
    