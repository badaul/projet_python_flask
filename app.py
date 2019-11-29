from flask import Flask, request, render_template, redirect, url_for
import csv
#from flask_sqlalchemy import SQLALchemy
#from flask_security import Security, SQLALchemyUserDatastore

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'thissecretkey'

@app.after_request
def after_request(response):
	response.headers['cache-controlle'] = 'max-age=300'
	response.headers['Access-Control-Allow-Origin'] = 'http://Ulysse.eu.pythonanywhere.com'
	return response


@app.route('/')
def home():
    return 'Bienvenue !'

@app.route('/gaz', methods=['GET','POST'])
def save_gazouille():
	if request.method == 'POST':
		print(request.form)
		if(len(request.form['user-text']) < 281):
			dump_to_csv(request.form)
		return redirect(url_for('timeline'))

	if request.method == 'GET':
		return render_template('formulaire.html')

@app.route('/timeline', defaults={'user': None}, methods=['GET'])
@app.route('/timeline/<user>/', methods=['GET'])
def timeline(user):
	gaz = parse_from_csv(user)
	return render_template("timeline.html", gaz = gaz)

def parse_from_csv(user):
	gaz = []
	with open('./gazouilles.csv', 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			if user != None and user == row[0]:
				gaz.append({"user":row[0], "text":row[1]})
			elif user == None:
				gaz.append({"user":row[0], "text":row[1]})


	return gaz

def dump_to_csv(d):
	donnees = [d["user-name"],d["user-text"] ]
	with open('./gazouilles.csv', 'a', newline='', encoding='utf-8') as f:
		writer = csv.writer(f)
		writer.writerow(donnees)

