from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from faker import Faker
from db import session, engine
import random
from models import Base, Student, Group, Teacher, Subject, Grade  # Import models

fake = Faker()

PREDEFINED_SUBJECTS = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "History",
    "Geography",
    "English",
    "Computer Science",
    "Physical Education",
    "Art",
]


def seed_database():
    # Clear all tables (for repeatable seeds)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    groups = [Group(name=f"Group {i+1}") for i in range(3)]
    session.add_all(groups)
    session.commit()

    teachers = [Teacher(name=fake.name()) for _ in range(random.randint(3, 5))]
    session.add_all(teachers)
    session.commit()

    subjects = [
        Subject(name=subject, teacher=random.choice(teachers))
        for subject in PREDEFINED_SUBJECTS
    ]
    session.add_all(subjects)
    session.commit()

    students = [
        Student(name=fake.name(), group=random.choice(groups))
        for _ in range(random.randint(30, 50))
    ]
    session.add_all(students)
    session.commit()

    grades = []
    for student in students:
        for _ in range(random.randint(15, 20)):
            subject = random.choice(subjects)
            grade = Grade(
                student=student,
                subject=subject,
                grade=round(random.uniform(1, 5), 2),
                received_at=fake.date_time_this_year(),
            )
            grades.append(grade)
    session.add_all(grades)
    session.commit()

    print("Database seeded successfully!")


if __name__ == "__main__":
    try:
        seed_database()
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        session.close()
