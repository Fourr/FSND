import os
from flask_migrate import Migrate
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

#database_path = 'postgres://iegqbkuxwfvlyx:86b85be0622cb66b45a2a7f5ce775642d455431a8fb3c7a4e62f576cc4061ff1@ec2-3-229-210-93.compute-1.amazonaws.com:5432/d9ddjavkel9st9'
database_path = os.environ.get('DATABASE_URL')
if not database_path:
    database_name = "capstone"
    database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()



    #binds a flask application and a SQLAlchemy service

def setup_db(app, database_path=database_path):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


'''
Person
Have title and release year
'''
class Actor(db.Model):  
  __tablename__ = 'actors'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  age = Column(Integer)
  gender = Column(String)

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender}

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()


class Movie(db.Model):  
  __tablename__ = 'Movies'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  release_date = Column(String)


  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date}

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
