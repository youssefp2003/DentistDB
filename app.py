from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this to a random secret key
app.config['UPLOAD_FOLDER'] = 'static/uploads/xrays'  # Add this line
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

UPLOAD_FOLDER = 'static/uploads/xrays'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

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
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    telephone = db.Column(db.String(20))
    numero_carte_national = db.Column(db.String(50))
    assurance = db.Column(db.String(100))
    profession = db.Column(db.String(100))
    maladie = db.Column(db.String(200))
    observation = db.Column(db.Text)
    xray_photo = db.Column(db.String(255))  # Store the path to the X-ray photo
    visits = db.relationship('Visit', backref='patient', lazy=True)

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    acte = db.Column(db.Text)  
    prix = db.Column(db.Float)
    paye = db.Column(db.Float)
    reste = db.Column(db.Float)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash('Veuillez remplir tous les champs', 'error')
            return render_template('login.html')
            
        user = User.query.filter_by(username=username).first()
        
        if not user:
            flash('Utilisateur non trouvé. Vérifiez votre nom d\'utilisateur ou contactez l\'administrateur.', 'error')
            return render_template('login.html')
            
        if not user.check_password(password):
            flash('Mot de passe incorrect. Veuillez réessayer.', 'error')
            return render_template('login.html')
            
        # If we get here, both username and password are correct
        login_user(user)
        return redirect(url_for('index'))
        
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
        date_str = request.form.get('date', '')
        acte = request.form.get('acte', '')
        prix_str = request.form.get('prix', '0')
        paye_str = request.form.get('paye', '0')
        
        # Convertir les chaînes vides en 0
        prix = float(prix_str) if prix_str.strip() else 0
        paye = float(paye_str) if paye_str.strip() else 0
        
        new_visit = Visit(
            date=datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.now().date(),
            acte=acte,
            prix=prix,
            paye=paye,
            reste=prix - paye,
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

@app.route('/edit_visit/<int:visit_id>', methods=['GET', 'POST'])
@login_required
def edit_visit(visit_id):
    visit = Visit.query.get_or_404(visit_id)
    if request.method == 'POST':
        date_str = request.form.get('date', '')
        acte = request.form.get('acte', '')
        prix_str = request.form.get('prix', '0')
        paye_str = request.form.get('paye', '0')
        
        # Convert empty strings to 0
        prix = float(prix_str) if prix_str.strip() else 0
        paye = float(paye_str) if paye_str.strip() else 0
        
        visit.date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.now().date()
        visit.acte = acte
        visit.prix = prix
        visit.paye = paye
        visit.reste = prix - paye
        
        db.session.commit()
        return redirect(url_for('patient_detail', patient_id=visit.patient_id))
    
    return render_template('edit_visit.html', visit=visit)

@app.route('/tooth_diagram/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def tooth_diagram(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if request.method == 'POST':
        # Here we would handle saving tooth status updates
        # This will be implemented with AJAX calls
        pass
    return render_template('tooth_diagram.html', patient=patient)

@app.route('/upload_xray/<int:patient_id>', methods=['POST'])
@login_required
def upload_xray(patient_id):
    if 'xray' not in request.files:
        flash('Aucun fichier sélectionné', 'error')
        return redirect(url_for('patient_detail', patient_id=patient_id))
    
    file = request.files['xray']
    if file.filename == '':
        flash('Aucun fichier sélectionné', 'error')
        return redirect(url_for('patient_detail', patient_id=patient_id))
    
    if file and allowed_file(file.filename):
        # Create upload directory if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Generate unique filename
        filename = f"xray_{patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file.filename.rsplit('.', 1)[1].lower()}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the file
        file.save(file_path)
        
        # Update patient record
        patient = Patient.query.get_or_404(patient_id)
        if patient.xray_photo:  # Delete old file if exists
            old_file = os.path.join(app.config['UPLOAD_FOLDER'], patient.xray_photo)
            if os.path.exists(old_file):
                os.remove(old_file)
        
        patient.xray_photo = filename
        db.session.commit()
        return redirect(url_for('patient_detail', patient_id=patient_id))
    
    flash('Type de fichier non autorisé', 'error')
    return redirect(url_for('patient_detail', patient_id=patient_id))

@app.route('/delete_xray/<int:patient_id>', methods=['POST'])
@login_required
def delete_xray(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if patient.xray_photo:
        # Delete the file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], patient.xray_photo)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Clear the database reference
        patient.xray_photo = None
        db.session.commit()
    
    return redirect(url_for('patient_detail', patient_id=patient_id))

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.static_folder, 'uploads'), filename)

if __name__ == '__main__':
    with app.app_context():
        # Drop all existing tables
        db.drop_all()
        # Create new tables with updated schema
        db.create_all()
        
        # Create default admin user if it doesn't exist
        admin_user = User.query.filter_by(username='mouna').first()
        if not admin_user:
            admin_user = User(username='mouna')
            admin_user.set_password('123')
            db.session.add(admin_user)
            db.session.commit()
            
    app.run(debug=True)
