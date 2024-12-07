from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from models import Student, Group, Grade, Subject, Teacher
from db import engine, session


# 1. Find the 5 students with the highest average score in all subjects.
def select_1(session: Session):
    result = (
        session.query(Student.name, func.avg(Grade.grade).label("average_score"))
        .join(Grade, Student.id == Grade.student_id)
        .group_by(Student.id)
        .order_by(desc("average_score"))
        .limit(5)
        .all()
    )
    return result


# 2. Find the student with the highest average score in a specific subject.
def select_2(session: Session, subject_name: str):
    result = (
        session.query(Student.name, func.avg(Grade.grade).label("average_score"))
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(desc("average_score"))
        .first()
    )
    return result


# 3. Find the average score in groups in a specific subject.
def select_3(session: Session, subject_name: str):
    result = (
        session.query(Group.name, func.avg(Grade.grade).label("average_score"))
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Group.id)
        .all()
    )
    return result


# 4. Find the average score in the stream (across the entire grade table).
def select_4(session: Session):
    result = session.query(func.avg(Grade.grade).label("average_score")).scalar()
    return result


# 5. Find which courses a certain teacher teaches.
def select_5(session: Session, teacher_id: int):
    result = (
        session.query(Subject.name)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .filter(Teacher.id == teacher_id)
        .all()
    )
    return [r[0] for r in result]


# 6. Find a list of students in a specific group.
def select_6(session: Session, group_name: str):
    result = (
        session.query(Student.name)
        .join(Group, Student.group_id == Group.id)
        .filter(Group.name == group_name)
        .all()
    )
    return [r[0] for r in result]


# 7. Find the grades of students in a separate group in a specific subject.
def select_7(session: Session, group_name: str, subject_name: str):
    result = (
        session.query(Student.name, Grade.grade, Grade.received_at)
        .join(Group, Student.group_id == Group.id)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .all()
    )
    return result


# 8. Find the average score that a certain teacher gives in his subjects.
def select_8(session: Session, teacher_id: int):
    result = (
        session.query(func.avg(Grade.grade).label("average_score"))
        .join(Subject, Grade.subject_id == Subject.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .filter(Teacher.id == teacher_id)
        .scalar()
    )
    return result


# 9. Find a list of courses that a certain student attends.
def select_9(session: Session, student_id: int):
    result = (
        session.query(Subject.name)
        .join(Grade, Subject.id == Grade.subject_id)
        .join(Student, Grade.student_id == Student.id)
        .filter(Student.id == student_id)
        .distinct()
        .all()
    )
    return [r[0] for r in result]


# 10. List of courses that a certain teacher teaches to a certain student.
def select_10(session: Session, teacher_id: int, student_id: int):
    result = (
        session.query(Subject.name)
        .join(Grade, Subject.id == Grade.subject_id)
        .join(Student, Grade.student_id == Student.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .filter(Teacher.id == teacher_id, Student.id == student_id)
        .distinct()
        .all()
    )
    return [r[0] for r in result]


if __name__ == "__main__":
    with Session(engine) as session:
        print(
            "5 students with the highest average score in all subjects: ",
            select_1(session),
        )
        print(
            "Student with the highest average score in Mathematics: ",
            select_2(session, "Mathematics"),
        )
        print("Average score in groups in Biology: ", select_3(session, "Biology"))
        print("Average score in the stream: ", select_4(session))
        print("Courses a certain teacher teaches: ", select_5(session, 1))
        print("List of students in group 1: ", select_6(session, "Group 1"))
        print(
            "Grades for students in group 2 in English: ",
            select_7(session, "Group 1", "English"),
        )
        print(
            "Average score that a certain teacher gives in his subjects: ",
            select_8(session, 2),
        )
        print("List of courses that a certain student attends: ", select_9(session, 10))
        print(
            "List of courses that a certain teacher teaches to a certain student: ",
            select_10(session, 3, 15),
        )
