from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from credentials import databaseName, databasePassword
from mail_conn import send_new_request

import datetime

app = Flask(__name__)

# Enable debugging and define the database URL
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:{databasePassword}@localhost/{databaseName}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create the Appliers class and define the fields of the table
class Appliers(db.Model):
    __tablename__ = 'appliers'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(125))
    email = db.Column(db.String(125), unique=True)
    location = db.Column(db.String(25))
    time = db.Column(db.String(25))
    comments = db.Column(db.Text())
    timestamp = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)

    def __init__(self, customer, email, location, time, comments):
        self.customer = customer
        self.email = email
        self.location = location
        self.time = time
        self.comments = comments

# Define the '/' route and render the apply.html template
@app.route('/')
def apply():
    return render_template('apply.html')

# Define the '/submit' route to handle form submissions
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        email = request.form['email']
        location = request.form['location']
        time = request.form['time']
        comments = request.form['comments']

        # Check if required fields are filled out
        if customer == '' or email == '':
            return render_template('apply.html', message='Error! Make sure the Customer Name and Customer Email fields are filled out.')

        # Check if the email has already been submitted
        if db.session.query(Appliers).filter(Appliers.email == email).count() == 0:
            data = Appliers(customer, email, location, time, comments)
            db.session.add(data)
            db.session.commit()
            # Send an email to confirm the submission
            send_new_request(customer, email, location, time, comments)
            return render_template('success.html')
        else:
            return render_template('repeat.html')

# Create the table if it doesn't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
