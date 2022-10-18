# CS50 Compiled


from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from string import ascii_letters, ascii_uppercase, digits
from re import sub

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
            flash(f"Card succesfully determined!", "success")
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
        flash("Grade level successfully determined!", "success")
        return render_template("readability.html", grade_level=grade_level, paragraph=paragraph)

    # GET via clicking links or redirects
    else:
        return render_template("readability.html")



@app.route("/substitution", methods=["GET", "POST"])
def substitution():
    """Encrypt or decrypt the given text based on the given key"""
    if request.method == "POST":
        process = request.form.get("process")
        key = request.form.get("key").upper()
        text = request.form.get("text")

        # Ensures user selected encrypt or decrypt
        if process == "Choose...":
            flash("Please choose whether 'encrypt' to 'decrypt'.", "error")
            return render_template("substitution.html")

        # HTML already ensures the key is 26 characters in length but included another check here
        if len(key) > 26 or len(key) < 26:
            flash("Key must contain 26 characters", "error")
            return render_template("substitution.html")

        # Ensure key is contains unique alphabet letters without symbols and numbers
        used_letters = []
        for character in key:
            if character not in ascii_uppercase:
                flash("Key must only contain alphabetical letters.", "error")
                return render_template("substitution.html")

            # Check if the letter is a repeat 
            if character in used_letters:
                flash("Key must not repeat letters.", "error")
                return render_template("substitution.html")

            # Append the letter to used letters list    
            used_letters.append(character)
        
        # Ensure text is not full of white space
        if text.isspace():
            flash("Please enter a valid text.", "error")
            return render_template("substitution.html")

        # Map the keys to its equivalent alphabetical letter
        for i in range(len(ascii_uppercase)):
            db.execute("UPDATE  substitute SET key = ? WHERE letter = ?", key[i].upper(), ascii_uppercase[i])

        if process == "Encrypt":
            result_text = ""
            for character in text:
                if character in ascii_letters:
                    if character.isupper():
                        result_text += db.execute("SELECT key FROM substitute WHERE letter = ?", character.upper())[0]["key"]
                    
                    # If letter is lowercase, use the the lowercase equivalent
                    else:
                        result_text += db.execute("SELECT key FROM substitute WHERE letter = ?", character.upper())[0]["key"].lower()
                
                # Character is not a alphabetical letter, keep it as is 
                else:
                    result_text += character

        elif process == "Decrypt":
            result_text = ""
            for character in text:
                if character in ascii_letters:
                    if character.isupper():
                        result_text += db.execute("SELECT letter FROM substitute WHERE key = ?", character.upper())[0]["letter"]
                    
                    # If letter is lowercase, use the the lowercase equivalent
                    else:
                        result_text += db.execute("SELECT letter FROM substitute WHERE key = ?", character.upper())[0]["letter"].lower()
                
                # Character is not a alphabetical letter, keep it as is 
                else:
                    result_text += character

        # Show enrcypted/decrypted
        flash(f"Success!", "success")
        return render_template("substitution.html", process=process, key=key, text=text, result_text=result_text)

    else:
        return render_template("substitution.html")



@app.route("/plurality_start", methods=["GET", "POST"])
def plurality_start():
    """ Get the number of candidates and voters"""

    if request.method == "POST":
        # Ensure that this is a new process
        db.execute("DELETE FROM pluralityCandidates")

        # Get values from plurality-1
        no_candidates = int(request.form.get("no_candidates"))
        no_voters = int(request.form.get("no_voters"))

        # Ensures number of candidates and number of voters are valid
        if no_candidates > 10 or no_voters > 10:
            flash("Number of candidates and voters must be within 1-10 inclusive.", "error")
            return render_template("plurality-1.html")

        # If inputs are valid then save infos and redirect to next page
        db.execute("UPDATE pluralityNumbers SET no_candidates = ?, no_voters = ? WHERE number = 1", no_candidates, no_voters)
        return render_template("plurality-2.html")
    
    # GET by clicking redirect or link 
    else:
        return render_template("plurality-1.html")



@app.route("/plurality_get_candidates", methods=["GET", "POST"])
def plurality_get_candidates():
    """ Get the names of the candidates"""
    if request.method == "POST":
        candidates = db.execute("SELECT * FROM pluralityCandidates")

        # Get values from plurality-2
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        # Ensure name is not empty
        if first_name.isspace() or last_name.isspace():
            flash("Name cannot be empty.", "error")
            return render_template("plurality-2.html", candidates=candidates)

        # Ensure name does not have any extra white spaces in front, end, and trailing
        full_name = (first_name + " " + last_name)
        full_name = sub(' +', ' ', full_name.strip()).upper()

        # Ensures full name does not have any numbers or some special characters
        for character in full_name:
            if character in digits:
                flash("Name cannot have any numbers.", "error")
                return render_template("plurality-2.html", candidates=candidates)

        # Ensure candidate is not already in database
        for candidate in candidates:
            print(candidate["full_name"])
            if full_name == candidate["full_name"]:
                flash(f"'{full_name}' is already a candidate.", "error")
                return render_template("plurality-2.html", candidates=candidates)
                    
        # If name is valid then save the name in candidates table in db and update candidates variable
        db.execute("INSERT INTO pluralityCandidates (full_name) VALUES (?)", full_name)
        candidates = db.execute("SELECT * FROM pluralityCandidates")
        no_candidates = int(db.execute("SELECT no_candidates FROM pluralityNumbers")[0]["no_candidates"])

        # If candidates are complete then go to next page
        if  no_candidates == len(candidates):
            return render_template("plurality-3.html", candidates=candidates)

        # if candidate is incomplete then ask for next candidate
        elif no_candidates > len(candidates):
            return render_template("plurality-2.html", candidates=candidates)

        # Catch errors when candidates exceed
        else:
            flash("An error has occured. Please try again.", "error")
            return render_template("plurality-1.html")

    # Get by clicking links or redirects
    else:
        return render_template("plurality-2.html")



@app.route("/plurality_get_votes", methods=["GET", "POST"])
def plurality_get_votes():
    """ Get the the vote of each voter then determine the winner(s)"""
    if request.method == "POST":
        vote = request.form.get("vote")

        # Ensure user voted
        if vote == "Vote...":
            flash("Please select who to vote for.", "error")
            return render_template("plurality-3.html")

        # Update the vote 
        db.execute("UPDATE pluralityCandidates SET votes = (votes + 1) WHERE full_name = ?", vote)

        # Get values from db 
        candidates = db.execute("SELECT * FROM pluralityCandidates")
        total_votes = int(db.execute("SELECT SUM(votes) AS total_votes FROM pluralityCandidates")[0]["total_votes"])
        no_voters = int(db.execute("SELECT no_voters FROM pluralityNumbers")[0]["no_voters"])

        # If all voters voted then show ther result
        if total_votes == no_voters:
            winners = db.execute("SELECT full_name FROM pluralityCandidates WHERE votes = (SELECT MAX(votes) as votes FROM pluralityCandidates)")
            return render_template("plurality-result.html", winners=winners, candidates=candidates)

        # If votes are incomplete ask for next vote
        elif total_votes < no_voters:
            return render_template("plurality-3.html", candidates=candidates)
        
        # Catch errors when number of voters do not match the number of votes
        else:
            flash("An error has occured. Please try again.", "error")
            return render_template("plurality-1.html")     
    
    # GET by clicking links or redirects
    else:
        return render_template("plurality-3.html")



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
# restrict the use of other languages

# substitution
# find a way to ensure that encrypt and decrypt select was chosen in html para d na magrerestart pag input error

# plurality
# add go back button and try again in result page
# try to test refresh and go back if it will error


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
# Try floating labels on some textbox
# Toggle dropdown similar to bootstrap website
# popovers in copy links
# add loading imagse called spinners
# add tooltip on hover of copy links 


# Special thanks to cs50, Hyperplexed and Superlist for the inspiration

# mario block: http://pixelartmaker.com/art/d53cda86152db67 
# cards template: https://www.figma.com/community/file/934454786523964614
# AMEX logo: https://www.pngegg.com/en/png-pswlb
# scrabble tile: https://thekatespanos.com/scrabble-score-calculator/

