# CS50 Compiled


from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from string import ascii_letters, ascii_uppercase, digits
from re import sub
import os

from helpers import login_required, check_card, get_grade_lvl, allowed_file, get_random_allele, get_blood_type



# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure a folder for images uploaded in filter page
UPLOAD_FOLDER = 'static/uploads/'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

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



@app.route("/plurality", methods=["GET", "POST"])
def plurality():
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



@app.route("/plurality/candidates", methods=["GET", "POST"])
def plurality_candidates():
    """ Get the names of the candidates"""
    if request.method == "POST":
        candidates = db.execute("SELECT * FROM pluralityCandidates")
        no_candidates = int(db.execute("SELECT no_candidates FROM pluralityNumbers")[0]["no_candidates"])

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
                return render_template("plurality-2.html", candidates=candidates, no_candidates=no_candidates)

        # Ensure candidate is not already in database
        for candidate in candidates:
            if full_name == candidate["full_name"]:
                
                # Catch error where user refresh as soon as it gets to plurality-3 where candidate might exceed 
                if no_candidates == len(candidates):
                    db.execute("UPDATE pluralityCandidates SET votes = 0")
                    return render_template("plurality-3.html", candidates=candidates)
                
                # Show error that candidate cannot repeat and ask for a new candidate name
                flash(f"'{full_name}' is already a candidate.", "error")
                return render_template("plurality-2.html", candidates=candidates, no_candidates=no_candidates)
                    
        # If name is valid then save the name in candidates db and update candidates variable
        db.execute("INSERT INTO pluralityCandidates (full_name) VALUES (?)", full_name)
        candidates = db.execute("SELECT * FROM pluralityCandidates")
        no_candidates = int(db.execute("SELECT no_candidates FROM pluralityNumbers")[0]["no_candidates"])

        # If candidates are complete then go to next page
        if  no_candidates == len(candidates):
            return render_template("plurality-3.html", candidates=candidates)

        # if candidate is incomplete then ask for next candidate
        elif no_candidates > len(candidates):
            return render_template("plurality-2.html", candidates=candidates, no_candidates=no_candidates)

        # Catch errors when candidates exceed
        else:
            flash("An error has occured. Please try again.", "error")
            return render_template("plurality-1.html")

    # Get by clicking links or redirects
    else:
        db.execute("DELETE FROM pluralityCandidates")
        return render_template("plurality-2.html")



@app.route("/plurality/votes", methods=["GET", "POST"])
def plurality_votes():
    """ Get the the vote of each voter then determine the winner(s)"""
    if request.method == "POST":
        vote = request.form.get("vote")
        candidates = db.execute("SELECT * FROM pluralityCandidates")
        candidates_sorted = db.execute("SELECT * FROM pluralityCandidates ORDER BY votes DESC")
        total_votes = int(db.execute("SELECT SUM(votes) AS total_votes FROM pluralityCandidates")[0]["total_votes"])
        no_voters = int(db.execute("SELECT no_voters FROM pluralityNumbers")[0]["no_voters"])

        # Ensure user voted
        if vote == "Candidate":
            flash("Please select a candidate to vote.", "error")
            return render_template("plurality-3.html", candidates=candidates, candidates_sorted=candidates_sorted, total_votes=total_votes, no_voters=no_voters)

        # Count the vote
        db.execute("UPDATE pluralityCandidates SET votes = (votes + 1) WHERE full_name = ?", vote)

        # Update the variables since db has an addition
        candidates = db.execute("SELECT * FROM pluralityCandidates")
        candidates_sorted = db.execute("SELECT * FROM pluralityCandidates ORDER BY votes DESC")
        total_votes = int(db.execute("SELECT SUM(votes) AS total_votes FROM pluralityCandidates")[0]["total_votes"])
        no_voters = int(db.execute("SELECT no_voters FROM pluralityNumbers")[0]["no_voters"])

        # If all voters voted then show the result and sort them also by votes
        if total_votes == no_voters:
            winners = db.execute("SELECT full_name FROM pluralityCandidates WHERE votes = (SELECT MAX(votes) as votes FROM pluralityCandidates)")
            return render_template("plurality-result.html", winners=winners, candidates_sorted=candidates_sorted)

        # If votes are incomplete ask for next vote
        elif total_votes < no_voters:
            return render_template("plurality-3.html", candidates=candidates, candidates_sorted=candidates_sorted, total_votes=total_votes, no_voters=no_voters)
        
        # Catch errors when user refresh as soon as it gets to results
        else:
            db.execute("UPDATE pluralityCandidates SET votes = (votes - 1) WHERE full_name = ?", vote)
            winners = db.execute("SELECT full_name FROM pluralityCandidates WHERE votes = (SELECT MAX(votes) as votes FROM pluralityCandidates)")
            candidates_sorted = db.execute("SELECT * FROM pluralityCandidates ORDER BY votes DESC")
            return render_template("plurality-result.html", winners=winners, candidates_sorted=candidates_sorted)     
    
    # GET by clicking links or redirects
    else:
        db.execute("UPDATE pluralityCandidates SET votes = 0")
        candidates = db.execute("SELECT * FROM pluralityCandidates")
        return render_template("plurality-3.html", candidates=candidates)



# credits to: https://roytuts.com/upload-and-display-image-using-python-flask/
@app.route("/filter", methods=["GET", "POST"])
def filter():
    """Filter a random image or an image from the user"""
    if request.method == "POST":
        type_of_filter = request.form.get("filter")
        random_image = request.form.get("random-image-button") 

        # Ensure a filter is chosen 
        if type_of_filter == "Choose filter to use ...":
            flash("Please select a filter to use.","error")
            return render_template("filter.html")

        # Check if random image is chosen
        if random_image:
            # Ensure only 1 image (the random image) is chosen by checking if a file is attached
            if 'file' not in request.files:
                flash("An error has occured. Please try again later.", "error")
                return render_template("filter.html")

            file = request.files['file']
            if file.filename != '':
                flash("Only one (1) image allowed. Either upload an image and submit or choose from the random image.", "error")
                return render_template("filter.html")

            # Load the random image filtered
            random_image_filename = f"/static/images/{random_image}.jpg"
            flash("Image successfully filtered!", "success")
            return render_template("filter.html", random_image_filename=random_image_filename, type_of_filter=type_of_filter)


        # Check if the post request has the file part
        if 'file' not in request.files:
            flash("An error has occured. Please try again later.", "error")
            return render_template("filter.html")

        # Ensure an image is uploaded 
        file = request.files['file']
        if file.filename == '':
            flash("No image selected.", "error")
            return render_template("filter.html")

        # If file extension is allowed, download it then load the image filtered
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("Image successfully filtered!", "success")
            return render_template("filter.html", filename=filename, type_of_filter=type_of_filter)
        
        # If file extension not allowed, show error and reload page
        else:
            flash("File extensions must be png, jpg, jpeg, and gif.", "error")
            return render_template("filter.html")

    # GET by clicking links or redirects
    else:
        return render_template("filter.html")

# Used in loading the uploaded image 
@app.route("/filter/<filename>")
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)



@app.route("/inheritance", methods=["GET", "POST"])
def inheritance():
    """Determines a possible blood type combination of a three generation family"""
    if request.method == "POST":
        submit = request.form.get("submit")

        # User chose to randomized all
        if submit == "randomize":
            # Randomize the allele of parents
            db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'child' AND number = 1", get_random_allele(), get_random_allele())
           
            # Read the alleles of child
            child_allele_1 = db.execute("SELECT allele_1 FROM inheritance WHERE generation = 'child' AND number = 1")[0].get("allele_1")
            child_allele_2 = db.execute("SELECT allele_2 FROM inheritance WHERE generation = 'child' AND number = 1")[0].get("allele_2")

            # Predict the allele of parents based on child
            db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'parent' AND number = 1", child_allele_1, get_random_allele())
            db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'parent' AND number = 2", child_allele_2, get_random_allele())

           # Read the alleles of the parents
            parent_1_allele_1 = db.execute("SELECT allele_1 FROM inheritance WHERE generation = 'parent' AND number = 1")[0].get("allele_1")
            parent_1_allele_2 = db.execute("SELECT allele_2 FROM inheritance WHERE generation = 'parent' AND number = 1")[0].get("allele_2")

            parent_2_allele_1 = db.execute("SELECT allele_1 FROM inheritance WHERE generation = 'parent' AND number = 2")[0].get("allele_1")
            parent_2_allele_2 = db.execute("SELECT allele_2 FROM inheritance WHERE generation = 'parent' AND number = 2")[0].get("allele_2")
            
            # Predict the alleles of the grandparents
            db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'grandparent' AND number = 1", parent_1_allele_1, get_random_allele())
            db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'grandparent' AND number = 2", parent_1_allele_2, get_random_allele())

            db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'grandparent' AND number = 3", parent_2_allele_1, get_random_allele())
            db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'grandparent' AND number = 4", parent_2_allele_2, get_random_allele())

            # Get the blood types of everyone bsaed on their alleles
            family = db.execute("SELECT allele_1, allele_2 FROM inheritance")

            for member in family:
                blood_type = get_blood_type(member)
                db.execute("UPDATE inheritance SET bloodtype = ? WHERE allele_1 = ? AND allele_2 = ?", blood_type, member.get("allele_1"), member.get("allele_2"))
            
            # Get the values to be shown in the family tree
            family = db.execute("SELECT allele_1, allele_2, bloodtype FROM inheritance")

            # Inform users that inputs in generation and alleles are disregarded
            if request.form.get("generation") != "Choose a generation ..." or request.form.get("allele-1") != "Choose an allele ..." or request.form.get("allele-2") != "Choose an allele ...":
                flash("Generation and allele inputs were disregarded.", "warning")
                return render_template("inheritance.html", family=family)

            # Load family tree with alleles and blood types
            flash("Successfully generated a family tree!", "success")
            return render_template("inheritance.html", family=family)


        # User submitted a generation and allele
        else:
            generation = request.form.get("generation")
            allele_1 = request.form.get("allele-1")
            allele_2 = request.form.get("allele-2")

            # Check if inputs are compelete
            if generation == "Choose a generation ...":
                flash("No generation selected.", "error")
                return render_template("inheritance.html")
            
            if allele_1 == "Choose an allele ..." or allele_2 == "Choose an allele ...":
                flash("Incomplete alleles.", "error")
                return render_template("inheritance.html")


            # Input values table

            # Predict the alleles of others

            # Load the image
            return render_template("inheritance.html")
    
    # GET by clicking links or redirects
    else:
        return render_template("inheritance.html")





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
# test for bugs

# inheritance
# catch error when pressing randomize all with input
# check bug spaming randomize all errors (maybe empty alleles and bloodtype row in table every post or might fix when login sign in is made)
# work on choosing gen, and alleles
# 

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

