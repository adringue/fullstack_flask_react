from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate


# db = SQLAlchemy()
# app = Flask(__name__, template_folder='templates')
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bizza.db"
# db.init_app(app)

# @app.route('/users')
# def get_users():
#     users = User.query.all()
#     return render_template('users.html', users=users)

# class User(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(55), unique=True)
#     name = db.Column(db.String(55), unique=False)
#     email = db.Column(db.String(100), unique=True)

#     def __repr__(self):
#         return '<User {}>'.format(self.username)




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin123@localhost:5432/bizza'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/users')
def get_users():
    users = User.query.all()
    return render_template('users.html', users=users)

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    roles = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    is_superuser = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime,default=datetime.now(),onupdate=datetime.now())

    def __repr__(self):
        return '<User %r>' % self.username
    
class Speaker(db.Model):
    # __tablename__ = 'speakers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    bio = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(100))
    contact_info = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('speaker', uselist=False))
    # is_active = db.Column(db.Boolean, default=True)
    # is_superuser = db.Column(db.Boolean, default=False)
    # created_at = db.Column(db.DateTime, default=datetime.now())
    # updated_at = db.Column(db.DateTime,default=datetime.now(),onupdate=datetime.now())

    def __repr__(self):
        return f"Speaker('{self.name}', '{self.bio}', '{self.photo}', '{self.contact_info}')"
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)    
