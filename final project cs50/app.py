import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
import calendar

from helpers import login_required, apology


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///DB.db")

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    if request.method == "POST":
        row = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        if not check_password_hash(row[0]["hash"], request.form.get("old_password")):
            return apology("invalid current password", 400)
        elif not request.form.get("old_password") or not request.form.get("new_password") or not request.form.get("confirmation"):
            return apology("must provide current password, new password and repeat it", 400)
        elif not request.form.get("new_password") == request.form.get("confirmation"):
            return apology("password not confirmed", 400)

        hash = generate_password_hash(request.form.get("new_password"), method='scrypt', salt_length=16)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, session["user_id"])
        flash("Password changed!")
        return redirect("/")

    else:
        return render_template("change.html")


# Register page
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        usernames = [user['username'] for user in db.execute("SELECT username FROM users")]
        if request.form.get("username") in usernames:
            return apology("username already exists", 400)

        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must provide password and repeat it", 400)

        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        hash = generate_password_hash(request.form.get("password"), method='scrypt', salt_length=16)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), hash)
        return redirect("/")

    else:
        return render_template("register.html")


# Main page for this month
@app.route("/", methods=["GET","POST"])
@login_required
def index():
    cal = calendar.HTMLCalendar(firstweekday=0)
    today = date.today()
    theyear = today.year
    themonth = today.month
    month1 = cal.formatmonth(theyear, themonth, withyear=True)

    priorities = db.execute("SELECT * FROM priorities WHERE user_id = ?", session["user_id"])

    events = db.execute("SELECT * FROM events WHERE user_id = ? AND month = ? ORDER BY day ASC", session["user_id"], themonth)

    success = db.execute("SELECT * FROM success WHERE user_id = ? AND month = ? ORDER BY day ASC", session["user_id"], themonth)

    list = db.execute("SELECT * FROM habits_list WHERE user_id = ?", session["user_id"])

    days = 0
    months31 = [1, 3, 5, 7, 8, 10, 12]
    if themonth == 2:
        days = 28
    elif themonth in months31:
        days = 31
    else:
        days = 30


    return render_template("index.html", calendar=month1, priorities=priorities, events=events, success=success, list=list, days=days)

# Delete a priority or event
@app.route("/deletepr", methods=["POST"])
@login_required
def delete():
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM priorities WHERE id = ?", id)
    return redirect("/")


@app.route("/addpr", methods=["POST"])
@login_required
def add():
        ammount = 0
        priorities = db.execute("SELECT * FROM priorities WHERE user_id = ?", session["user_id"])
        for i in priorities:
            if request.form.get("priority") == i["priority"]:
                flash("Priority already added")
                return redirect("/")
            else:
                ammount += 1
                if ammount > 2:
                    flash("Too many priorities!")
                    return redirect("/")
        else:
            priorities = db.execute("INSERT INTO priorities (priority, user_id) VALUES (?, ?)", request.form.get("priority"), session["user_id"])
            return redirect("/")


# Edit events for this month
@app.route("/editevents", methods=["GET"])
@login_required
def editevents():
    month = date.today().month
    events = db.execute("SELECT * FROM events WHERE user_id = ? AND month = ? ORDER BY day ASC", session["user_id"], month)
    days = 0
    months31 = [1, 3, 5, 7, 8, 10, 12]
    if month == 2:
        days = 28
    elif month in months31:
        days = 31
    else:
        days = 30

    return render_template("events.html", events=events, days=days)

@app.route("/addevent", methods=["POST"])
@login_required
def addevent():
    if not request.form.get("day"):
        flash("Choose day")
        return redirect("/editevents")
    elif not request.form.get("event"):
        flash("Empty event")
        return redirect("/editevents")

    today = date.today()
    month = today.month
    db.execute("INSERT INTO events (day, month, event, user_id) VALUES (?, ?, ?, ?)", request.form.get("day"), month, request.form.get("event"), session["user_id"])
    return redirect("/editevents")

@app.route("/deleteevent", methods=["POST"])
@login_required
def deleteevent():
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM events WHERE id = ?", id)
    return redirect("/editevents")


@app.route("/addsuccess", methods=["POST"])
@login_required
def addsuccess():
    if not request.form.get("day"):
        flash("Choose day of success")
        return redirect("/editevents")
    elif not request.form.get("success"):
        flash("Empty field")
        return redirect("/")

    else:
        month = date.today().month
        db.execute("INSERT INTO success (day, month, success, user_id) VALUES (?, ?, ?, ?)", request.form.get("day"), month, request.form.get("success"), session["user_id"])
        flash("WELL DONE!")
        return redirect("/")

@app.route("/deletesuccess", methods=["POST"])
@login_required
def deletesuccess():
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM success WHERE id = ?", id)
    return redirect("/")

# Habit tracker for the current month
@app.route("/addhabit", methods=["GET", "POST"])
@login_required
def addhabit():
    if not request.form.get("newhabit"):
        flash("Empty habit")
        return redirect("/habit")
    db.execute("INSERT INTO habits_list (habit, user_id) VALUES (?, ?)", request.form.get("newhabit"), session["user_id"])
    habit_id = db.execute("SELECT id FROM habits_list WHERE habit = ?", request.form.get("newhabit"))[0]
    day = date.today().day
    month = date.today().month
    for i in range(day):
        db.execute("INSERT INTO habits (habit_id, habit, user_id, day, month, done) VALUES (?, ?, ?, ?, ?, ?)", habit_id["id"], request.form.get("newhabit"), session["user_id"], i + 1, month, "no")
    return redirect("/habit")

@app.route("/deletehabit", methods=["POST"])
@login_required
def deletehabit():
    id = request.form.get("id")
    habits = db.execute("SELECT * FROM habits WHERE habit_id = ?", id)
    if habits:
        db.execute("DELETE FROM habits WHERE habit_id = ?", id)

    db.execute("DELETE FROM habits_list WHERE id = ?", id)
    return redirect("/habit")

@app.route("/habit", methods=["GET", "POST"])
@login_required
def habit():
    if request.method == "GET":
        month = date.today().month
        today = date.today().day
        months31 = [1, 3, 5, 7, 8, 10, 12]
        if month == 2:
            days = 28
        elif month in months31:
            days = 31
        else:
            days = 30

        list = db.execute("SELECT * FROM habits_list WHERE user_id = ?", session["user_id"])
        habits = db.execute("SELECT * FROM habits WHERE user_id = ?", session["user_id"])
        return render_template("habit.html", list=list, days=days, today=today, habits=habits)

@app.route("/done", methods=["POST"])
@login_required
def done():
    habits = db.execute("SELECT * FROM habits_list WHERE user_id = ?", session["user_id"])
    day = date.today().day
    month = date.today().month
    for habit in habits:
        habit_name = habit["habit"]
        if request.form.get(habit["habit"]):
            db.execute("UPDATE habits SET done = ? WHERE user_id = ? AND habit = ? AND day = ? AND month = ?", "yes", session["user_id"], habit["habit"], day, month)
    return redirect("/habit")

@app.route("/update", methods=["POST"])
@login_required
def update():
    if not request.form.get("habit"):
        return apology("choose a habit to update", 400)

    if not request.form.get("day"):
        return apology("choose a day before today", 400)

    if not request.form.get("done"):
        return apology("choose status ('done -> yes')", 400)

    habit = request.form.get("habit")
    day = request.form.get("day")
    done = request.form.get("done")
    month = date.today().month

    db.execute("UPDATE habits SET done = ? WHERE user_id = ? AND habit = ? AND day = ? AND month = ?", done, session["user_id"], habit, day, month)

    return redirect ("/habit")
