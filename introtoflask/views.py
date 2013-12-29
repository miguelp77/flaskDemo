from introtoflask import app
from flask import Flask, render_template, request, flash, redirect, url_for
from forms import ContactForm, LoginForm

 
@app.route('/')
def home():
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

# @app.route('/contact')
# def contact():
# 	form = ContactForm()
# 	return render_template('contact.html', form=form)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
	form = ContactForm()
 
	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('contact.html', form=form)
		else:
			return 'Form posted.'
 
	elif request.method == 'GET':
		return render_template('contact.html', form=form)


# if __name__ == '__main__':
	# app.run(debug=True)
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	error = None
	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('login.html', form=form)
		else:
			return 'Form posted.'
	
	elif request.method == 'GET':
		# session['logged_in'] = True
		# flash('')
		# return redirect(url_for('login'))
		return render_template('login.html', form=form)

	return render_template('login.html', form=form)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))