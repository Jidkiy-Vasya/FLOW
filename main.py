from flask import Flask, render_template, redirect, request, flash, get_flashed_messages
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kf302mofkmdfsl1kfk'
posts_site = sqlite3.connect('PostSite.db', check_same_thread=False)
username_id = sqlite3.connect('USERSDB.db', check_same_thread=False)

curpost = posts_site.cursor()
curusers = username_id.cursor()

login_user = ''


def get_all():
    records = []
    curpost.execute('SELECT * FROM Users')
    rows = curpost.fetchall()
    for row in rows:
        records.append({'title': str(row[0]),'text': str(row[1])})
    return records





def intotable(login_user, password_user):
    data = curusers.execute("SELECT * FROM UsersDATA")
    for i in data:
        if login_user == i[0] and password_user == i[2]:
            return True
    else:
        return False


def name(login_user):
    data = curusers.execute("SELECT * FROM UsersDATA")
    for i in data:
        if login_user == i[0]:
            return i[1]
    else:
        return False



    

@app.route('/', methods=['POST', 'GET'])
def registration():
    if request.method == "POST":
        username = request.form['username']
        login = request.form['login']
        password = request.form['password']
        print(username)
        print(login)
        print(password)
        try:
            curusers.execute('INSERT INTO UsersDATA (username, email, password) VALUES (?, ?, ?)', (username, login, password))
            
        except:
            flash('Данные введены неверно')
            return render_template('registration.html')
        username_id.commit()
        return redirect('/home')
    else:
        return render_template('registration.html')
    
print(login_user)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        login = request.form['loginin']
        password = request.form['passwordin']
        if intotable(login, password):
            flash('Успешная авторизация')
            
            return redirect(f'/home')
            
        else:
            flash('Данные неверны')
            return render_template('login.html')
    else:
        return render_template('login.html')




@app.route('/home')
def home():
    
    posts = get_all()
    return render_template('home.html', posts=posts)


@app.route('/create',methods=["POST", "GET"])
def create():
    if request.method == "POST":
        titl = request.form['title']
        text = request.form['text']
        if len(titl) > 0 and len(text) > 0 and len(titl) < 10:
            curpost.execute('INSERT INTO Users (Title, Text) VALUES (?, ?)', (titl, text))
        else:
            flash('Данные введены неверно')
            return render_template('create.html')
        flash('Пост опубликован')
        posts_site.commit()
        return render_template('create.html')
    else:
        return render_template('create.html')




if __name__ == '__main__':
    app.run(debug=True)

posts_site.commit()
posts_site.close()
username_id.commit()
username_id.close() 
