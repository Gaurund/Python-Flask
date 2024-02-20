from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Faculty:
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    students = db.relationship('Student', backref='student', lazy=True)

    def __repr__(self):
        return f'Faculty({self.id}, {self.name})'


class Student:
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Boolean, nullable=False)
    group = db.Column(db.Integer, nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)

    def __repr__(self):
        return f'Student({self.id}, {self.first_name}, {self.last_name}, {self.age}, {self.gender}, {self.group}'
