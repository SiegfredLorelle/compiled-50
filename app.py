# CS50 Compiled


from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///final-project.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

@app.route("/promotional", methods=["GET", "POST"])
def promotional():
    """Load promotional page that allows log in and sign-in"""
    if request.method == "POST":
        pass

    else:
        return render_template("promotional.html")



# WORK ON BRANCH - git checkout -b "test"

# Promotional page
# Add transparent nav bar with login and signup
# Add modal when clicking carousel that enter as guest
# Put links to footer
# img with handlebar for mobile in the title

# Special thanks to cs50, Hyperplexed and Superlist for the inspiration
