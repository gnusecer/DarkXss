from flask.ext.wtf import Form
from wtforms_alchemy import model_form_factory
from wtforms import StringField
from wtforms.validators import DataRequired
from xss import db
from models import User, Project

BaseModelForm = model_form_factory(Form)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

class UserCreateForm(ModelForm):
    class Meta:
        model = User

class SessionCreateForm(Form):
    email = StringField('name', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])

class ProjectCreateForm(ModelForm):
    class Meta:
        model = Project