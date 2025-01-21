---

# 🦷 **DentisteDB - Dental Practice Management System**

DentisteDB is an all-in-one dental practice management solution designed to streamline patient management, appointments, and medical records for dental practitioners. It features a modern interface, secure authentication, and robust functionality to make managing a dental practice efficient and intuitive.

---

## ✨ **Features**

### **Patient Management**
- Add, edit, and manage comprehensive patient profiles.
- Store details such as name, contact information, insurance, and medical history.
- Upload and manage X-ray images efficiently.
- Track patient visits and associated treatments.

### **Visit Tracking**
- Record detailed information about treatments and procedures performed.
- Manage pricing and payment records, including unpaid balances.
- Edit and update visit information as needed.

### **Dental Records**
- Utilize an interactive tooth diagram for detailed records.
- Manage and view X-ray images with ease.
- Track medical history and treatment observations.

### **Search Functionality**
- Quickly search for patient records with live search capabilities.
- Filter and sort patient records for improved efficiency.

### **Financial Management**
- Track unpaid balances for patients.
- View and manage financial summaries for the practice.

### **Security**
- Robust user authentication system for secure access.
- Password-protected login/logout functionality.
- Ensure patient data is protected and complies with privacy regulations.

---

## 🚀 **Technologies Used**

### **Backend**
- **Python 3.x**: Core programming language.
- **Flask**: Lightweight web framework for building scalable web applications.
- **Flask-SQLAlchemy**: ORM for database interactions.
- **SQLite**: Default database for record storage.
- **Flask-Login**: Secure user authentication.
- **Werkzeug**: Password hashing and security utilities.

### **Frontend**
- **HTML5 & CSS3**: Templates and styling.
- **Custom Styles**: Includes tailored styles such as `Login.css` and `style.css`.

### **Desktop Integration**
- **PyQt5**: For building a desktop client.
- **PyQtWebEngine**: Embeds the web interface in the desktop app.

---

## 📦 **Installation**

### Prerequisites
- Install [Python 3.x](https://www.python.org/).
- Ensure `pip` (Python package manager) is installed.

### 1. Clone the Repository
```bash
git clone <repository-link>
cd DentisteDB
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize the Database
Run the Flask app to set up the database:
```bash
python app.py
```

---

## 📂 **File Structure**

```plaintext
DentisteDB/
├── app.py                   # Main Flask application
├── desktop_app.py           # Desktop application wrapper
├── requirements.txt         # Python dependencies
├── src/
│   └── styles/
│       └── Login.css        # Login-specific styles
├── static/                  # Static assets (CSS, uploads, etc.)
│   ├── style.css            # Global stylesheet
│   └── uploads/
│       └── xrays/           # X-ray image storage
└── templates/               # HTML templates for Flask
    ├── add_patient.html     # Form to add a patient
    ├── add_visit.html       # Form to add a visit
    ├── edit_patient.html    # Edit patient details
    ├── edit_visit.html      # Edit visit details
    ├── index.html           # Dashboard
    ├── login.html           # Login page
    ├── patient_detail.html  # Patient profile and visit history
    ├── tooth_diagram.html   # Tooth condition visualization
    └── unpaid_balances.html # List of unpaid balances
```

---

## 🔧 **Technical Requirements**

Dependencies:
- **Python 3.x**
- **Flask 2.3.3**
- **Flask-SQLAlchemy 3.1.1**
- **Flask-Login 0.6.2**
- **PyQt5 5.15.9**
- **PyQtWebEngine 5.15.6**
- **Werkzeug 2.3.7**
- **PyInstaller 5.13.2**

---

## 🖥️ **Usage**

1. **Start the Web Application**
   ```bash
   python app.py
   ```

2. **Access the Interface**
   Open your browser and navigate to:  
   [http://localhost:5000](http://localhost:5000)

3. **Use the Desktop Application**
   Run the desktop wrapper:
   ```bash
   python desktop_app.py
   ```

---

## 🗄️ **Database Structure**

### **Patients Table**
Stores patient details, including:
- Personal information (name, contact details).
- Medical history and insurance details.
- X-ray images.

### **Visits Table**
Tracks patient visits with:
- Treatment records and observations.
- Pricing and payment details.
- Visit dates and relevant information.

---

## 🤝 **Contributing**

Contributions are welcome! Follow these steps to contribute:

1. **Fork the Repository**.
2. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Commit Your Changes**:
   ```bash
   git commit -m "Add YourFeatureName"
   ```

4. **Push to the Branch**:
   ```bash
   git push origin feature/YourFeatureName
   ```

5. **Submit a Pull Request**.

---

## 📄 **License**

This project is proprietary software. All rights reserved.

--- 
