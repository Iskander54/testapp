from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://user:password@db:5432/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    job = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    comment = db.Column(db.Text, nullable=True)

# Create the database and the database tables
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    return jsonify({
        "data": [{
            'id': contact.id,
            'first_name': contact.first_name,
            'last_name': contact.last_name,
            'job': contact.job,
            'email': contact.email,
            'comment': contact.comment
        } for contact in contacts]
    })

@app.route('/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    contact = Contact.query.get_or_404(id)
    return jsonify({
        'id': contact.id,
        'first_name': contact.first_name,
        'last_name': contact.last_name,
        'job': contact.job,
        'email': contact.email,
        'comment': contact.comment
    })

@app.route('/contacts', methods=['POST'])
def add_contact():
    data = request.get_json()
    new_contact = Contact(
        first_name=data['first_name'],
        last_name=data['last_name'],
        job=data['job'],
        email=data['email'],
        comment=data.get('comment', '')
    )
    db.session.add(new_contact)
    db.session.commit()
    return jsonify({'message': 'Contact added successfully!'})

@app.route('/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    data = request.get_json()
    contact = Contact.query.get_or_404(id)
    contact.first_name = data.get('first_name', contact.first_name)
    contact.last_name = data.get('last_name', contact.last_name)
    contact.job = data.get('job', contact.job)
    contact.email = data.get('email', contact.email)
    contact.comment = data.get('comment', contact.comment)
    db.session.commit()
    return jsonify({'message': 'Contact updated successfully!'})

@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'message': 'Contact deleted successfully!'})

@app.route('/test_db')
def test_db():
    try:
        db.session.execute('SELECT 1')
        return 'Database connection successful!'
    except Exception as e:
        return f'Error connecting to the database: {e}'

if __name__ == '__main__':
    app.run(debug=True)
