from flask import Flask, render_template, request, render_template_string, Response
from flask import url_for, redirect
from flask import stream_with_context
from collections import defaultdict
import os
import json
import codecs

app = Flask(__name__)

data_path = 'data_json_final.json'
questions = json.load(codecs.open(data_path, 'r', 'utf-8-sig'))
# questions =  {1:{"qn":"What color is Red Apple?", "op":["Red", "Green"]},
# 			  2:{"qn":"What color is White Rabbit?", "op":["White", "Black"]},
# 			  3:{"qn":"What's your name, Nitin?", "op":["Nitin", "Vamsi"]}}
# questions = {'1': {'q': 'You finalized two sets of clothing during shopping to wear on a festival to your workplace. Which do you finally pick?',
# 				  'op': {'sop': 'This set contains clothing that matches your usual clothing',
# 				         'rop': 'This set contains the type of clothing that you would not normally pick(MIght even consider not your usual style)'},
# 				  'feed': {'sp': 'Wearing your usual clothes demonstrates your ability to separate your work from personal events. You made a good impression with your colleagues',
# 				   		   'rp': 'Once in a while it is good to loosen up with the formal dress code especially when it is a festival. You made a good impression with your colleagues',
# 				   		   'sn': 'Even if the formal wear is the unofficial dress code at your work, you were expected to loosen up at least during festivals. You got a lot of raised eyebrows from your colleagues.',
# 				   		   'rn': 'Even if it is a festival day, it is still the place of work and you were expected to follow the unofficial formal dress code. You got a lot of raised eyebrows from your colleagues.'}}}

global answers
answers = defaultdict(int)
results = open('data.txt','a')

@app.route('/')
def root():
	return render_template('index.html')

@app.route('/questionnaire')
@app.route('/questionnaire/<id>/')
def show_question(id=1):
	global answers
	id = int(id)
	name = request.args.get('field1')
	email_id = request.args.get('field2')
	if name != None and email_id != None:
		results = open('data.txt','a')
		results.write(name + " " + email_id + " SAFE " + '\n')
		results.close()
	ans = request.args.get('qn')
	answers[id] = ans

	return render_template("questions.html", question = questions[str(id)], idx = id)

@app.route('/thanks')
def thanks():
	global answers
	ans = request.args.get('qn')
	lastkey = sorted(answers.keys())[-1]
	answers[lastkey+1] = ans
	answers.pop(1)
	print(answers)
	results = open('data.txt','a')
	for k, v in answers.items():
		results.write(questions[str(k-1)]["q"] + " Ans:" + v + '\n\n')
	results.write('\n\n\n')
	results.close()
	return render_template("thanks.html")

@app.route('/reset')
def reset():
	global answers
	answers = {}
	return redirect(url_for('root'))

if __name__ == '__main__':
	app.run(debug=True)
