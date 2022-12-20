
# **COMPILED 50**

#### Video Demo:  TODO URL

#### Description: A web-based application where projects from CS50x course are compiled.

---

> A CS50 Compilation and more!

![Homepage](/cs50-final-project/static/images/homepage.PNG)

---

### Table of Contents



---

## Description

It is a responsive web-based application where most project from CS50x 2022 course are compiled. Compiled projects are given a graphical interface with additional/different features. It has a 'login' system which requires users to log in before accessing and trying out the compiled projects. Although logging in as 'guest' works too. A 'contact us' feature allows user to send message to the developers via email. Compiled projects consist of 10 projects derived from labs and problem sets of CS50x 2022.

#### Technologies

- Python 3.10
- Flask
- SQLite 3
- HTML, CSS, Javascript

#### Compiled Projects

- Mario
- Credit
- Scrabble
- Readability
- Substitution
- Plurality
- Filter
- Inheritance
- Trivia
- Birthday

---

## How to Use

#### Installation (TODO INSTALL PACKAGES OR REDIRECT TO HEROKU)


#### Configuration (TODO maybe set up their email to mail)

---

## Compiled Project Details

#### **Mario**

Mario is derived from [CS50x 2022 Problem Set 1](https://cs50.harvard.edu/x/2022/psets/1/mario/more/). This follows the 'feeling more comfortable' version of Mario. It works exactly the same as the problem set. Height is limited to 1-8 inclusive. The main difference is that the blocks are reperesented as an actual image from [Super Mario Bros.](https://mario.nintendo.com/history/) in the web-app, instead of printing '#' in command line.

![Mario](/cs50-final-project/static/images/mario.PNG)

#### **Credit**

Credit is derived from [CS50x 2022 Problem Set 1](https://cs50.harvard.edu/x/2022/psets/1/credit/). It also works exactly the same as the problem set. It also utilizes [Luhn's Algorithm](https://www.geeksforgeeks.org/luhn-algorithm/) to determine the validity of the card. It shows type and an image of a sample card.

The added feature here is a 'Not sure what to enter?' dropdown. The dropdown shows sample American Express (AMEX), Mastercard, and Visa credit card numbers. Beside each credit card number is a 'copy' button. Hovering the copy button triggers a tooltip saying 'copy'. Clicking the copy button automatically copy the credit card number it is assign to (or just beside it) as clipboard and automatically type the credit card number in the credit card number input box. A javascript alert informs the user about the automatic copy-paste of the credit card number.

The downside of Credit is that it is limited to the given constraints of the problem set. Card types does not always align with the given conditions, there are always exceptions. For example, according to the problem set, MasterCard starts with numbers from 51-56, but according to [PayPal](https://developer.paypal.com/api/nvp-soap/payflow/integration-guide/test-transactions/#standard-test-cards) some MasterCard starts at 2.

![Credit](/cs50-final-project/static/images/credit.PNG)

#### **Scrabble**

Scrabble is derived from [CS50x 2022 Lab 2](https://cs50.harvard.edu/x/2022/labs/2/). It works slightly different from the lab. This only asks one word from the user, instead of asking two words in the lab. It only shows the total score of given word (with each letters' score), instead of comparing the score of the two words in lab. It is also stricter in terms of accepting words. Before showing the score of the word, it verifies the validity of the world by checking it to a dictionary. The dictionary used is the large dictionary from [CS50x 2022 Week 5 Problem Set 5: Speller](https://cs50.harvard.edu/x/2022/psets/5/speller/).

![Scrabble](/cs50-final-project/static/images/scrabble.PNG)

#### **Readability**

Readability is derived from [CS50x 2022 Problem Set 2](https://cs50.harvard.edu/x/2022/psets/2/readability/). It works similar to the problem set. The readability test used is [Coleman-Liau Index](https://readable.com/readability/coleman-liau-readability-index/) which considers the number of letters, words, and sentences of the paragraph. It will show the approximate grade level needed to comprehend the given paragraph.

The added feature here is similar to credit, a 'Not sure what to enter?' dropdown. The dropdown shows a list different grade levels with a 'copy' button beside. Clicking a grade level, shows a sample paragraph intented for that grade level. Hovering the 'copy button triggers a tooltip saying 'copy'. Clicking the copy button, automatically copies the paragraph assigned to (under) the grade level as clipboard and automatically paste the copied paragraph in the paragraph input box. A javascript alerts informs the user about the automatic copy-paste of the paragraph.

A downside of using readability is its lack of validity checks. Any character, including digits, special characters, characters from other languages, are accepted as letter which can affect accuracy of the results. Considering the readability test used is intented only for the English language.

![Readability](/cs50-final-project/static/images/readability.PNG)

#### **Substitution**

Subsitution is derivede from [CS50x 2022 Problem Set 2](https://cs50.harvard.edu/x/2022/psets/2/substitution/). it is similar to the problem set, difference being the function to also decrypt. The encryption works by mapping the given key (sequence of 26 distinct letters) to the English alphabet. It allows user to encrypt or decrypt, instead of just encrypt in the problem set. If the user decided to encrypt, the result is the ciphertext of the given plaintext. If the user decided to decrypt, the result is the plaintext of the given ciphertext.

Another additional feature is similar to credit and readability, a 'Not sure what to enter?' dropdown. The dropdown shows a list of different keys with each having a copy button beside it. Hovering the copy button, triggers a tooltip saying 'copy'. Clicking the copy button, copies the key assigned to (beside) it as clipboard and paste the copied key to the key input box. A javascript alert informs the user about the automatic copy-paste of the paragraph.

The downside of substitution is that entering with incorrect/lacking inputs will clear the input boxes. A possible fix would be to check the inputs from the front-end using javascript, preventing incorrect/lacking inputs to reach the back-end (flask).

![Substitution](/cs50-final-project/static/images/substitution.PNG)

#### **Plurality**

Plurality is derived from [CS50x 2022 Problem Set 3](https://cs50.harvard.edu/x/2022/psets/3/). It works similar to the problem set. It is divided into three steps. The first step asks for the number of candidates and voters.

 The next step asks for the name of each candidates. It checks the validity of the name by ensuring that the given name does not contains a digit or that it is duplicate. The progress bar represents the progress in naming the candidates. An empty bar means no candidate has been named. A full bar means all candidates have been named. The next step starts, if all candidates have been named.

  The next step is voting phase. Each voters cast their vote by selecting the name of the candidate. Similar to the previous step, a progress bar is present. The progress bar represent the progress in voting. Empty bar means no votes has been cast yet. Full bar means all voters have casted their votes. The result can be seen in a table below, updating with each cast of votes. If all voters have voted, then the winner will be presented. User can also see the final tally of votes by clicking the 'see result' button.

![Plurality](/cs50-final-project/static/images/plurality.PNG)

#### **Filter**

Filter is derived from [CS50x 2022 Problem Set 4](https://cs50.harvard.edu/x/2022/psets/4/filter/less/). It follows the 'less comfortable' version of Filter. All features from the problem set is present. The four (4) filters available are grayscale, sepia, reflection, and blur. 

The additional feature here is that it allows user to upload any images (assuming its file extension is valid). For users hesistant to upload an image, there is also a 'random image' button. Clicking random image button opens up 4 images of dogs. Selecting one of them applies the selected filter to the selected image.

Editing images manually via bitmaps in the problem set is far more complicated than using CSS filers and transforms.

![Filter](/cs50-final-project/static/images/filter.PNG)

#### **Inheritance**

Inheritance is derived from [CS50x 2022 Lab 5](https://cs50.harvard.edu/x/2022/labs/5/). It works similar to the lab. Although this gives the user an option to select a generation and its alleles. 'Randomize all' button exists which works the same as lab. CLicking randomize all button randomizes both alleles of the all grandparents. And parent and child must inherit one allele from each of their parents randomly.

A downside of inheritance is its implementation. The code could use a more efficient algorithm and a better data structure instead of using conditionals to all possible outcomes.

![Filter](/cs50-final-project/static/images/inheritance.PNG)

#### **Trivia**

Trivia is derived from [CS50x 2022 Lab 8](https://cs50.harvard.edu/x/2022/labs/8/). The lab itself give us freedom to aks any questions that we want. I personalize it to be a 5 item quiz about the Philippines. There are 7 multiple choice questions in the pool of questions. Only 5 from the 7 questions are going to be asked. The probability of each question being picked from the pool is random. Clicking submit redirects to the result page. But users must answer all items before the it proceeds to the result page.

The result page shows the score of user out of 5. Score below 3 are rated as failed. A score of 3 or 4 is rated as passing. And a 5 out of 5 score is rated as perfect. If user has mistakes, a 'see mistakes' button is present. Clicking see mistake button, will show all items answered incorrectly. The user's answer is highlighted as red, and the correct answer is highlighted as green. There are two small dots on top labeled as legends. Hovering the green dot, triggers a tooltip saying 'correct answer.' Hovering red dot, triggeres a tooltip saying 'your answer.'

![Filter](/cs50-final-project/static/images/trivia.PNG)

#### **Birthday**

Birthday is derived from [CS50x 2022 Lab 9](https://cs50.harvard.edu/x/2022/labs/9/). It works similar to the lab. Enter the name, birth month, and birth day of a person to add them to the birthday lists. The list is sorted by upcoming birthday. It has date check feature which ensures that the month date is valid. Hovering on a row of the birthday list displays an 'X' remove button on its right. Clicking the remove button removes that person on the birthday lists.

The downside of birthday is in the implementation of sorting by upcoming date. There seems to be bug where sometimes it does not sort it properly. Adding more person or refreshing the page fixes the bug.

![Filter](/cs50-final-project/static/images/birthday.PNG)












---

## Other features
---

## Credits
YT OF HOMEPAGE DRAG
IMAGE OF MARIO
FIGMA AUTHOR OF CREDIT CARDS
CREDITS TO SCRABBLE TILE
CREDIT DOG IMGS FROM FILTER
CREDITS TO CSS OF INHERITANCE
---

## Author Info
