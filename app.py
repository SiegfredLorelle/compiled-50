# CS50 Compiled


from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
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


@app.route("/", methods=["GET", "POST"])
def index():
    """Load homepage that allows user to go to other pages"""
    if request.method == "POST":
        pass

    else:
        return render_template("index.html")


@app.route("/mario", methods=["GET", "POST"])
def mario():
    """Load pyramid with the given height similar to one in Super Mario Bros."""
    if request.method == "POST":
        height = int(request.form.get("height"))

        # Ensure input is valid
        if height < 1 or height > 8:
            flash("Height must be within 1-8 inclusive.", "error")
            return render_template("mario.html")

        # Load the pyramid 
        flash(f"Pyramid with a height of {height} is made!", "success")
        return render_template("mario.html", height=height)

    # GET via redirect and clicking links   
    else:
        return render_template("mario.html")

@app.route("/credit", methods=["GET", "POST"])
def credit():
    """Tell what credit card is entered"""
    if request.method == "POST":
        pass
        return redirect("/")
    
    else:
        return render_template("credit.html")


# WORK ON BRANCH - git checkout -b "test"

# homepage page
# Change color of dropdown onclick
# Add limit to how much it can drag kasi lumalagpas kapag mobile tapos sobra sa drag
# Add modal when clicking carousel that enter as guest
# turn off ung on click sa buttons ng nav
# itry ung if and else ng mobile and pc para maayos ung nav bar
# Put links to footer
# Change homepage to only get 


# credit page
# add warning to not enter your actual credit card number
# suggestion to what credit cards are possible to enter
# find credit card of visa amex and mastercard
# display the card with maybe the number
# ensure input is valid



# add project drop down in nav bar in layout
# Start working on login and sign up maybe via modals nlng
# Plan out what projects are needed to be done
# mario, credit, ...


# add white bg to icon
# login required




# Special thanks to cs50, Hyperplexed and Superlist for the inspiration

# http://pixelartmaker.com/art/d53cda86152db67 MARIO BLOCK
