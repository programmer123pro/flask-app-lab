from flask import *
from . import posts_bp
from .forms import PostForm
from datetime import datetime 

class Post:
    _lastId = 0
    _post = dict()

    def __init__(self, title, content, category, is_active, date, author):
        self.title = title
        self.content = content
        self.category = category
        self.is_active = is_active
        self.publication_date = str(date)
        self.author = author
    
    def save(self):
        file = open('app/posts/posts.json ', 'r+')
        posts = json.load(file)
        if(len(posts) > 0):
            id = posts[-1]['id'] + 1
        else:
            id = 0

        post = {
            'id' : id,
            'title' : self.title,
            'content' : self.content,
            'category' : self.category,
            'is_active' : self.is_active,
            'publication_date' : self.publication_date,
            'author' : self.author
        }

        posts.append(post)
        file.seek(0)
        json.dump(posts, file, indent=4)

@posts_bp.route('/')
def posts():
    file = open('app/posts/posts.json ', 'r')
    posts = json.load(file)
    return render_template('posts.html', posts=posts)

@posts_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        if('username' in session):
            author = session['username']
        else:
            author = 'Невідомий'

        post = Post(
                form.title.data,
                form.content.data,
                form.category.data,
                form.is_active.data,
                form.publish_date.data,
                author
        )
        post.save()

        flash('Post added successfully!', 'success')
        return redirect(url_for('posts.add_post'))
    return render_template('add_post.html', form=form)