from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # needed for session

# Sample passage and questions
PASSAGE = "This is a sample reading passage. Please read it carefully."
QUESTIONS = [
    {"id": 1, "question": "What is the main topic of the passage?", "answer": "reading"},
    {"id": 2, "question": "Is this passage long or short?", "answer": "short"},
]

@app.route('/')
def index():
    # Render your custom index page Website_index.html
    return render_template('Website_index.html', passage=PASSAGE)

@app.route('/questions', methods=['GET', 'POST'])
def questions():
    if request.method == 'POST':
        reading_time = float(request.form.get('reading_time', 0))
        session['reading_time'] = reading_time
        return render_template('questions.html', questions=QUESTIONS)
    else:
        return redirect(url_for('index'))

@app.route('/results', methods=['POST'])
def results():
    reading_time = session.get('reading_time', 0)
    user_answers = request.form
    correct_count = 0
    for q in QUESTIONS:
        qid = str(q["id"])
        if user_answers.get(qid, "").strip().lower() == q["answer"].lower():
            correct_count += 1
    accuracy = correct_count / len(QUESTIONS)
    speed_score = max(0, 100 - reading_time)  # example speed score calculation
    total_score = accuracy * 70 + (speed_score / 100) * 30  # weighted score
    return render_template('results.html', accuracy=accuracy, reading_time=reading_time, total_score=total_score)

if __name__ == '__main__':
    app.run(debug=True)
