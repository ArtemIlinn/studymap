from flask import Flask, redirect, render_template, send_from_directory, request, jsonify
import pandas as pd

from flask import url_for
import csv

from flask_wtf import FlaskForm
from wtforms import SelectMultipleField

import os
from werkzeug.utils import secure_filename

#import send_from_directory

from chat2 import get_response


flag_logged_in = 0

class User:
    def __init__(self, username, password, coins, user_id=None, name=None, first_name=None, last_name=None, 
                 middle_name=None, email=None, phone_number=None, educational_programs=None, date_of_birth=None,
                 correct_school=None, current_city=None, chat_history=None, liked_articles=None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.coins = coins
        self.name = name
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.email = email
        self.phone_number = phone_number
        self.educational_programs = educational_programs
        self.date_of_birth = date_of_birth
        self.correct_school = correct_school
        self.current_city = current_city
        self.chat_history = chat_history
        self.liked_articles = liked_articles

    def __str__(self):
        return f"User ID: {self.user_id}, Username: {self.username}, Coins: {self.coins}"

current_user = User(username='Timmy', password='1', coins=999)



app = Flask(__name__, static_url_path='/static', static_folder='templates/static') ##important
app.config['SECRET_KEY'] = 'nrfirfrifj_secret_key'


@app.route('/')
@app.route('/index')
def index():
    if flag_logged_in == 0:
        return render_template('index.html', flag_logged_in=flag_logged_in, user=current_user) #return render_template('index.html')
    elif flag_logged_in == 1:
        return render_template('indexuser.html', flag_logged_in=flag_logged_in, user=current_user)



@app.route('/education')
def education():
    return render_template('education.html', flag_logged_in=flag_logged_in, user=current_user)


@app.route('/careers')
def careers():
    return render_template('careers.html', flag_logged_in=flag_logged_in, user=current_user)


@app.route('/blog')
def blog():
    return render_template('blog1.html', flag_logged_in=flag_logged_in, user=current_user)

@app.route('/blog1')
def blog1():
    return render_template('blog1.html', flag_logged_in=flag_logged_in, user=current_user)


@app.route('/mentalhealth')
def mentalhealth():
    return render_template('mentalhealth1.html', flag_logged_in=flag_logged_in, user=current_user)

@app.route('/mentalhealth1')
def mentalhealth1():
    return render_template('mentalhealth1.html', flag_logged_in=flag_logged_in, user=current_user)




"""@app.route('/login')
def login():
    return render_template('login.html')"""


"""@app.route('/signup')
def signup():
    return render_template('signup.html')"""


@app.route('/coins')
def coins():
    return render_template('coins.html', flag_logged_in=flag_logged_in, user=current_user)


@app.route('/user')
def user():
    return render_template('user.html', flag_logged_in=flag_logged_in, user=current_user)


@app.route('/explore')
def explore():
    return render_template('explore.html', flag_logged_in=flag_logged_in, user=current_user)


@app.route('/explore/chatbot', methods=['POST'])
def chatbot():
    user_input = request.form['user_input']
    # Your chatbot logic here
    chatbot_response = get_response(user_input)
    return jsonify({'response': chatbot_response})


df = pd.read_csv('/Users/artemilin/Downloads/Образовательные_программы_НИУ_ВШЭ_Бакалавриат.csv')


@app.route('/explore/filter', methods=['GET', 'POST'])
def filter():
    filtered_df = df.copy()

    if request.method == 'POST':
        # Применяем фильтры
        filters = request.form.to_dict()
        for column, value in filters.items():
            filtered_df = filtered_df[filtered_df[column] == value]

    # Выводим страницу с фильтром и DataFrame
    columns = df.columns.tolist()
    return render_template('explore.html', data=filtered_df.to_html(), columns=columns)


from hse_bachelor_list import hse_bc_
programs = hse_bc_


class ApplyForm(FlaskForm):
    program_choices = SelectMultipleField('Select Programs', choices=[(p, p) for p in programs])


selected_programs = []
selected_files = []


@app.route('/apply', methods=['GET', 'POST'])
def apply():
    form = ApplyForm()
    global selected_programs
    selected_programs_locally = []
    program_to_cancel = ''

    global selected_files
    selected_files_locally = []
    file_to_cancel = ''

    if form.validate_on_submit():
        selected_programs_locally = form.program_choices.data

    # Handle "Cancel" button
    if request.method == 'POST':
        if 'program-cancel' in request.form:
            program_to_cancel = request.form['program-cancel']
            selected_programs.remove(program_to_cancel)

        try:
            f = request.files['file']
            #f.save(f.filename)
            name = f.filename
            print(name)
            selected_files_locally.append(name)
            selected_files.extend(selected_files_locally)
            print(selected_files)
        except:
            print('no file')

            if 'file-cancel' in request.form:
                file_to_cancel = request.form['file-cancel']
                selected_files.remove(file_to_cancel)

            # Check if a file was included in the form submission

    selected_programs.extend(selected_programs_locally)
    #selected_files.extend(selected_files_locally)

    return render_template('apply.html', form=form, selected_programs=selected_programs, selected_files=selected_files, 
                           flag_logged_in=flag_logged_in, user=current_user
                           )







# Function to write username and password to user_info.csv
def write_to_csv(data):
    with open('pythonProject/spotifysongs-master/user_info.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Function to check if username exists in user_info.csv
def username_exists(username):
    with open('pythonProject/spotifysongs-master/user_info.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username:
                return True
        return False

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if username already exists
        if username_exists(username):
            return render_template('signup.html', error='Username already exists. Please choose a different one.')
        
        # Write username and password to CSV file
        write_to_csv([username, password, 100])
        
        # Redirect to login page
        return redirect('/login')
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if username and password match the ones in user_info.csv
        with open('pythonProject/spotifysongs-master/user_info.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username and row[1] == password:
                    
                    global flag_logged_in
                    flag_logged_in = 1

                    global current_user
                    current_user = User(username=username, password=password, coins=101)

                    return redirect('/indexuser')
                
        
        # Authentication failed, display error message
        return render_template('login.html', error='Invalid username or password.')

    return render_template('login.html')





@app.route('/indexuser')
def Indexuser():
    return render_template('indexuser.html',  flag_logged_in=flag_logged_in, user=current_user)

@app.route('/success')
def Success():
    return render_template('success.html',  flag_logged_in=flag_logged_in, user=current_user)

@app.route('/base')
def base():
    #return render_template('base.html')
    global current_user
    return render_template('base.html', flag_logged_in=flag_logged_in, user=current_user)














@app.route('/edu1')
def edu1():
    return render_template('edu1.html', flag_logged_in=flag_logged_in, user=current_user)

@app.route('/edu2')
def edu2():
    return render_template('edu2.html', flag_logged_in=flag_logged_in, user=current_user)

@app.route('/edu3')
def edu3():
    return render_template('edu3.html', flag_logged_in=flag_logged_in, user=current_user)

@app.route('/edu4')
def edu4():
    return render_template('edu4.html', flag_logged_in=flag_logged_in, user=current_user)

@app.route('/edu5')
def edu5():
    return render_template('edu5.html', flag_logged_in=flag_logged_in, user=current_user)

@app.route('/edu6')
def edu6():
    return render_template('edu6.html', flag_logged_in=flag_logged_in, user=current_user)



@app.route('/car1')
def car1():
    return render_template('car1.html', flag_logged_in=flag_logged_in, user=current_user)

@app.route('/car2')
def car2():
    return render_template('car2.html', flag_logged_in=flag_logged_in, user=current_user)

@app.route('/car3')
def car3():
    return render_template('car3.html', flag_logged_in=flag_logged_in, user=current_user)

@app.route('/car4')
def car4():
    return render_template('car4.html', flag_logged_in=flag_logged_in, user=current_user)

@app.route('/car5')
def car5():
    return render_template('car5.html', flag_logged_in=flag_logged_in, user=current_user)

@app.route('/car6')
def car6():
    return render_template('car6.html', flag_logged_in=flag_logged_in, user=current_user)




@app.route('/bl1')
def bl1():
    return render_template('bl1.html', flag_logged_in=flag_logged_in, user=current_user)

@app.route('/bl2')
def bl2():
    return render_template('bl2.html', flag_logged_in=flag_logged_in, user=current_user)

@app.route('/bl3')
def bl3():
    return render_template('bl3.html', flag_logged_in=flag_logged_in, user=current_user)

@app.route('/blf')
def blf():
    return render_template('blf.html', flag_logged_in=flag_logged_in, user=current_user)



if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1', debug=True)


