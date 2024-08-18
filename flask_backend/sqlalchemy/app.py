from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
# from sqlalchemy import MetaData
# metadata = MetaData()


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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/users')
def get_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/api/v1/venues', methods=['GET'])
def retrieve_venues():
    if request.method == 'GET':
        all_venues = Venue.query.all()
        if all_venues:
            return jsonify({
                'success': True,
                'venues': [venue.format() for venue in all_venues]
            }), 200
        return jsonify(message="No venue record found"), 404

@app.route("/app/v1/venues/<int:id>", methods=['GET'])
def retrieve_venue(id):
    if request.method == 'GET':
        venue = Venue.query.filter(Venue.id == id).first()
        if venue:
            return jsonify({
                'success': True,
                'venue': venue.format()
            }), 200
        return jsonify(message="Record id not found"), 404
    
@app.route("/api/v1/venues/<int:id>", methods=['PUT'])
def update_venue(id):
    if request.method == 'PUT':
        name = request.get_json().get('name')
        venue = Venue.query.get(id)
        if not venue:
            return jsonify(message='Venue record not found'), 404
        venue.name = name
        db.session.commit()
    return jsonify({
        'success': True,
        'updated venue': venue.format()
    }), 200        

@app.route('/venues/<int:id>', methods=['DElETE'])
def remove_venue(id):
    venue = Venue.query.ffilter_by(id=id).first()
    if venue:
        db.session.delete(venue)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'You deleted a venue',
            'deleted': venue.format()
        }), 202
    else:
        return jsonify(message="That venue does not exist"), 404

@app.route("/api/v1/venues", methods=['POST'])
def add_venues():
    if request.method == 'POST':
        name = request.get_json().get('name')
        all_venues = Venue.query.filter_by(name=name).first()
        if all_venues:
            return jsonify(message="Venue name already exist!"), 409
        else:
            venue = Venue(name=name)
            db.session.add(venue)
            db.session.commit()
            return jsonify({
                'success': True,
                'venues': venue.format()
            }), 201
        

@app.route("/api/v1/speakers")
def speakers():
    firstname = request.args.get("firstname")
    lastname = request.args.get("lastname")

    if firstname is not None and lastname is not None:
        return jsonify(message="The speaker's fullname :" + firstname+" "+lastname)
    else:
        return jsonify(message="No query parameters in the url")

@app.route('/api/v1/speakers/<int:speaker_id>')
def get_speaker(speaker_id):
    all_users = User.query.all()
    if all_users is not None:
        return jsonify({"results":[user.username for user in all_users]})
    else:
        return jsonify(message="No Users")    
    
@app.route("/api/v1/events-registration", methods=['POST'])
def add_attendees():
    if request.method == 'POST':
        first_name = request.get_json().get('first_name')
        last_name = request.get_json().get('last_name')
        email = request.get_json().get('email')
        phone = request.get_json().get('phone')
        job_title = request.get_json().get('job_title')
        company_name = request.get_json().get('company_name')
        company_size = request.get_json().get('company_size')
        subject = request.get_json().get('subject')

        if first_name and last_name and email and phone and subject:
            all_attendees = EventRegistration.query.filter_by(
                email=email
            ).first()
            if all_attendees:
                return jsonify(message="Email address already exist!"), 409
        else:
            new_attendee = EventRegistration (
                first_name = first_name,
                last_name = last_name,
                email = email,
                phone = phone,
                job_title = job_title,
                company_name = company_name,
                company_size = company_size,
                subject = subject
            ) 
            db.session.add(new_attendee)
            db.session.commit()
            return jsonify({
                'success': True,
                'success': True,
                'new_attendee': new_attendee.format()
            }), 201
    else:
        return jsonify({'error': 'Invalid input'}), 400       
        

# A model is stored within a table with a table name
#db.Model class is a base class for all models in Flask-SQLALchemy

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
    
class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    def format(self):
        return{
            'id': self.id,
            'name': self.name
        }    
    
    

class EventRegistration(db.Model):
    __tablename__ = 'attendees'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), unique=True, nullable=False)
    last_name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(100), unique=True, nullable=False)
    job_title = db.Column(db.String(100), unique=True, nullable=False)
    company_size = db.Column(db.String(50), unique=True, nullable=False)
    company_name = db.Column(db.String(100), unique=True, nullable=False)
    subject = db.Column(db.String(250), nullable=False)

    def format(self):

        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'job_title': self.job_title,
            'company_name': self.company_name,
            'company_size': self.company_size,
            'subject': self.subject
        }



    
