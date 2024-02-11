from flask import Flask, render_template, request, redirect
import csv
from pymongo_database import start_client
app = Flask(__name__)


@app.route('/')
def my_home():
    return render_template('index.html')

@app.route('/<string:page_name>')
def about(page_name):
    return render_template(page_name)


def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        database.write(f'\n{email}, {subject}, {message}\n')


def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database2:
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(database2, delimiter=',',  quotechar='"', quoting= csv.QUOTE_MINIMAL)

        csv_writer.writerow([email, subject, message])

def write_to_mongodb(data):
    try:
        client = start_client()
        if client:
            db = client.ServiceInquiries
            collection = db.Inquiries
            entry = {
                "email": data["email"],
                "subject": data["subject"],
                "message": data["message"]
            }
            result = collection.insert_one(entry)
            print(f'Inserted {result.inserted_id}: {entry}') 
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
 


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            write_to_mongodb(data)
            return redirect('/thankyou.html')
        except:
            return 'Did not save to database!'
    else:
        return 'something went wrong, try again!'