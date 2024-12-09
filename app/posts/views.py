from flask import *
from . import posts_bp
from .forms import PostForm
from datetime import datetime 
from .models import Post
from app import db
from app.users.models import User
from app.posts.models import Tag

@posts_bp.route('/')
def posts():
    stmt = db.select(Post).order_by(Post.posted.asc())
    posts = db.session.scalars(stmt)
    postsDict = []
    for post in posts:
        postsDict.append({
            'title' : post.title,
            'content' : post.content,
            'date' : post.posted.strftime("%Y-%m-%d %H:%M"),
            'category' : (post.category if post.category else ''),
            'author' : (post.author.username if post.author else 'Невідомий'),
            'id' : post.id
        })

    return render_template('posts.html', posts=postsDict)

@posts_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    
    authors = User.query.all()
    form.author_id.choices = [(author.id, author.username) for author in authors]
    tags = Tag.query.all()
    form.tags.choices = [(tag.id, tag.name) for tag in tags]

    if form.validate_on_submit(): 
        post = Post(
                title = form.title.data,
                content = form.content.data,
                category = form.category.data,
                is_active = form.is_active.data,    
                posted = form.publish_date.data,
                user_id = form.author_id.data,
                tags = [tags[id-1] for id in form.tags.data]
        )
        db.session.add(post)
        db.session.commit()

        flash('Post added successfully!', 'success')
        return redirect(url_for('posts.add_post'))
    
    return render_template('add_post.html', form=form)

@posts_bp.route('/<int:id>')
def view_post(id):
    post = db.get_or_404(Post, id)
    postDict = {            
            'title' : post.title,
            'content' : post.content,
            'date' : post.posted.strftime("%Y-%m-%d %H:%M"),
            'category' : (post.category if post.category else ''),
            'author' : (post.author.username if post.author else 'Невідомий'),
            'id' : post.id,
            'tags' : [tag.name for tag in post.tags]
        }

    return render_template('post.html', post=postDict)

@posts_bp.route('/delete')
def delete_post():
    if('id' in request.args):
        try:
            id = int(request.args.get('id'))
        except ValueError:
            flash('Enter valid integer', 'danger')    
        else:
            post = db.session.get(Post, id)
            if post:
                db.session.delete(post)
                db.session.commit()
                flash('Delete successfull', 'success')
            else:
                flash('Such post does not exist', 'danger')
            return redirect(url_for(".delete_post"))

    return render_template('delete_post.html')

@posts_bp.route("/edit/<int:id>", methods=["POST", "GET"])
def edit_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm()

    authors = User.query.all()
    form.author_id.choices = [(author.id, author.username) for author in authors]
    tags = Tag.query.all()
    form.tags.choices = [(tag.id, tag.name) for tag in tags]

    if(request.method == "GET"):
        form.init(
            title = post.title,
            content = post.content,
            category = post.category,
            publish_date = post.posted,
            is_active = post.is_active,
            author = post.user_id,
            tags = [tag.id for tag in post.tags]
        )
        return render_template("edit_post.html", form=form)
    
    elif(request.method == "POST"):
        if form.validate_on_submit(): 
            post.title = form.title.data
            post.content = form.content.data
            post.category = form.category.data
            post.is_active = form.is_active.data
            post.posted = form.publish_date.data
            post.user_id = (form.author_id.data)
            post.tags = [tags[id-1] for id in form.tags.data]
            db.session.commit()
            flash('Post edited successfull', 'success')     

        return redirect(url_for('.edit_post', id=id))