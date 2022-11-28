# Compiled 50


from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from string import ascii_letters, ascii_uppercase, ascii_lowercase ,digits
from random import randint
from re import sub
from datetime import date
import os

from helpers import login_required, check_card, get_grade_lvl, allowed_file, get_random_allele, get_blood_type, get_allele_to_inherit, sort_dates



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
        if len(session) == 1:
            username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0].get("username")
            return render_template("index.html", username=username)
        else:
            return render_template("index.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Login the user"""
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Ensure username password is not empty
        if username.isspace() or password.isspace():
            flash("Username and Password cannot be empty.", "error")
            return render_template("login.html")
        
        # Ensure username password is submitted (already required in html but to be sure)
        if not username or not password:
            flash("Username and Password cannot be empty.", "error")
            return render_template("login.html")

        # Check if user is in the database
        user = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username is found
        if len(user) != 1:
            flash("Username is not registered.", "error")
            return render_template("login.html")

        # Ensure username matches the password
        if  not check_password_hash(user[0]["hashed_password"], password):
            flash("Invalid Username and/or Password.", "error")
            return render_template("login.html")

        # Remember which user logged in
        session["user_id"] = user[0]["id"]

        # Log the user in
        return redirect("/")

    # GET via redirect and clicking links    
    else:
        return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Create a new account"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_verification = request.form.get("password-verification")

        # Ensure username, password, and password(verification) is not empty
        if username.isspace() or password.isspace() or password_verification.isspace():
            flash("Username and Password cannot be empty.", "error")
            return render_template("signup.html")

        # Ensure username, password, and password(verification) is submitted (required in html but just ot be sure)
        if not username or not password or not password_verification:
            flash("Username and Password cannot be empty.", "error")
            return render_template("signup.html")

        # Check if username is already registered
        user = db.execute("SELECT username FROM users WHERE username = ?", username)

        # Ensure username is not already registered
        if len(user) != 0:
            flash("Username is already used.", "error")
            return render_template("signup.html")

        # Ensure passwords is matching
        if password != password_verification:
            flash("Passwords do not match.", "error")
            return render_template("signup.html")

        # Ensure password is atleast 6 characters long
        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "error")
            return render_template("signup.html")


        # Determine if password has whitespace, uppercase letter, lowercase letter, and number
        has_uppercase = has_lowercase = has_number = has_space = False
        for character in password:
            if character in list(ascii_lowercase):
                has_lowercase = True
            elif character in list(ascii_uppercase):
                has_uppercase = True
            elif character in list(digits):
                has_number = True
            elif character.isspace():
                has_space = True

        # Ensure password has no whitespace, has uppercase, lowercase letter, a number
        if not has_uppercase or not has_lowercase or not has_number or has_space:
            flash("Password must have no whitespaces, and at least have 1 lowercase letter, uppercase letter, and digit.", "error")
            return render_template("signup.html")

        # Add the new user to the database
        db.execute("INSERT INTO users (username, hashed_password) VALUES (?, ?)", username, generate_password_hash(password))

        # Remember which user logged in
        user_id = db.execute("SELECT id FROM users WHERE username = ?", username)[0].get("id")
        session["user_id"] = user_id

        # Log the user in
        return redirect("/")

    # GET via redirect and clicking links    
    else:
        return render_template("signup.html")




@app.route("/logout")
def logout():
    """Log the user out"""
    # Clear data if the user is a guest
    if session["user_id"] == 1:
        db.execute("DELETE FROM birthday WHERE id = 1")

    # Forget any user_id
    session.clear()

    # Redirect to homepage
    return redirect("/")



@app.route("/mario", methods=["GET", "POST"])
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
        flash("Name the candidates!", "warning")
        return render_template("plurality-2.html")
    
    # GET by clicking redirect or link 
    else:
        return render_template("plurality-1.html")



@app.route("/plurality/candidates", methods=["GET", "POST"])
@login_required
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

        # Ensures full name does not have any numbers
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
            flash("Choose who to vote!", "warning")

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
@login_required
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
            flash("Winners determined!", "success")
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
@login_required
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
@login_required
def inheritance():
    """Determines a possible blood type combination of a three generation family"""
    if request.method == "POST":
        # Empty the columns before a submit
        db.execute("UPDATE inheritance SET allele_1 = NULL, allele_2 = NULL, bloodtype = NULL")

        # Know if user submitted inputs or chose to randomize all
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

            # Get the blood types of everyone based on their alleles
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

            # Input the values given by user in the database
            db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = ? AND number = 1", allele_1, allele_2, generation)

            # Predict the alleles of others
            if generation == "grandparent":
                # Predict alleles of other grandparents randomly
                db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'grandparent' AND number == 2", get_random_allele(), get_random_allele())
                db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'grandparent' AND number == 3", get_random_allele(), get_random_allele())
                db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'grandparent' AND number == 4", get_random_allele(), get_random_allele())

                # Read allele of grandparent 1 and 2 then inherit it to parent 1
                allele_to_inherit = get_allele_to_inherit(allele_1, allele_2)
                grandparent_2_allele = db.execute("SELECT allele_1 FROM inheritance WHERE generation = 'grandparent' AND number = 2")[0].get("allele_1")
                db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'parent' AND number = 1", allele_to_inherit, grandparent_2_allele)

                # Read alleles of grandparents 3 and 4 then inherit it to parent 2
                grandparent_3_allele = db.execute("SELECT allele_1 FROM inheritance WHERE generation = 'grandparent' AND number = 3")[0].get("allele_1")
                grandparent_4_allele = db.execute("SELECT allele_1 FROM inheritance WHERE generation = 'grandparent' AND number = 4")[0].get("allele_1")
                db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'parent' AND number = 2", grandparent_3_allele, grandparent_4_allele)

                # Read allele of parent 1 then randomize which to inherit to child
                parent_1_allele_1 = db.execute("SELECT allele_1 FROM inheritance WHERE generation = 'parent' AND number = 1")[0].get("allele_1")
                parent_1_allele_2 = db.execute("SELECT allele_2 FROM inheritance WHERE generation = 'parent' AND number = 1")[0].get("allele_2")

                allele_to_inherit = get_allele_to_inherit(parent_1_allele_1, parent_1_allele_2)

                # Read allele of parent 2 then update allele of the child
                parent_2_allele = db.execute("SELECT allele_1 FROM inheritance WHERE generation = 'parent' AND number = 2")[0].get("allele_1")
                db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'child'", allele_to_inherit, parent_2_allele)

                # Let user know which is their input
                flash("Successfully generated a family tree! (your input is grandparent 1)", "success")


        if generation == "parent":
            # Give the allele inherited by parent 1 to grandparent 1 and 2
            db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'grandparent' AND number = 1", allele_1, get_random_allele())
            db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'grandparent' AND number = 2", allele_2, get_random_allele())

            # Randomize the alleles of other grandparents
            db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'grandparent' AND number = 3", get_random_allele(), get_random_allele())
            db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'grandparent' AND number = 4", get_random_allele(), get_random_allele())

            # Read alleles of grandparents 3 and 4 then inherit it to parent 2
            grandparent_3_allele = db.execute("SELECT allele_1 FROM inheritance WHERE generation = 'grandparent' AND number = 3")[0].get("allele_1")
            grandparent_4_allele = db.execute("SELECT allele_1 FROM inheritance WHERE generation = 'grandparent' AND number = 4")[0].get("allele_1")

            db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'parent' AND number = 2", grandparent_3_allele, grandparent_4_allele)

            # Randomize alleles of parent 1 then inherit it to child
            allele_to_inherit = get_allele_to_inherit(allele_1, allele_2)
            parent_2_allele = db.execute("SELECT allele_1 FROM inheritance WHERE generation = 'parent' AND number = 2")[0].get("allele_1")

            db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'child'", allele_to_inherit, parent_2_allele)

            # Let user know which is their input
            flash("Successfully generated a family tree! (your input is parent 1)", "success")


        if generation == "child":
            # Give the inherited allele of child to parent 1 and 2
            db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'parent' AND number = 1", allele_1, get_random_allele())
            db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'parent' AND number = 2", allele_2, get_random_allele())
            
            # Read inherited allele of parents
            parent_1_allele_2 = db.execute("SELECT allele_2 FROM inheritance WHERE generation = 'parent' AND number = 1")[0].get("allele_2")
            parent_2_allele_2 = db.execute("SELECT allele_2 FROM inheritance WHERE generation = 'parent' AND number = 2")[0].get("allele_2")

            # Give inherited values of parents to their grandparents
            db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'grandparent' AND number = 1", allele_1, get_random_allele())
            db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'grandparent' AND number = 2", parent_1_allele_2, get_random_allele())
            db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'grandparent' AND number = 3", allele_2, get_random_allele())
            db.execute("UPDATE inheritance SET allele_1 = ?, allele_2 = ? WHERE generation = 'grandparent' AND number = 4", parent_2_allele_2, get_random_allele())

            # Let user know which is their input
            flash("Successfully generated a family tree! (your input is child)", "success")    


        # Get the blood types of everyone based on their alleles
        family = db.execute("SELECT allele_1, allele_2 FROM inheritance")

        for member in family:
            blood_type = get_blood_type(member)
            db.execute("UPDATE inheritance SET bloodtype = ? WHERE allele_1 = ? AND allele_2 = ?", blood_type, member.get("allele_1"), member.get("allele_2"))
        
        # Update the family to include their blood types
        family = db.execute("SELECT allele_1, allele_2, bloodtype FROM inheritance")

        # Load family tree with alleles and blood types
        return render_template("inheritance.html", family=family)

    # GET by clicking links or redirects
    else:
        # Empty the columns before starting
        db.execute("UPDATE inheritance SET allele_1 = NULL, allele_2 = NULL, bloodtype = NULL")
        return render_template("inheritance.html")



@app.route("/trivia", methods=["GET", "POST"])
@login_required
def trivia():
    """A 5 item trivia quiz about the Philippines"""
    if request.method == "POST":
        # Count the total score and determine which questions were asked and which the user got wrong
        score = 0
        questions = []
        mistakes = {}

        if request.form.get("btnradio1"):
            questions.append(1) 
            if request.form.get("btnradio1") == "Manila":
                score += 1
            else:
                if request.form.get("btnradio1") == "Jakarta":
                    mistakes[1] = "Jakarta"

                elif request.form.get("btnradio1") == "Taipei":
                    mistakes[1] = "Taipei"
                
                elif request.form.get("btnradio1") == "Kuala Lumpur":
                    mistakes[1] = "Kuala Lumpur"


        if request.form.get("btnradio2"):
            questions.append(2) 
            if request.form.get("btnradio2") == "Basketball":
                score += 1   
            else:
                if request.form.get("btnradio2") == "Cricket":
                    mistakes[2] = "Cricket"

                elif request.form.get("btnradio2") == "Hockey":
                    mistakes[2] = "Hockey"
                
                elif request.form.get("btnradio2") == "Baseball":
                    mistakes[2] = "Baseball"


        if request.form.get("btnradio3"):
            questions.append(3) 
            if request.form.get("btnradio3") == "Dwayne Johnson":
                score += 1 
            else:
                if request.form.get("btnradio3") == "Bella Poarch":
                    mistakes[3] = "Bella Poarch"

                elif request.form.get("btnradio3") == "Bruno Mars":
                    mistakes[3] = "Bruno Mars"
                
                elif request.form.get("btnradio3") == "Olivia Rodrigo":
                    mistakes[3] = "Olivia Rodrigo"


        if request.form.get("btnradio4"): 
            questions.append(4)    
            if request.form.get("btnradio4") == "Jollibee":
                score += 1    
            else:
                if request.form.get("btnradio4") == "McDonald's":
                    mistakes[4] = "McDonald's"

                elif request.form.get("btnradio4") == "Wendy's":
                    mistakes[4] = "Wendy's"
                
                elif request.form.get("btnradio4") == "KFC":
                    mistakes[4] = "KFC"
                
        if request.form.get("btnradio5"): 
            questions.append(5)  
            if request.form.get("btnradio5") == "fertilized duck egg":
                score += 1  
            else:
                if request.form.get("btnradio5") == "fertilized chicken egg":
                    mistakes[5] = "fertilized chicken egg"

                elif request.form.get("btnradio5") == "fertilized turkey egg":
                    mistakes[5] = "fertilized turkey egg"
                
                elif request.form.get("btnradio5") == "fertilized quail egg":
                    mistakes[5] = "fertilized quail egg"
                
        if request.form.get("btnradio6"):
            questions.append(6) 
            if request.form.get("btnradio6") == "Asia":
                score += 1    
            else:
                if request.form.get("btnradio6") == "Africa":
                    mistakes[6] = "Africa"

                elif request.form.get("btnradio6") == "Europe":
                    mistakes[6] = "Europe"
                
                elif request.form.get("btnradio6") == "Oceania":
                    mistakes[6] = "Oceania"

        if request.form.get("btnradio7"):
            questions.append(7) 
            if request.form.get("btnradio7") == "Flag4":
                score += 1     
            else:
                if request.form.get("btnradio7") == "Flag1":
                    mistakes[7] = "Flag1"

                elif request.form.get("btnradio7") == "Flag2":
                    mistakes[7] = "Flag2"
                
                elif request.form.get("btnradio7") == "Flag3":
                    mistakes[7] = "Flag3"

        # Load the next page with the total score
        flash("Result is out!", "success")
        return render_template("trivia-result.html", score=score, questions=questions, mistakes=mistakes)


    # GET by clicking links or redirects
    else:
        # Randomize the questions 
        questions = []
        while len(questions) < 5:
            question = randint(1, 7)
            if question not in questions:
                questions.append(question)
            questions.sort()

        return render_template("trivia.html", questions=questions)



@app.route("/birthday", methods=["GET", "POST"])
@login_required
def birthday():
    """List the birthdays inputted"""
    if request.method == "POST":
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        # Ensure month and day is selected
        if month == "Month" or day == "Day":
            flash("Must select 'month' and 'day'.", "error")
            return redirect("/birthday")

        # Ensure name is not empty
        if name.isspace():
            flash("Name cannot be empty.", "error")
            return redirect("/birthday")

        # Ensure name do not have numbers
        for character in name:
            if character in digits:
                flash("Name cannot have numbers.", "error")
                return redirect("/birthday")

        # Ensure name do not have whitespace in front, back and trailing
        name = sub(' +', ' ', name.strip())

        # Ensure month and day is valid
        # Month has 30 maximum days
        if month in [ "4", "6", "9", "11"]:
            if day == "31":
                flash("Invalid date.", "error")
                return redirect("/birthday")

        # Month is February (29 maximum days)
        elif month == "2":
            if day in ["30", "31"]:
                flash("Invalid date.", "error")
                return redirect("/birthday")

        # Ensure person is not already in db
        people = db.execute("SELECT name FROM birthday WHERE id = ?", session["user_id"])
        print(people)
        for person in people:
            if person["name"] == name:
                flash("That person is already in the lists.", "error")
                return redirect("/birthday")

        # Add the birthday to db
        db.execute("INSERT INTO birthday VALUES (?, ?, ?)",  session["user_id"], name, f"{month}/{day}")

        # Reload the page 
        flash(f"Added '{name}' to birthday list.", "success")
        return redirect("/birthday")

    # GET by clicking links or redirects
    else:
        # Read table with birthday
        people = db.execute("SELECT name, birthday FROM birthday WHERE id = ?", session["user_id"])

        # Sort the birthday list if 2 or more people in the list
        if len(people) > 1:
            # Get the current month and day and split it into a list
            today = date.today().strftime("%m %d").split()
            month, day = int(today[0]), int(today[1])

            # Sort birthday list by date
            people.sort(key=sort_dates)
            
            # Sort the birthday list based on who has an upcoming birthday relative to current date
            for person in people:

                # Place at the end if the person's birthday already passed
                if int(person["birthday"].split("/")[0]) >= month:

                    # Continue putting person in the end until the persons birthday that haven't passe is in the front
                    while True:
                        birthday_month, birthday_day = int(people[0]["birthday"].split("/")[0]), int(people[0]["birthday"].split("/")[1])

                        if birthday_month - month < 0 or (birthday_month == month and birthday_day - day < 0):
                            tmp = people[0]
                            people.pop(0)
                            people.append(tmp)
                        else:
                            break

        # Add a counter for people if not empty
        if len(people) != 0:
            people = enumerate(people, start=1)

        # Load the page
        return render_template("birthday.html", people=people)


# TODOs

# homepage page
# Add limit to how much it can drag kasi lumalagpas kapag mobile tapos sobra sa drag
# Add modal when clicking carousel that enter as guest
# turn off ung on click sa buttons ng nav
# itry ung if and else ng mobile and pc para maayos ung nav bar
# Put links to footer
# Change homepage to only get 
# add icons for on log in sign in log out

# scrabble page
# clicking dictionary will lead to modal of list of the words in the dictionary or redirect to download of the text file

# readability
# add use proper grammar and punctuation below the text box itself
# find a way to count words and sentences better (especially sentences)
# restrict the use of other languages

# substitution
# find a way to ensure that encrypt and decrypt select was chosen in html para d na magrerestart pag input error

# inheritance
# check bug spaming randomize all errors (maybe empty alleles and bloodtype row in table every post or might fix when login sign in is made)


# TODO 
# add login as guest in login page (automate login)
# screenshot every project, add picture of project in sample project in index
# redirect to sample project when clicking projects if not logged in




# change pass username and password in accounts



# about

# lagay logo sa navbar
# add divider in project dropdown (divide by weeks in cs50) maybe not
# add space below title of project 
# make buttons to pills
# put copy buttons in a pill or round button (add tooltip on hover and click and change shade)
# upload to heroku
# fix mobile in index
# add white bg to icon
# login required, restrict opening projects in index if not logged in, redirect maybe to carousel below
# add focus on textbox for copy clipboards in js
# maybe add a way to keep entered value in form text box
# Try floating labels on some textbox
# Toggle dropdown similar to bootstrap website
# add loading imagse called spinners
# add tooltip on hover of copy links 
# put links in homepage

