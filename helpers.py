from flask import redirect, render_template, session
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/promotional")
        return f(*args, **kwargs)
    return decorated_function


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

