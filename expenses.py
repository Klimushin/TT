from datetime import datetime, timedelta

from flask import render_template, request, redirect

from app import app, db
from database import ExpenseType, Expense


@app.route('/create-expense-type', methods=['POST', 'GET'])
def create_expense_type():
    if request.method == 'POST':
        name = request.form['name']
        existing_name = ExpenseType.query.filter(ExpenseType.name == name).first()
        if name != str(existing_name):
            expense_type = ExpenseType(name=name)
            try:
                db.session.add(expense_type)
                db.session.commit()
                return redirect('/expense-types')
            except:
                data = f'Database write error!!!'
                return render_template('error.html', data=data)
        else:
            data = f'This name already exists!!!'
            return render_template('app/error.html', data=data)

    else:
        return render_template('app/create-expense-type.html')


@app.route('/expense-types')
def expense_type():
    expense_types = ExpenseType.query.all()
    return render_template('app/expense-types.html', expense_type=expense_types)


@app.route('/expense-type/<int:id>')
def expense_type_detail(id):
    expense_type = ExpenseType.query.get(id)
    expenses = Expense.query.filter(Expense.expense_type_id == id).all()
    total_sum = 0
    for expense in expenses:
        total_sum += expense.expense_sum
    return render_template('app/expense-type-detail.html', expense_type=expense_type, total_sum=total_sum)


@app.route('/expense-type/<int:id>/update', methods=['POST', 'GET'])
def expense_type_update(id):
    expense_type = ExpenseType.query.get(id)
    if Expense.query.filter(Expense.expense_type_id == id).first() is None:
        if request.method == 'POST':
            name = request.form['name']
            existing_name = ExpenseType.query.filter(ExpenseType.name == name).first()
            if expense_type.name == name:
                return redirect('/expense-types')
            else:
                expense_type.name = request.form['name']
                if expense_type.name != str(existing_name):
                    try:
                        db.session.commit()
                        return redirect('/expense-types')
                    except:
                        data = f'Database write error!!!'
                        return render_template('app/error.html', data=data)
                else:
                    data = f'This name already exists!!!'
                    return render_template('app/error.html', data=data)
        else:
            expense_type = ExpenseType.query.get(id)
            return render_template('app/expense-type-update.html', expense_type=expense_type)
    else:
        data = f'Update error. Expense type used!!!'
        return render_template('app/error.html', data=data)


@app.route('/expense-type/<int:id>/delete')
def expense_type_delete(id):
    expense_type = ExpenseType.query.get_or_404(id)
    if Expense.query.filter(Expense.expense_type_id == id).first() is None:
        try:
            db.session.delete(expense_type)
            db.session.commit()
            return redirect('/expense-types')
        except:
            data = f'Delete error!!!'
            return render_template('app/error.html', data=data)
    else:
        data = f'Delete error. Expense type used!!!'
        return render_template('app/error.html', data=data)


@app.route('/create-expense', methods=['POST', 'GET'])
def create_expense():
    if request.method == 'POST':
        name = request.form['name']
        expense_sum = float(request.form['expense_sum'])
        notes = request.form['notes']
        expense_type_id = request.form['expense_type']
        expense = Expense(name=name, expense_sum=expense_sum, notes=notes, expense_type_id=expense_type_id)
        try:
            db.session.add(expense)
            db.session.commit()
            return redirect('/')
        except:
            data = f'Database write error!!!'
            return render_template('app/error.html', data=data)
    else:
        types = ExpenseType.query.all()
        return render_template('app/create-expenses.html', types=types)


@app.route('/')
def expense():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    total_sum = 0
    for el in expenses:
        total_sum += el.expense_sum
    return render_template('app/expenses.html', expenses=expenses, total_sum=total_sum)


@app.route('/expense/<int:id>')
def expense_detail(id):
    expense = Expense.query.get(id)
    return render_template('app/expense-detail.html', expense=expense)


@app.route('/expense/<int:id>/update', methods=['POST', 'GET'])
def expense_update(id):
    expense = Expense.query.get(id)
    if request.method == 'POST':
        expense.name = request.form['name']
        expense.expense_sum = float(request.form['expense_sum'])
        expense.notes = request.form['notes']
        expense.expense_type_id = request.form['expense_type']
        try:
            db.session.commit()
            return redirect('/')
        except:
            data = f'Database write error!!!'
            return render_template('app/error.html', data=data)
    else:
        expense_types = ExpenseType.query.all()
        return render_template('app/expenses-update.html', expense=expense, expense_types=expense_types)


@app.route('/expense/<int:id>/delete')
def expense_delete(id):
    expense = Expense.query.get_or_404(id)
    try:
        db.session.delete(expense)
        db.session.commit()
        return redirect('/')
    except:
        data = f'Delete error!!!'
        return render_template('app/error.html', data=data)


@app.route('/report', methods=['POST', 'GET'])
def report():
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = (datetime.strptime(request.form['end_date'], '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
        expenses = Expense.query.filter(Expense.date.between(start_date, end_date)).all()
        total_expenses = 0
        for expense in expenses:
            total_expenses += expense.expense_sum
        return render_template('app/report-form.html', total_expenses=total_expenses)
    else:
        expenses = Expense.query.all()
        total_expenses = 0
        for el in expenses:
            total_expenses += el.expense_sum
        return render_template('app/report-form.html', total_expenses=total_expenses)
