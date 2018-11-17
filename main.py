from flask import Flask, render_template, request, render_template_string, Response
from flask import url_for, redirect
from collections import defaultdict
import os
import json
import codecs

app = Flask(__name__)

data_path = 'data_json_final.json'
questions = json.load(codecs.open(data_path, 'r', 'utf-8-sig'))

global answers
answers = defaultdict(int)
NAME = str()

@app.route('/')
def root():

	return render_template('index.html')

@app.route('/questionnaire')
@app.route('/questionnaire/<id>/')
def show_question(id=1):

	global answers
	global NAME
	id = int(id)
	name = request.args.get('field1')
	email_id = request.args.get('field2')

	if name != None and email_id != None:
		NAME = name
		results = open(NAME+'.txt','a')
		results.write(name + " " + email_id + " SAFE " + '\n')
		results.close()

	ans = request.args.get('qn')
	answers[id] = ans

	return render_template("questions.html", question = questions[str(id)], idx = id)

@app.route('/thanks')
def thanks():

	global answers
	global NAME

	ans = request.args.get('qn')
	lastkey = sorted(answers.keys())[-1]
	answers[lastkey+1] = ans
	answers.pop(1)
	results = open(NAME+'.txt','a')

	for k, v in answers.items():
		results.write(questions[str(k-1)]["q"] + " Ans:" + v + '\n\n')
	results.write('\n\n\n')
	results.close()

	return render_template("thanks.html")

@app.route('/reset')
def reset():

	global answers
	global NAME

	answers = {}
	NAME = ''

	return redirect(url_for('root'))

if __name__ == '__main__':
	app.run(debug=True)
