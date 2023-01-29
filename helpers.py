from flask import redirect, render_template, session
from functools import wraps
from string import ascii_lowercase, ascii_uppercase, ascii_letters
from re import sub
from random import choice

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function


# Referenced in credit page
def check_card(number):
    """
    Use Luhn’s Algorithm to determine the validity of the card then check what card it is
    """
    current_digit = number
    counter = 0
    sum = 0

    # Loop until all digits were passed
    while number > 0:
        # Get the last digit as current digit
        current_digit = number % 10
        # Step1 or 2 of Luhn's Algo depending on the position of the digit
        if (counter % 2) == 0:
            sum = Luhns_step2(current_digit, sum)
        else:
            sum = Luhns_step1(current_digit, sum)

        # Get the first and first 2 digits of the card
        if number < 10:
            first_digit = number
        elif number < 100:
            first_2digits = number

        # Go to the next digit, and increment the digit counter
        number //= 10
        counter += 1

    # Step3 of Luhn's Algo, return needed values
    if sum % 10 == 0:
        # Determine what card it is
        if counter == 15 and (first_2digits in [34, 37]):
            return "American Express"

        elif counter == 16 and (first_2digits in [51, 52, 53, 54, 55]):
            return "MasterCard"

        elif counter in [13, 16] and first_digit == 4:
            return "VISA"

        else:
            return "INVALID"

    else:
        return "INVALID"


# Referenced in check_card() above
def Luhns_step1(digit, sum):
    """Step 1 of Luhn's Algorithms"""
    # Multiply the digit by 2
    digit *= 2
    # If the product has 2 digits, break them down and add to the sum
    if (digit >= 10):
        sum += (digit % 10) + (digit // 10)
    else:
        sum += digit
    return sum

# Referenced in check_card() above
def Luhns_step2(digit, sum):
    """Step 2 of Luhn's Algorithms """
    # Add the digit to the sum
    sum += digit
    return sum


# Referenced in readability page
def get_grade_lvl(text):
    """
    Counts the number of letters, words, and sentences then Use Coleman Liau Index to get grade level
    """
    # Strip all of extra white spaces in the start and end of the string and 
    # Sub removes all trailing whitespaces within the string, then lowercase the entire text
    text = sub(' +', ' ', text.strip()).lower()

    # Counter for word is set to 1 since a whitespace signifies two words
    no_letters = no_sentences = 0
    no_words = 1

    for character in text:

        if character in ascii_lowercase:
            no_letters += 1
        
        if character == " ":
            no_words += 1

        if character in ["!", "?", "."]:
            no_sentences += 1

    # Use Coleman Liau Index to get the grade level
    grade_level = round(0.0588 * (no_letters / no_words * 100) - 0.296 * (no_sentences / no_words * 100) - 15.8)
    
    # Ensure the grade level is within 1-16
    if grade_level < 1:
        return "Pre-Grade 1"
    elif grade_level > 16:
        return "Grade 16+"
    else:
        return f"Grade {grade_level}"


# Referenced in filter page 
def allowed_file(filename):
    """Check if the uploaded image's file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}   

    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Referenced in inheritance page 
def get_random_allele():
    """Returns a random allele with equal chances"""
    alleles = ["A", "B", "O"]
    return choice(alleles)


# Referenced in inheritance page 
def get_blood_type(alleles):
    """Determines the blood type based on the person's alleles"""
    alleles = alleles.get("allele_1") + alleles.get("allele_2")

    if alleles == "AB" or alleles == "BA":
        return "AB"

    if alleles == "OO":
        return "O"
    
    for allele in alleles:
        if allele == "A":
            return "A"

        if allele == "B":
            return "B" 


# Referenced in inheritance page
def get_allele_to_inherit(allele_1, allele_2):
    """Randomly determine which allele to inherit"""
    alleles = [allele_1, allele_2]
    return choice(alleles)


# Referenced in birthday page
def sort_dates(dates):
    month_day = dates["birthday"].split("/")
    month_day = [int(date) for date in month_day]
    return month_day[0], month_day[1]
