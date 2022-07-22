from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"
app = Flask(__name__)
app.config['SECRET_KEY'] = "password"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route("/")
def startSurvey():
    return render_template("startPage.html", survey = survey)

@app.route("/begin", methods = ["POST"])
def displaySurvey():
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def showQuestion():
    op = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(op)
    session[RESPONSES_KEY] = responses
    if (len(responses) == len(survey.questions)):
        return redirect("/finish")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/questions/<int:qid>")
def postQuestion(qid)):
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        return redirect("/finish")

    if (len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "questions.html", question_num=qid, question=question)

@app.route("/finish")
def finish():
    return render_template("finish.html")