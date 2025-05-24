from models import db, User, Assessment
from werkzeug.security import generate_password_hash

def init_database(app):
    """Initialize database and create tables"""
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                role='admin',
                email='admin@company.com'
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
        # Create sample employees if not exist
        employee1 = User.query.filter_by(username='john_doe').first()
        if not employee1:
            employee1 = User(
                username='john_doe',
                role='employee',
                email='john@company.com'
            )
            employee1.set_password('password123')
            db.session.add(employee1)
        
        employee2 = User.query.filter_by(username='jane_smith').first()
        if not employee2:
            employee2 = User(
                username='jane_smith',
                role='employee',
                email='jane@company.com'
            )
            employee2.set_password('password123')
            db.session.add(employee2)
        
        try:
            db.session.commit()
            print("Database initialized successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error initializing database: {e}")

def get_all_users():
    """Get all users from database"""
    return User.query.all()

def get_user_by_username(username):
    """Get user by username"""
    return User.query.filter_by(username=username).first()

def create_assessment(user_id, assessment_name, score=None):
    """Create new assessment record"""
    assessment = Assessment(
        user_id=user_id,
        assessment_name=assessment_name,
        score=score
    )
    db.session.add(assessment)
    db.session.commit()
    return assessment