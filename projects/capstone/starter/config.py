import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
# Enable debug mode.
DEBUG = True
# Database connection string

SQLALCHEMY_DATABASE_URI = 'postgres://iegqbkuxwfvlyx:86b85be0622cb66b45a2a7f5ce775642d455431a8fb3c7a4e62f576cc4061ff1@ec2-3-229-210-93.compute-1.amazonaws.com:5432/d9ddjavkel9st9'

#SQLALCHEMY_DATABASE_URI = 'postgres://johnnysheffer@localhost:5432/capstone'

SQLALCHEMY_TRACK_MODIFICATIONS = False

bearer_tokens = {
    "casting_assistant": "Bearer ",
    "casting_director": "Bearer ",
    "executive_producer": "Bearer ",
}