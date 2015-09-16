from flask import g
from flask.ext import restful

from xss import api, db, flask_bcrypt, auth
from models import User, Project
from forms import UserCreateForm, SessionCreateForm, ProjectCreateForm
from serializers import UserSerializer, ProjectSerializer

@auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    g.user = user
    return flask_bcrypt.check_password_hash(user.password, password)

class UserView(restful.Resource):
    def post(self):
        form = UserCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422

        user = User(form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        return UserSerializer(user).data

class SessionView(restful.Resource):
    def post(self):
        form = SessionCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422

        user = User.query.filter_by(email=form.email.data).first()
        if user and flask_bcrypt.check_password_hash(user.password, form.password.data):
            return UserSerializer(user).data, 201
        return '', 401

class ProjectListView(restful.Resource):
    def get(self):
        projects = Project.query.all()
        return ProjectSerializer(projects, many=True).data

    @auth.login_required
    def post(self):
        form = ProjectCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        project = Project(form.title.data, form.body.data)
        db.session.add(project)
        db.session.commit()
        return ProjectSerializer(project).data, 201

class ProjectView(restful.Resource):
    def get(self, id):
        projects = Project.query.filter_by(id=id).first()
        return ProjectSerializer(projects).data

api.add_resource(UserView, '/api/v1/users')
api.add_resource(SessionView, '/api/v1/sessions')
api.add_resource(ProjectListView, '/api/v1/projects')
api.add_resource(ProjectView, '/api/v1/projects/<int:id>')