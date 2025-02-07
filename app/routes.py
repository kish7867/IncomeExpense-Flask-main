from app import app
from flask import render_template,flash,redirect, url_for,get_flashed_messages
from app.form import UserInputForm
from app.models import IncomeExpenses
from app import db
import json

@app.route("/")
def index():
    entries = IncomeExpenses.query.order_by(IncomeExpenses.date.desc()).all()
    return render_template('index.html',title='index', entries = entries)


@app.route("/add", methods=["GET","POST"])
def add_expense():
    form = UserInputForm()
    if form.validate_on_submit():
        entry = IncomeExpenses(type= form.type.data, amount=form.amount.data, category=form.category.data)
        db.session.add(entry)
        db.session.commit()
        flash("Successful entry", 'success')
        return redirect(url_for('index'))
    return render_template("add.html", title="Add expenses", form=form)

@app.route('/delete/<int:entry_id>')
def delete(entry_id):
    entry = IncomeExpenses.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Deletion was successful", 'success')
    return redirect(url_for('index'))

@app.route("/dashboard")
def dashboard():
    income_vs_expenses = db.session.query(db.func.sum(IncomeExpenses.amount),IncomeExpenses.type).group_by(IncomeExpenses.type).order_by(IncomeExpenses.type).all()

    category_comparison = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.category).group_by(IncomeExpenses.category).order_by(IncomeExpenses.category).all()


    dates = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.date).group_by(IncomeExpenses.date).order_by(IncomeExpenses.date).all()

    income_category = []
    for amounts, _ in category_comparison:
        income_category.append(amounts)

    income_expense = []
    for total_amount, _ in income_vs_expenses:
        income_expense.append(total_amount)

    over_time_expenditure =[]
    dates_labels=[]
    for amount,date in dates:
        over_time_expenditure.append(amount)
        dates_labels.append(date.strftime("%m-%d-%Y"))

    return render_template("dashboard.html", income_vs_expenses=json.dumps(income_expense),income_category=json.dumps(income_category),
    over_time_expenditure= json.dumps(over_time_expenditure),
    dates_labels=json.dumps(dates_labels)
    )

