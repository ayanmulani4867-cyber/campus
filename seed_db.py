"""
Seed script to populate Campus Connect with comprehensive realistic institutional data.
"""
from datetime import datetime, date, time, timedelta
from werkzeug.security import generate_password_hash
from app import create_app
from app.extensions import db
from app.models.user import User, Role
from app.models.department import Department
from app.models.course import Course
from app.models.semester import Semester
from app.models.academic_session import AcademicSession
from app.models.class_division import ClassDivision
from app.models.subject import Subject
from app.models.faculty import Faculty
from app.models.student import Student
from app.models.timetable import Timetable
from app.models.attendance import AttendanceSession, AttendanceRecord
from app.models.assignment import Assignment, AssignmentSubmission, StudyMaterial
from app.models.exam import Exam, ExamResult
from app.models.fee import FeeStructure, StudentFee, FeePayment
from app.models.leave import LeaveRequest
from app.models.notice import Notice
from app.models.feedback import Feedback
from app.models.complaint import Complaint
from app.models.event import Event, EventRegistration
from app.models.certificate import CertificateRequest
from app.models.audit_log import AuditLog
from app.models.notification import Notification
from app.utils.helpers import generate_receipt_number, generate_transaction_id, generate_certificate_code


def seed_database():
    app = create_app('development')
    with app.app_context():
        print("Recreating database tables...")
        db.drop_all()
        db.create_all()

        print("Seeding Academic Sessions & Semesters...")
        session_2025_26 = AcademicSession(name='2025-26', start_year=2025, end_year=2026, is_current=True)
        session_2024_25 = AcademicSession(name='2024-25', start_year=2024, end_year=2025, is_current=False)
        db.session.add_all([session_2025_26, session_2024_25])
        db.session.flush()

        semesters = []
        for i in range(1, 9):
            sem = Semester(number=i, name=f'Semester {i}', is_active=True)
            semesters.append(sem)
            db.session.add(sem)
        db.session.flush()

        print("Seeding Departments & Courses...")
        dept_cse = Department(name='Computer Science & Engineering', code='CSE', description='Department of Computer Science & Engineering with state-of-the-art AI & Cloud labs.')
        dept_ece = Department(name='Electronics & Communication Engineering', code='ECE', description='Department of ECE focusing on Embedded Systems, VLSI, and IoT.')
        dept_it = Department(name='Information Technology', code='IT', description='Department of IT focusing on Software Architecture, Cybersecurity, and Data Analytics.')
        dept_mech = Department(name='Mechanical Engineering', code='MECH', description='Department of Mechanical Engineering with advanced Robotics and CAD/CAM labs.')
        dept_mba = Department(name='Management Studies', code='MBA', description='School of Management offering finance, marketing, and systems specialization.')

        db.session.add_all([dept_cse, dept_ece, dept_it, dept_mech, dept_mba])
        db.session.flush()

        course_btech_cse = Course(name='B.Tech Computer Science & Engineering', code='BT-CSE', department_id=dept_cse.id, duration_years=4, total_semesters=8)
        course_btech_ece = Course(name='B.Tech Electronics & Communication', code='BT-ECE', department_id=dept_ece.id, duration_years=4, total_semesters=8)
        course_btech_it = Course(name='B.Tech Information Technology', code='BT-IT', department_id=dept_it.id, duration_years=4, total_semesters=8)
        course_mba = Course(name='Master of Business Administration', code='MBA', department_id=dept_mba.id, duration_years=2, total_semesters=4)

        db.session.add_all([course_btech_cse, course_btech_ece, course_btech_it, course_mba])
        db.session.flush()

        print("Seeding Class Divisions...")
        div_cse_4a = ClassDivision(name='A', department_id=dept_cse.id, course_id=course_btech_cse.id, semester_id=semesters[3].id, session_id=session_2025_26.id, room_number='LT-301')
        div_cse_4b = ClassDivision(name='B', department_id=dept_cse.id, course_id=course_btech_cse.id, semester_id=semesters[3].id, session_id=session_2025_26.id, room_number='LT-302')
        div_ece_4a = ClassDivision(name='A', department_id=dept_ece.id, course_id=course_btech_ece.id, semester_id=semesters[3].id, session_id=session_2025_26.id, room_number='LT-201')
        div_it_4a = ClassDivision(name='A', department_id=dept_it.id, course_id=course_btech_it.id, semester_id=semesters[3].id, session_id=session_2025_26.id, room_number='LT-104')

        db.session.add_all([div_cse_4a, div_cse_4b, div_ece_4a, div_it_4a])
        db.session.flush()

        print("Seeding Users & Faculty...")
        # 1. Admin User
        user_admin = User(
            username='admin',
            email='admin@campusconnect.edu',
            password_hash=generate_password_hash('admin'),
            role=Role.ADMIN,
            first_name='Ayan',
            last_name='',
            phone='+91 98765 00001',
            must_change_password=True,
            is_active=True
        )
        db.session.add(user_admin)

        # 2. HOD User & Faculty
        user_hod = User(
            username='hod_cse',
            email='hod.cse@campusconnect.edu',
            password_hash=generate_password_hash('hod123'),
            role=Role.HOD,
            first_name='Dr. Rajesh',
            last_name='Sharma',
            phone='+91 98765 00002',
            is_active=True
        )
        db.session.add(user_hod)
        db.session.flush()

        faculty_hod = Faculty(
            user_id=user_hod.id,
            faculty_id='FAC-CSE-001',
            employee_id='EMP1001',
            first_name='Dr. Rajesh',
            last_name='Sharma',
            full_name='Dr. Rajesh Sharma',
            designation='Professor & Head of Department',
            department_id=dept_cse.id,
            official_email='hod.cse@campusconnect.edu',
            mobile='+91 98765 00002',
            qualification='Ph.D. in Computer Science (IIT Bombay)',
            specialization='Distributed Systems & Cloud Computing',
            joining_date=date(2016, 7, 1),
            status='Active',
            blood_group='O+'
        )
        db.session.add(faculty_hod)
        db.session.flush()
        dept_cse.hod_faculty_id = faculty_hod.id

        # 3. Faculty Member User & Record
        user_faculty = User(
            username='faculty',
            email='faculty@campusconnect.edu',
            password_hash=generate_password_hash('faculty123'),
            role=Role.FACULTY,
            first_name='Prof. Priya',
            last_name='Nair',
            phone='+91 98765 00003',
            is_active=True
        )
        db.session.add(user_faculty)
        db.session.flush()

        faculty_priya = Faculty(
            user_id=user_faculty.id,
            faculty_id='FAC-CSE-002',
            employee_id='EMP1002',
            first_name='Prof. Priya',
            last_name='Nair',
            full_name='Prof. Priya Nair',
            designation='Associate Professor',
            department_id=dept_cse.id,
            official_email='faculty@campusconnect.edu',
            mobile='+91 98765 00003',
            qualification='M.Tech CSE, Ph.D. (Pursuing)',
            specialization='Database Systems & Web Technologies',
            joining_date=date(2019, 8, 15),
            status='Active',
            blood_group='B+'
        )
        db.session.add(faculty_priya)
        db.session.flush()

        # 4. Student User & Record
        user_student = User(
            username='student',
            email='student@campusconnect.edu',
            password_hash=generate_password_hash('student123'),
            role=Role.STUDENT,
            first_name='Aarav',
            last_name='Patel',
            phone='+91 98765 11111',
            is_active=True
        )
        db.session.add(user_student)
        db.session.flush()

        student_aarav = Student(
            user_id=user_student.id,
            student_id='STD-2023-0101',
            enrollment_no='EN2023CSE0101',
            admission_no='ADM-2023-0101',
            roll_no='23CS401',
            first_name='Aarav',
            last_name='Patel',
            full_name='Aarav Patel',
            dob=date(2004, 5, 14),
            gender='Male',
            blood_group='O+',
            college_email='student@campusconnect.edu',
            mobile='+91 98765 11111',
            department_id=dept_cse.id,
            course_id=course_btech_cse.id,
            semester_id=semesters[3].id,
            session_id=session_2025_26.id,
            division_id=div_cse_4a.id,
            admission_date=date(2023, 8, 1),
            batch='2023-2027',
            status='Active',
            father_name='Vikram Patel',
            father_phone='+91 98765 22222',
            father_occupation='Software Architect',
            mother_name='Sunita Patel',
            curr_address_line1='Flat 402, Green Meadows, Tech Park Road',
            curr_city='Knowledge City',
            curr_state='State Capital',
            curr_pincode='560100',
            emergency_name='Vikram Patel',
            emergency_phone='+91 98765 22222',
            emergency_relation='Father'
        )
        db.session.add(student_aarav)

        # Add 5 more classmates in CSE-4A for realistic attendance & rankings
        classmates_data = [
            ('Ananya', 'Deshmukh', 'Female', 'STD-2023-0102', 'EN2023CSE0102', '23CS402', 'ananya.d@campusconnect.edu', 'A+'),
            ('Rohan', 'Verma', 'Male', 'STD-2023-0103', 'EN2023CSE0103', '23CS403', 'rohan.v@campusconnect.edu', 'B+'),
            ('Sneha', 'Iyer', 'Female', 'STD-2023-0104', 'EN2023CSE0104', '23CS404', 'sneha.i@campusconnect.edu', 'AB+'),
            ('Dev', 'Kapoor', 'Male', 'STD-2023-0105', 'EN2023CSE0105', '23CS405', 'dev.k@campusconnect.edu', 'O-'),
            ('Tanvi', 'Mehta', 'Female', 'STD-2023-0106', 'EN2023CSE0106', '23CS406', 'tanvi.m@campusconnect.edu', 'A-'),
        ]
        classmate_students = [student_aarav]
        for fn, ln, gen, sid, enr, rno, mail, bg in classmates_data:
            u = User(
                username=sid.lower().replace('-', '_'),
                email=mail,
                password_hash=generate_password_hash('student123'),
                role=Role.STUDENT,
                first_name=fn,
                last_name=ln,
                is_active=True
            )
            db.session.add(u)
            db.session.flush()
            std = Student(
                user_id=u.id,
                student_id=sid,
                enrollment_no=enr,
                admission_no=f"ADM-{sid[4:]}",
                roll_no=rno,
                first_name=fn,
                last_name=ln,
                full_name=f"{fn} {ln}",
                dob=date(2004, 3, 20),
                gender=gen,
                blood_group=bg,
                college_email=mail,
                mobile=f'+91 98765 {rno[-3:]}00',
                department_id=dept_cse.id,
                course_id=course_btech_cse.id,
                semester_id=semesters[3].id,
                session_id=session_2025_26.id,
                division_id=div_cse_4a.id,
                admission_date=date(2023, 8, 1),
                batch='2023-2027',
                status='Active',
                father_name=f'{ln} Senior',
                father_phone='+91 98765 99999',
                curr_city='Knowledge City',
                curr_state='State Capital',
                curr_pincode='560100'
            )
            db.session.add(std)
            classmate_students.append(std)

        db.session.flush()

        print("Seeding Subjects...")
        sub_dbms = Subject(name='Database Management Systems', code='CS401', credits=4, subject_type='Theory', department_id=dept_cse.id, course_id=course_btech_cse.id, semester_id=semesters[3].id)
        sub_os = Subject(name='Operating Systems', code='CS402', credits=4, subject_type='Theory', department_id=dept_cse.id, course_id=course_btech_cse.id, semester_id=semesters[3].id)
        sub_dsa = Subject(name='Design & Analysis of Algorithms', code='CS403', credits=4, subject_type='Theory', department_id=dept_cse.id, course_id=course_btech_cse.id, semester_id=semesters[3].id)
        sub_web = Subject(name='Full Stack Web Technologies', code='CS404', credits=3, subject_type='Practical', department_id=dept_cse.id, course_id=course_btech_cse.id, semester_id=semesters[3].id)
        sub_se = Subject(name='Software Engineering & Agile Methodologies', code='CS405', credits=3, subject_type='Theory', department_id=dept_cse.id, course_id=course_btech_cse.id, semester_id=semesters[3].id)

        db.session.add_all([sub_dbms, sub_os, sub_dsa, sub_web, sub_se])
        db.session.flush()

        # Link faculty to subjects
        sub_dbms.assigned_faculty.append(faculty_priya)
        sub_web.assigned_faculty.append(faculty_priya)
        sub_os.assigned_faculty.append(faculty_hod)
        sub_dsa.assigned_faculty.append(faculty_hod)

        # Link faculty to class divisions
        div_cse_4a.assigned_faculty.append(faculty_priya)
        div_cse_4a.assigned_faculty.append(faculty_hod)

        print("Seeding Timetable Slots...")
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        time_slots = [
            (time(9, 0), time(10, 0), sub_dbms, faculty_priya, 'LT-301'),
            (time(10, 0), time(11, 0), sub_os, faculty_hod, 'LT-301'),
            (time(11, 15), time(12, 15), sub_dsa, faculty_hod, 'LT-301'),
            (time(13, 0), time(14, 0), sub_web, faculty_priya, 'Lab-2'),
            (time(14, 0), time(15, 0), sub_se, faculty_priya, 'LT-301'),
        ]
        for d in days:
            for st, et, sub, fac, room in time_slots:
                tt = Timetable(
                    class_division_id=div_cse_4a.id,
                    subject_id=sub.id,
                    faculty_id=fac.id,
                    semester_id=semesters[3].id,
                    session_id=session_2025_26.id,
                    day_of_week=d,
                    start_time=st,
                    end_time=et,
                    room_number=room
                )
                db.session.add(tt)

        print("Seeding Attendance Sessions & Records...")
        # Create 15 past attendance sessions
        today = date.today()
        for offset in range(15, 0, -1):
            sess_date = today - timedelta(days=offset)
            if sess_date.weekday() >= 5:
                continue  # Skip weekends
            att_sess = AttendanceSession(
                class_division_id=div_cse_4a.id,
                subject_id=sub_dbms.id,
                faculty_id=faculty_priya.id,
                date=sess_date,
                time_slot='09:00 - 10:00',
                topic_covered=f'Unit {(offset % 4) + 1}: DBMS Core Concepts Part {offset}'
            )
            db.session.add(att_sess)
            db.session.flush()

            for idx, std in enumerate(classmate_students):
                # Ensure Aarav has ~88% attendance
                status = 'Present'
                if std.id == student_aarav.id and offset in (3, 9):
                    status = 'Absent'
                elif idx % 3 == 0 and offset % 5 == 0:
                    status = 'Absent'

                rec = AttendanceRecord(
                    attendance_session_id=att_sess.id,
                    student_id=std.id,
                    status=status
                )
                db.session.add(rec)

        print("Seeding Assignments & Study Materials...")
        assign1 = Assignment(
            title='Mini Project: Relational Schema Design & Normalization (3NF/BCNF)',
            description='Design a normalized PostgreSQL schema for a hospital management module with ER diagram and 10 complex queries.',
            subject_id=sub_dbms.id,
            class_division_id=div_cse_4a.id,
            faculty_id=faculty_priya.id,
            due_date=datetime.utcnow() + timedelta(days=7),
            max_marks=20.0
        )
        assign2 = Assignment(
            title='Lab Assignment: REST API Backend with Flask & SQLAlchemy',
            description='Implement CRUD endpoints with JWT authentication and unit tests.',
            subject_id=sub_web.id,
            class_division_id=div_cse_4a.id,
            faculty_id=faculty_priya.id,
            due_date=datetime.utcnow() + timedelta(days=12),
            max_marks=25.0
        )
        db.session.add_all([assign1, assign2])
        db.session.flush()

        # Seed student submission for assign1
        subm = AssignmentSubmission(
            assignment_id=assign1.id,
            student_id=student_aarav.id,
            submission_text='Submitted relational schema repository and ER diagrams in PDF format with test queries.',
            submitted_at=datetime.utcnow() - timedelta(days=1),
            marks_obtained=18.5,
            feedback='Excellent normalization work. Foreign key constraints and indexing well specified.',
            evaluated_at=datetime.utcnow() - timedelta(hours=6),
            status='Graded'
        )
        db.session.add(subm)

        # Study materials
        mat1 = StudyMaterial(
            title='Lecture Notes: B-Trees and Query Optimization Techniques',
            description='Comprehensive guide on query execution plans, indexes, and storage engines.',
            subject_id=sub_dbms.id,
            class_division_id=div_cse_4a.id,
            faculty_id=faculty_priya.id,
            file_path='dbms_unit3_notes.pdf',
            file_type='PDF',
            file_size_kb=2450.0
        )
        mat2 = StudyMaterial(
            title='Cheat Sheet: Operating Systems Concurrency & Semaphores',
            description='Quick revision sheet covering mutexes, dining philosophers, and deadlock prevention.',
            subject_id=sub_os.id,
            class_division_id=div_cse_4a.id,
            faculty_id=faculty_hod.id,
            file_path='os_concurrency_cheatsheet.pdf',
            file_type='PDF',
            file_size_kb=1280.0
        )
        db.session.add_all([mat1, mat2])

        print("Seeding Exams & Published Results...")
        exam_midterm = Exam(
            name='Mid-Term Examination Spring 2026',
            exam_type='Midterm',
            subject_id=sub_dbms.id,
            semester_id=semesters[3].id,
            session_id=session_2025_26.id,
            class_division_id=div_cse_4a.id,
            exam_date=today - timedelta(days=20),
            start_time=time(10, 0),
            end_time=time(12, 0),
            max_marks=50.0,
            room_number='LT-301'
        )
        exam_dsa = Exam(
            name='Mid-Term Examination: Algorithms',
            exam_type='Midterm',
            subject_id=sub_dsa.id,
            semester_id=semesters[3].id,
            session_id=session_2025_26.id,
            class_division_id=div_cse_4a.id,
            exam_date=today - timedelta(days=18),
            start_time=time(10, 0),
            end_time=time(12, 0),
            max_marks=50.0,
            room_number='LT-301'
        )
        exam_upcoming = Exam(
            name='End-Semester Theory Examination 2026',
            exam_type='Final',
            subject_id=sub_dbms.id,
            semester_id=semesters[3].id,
            session_id=session_2025_26.id,
            class_division_id=div_cse_4a.id,
            exam_date=today + timedelta(days=25),
            start_time=time(9, 30),
            end_time=time(12, 30),
            max_marks=100.0,
            room_number='Auditorium Hall B'
        )
        db.session.add_all([exam_midterm, exam_dsa, exam_upcoming])
        db.session.flush()

        # Seed exam results for students
        results_seed = [
            (student_aarav, 46.0, 50.0, 'A+', 10.0),
            (classmate_students[1], 48.0, 50.0, 'A+', 10.0),
            (classmate_students[2], 39.0, 50.0, 'A', 9.0),
            (classmate_students[3], 42.0, 50.0, 'A', 9.0),
            (classmate_students[4], 34.0, 50.0, 'B', 8.0),
            (classmate_students[5], 44.0, 50.0, 'A+', 10.0),
        ]
        for std, marks, mm, grade, gp in results_seed:
            er = ExamResult(
                exam_id=exam_midterm.id,
                student_id=std.id,
                subject_id=sub_dbms.id,
                semester_id=semesters[3].id,
                session_id=session_2025_26.id,
                marks_obtained=marks,
                max_marks=mm,
                percentage=(marks / mm) * 100,
                grade=grade,
                grade_point=gp,
                is_passed=True,
                is_published=True,
                status='Published_By_Admin',
                entered_by_faculty_id=faculty_priya.id,
                reviewed_by_hod_id=faculty_hod.id,
                published_by_admin_id=user_admin.id,
                published_at=datetime.utcnow() - timedelta(days=10)
            )
            db.session.add(er)

        print("Seeding Fee Structures, Records & Payments...")
        fee_struct = FeeStructure(
            title='Academic Year 2025-26 - B.Tech Semester 4 Fee',
            course_id=course_btech_cse.id,
            semester_id=semesters[3].id,
            session_id=session_2025_26.id,
            tuition_fee=45000.0,
            library_fee=2000.0,
            lab_fee=5000.0,
            exam_fee=3500.0,
            other_fee=9500.0,
            total_amount=65000.0,
            due_date=today + timedelta(days=30),
            is_active=True
        )
        db.session.add(fee_struct)
        db.session.flush()

        std_fee = StudentFee(
            student_id=student_aarav.id,
            fee_structure_id=fee_struct.id,
            total_amount=65000.0,
            discount_amount=5000.0,
            net_payable=60000.0,
            paid_amount=40000.0,
            pending_amount=20000.0,
            status='Partial',
            due_date=today + timedelta(days=30)
        )
        db.session.add(std_fee)
        db.session.flush()

        payment = FeePayment(
            student_fee_id=std_fee.id,
            student_id=student_aarav.id,
            receipt_number=generate_receipt_number(),
            amount=40000.0,
            payment_mode='Online',
            transaction_id=generate_transaction_id(),
            payment_date=datetime.utcnow() - timedelta(days=15),
            status='Success',
            notes='Semester 4 partial tuition & lab fee payment'
        )
        db.session.add(payment)

        print("Seeding Notices, Leaves, Certificates, Feedback & Events...")
        # Notices
        n1 = Notice(
            title='Campus Placement Drive 2026: Apex Tech & Global Solutions',
            content='We are pleased to announce the upcoming on-campus recruitment drive for final and pre-final year engineering students starting March 10th. Register via the portal.',
            target_audience='ALL',
            department_id=dept_cse.id,
            published_by_id=user_admin.id,
            priority='High',
            is_active=True
        )
        n2 = Notice(
            title='Schedule for Mid-Term Lab Practical Assessments & Project Demos',
            content='All 4th and 6th semester students must submit their laboratory record notebooks and code repositories by Friday.',
            target_audience='STUDENT',
            department_id=dept_cse.id,
            published_by_id=faculty_hod.user_id,
            priority='Normal',
            is_active=True
        )
        n3 = Notice(
            title='Annual National Hackathon "InnovateX 2026" Registrations Open',
            content='Form teams of 3-4 members and participate in the 36-hour hackathon with cash prizes up to INR 1,50,000.',
            target_audience='ALL',
            published_by_id=user_admin.id,
            priority='Urgent',
            is_active=True
        )
        db.session.add_all([n1, n2, n3])

        # Leave application
        leave_app = LeaveRequest(
            user_id=user_student.id,
            student_id=student_aarav.id,
            applicant_role='STUDENT',
            leave_type='Medical',
            start_date=today - timedelta(days=12),
            end_date=today - timedelta(days=10),
            total_days=3,
            reason='Severe viral fever and physician advised bed rest.',
            status='Approved',
            reviewed_by_id=user_hod.id,
            review_comment='Medical certificate verified. Approved.',
            reviewed_at=datetime.utcnow() - timedelta(days=9)
        )
        db.session.add(leave_app)

        # Certificate Request
        cert_req = CertificateRequest(
            student_id=student_aarav.id,
            certificate_type='Bonafide Certificate',
            purpose='Application for National Merit Scholarship Portal',
            status='Approved',
            certificate_number=f"BONA-{today.year}-0412",
            verification_code=generate_certificate_code(),
            approved_by_id=user_admin.id,
            approved_at=datetime.utcnow() - timedelta(days=5),
            issued_date=today - timedelta(days=5)
        )
        db.session.add(cert_req)

        # Feedback
        fb = Feedback(
            student_id=student_aarav.id,
            feedback_type='Faculty',
            faculty_id=faculty_priya.id,
            course_id=course_btech_cse.id,
            department_id=dept_cse.id,
            rating=5,
            clarity_rating=5,
            punctuality_rating=5,
            helpfulness_rating=5,
            comments='Prof. Priya explains query optimization with exceptional clarity and real-world examples.',
            is_anonymous=False
        )
        db.session.add(fb)

        # Complaint
        comp = Complaint(
            ticket_number='TKT-2026-0042',
            student_id=student_aarav.id,
            category='Infrastructure',
            title='Request for Additional Database System Reference Books',
            description='Requesting 5 additional copies of Fundamentals of Database Systems (Elmasri/Navathe 7th Ed) in the CS Departmental Library.',
            status='Resolved',
            priority='Medium',
            assigned_to_id=user_admin.id,
            resolution_notes='Procured and added 6 new copies to Departmental Reference Section.',
            resolved_at=datetime.utcnow() - timedelta(days=2)
        )
        db.session.add(comp)

        # Event
        evt = Event(
            title='InnovateX National AI & Robotics Hackathon 2026',
            description='36-hour non-stop hackathon with tracks in Generative AI, IoT Hardware, and Sustainable Smart Cities.',
            event_type='Hackathon',
            start_datetime=datetime.utcnow() + timedelta(days=14, hours=9),
            end_datetime=datetime.utcnow() + timedelta(days=15, hours=21),
            venue='Central Tech Amphitheater & Innovation Hub',
            created_by_id=user_admin.id,
            max_participants=200,
            registration_deadline=datetime.utcnow() + timedelta(days=10),
            is_open_for_registration=True
        )
        db.session.add(evt)
        db.session.flush()

        evt_reg = EventRegistration(
            event_id=evt.id,
            student_id=student_aarav.id,
            status='Confirmed'
        )
        db.session.add(evt_reg)

        # Notifications
        notif1 = Notification(
            user_id=user_student.id,
            title='Exam Result Published',
            message='Your result for Mid-Term Examination Spring 2026 (CS401) has been published. Grade: A+ (10.0).',
            link='/exams/results',
            notification_type='Academic'
        )
        notif2 = Notification(
            user_id=user_student.id,
            title='Certificate Approved',
            message='Your Bonafide Certificate request has been approved and is ready for download.',
            link='/certificates/',
            notification_type='Administrative'
        )
        db.session.add_all([notif1, notif2])

        db.session.commit()
        print("DATABASE SEEDING COMPLETED SUCCESSFULLY!")


if __name__ == '__main__':
    seed_database()
