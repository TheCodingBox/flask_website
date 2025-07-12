from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'f2d3a3c9e2b94d1f9e7a4b8c2d5f6a1b'

# Reading passage and questions
PASSAGE = PASSAGE = """One sunny afternoon, a young girl named Emma was walking home from school\nwhen she heard a faint whimpering sound. Following the noise,\nshe found a small puppy stuck under a bush. The puppy looked scared and hungry.\nEmma gently picked it up and decided to take it home. She gave the puppy some water and food,\nand soon the puppy was wagging its tail happily. Emma named the puppy Max and promised\nto take care of him forever."""


QUESTIONS = [
    {"id": 1, "question": "Who found the puppy?", "answer": "emma"},
    {"id": 2, "question": "Where was the puppy stuck?", "answer": "under a bush"},
    {"id": 3, "question": "What did Emma give the puppy?", "answer": "water and food"},
    {"id": 4, "question": "What did Emma name the puppy?", "answer": "max"},
]

@app.route('/')
def index():
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
    results_list = []

    for q in QUESTIONS:
        qid = str(q["id"])
        question = q["question"]
        correct_answer = q["answer"].strip().lower()
        user_answer = user_answers.get(qid, "").strip().lower()
        is_correct = False

        if correct_answer == "water and food":
            is_correct = (
                ("water" in user_answer and "food" in user_answer)
                or user_answer == "water"
                or user_answer == "food"
            )
        elif correct_answer == "under a bush":
            bush_keywords = ["under a bush", "in a bush", "bush", "a bush"]
            is_correct = any(phrase in user_answer for phrase in bush_keywords)
        else:
            is_correct = user_answer == correct_answer

        if is_correct:
            correct_count += 1

        results_list.append({
            "question": question,
            "your_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct
        })

    accuracy = correct_count / len(QUESTIONS)
    speed_score = max(0, 100 - reading_time)
    total_score = accuracy * 70 + (speed_score / 100) * 30

    return render_template(
        'results.html',
        accuracy=int(round(accuracy * 100)),
        reading_time=int(round(reading_time)),
        total_score=int(round(total_score)),
        results_list=results_list
    )

if __name__ == '__main__':
    app.run(debug=True)
