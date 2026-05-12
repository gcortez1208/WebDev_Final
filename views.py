from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

questions = [
    {"country": "France", "capital": "Paris"},
    {"country": "Canada", "capital": "Ottawa"},
    {"country": "Brazil", "capital": "Brasilia"},
    {"country": "Monaco", "capital": "Monaco"},
    {"country": "Spain", "capital": "Madrid"},
    {"country": "Singapore", "capital": "Singapore"},
    {"country": "Japan", "capital": "Tokyo"},
    {"country": "Israel", "capital": "Jerusalem"},
    {"country": "China", "capital": "Beijing"},
    {"country": "Australia", "capital": "Canberra"},
]

@app.route('/')
def index():
    # Shuffle questions for each session
    session['questions'] = random.sample(questions, len(questions))
    session['current_index'] = 0
    session['score'] = 0
    return render_template('index.html', question=session['questions'][0], index=0, score=0)

@app.route('/submit', methods=['POST'])
def submit():
    user_answer = request.form.get('answer').strip().lower()
    correct_answer = session['questions'][session['current_index']]['capital'].lower()
    index = session['current_index']
    score = session['score']

    if user_answer == correct_answer:
        score += 1
        session['score'] = score
        result = 'correct'
    else:
        result = 'incorrect'
        'upadate the game score bhy rewarding the user with points for correct answers and keeping track of the score across multiple questions. You can use a session variable to store the score and update it each time the user submits an answer.'
        'send the next question to the user after they submit an answer, allowing them to continue playing without having to refresh the page or navigate back to the homepage. You can achieve this by redirecting the user to a new route that serves the next question after processing their answer.'
        

    index += 1
    session['current_index'] = index

    if index < len(session['questions']):
        next_question = session['questions'][index]
        return render_template('index.html', question=next_question, index=index, score=score, result=result, previous_answer=user_answer, correct_answer=correct_answer)
    else:
        return render_template('results.html', final_score=score, total=len(questions))
    
    

if __name__ == '__main__':
    app.run(debug=True)
