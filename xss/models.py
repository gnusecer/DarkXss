from flask import g
from wtforms.validators import Email,Length
from xss import db, flask_bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, info={'validators': Length(min=6, max=25) })
    email = db.Column(db.String(120), unique=True, nullable=False, info={'validators': Email()})
    password = db.Column(db.String(80), nullable=False)
    key = db.Column(db.String(120), nullable=False)
    ip = db.Column(db.String(64), nullable=False)
    #posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username;
        self.email = email
        self.password = flask_bcrypt.generate_password_hash(password)

    def __repr__(self):
        return '<User %r> | <Mail %r>' % self.username, self.email

class Project(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    desc = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(12),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, title, desc , url ):
        self.title = title
        self.desc = desc
        self.url = url
        self.user_id = g.user.id

    def __repr__(self):
        return '<Post %r>' % self.title
    
    
    
class Info(db.Model):
    info_id = db.Column(db.Integer, primary_key=True)
    target_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(120),nullable=False)
    cookie = db.Column(db.Text, nullable=False)
    
    def __init__(self, title, url , cookie ):
        self.title = title
        self.url = url
        self.cookie = cookie
        self.target_id = g.target.target_id

    def __repr__(self):
        return '<Post %r>' % self.title
    
    
    
class Target(db.Model):
    target_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(120),nullable=False)
    desc = db.Column(db.Text, nullable=False)
    ip = db.Column(db.String(64),nullable=False)
    os = db.Column(db.String(120),nullable=False)
    browser_type = db.Column(db.String(120),nullable=False)
    is_active = db.Column(db.Integer,default=0)
    created_at = db.Column(db.Integer)
    last_visit = db.Column(db.Integer)

    def __init__(self, name, desc , ip , btype ):
        self.name = name
        self.desc = desc
        self.ip = ip
        self.os = os
        self.browser_type = btype
        self.user_id = g.project.project_id

    def __repr__(self):
        return '<Post %r>' % self.name
    
    
class Payload(db.Model):
    payload_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120),unique=True,nullable=False)
    desc = db.Column(db.Text, nullable=False)
    code = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, name, desc , code ):
        self.name = name
        self.desc = desc
        self.code = code


    def __repr__(self):
        return '<Post %r>' % self.title