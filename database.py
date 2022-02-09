from datetime import datetime

from app import db


class Expense(db.Model):
    __tablename__ = 'expense'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    expense_sum = db.Column(db.Numeric, nullable=False)
    notes = db.Column(db.String(200), nullable=True)
    expense_type_id = db.Column(db.Integer, db.ForeignKey('expense_type.id'), nullable=False)
    expense = db.relationship('ExpenseType', backref=db.backref('expenses', lazy=True))

    def __repr__(self):
        return self.name


class ExpenseType(db.Model):
    __tablename__ = 'expense_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return self.name


db.create_all()
