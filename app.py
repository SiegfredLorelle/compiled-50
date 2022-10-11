# CS50 Compiled


from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, check_card

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
        cc_number = request.form.get("cc_number")
        num_of_digits = len(cc_number)

        # Ensure credit card number is valid based on its number of digits
        if num_of_digits == 13 or num_of_digits == 15 or num_of_digits == 16:
            
            # Use Luhn’s Algorithm to determine the validity of the card then check what card it is
            card = check_card(int(cc_number))

            # Ensure card is valid
            if card.upper() == "INVALID":
                flash(f"Invalid credit card.", "error")
                return render_template("credit.html")

            # Load the what card it is
            flash(f"The credit card is {card}!", "success")
            return render_template("credit.html", card=card)

        else:
            flash("13-, 15-, and 16-digits are the only valid credit card numbers.", "error")
            return render_template("credit.html")

    # GET via redirect and clicking links
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
# msg on hover for copy clipboard
# msg below instead of alert that it is copied to clipboard 

# scrabble page
# start scrabble page
# add a dictionary, check dictionary first before outputting score
# ui will be input with subscript of score and bg color for each letter


# lagay logo sa navbar
# Start working on login and sign up maybe via modals nlng
# Plan out what projects are needed to be done
# mario, credit, scrabble, ...


# add white bg to icon
# login required



# Special thanks to cs50, Hyperplexed and Superlist for the inspiration

# mario block: http://pixelartmaker.com/art/d53cda86152db67 
# cards template: https://www.figma.com/community/file/934454786523964614
# AMEX logo: https://www.pngegg.com/en/png-pswlb

