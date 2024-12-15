from flask import Flask, request, render_template, redirect, url_for, flash, session
import spacy
import os
import pyotp

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# In-memory user storage (replace with a database in production)
users = {}

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Create uploads directory if it doesn't exist
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def generate_totp_secret(email):
    """Generate a TOTP secret and provisioning URI."""
    totp = pyotp.TOTP(pyotp.random_base32())
    return totp.secret, totp.provisioning_uri(name=email, issuer_name="YourAppName")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user' not in session:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('index'))

    summary = None
    keywords = None
    informality_status = None

    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file part", "danger")
            return redirect(url_for('home'))

        file = request.files['file']
        
        if file.filename == '':
            flash("No selected file", "danger")
            return redirect(url_for('home'))
        
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            summary, keywords, informality_status = process_document(filepath)

    return render_template('home.html', user=session['user'], summary=summary, keywords=keywords, informality_status=informality_status)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email in users:
            flash('Email already exists. Please log in.', 'danger')
            return redirect(url_for('login'))
        
        # Generate TOTP secret and provisioning URI
        totp_secret, provisioning_uri = generate_totp_secret(email)
        
        # Store user credentials and TOTP secret
        users[email] = {'password': password, 'totp_secret': totp_secret}
        
        flash(f'Sign up successful! Scan this QR code with your authenticator app: {provisioning_uri}', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email in users and users[email]['password'] == password:
            session['user'] = email  # Store user in session
            flash('Login successful! Please enter the TOTP token.', 'success')
            return redirect(url_for('verify_totp'))  # Redirect to TOTP verification page
        
        flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/verify_totp', methods=['GET', 'POST'])
def verify_totp():
    if request.method == 'POST':
        token = request.form.get('token')
        email = session.get('user')
        
        if email:
            totp_secret = users[email]['totp_secret']
            totp = pyotp.TOTP(totp_secret)

            if totp.verify(token):
                flash('TOTP verification successful!', 'success')
                return redirect(url_for('home'))
        
        flash('Invalid TOTP token. Please try again.', 'danger')

    return render_template('verify_totp.html')

def process_document(filepath):
    encodings = ['utf-8', 'latin-1', 'utf-16']
    text = ""
    
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as file:
                text = file.read()
            break
        except (UnicodeDecodeError, FileNotFoundError):
            continue
    
    if not text:
        return "Error: Unable to read the document with supported encodings.", [], ""

    doc = nlp(text)
    keywords = [chunk.text for chunk in doc.noun_chunks]
    summary = ' '.join([sent.text for sent in doc.sents][:2])
    
    informal_keywords = ["gonna", "wanna", "gotta", "kinda", "sorta", "hey", "yo"]
    informality_status = "Informal language detected." if any(word in text.lower() for word in informal_keywords) else "Language is formal."
    
    return summary, keywords, informality_status

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('totp_secret', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)










