from flask import Flask, render_template, request, redirect
from twilio.rest import Client
import csv

app = Flask(__name__)


@app.route('/')
def my_website():
    return render_template('index.html')


@app.route('/<string:page_name>')
def generic(page_name):
    return render_template(page_name)


def write_to_csv(data):
    with open('database.csv', newline='', mode='a') as database:
        email = data["email"]
        name = data["name"]
        message = data["message"]
        file = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        file.writerow([email, name, message])


def send_sms(data):
    account_sid = 'AC7c0a6c2208b6336538e1a3233877d1ad'
    auth_token = '59d1f14c066d949bdd7613b57469138b'

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='+18647135982',
        body=f'Hey Vishal! \nYou have a message from your website\nSent by {data["name"]}, containing \n Email ID {data["email"]} As \n\n {data["message"]}',
        to='+917349701450'
    )


@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == "POST":
         try:
            data = request.form.to_dict()
            write_to_csv(data)
            send_sms(data)
            return redirect('thankyou.html')


         except:
             return redirect('thankyou.html')
    else:
        return redirect('thankyou.html')
