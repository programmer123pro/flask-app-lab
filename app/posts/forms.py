from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import *
from wtforms.validators import DataRequired, Length
from datetime import datetime as dt

CATEGORIES = [('tech', 'Tech'), ('science', 'Science'), ('lifestyle', 'Lifestyle')]

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2)])
    content = TextAreaField('Content', render_kw={'rows' : 5, 'cols' : 40}, validators=[DataRequired()])
    submit = SubmitField('Add Post')
    is_active = BooleanField('Active post')
    publish_date = DateTimeLocalField('Publish Date', format='%Y-%m-%dT%H:%M', default=dt.now())
    category = SelectField('Category', choices=CATEGORIES, validators=[DataRequired()])

    def init(self, title=None, content=None, is_active=None, publish_date=None, category=None):
        self.title.data = title
        self.content.data = content
        self.is_active.data = is_active
        self.publish_date.data = publish_date
        self.category.data = category
