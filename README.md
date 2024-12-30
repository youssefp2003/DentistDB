# **DentisteDB - Dental Practice Management System**  
DentisteDB is an all-in-one dental practice management solution designed to streamline patient management, appointments, and medical records for dental practitioners.  

---

## **Features**  

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

### **Security**  
- Robust user authentication system for secure access.  
- Password-protected login/logout functionality.  
- Ensure patient data is protected and complies with privacy regulations.  

---

## **Technical Requirements**  

Ensure the following dependencies are installed to run DentisteDB:  

- **Python**: Version 3.x  
- **Flask**: Version 2.3.3  
- **Flask-SQLAlchemy**: Version 3.1.1  
- **Flask-Login**: Version 0.6.2  
- **PyQt5**: Version 5.15.9  
- **PyQtWebEngine**: Version 5.15.6  
- **Werkzeug**: Version 2.3.7  
- **PyInstaller**: Version 5.13.2  

---

## **Installation**  

Follow these steps to install DentisteDB:  

1. **Clone the Repository**:  
   ```bash  
   git clone <repository-link>  
   cd DentisteDB  
   ```  

2. **Install Dependencies**:  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. **Initialize the Database**:  
   ```bash  
   python app.py  
   ```  

---

## **Usage**  

1. **Start the Application**:  
   ```bash  
   python app.py  
   ```  

2. **Access the Interface**:  
   Open your web browser and navigate to:  
   [http://localhost:5000](http://localhost:5000)  

3. **Log In**:  
   Use your credentials to access the system.  

4. **Begin Managing Your Dental Practice**:  
   - Add patients, track visits, and manage dental records efficiently.  

---

## **File Structure**  

- **`app.py`**: Main application file containing routes and database models.  
- **`desktop_app.py`**: Desktop application wrapper.  
- **`templates/`**: HTML templates for the web interface.  
- **`static/`**: Static files (CSS, JavaScript, images).  
- **`instance/`**: Database files.  
- **`requirements.txt`**: List of Python dependencies.  

---

## **Database Structure**  

### **Patients Table**  
Stores patient details, including:  
- Personal information (name, contact details).  
- Medical history.  
- Insurance details.  
- X-ray images.  

### **Visits Table**  
Tracks patient visits with:  
- Detailed treatment records.  
- Pricing and payment details.  
- Visit dates and other relevant information.  

---

## **Contributing**  

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

## **License**  

This project is proprietary software. All rights reserved.  
