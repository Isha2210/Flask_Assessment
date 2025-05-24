from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User, Assessment
from database import init_database, get_all_users, get_user_by_username
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Initialize database on first run
with app.app_context():
    init_database(app)

def login_required(f):
    """Decorator to require login for certain routes"""
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/')
def index():
    """Home page - redirect to login if not authenticated, dashboard if authenticated"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Validate input
        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template('login.html')
        
        # Check user credentials
        user = get_user_by_username(username)
        if user and user.check_password(password):
            # Create session
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash(f'Welcome, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page - shows employee list and user info"""
    users = get_all_users()
    current_user = User.query.get(session['user_id'])
    
    # Get user's assessments
    user_assessments = Assessment.query.filter_by(user_id=current_user.id).all()
    
    return render_template('dashboard.html', 
                         users=users, 
                         current_user=current_user,
                         assessments=user_assessments)

@app.route('/logout')
@login_required
def logout():
    """Logout and clear session"""
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}! You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/create_assessment', methods=['POST'])
@login_required
def create_assessment():
    """Create a new assessment (demo functionality)"""
    assessment_name = request.form.get('assessment_name', '').strip()
    
    if assessment_name:
        from database import create_assessment
        create_assessment(session['user_id'], assessment_name)
        flash(f'Assessment "{assessment_name}" created successfully!', 'success')
    else:
        flash('Please enter an assessment name.', 'error')
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)