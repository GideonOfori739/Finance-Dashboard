import os
import sqlite3
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import create_connection, create_table
from tracker import Tracker
from models import Expense, Habit
from analytics import category_totals, weekly_spending



tracker = Tracker()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "your_secret_key"
)
create_table()



def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "error")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    
    return wrapped_view

@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Username and password are required.", "error")
            return render_template("register.html")

        if len(password) < 8:
            flash("Password must be at least 8 characters long.", "error")
            return render_template("register.html")
        hashed_password = generate_password_hash(password)

        conn = create_connection()
        try:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            flash("Username already exists. Please choose a different one.", "error")
            return render_template("register.html")
        finally:
            conn.close()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Username and password are required.", "error")
            return render_template("login.html")

        conn = create_connection()
        user = conn.execute(
            "SELECT id,username,password FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        conn.close()

        if user is None or not check_password_hash(user["password"], password):
            flash("Invalid username or password.", "error")
            return render_template("login.html")

        session.clear()
        session["user_id"] = user["id"]
        session["username"] = user["username"]

        flash("Login successful!", "success")
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))



@app.route("/dashboard")
@login_required
def dashboard():
    user_id = session["user_id"]
    expenses = tracker.get_expenses(user_id)
    summary = tracker.summarise_by_category(user_id)
    habits = tracker.get_habits(user_id)
    weekly_summary = weekly_spending(expenses)
    total_expenses = sum(expense.amount for expense in expenses)
    return render_template(
            "dashboard.html",
            username=session["username"],
            expenses=expenses,
            summary=summary,
            weekly_summary = weekly_summary,
            total_expenses=total_expenses,
            habits = habits
              )
            
        
        



@app.route("/expenses/add", methods=["POST"])
@login_required
def add_expense():
    from models import Expense
    amount_text = request.form.get("amount", "").strip()
    category = request.form.get("category", "").strip()
    description = request.form.get("description", "").strip()
    date = request.form.get("date", "").strip()

    try:
        amount = float(amount_text)

        if amount <= 0:
            raise ValueError

        if not category or not date:
            raise ValueError

    except ValueError:
        flash("Please provide valid expense details.", "error")
        return redirect(url_for("dashboard"))

    expense = Expense(
        amount=amount,
        category=category,
        description=description,
        date=date,
    )

    tracker.add_expense(
        user_id=session["user_id"],
        expense=expense
    )
    flash("Expense added successfully!", "success")
    return redirect(url_for("dashboard"))

@app.route("/expenses/delete/<int:expense_id>", methods=["POST"])
@login_required
def delete_expense(expense_id):
    user_id =  session["user_id"]

    deleted = tracker.remove_expense(
        expense_id= expense_id,
        user_id= user_id
    )

    if deleted:
        flash("Expense deleted successfully!", "success")
    else:
        flash("Expense not found or.", "error")

    return redirect(url_for("dashboard"))

@app.route("/habits/add", methods=["POST"])
@login_required
def add_habit():
    name = request.form.get("name", "").strip()
    date = request.form.get("date", "").strip()

    if not name or not date:
        flash("Please provide valid habit details.", "error")
        return redirect(url_for("dashboard"))

    habit = Habit(
        name=name,
        date=date
    )

    tracker.add_habit(
        user_id=session["user_id"],
        habit=habit
    )
    flash("Habit added successfully!", "success")
    return redirect(url_for("dashboard"))


@app.route("/habits/complete/<int:habit_id>", methods=["POST"])
@login_required
def complete_habit(habit_id):
    updated = tracker.mark_habit_completed(
        habit_id=habit_id,
        user_id=session["user_id"]
    )

    if updated:
        flash("Habit marked as completed!", "success")
    else:
        flash("Habit not found or already completed.", "error")

    return redirect(url_for("dashboard"))

@app.route("/habits/delete/<int:habit_id>", methods =["POST"])
@login_required
def delete_habit(habit_id):
    deleted = tracker.remove_habit(
        habit_id =habit_id,
        user_id= session["user_id"]
    )

    if deleted:
        flash("Habit deleted succesfully ", "succes")
    else:
        flash("Habit not found.", "errror")

    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)
