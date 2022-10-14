# CS50 Compiled


from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from string import ascii_letters

from helpers import login_required, check_card, get_grade_lvl

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

            # Load what card it is
            flash(f"Succesfully determined!", "success")
            return render_template("credit.html", card=card)

        else:
            flash("13-, 15-, and 16-digits are the only valid credit card numbers.", "error")
            return render_template("credit.html")

    # GET via redirect and clicking links
    else:
        return render_template("credit.html")



@app.route("/scrabble", methods=["GET", "POST"])
def scrabble():
    """Checks if a word is real and give its score in scrabble"""
    if request.method == "POST":
        word = request.form.get("word").strip().lower()

        # Ensure word does not contain numbers and special characters
        for character in word:
            if character not in ascii_letters:
                flash("Scrabble does not accept words with numbers, symbols, and whitespaces.", "error")
                return render_template("scrabble.html")        

        # Ensure word is in the dictionary 
        # The dictionary used was the large dictionary from Week 5 Problem Set 5 Speller uploaded to final-project.db
        check_dictioanary = db.execute("SELECT word FROM scrabbleDictionary WHERE word == ? ", word)
        if not check_dictioanary:
            flash(f"Sorry, '{word}' was not found in the dictionary.", "error")
            return render_template("scrabble.html")  
        
        # Get the score of the word by adding the score equivalent of each letters
        total_score = 0
        scores = []
        for letter in word:
            # Get the score of the letter 
            letter_score = db.execute("SELECT * FROM scrabbleScores WHERE letter == ? ", letter)[0]
            scores.append(letter_score)
            
            # Get score of word 
            total_score += letter_score["score"]

        # Show the score
        flash(f"'{word}' was found in the dictionary.", "success")
        return render_template("scrabble.html", scores=scores, total_score=total_score)
    
    # GET via clicking links or redirects
    else:
        return render_template("scrabble.html")


@app.route("/readability", methods=["GET", "POST"])
def readability():
    """Determines the readability level of the paragraph prompted"""
    if request.method == "POST":
        paragraph = request.form.get("paragraph")

        # Ensure the paragraph is not full of whitespaces
        if paragraph.isspace():
            flash("Please enter a valid paragraph.", "error")
            return render_template("readability.html")

        # Get grade level intented for text based on Coleman Liau Index
        grade_level = get_grade_lvl(paragraph)

        # Show results
        flash("Successfully determined!", "success")
        return render_template("readability.html", grade_level=grade_level, paragraph=paragraph)

    # GET via clicking links or redirects
    else:
        return render_template("readability.html")



@app.route("/substitution", methods=["GET", "POST"])
def substitution():
    """Cypher the given plaintext based on the given key"""
    if request.method == "POST":
        return render_template("substitution.html")

    else:
        return render_template("substitution.html")






# TODOs

# homepage page
# Change color of dropdown onclick
# Add limit to how much it can drag kasi lumalagpas kapag mobile tapos sobra sa drag
# Add modal when clicking carousel that enter as guest
# turn off ung on click sa buttons ng nav
# itry ung if and else ng mobile and pc para maayos ung nav bar
# Put links to footer
# Change homepage to only get 
# add icons for on log in sign in log out


# credit page
# msg on hover for copy clipboard
# msg below instead of alert that it is copied to clipboard 

# scrabble page
# clicking dictionary will lead to modal of list of the words in the dictionary or redirect to download of the text file

# readability
# add use proper grammar and punctuation below the text box itself
# find a way to count words and sentences better (especially sentences)

# substitution
# make it that it does not require a 26 letter key, just loop to the given key until 26 letters
# add not sure what to enter
# Show plaintext, cyphertext, and key in output
# error if plaintext is only space
# accept symbols and numbers, show them both in plain and cypher

# lagay logo sa navbar
# Start working on login and sign up maybe via modals nlng
# Plan out what projects are needed to be done
# mario, credit, scrabble, readability, substitution...


# upload to heroku
# remove cs50 from title
# add white bg to icon
# login required
# add search and history that shows everything the user does by looking at db
# add focus on textbox for copy clipboards in js
# add divider per week in dropdown projects 
# maybe add a way to keep entered value in form text box
# gawing table or grid ung may copy button para pantay pantay ung pwesto ng copy ?
# make all google fonts oneline by adding in the family in google fonts.com




# Special thanks to cs50, Hyperplexed and Superlist for the inspiration

# mario block: http://pixelartmaker.com/art/d53cda86152db67 
# cards template: https://www.figma.com/community/file/934454786523964614
# AMEX logo: https://www.pngegg.com/en/png-pswlb
# scrabble tile: https://thekatespanos.com/scrabble-score-calculator/

