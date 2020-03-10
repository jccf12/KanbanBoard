from flask import Flask, render_template, request, redirect, url_for
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from project import db, app, ma

class Tasks(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	taskname =  db.Column(db.String(50))
	description = db.Column(db.String(300))
	dateadded =  db.Column(db.DateTime())
	lastmodified = db.Column(db.DateTime())
	duedate = db.Column(db.DateTime())
	status = db.Column(db.String(10))

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route("/", methods=['GET','POST'])
def index():
	todo = Tasks.query.filter_by(status='todo').all()
	doing = Tasks.query.filter_by(status='doing').all()
	done = Tasks.query.filter_by(status='done').all()
	deleted = Tasks.query.filter_by(status='deleted').all()

	return render_template('index.html', todo=todo, doing=doing, done=done, deleted=deleted)

@app.route('/add/<type>', methods = ['GET', 'POST'])
def add(type):
	if type == 'addtodo':
		status = "todo"
	elif type == 'adddoing':
		status = "doing"
	elif type == 'adddone':
		status ="done"

	taskname = request.form['taskname']
	if request.form['description'] == '':
		description = "No description"
	else:
		description = request.form['description']

	dateadded = datetime.now()
	lastmodified = dateadded
	duedate = datetime.strptime(request.form['duedate'], '%Y-%m-%d')

	todo = Tasks(taskname=taskname, description=description, dateadded=dateadded, lastmodified=dateadded, duedate=duedate, status=status)
	db.session.add(todo)
	db.session.commit()

	return redirect(url_for('index'))


@app.route('/move/<id>/<type>', methods = ['GET'])
def move(id,type):
	todo = Tasks.query.filter_by(id=int(id)).first()
	if type == 'movetodo':
		status = "todo"
	elif type == 'movedoing':
		status = "doing"
	elif type == 'movedone':
		status ="done"
	elif type == 'delete':
		status="deleted"

	todo.status = status
	todo.lastmodified = datetime.now()
	db.session.commit()

	return redirect(url_for('index'))

if __name__ == '__main__':
		app.run(debug=True) 