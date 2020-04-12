from flask_sqlalchemy import SQLAlchemy
import os

# database_path = "postgres://aar92_22@localhost:5432/agencyDB"
database_path = ('postgres://sjtmsunvoblvdc:28616399cc7bd7b269a'
                 '82fbcace62d274cb65f500eda8f8ba35946afe960d1e8'
                 '@ec2-35-171-31-33.compute-1.amazonaws.com:543'
                 '2/d857cptkuo45vv')

db = SQLAlchemy()

# setup_db(app) binds flask app to SQLAlchemy service


def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class Movies(db.Model):
    __tablename__ = 'movies_heroku'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    release_date = db.Column(db.String(), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }


class Actors(db.Model):
    __tablename__ = 'actors_heroku'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
