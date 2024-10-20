from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this to a random secret key
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    numero_carte_national = db.Column(db.String(50), nullable=False)
    assurance = db.Column(db.String(100))
    profession = db.Column(db.String(100))
    maladie = db.Column(db.String(200))
    observation = db.Column(db.Text)
    visits = db.relationship('Visit', backref='patient', lazy=True)

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    acte = db.Column(db.String(200), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    paye = db.Column(db.Float, nullable=False)
    reste = db.Column(db.Float, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'mouna' and password == '123':
            user = User.query.filter_by(username='mouna').first()
            if not user:
                user = User(username='mouna')
                user.set_password('123')
                db.session.add(user)
                db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    patients = Patient.query.all()
    return render_template('index.html', patients=patients)

@app.route('/add_patient', methods=['GET', 'POST'])
@login_required
def add_patient():
    if request.method == 'POST':
        new_patient = Patient(
            nom=request.form['nom'],
            prenom=request.form['prenom'],
            telephone=request.form['telephone'],
            numero_carte_national=request.form['numero_carte_national'],
            assurance=request.form['assurance'],
            profession=request.form['profession'],
            maladie=request.form['maladie'],
            observation=request.form['observation']
        )
        db.session.add(new_patient)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('add_patient.html')

@app.route('/patient/<int:patient_id>')
@login_required
def patient_detail(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return render_template('patient_detail.html', patient=patient)

@app.route('/add_visit/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def add_visit(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if request.method == 'POST':
        new_visit = Visit(
            date=datetime.strptime(request.form['date'], '%Y-%m-%d').date(),
            acte=request.form['acte'],
            prix=float(request.form['prix']),
            paye=float(request.form['paye']),
            reste=float(request.form['prix']) - float(request.form['paye']),
            patient_id=patient.id
        )
        db.session.add(new_visit)
        db.session.commit()
        return redirect(url_for('patient_detail', patient_id=patient.id))
    
    return render_template('add_visit.html', patient=patient)

@app.route('/search')
@login_required
def search():
    query = request.args.get('query')
    patients = Patient.query.filter(
        (Patient.nom.contains(query)) |
        (Patient.prenom.contains(query)) |
        (Patient.numero_carte_national.contains(query))
    ).all()
    return render_template('index.html', patients=patients)

@app.route('/live_search')
@login_required
def live_search():
    query = request.args.get('query', '')
    patients = Patient.query.filter(
        (Patient.nom.contains(query)) |
        (Patient.prenom.contains(query)) |
        (Patient.numero_carte_national.contains(query))
    ).all()
    results = [
        {
            'id': patient.id,
            'nom': patient.nom,
            'prenom': patient.prenom,
            'telephone': patient.telephone,
            'numero_carte_national': patient.numero_carte_national
        }
        for patient in patients
    ]
    return jsonify(results)

@app.route('/edit_patient/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if request.method == 'POST':
        patient.nom = request.form['nom']
        patient.prenom = request.form['prenom']
        patient.telephone = request.form['telephone']
        patient.numero_carte_national = request.form['numero_carte_national']
        patient.assurance = request.form['assurance']
        patient.profession = request.form['profession']
        patient.maladie = request.form['maladie']
        patient.observation = request.form['observation']
        db.session.commit()
        return redirect(url_for('patient_detail', patient_id=patient.id))
    return render_template('edit_patient.html', patient=patient)

@app.route('/delete_patient/<int:patient_id>', methods=['POST'])
@login_required
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/unpaid_balances')
@login_required
def unpaid_balances():
    # Récupérer tous les patients avec des visites impayées
    patients_with_unpaid = db.session.query(Patient).join(Visit).filter(Visit.reste > 0).distinct().all()
    
    # Calculer le total impayé pour chaque patient
    patient_balances = []
    for patient in patients_with_unpaid:
        total_unpaid = sum(visit.reste for visit in patient.visits if visit.reste > 0)
        patient_balances.append({
            'patient': patient,
            'total_unpaid': total_unpaid
        })
    
    return render_template('unpaid_balances.html', patient_balances=patient_balances)

# Add these lines at the end of your app.py file, just before if __name__ == '__main__':
with app.app_context():
    # This will drop all existing tables
    db.create_all()  # This will create new tables based on your current models
    # Create a default user
    if not User.query.filter_by(username='admin').first():
        user = User(username='admin')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
    # Create the 'mouna' user if it doesn't exist
    if not User.query.filter_by(username='mouna').first():
        user = User(username='mouna')
        user.set_password('123')
        db.session.add(user)
        db.session.commit()
if __name__ == '__main__':
    app.run(debug=True)
