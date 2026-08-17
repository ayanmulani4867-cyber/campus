import os
import sys
from app import create_app
from app.extensions import db
from app.models.user import User, Role
from app.models.student import Student
from app.models.faculty import Faculty
from app.models.department import Department
from app.models.course import Course
from app.models.subject import Subject
from app.models.academic import Semester, AcademicSession, ClassDivision


def init_database():
    """Initializes database tables and creates the master Admin user."""
    config_name = os.environ.get('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        print(f"Creating all database tables using environment: {config_name}...")
        db.create_all()

        # Check for initial Admin user
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@campusconnect.edu',
                first_name='Ayan',
                last_name='',
                role=Role.ADMIN,
                must_change_password=True,
                is_active=True
            )
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()
            print("Successfully created initial Admin account:")
            print("   Name:     Ayan")
            print("   Username: admin")
            print("   Password: admin (Hashed, must change on initial sign in)")
            print("   Role:     ADMIN")
        else:
            if not admin.first_name:
                admin.first_name = 'Ayan'
                db.session.commit()
            print(f"Admin account @{admin.username} ({admin.full_name}) already initialized.")


if __name__ == '__main__':
    init_database()
