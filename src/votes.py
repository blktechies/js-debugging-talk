import redis
import json
from random import shuffle
from flask import Flask, request, render_template, url_for, redirect

r = redis.StrictRedis(host='localhost', port=6379, db=0)
app = Flask(__name__)

def valid_question(form):
    if (form['question'] and len(form['question']) < 50):
        return True
    else:
        return False

def add_new_question(form):
    question_id = str(r.incr('globals.question_id'))
    r.set("questions:" + question_id + ":up", "0")
    r.set("questions:" + question_id + ":down", "0")
    r.set("questions:" + question_id + ":text", form['question'])
    return question_id

def all_questions():
    max_id = int(r.get('globals.question_id'))
    # take 10 at random
    all_ids = range(1, max_id+1)
    shuffle(all_ids)
    all_ids = all_ids[:11]
    all_questions = []
    for q_id in all_ids:
        body = r.get("questions:" + str(q_id) + ":text")
        q = { "id": q_id, "body": body }
        all_questions.append(q)
    return all_questions

def do_vote(question_id, direction):
    question_id = str(question_id)
    votes = r.incr("questions:" + question_id + ":" + direction)
    return votes

@app.route("/")
def hello():
    questions = all_questions()
    return render_template('index.html', questions=questions)

@app.route("/question/new", methods=['GET', 'POST'])
def new_question():
    question_id = False
    error = False
    if request.method == 'POST':
        if valid_question(request.form):
            qid = add_new_question(request.form)
            question_id = qid
        else:
            error = "Invalid Question."
    return render_template('new_question.html', question_id=question_id, error=error)

@app.route("/question/<int:question_id>", methods=['GET', 'HEAD'])
def display_question(question_id):
    question_id = str(question_id)
    up = r.get("questions:" + question_id + ":up")
    down = r.get("questions:" + question_id + ":down")
    question = r.get("questions:" + question_id + ":text")
    resp = { "up": up, "down": down, "question": question, "id": int(question_id) }
    return render_template("question.html", question=resp)

@app.route("/question/<int:question_id>/up", methods=['POST'])
def vote_up(question_id):
    votes = do_vote(question_id, "up")
    return redirect(url_for('display_question', question_id=question_id))

@app.route("/question/<int:question_id>/down", methods=['POST'])
def vote_down(question_id):
    votes = do_vote(question_id, "down")
    return redirect(url_for('display_question', question_id=question_id))

@app.route("/question/<int:question_id>/up")
@app.route("/question/<int:question_id>/down")
def redirect_to_question(question_id):
    return redirect(url_for('display_question', question_id=question_id))

@app.route("/redis")
def list_keys():
    return r.keys('*')


if __name__ == "__main__":
    app.run(debug=True)
