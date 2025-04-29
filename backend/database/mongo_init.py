
from flask_pymongo import PyMongo

mongo = PyMongo()

def init_db(app):
    app.config['MONGO_URI'] = 'mongodb+srv://patilmonika931:patil0305@cluster0.il92b.mongodb.net/?retryWrites=true&w=majority'
    mongo.init_app(app)
    
