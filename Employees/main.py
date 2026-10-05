from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import Student
from schemas import StudentCreate, StudentResponse

app = FastAPI()



# Create table
Base.metadata.create_all(bind=engine)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def home():
    return {"message": "Welcome to Students API running on FastAPI"}


@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


@app.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


@app.post("/students", response_model=StudentResponse)
def add_student(student: StudentCreate,
                db: Session = Depends(get_db)):

    new_student = Student(
        name=student.name,
        course=student.course
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    updated_student: StudentCreate,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student.name = updated_student.name
    student.course = updated_student.course

    db.commit()
    db.refresh(student)

    return student


@app.delete("/students/{student_id}")
def delete_student(student_id: int,
                   db: Session = Depends(get_db)):

    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully"}