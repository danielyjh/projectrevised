from flask import Flask, render_template, request, session
from wtforms import Form, StringField, validators

import MainProcess

app = Flask(__name__)


class RegisterUser(Form):
    firstname = StringField('Firstname', [validators.Length(min=1, max=150), validators.DataRequired()])
    lastname = StringField('Lastname', [validators.Length(min=1, max=150), validators.DataRequired()])
    age = StringField('Age')

@app.route('/home', methods=['GET', 'POST'])
def home():
    session['userid'] = 'John'
    form = RegisterUser(request.form)
    if request.method == 'POST' and form.validate():
        MainProcess.registerNewUser(form.firstname.data, form.lastname.data, form.age.data)
        print("User Successfully Register")

    return render_template('home.html', form=form)

@app.route('/views')
def views():
    return render_template('views.html')

@app.route('/graph')
def graph():
    totalDeposit = 0
    totalWithdrawal = 0
    totalDeposit = MainProcess.processTransaction(session['userid'], 'Dec', 'deposit')
    totalWithdrawal = MainProcess.processTransaction(session['userid'], 'Dec', 'withdraw')

    return render_template('Graph.html', totalDepositAmount = totalDeposit, totalWithdrawalAmount = totalWithdrawal)

@app.route('/details')
def details():
    userslist = []
    userslist = MainProcess.processUser()
    return render_template('Details.html', users=userslist, count=len(userslist))

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run()