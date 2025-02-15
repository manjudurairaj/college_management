from flask import Flask, render_template, request, redirect
from dbconnect import connection, getCursor
from studentprofile import studentprofilePage
from education import educationPage
from fees import feesPage

app = Flask(__name__, template_folder="templates")


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register',methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/debug/<id>')
def debug(id):
    return render_template('debug.html', id=id)

@app.route('/do-login',methods=['post'])
def dologin():
    email = request.form['email']
    password = request.form['password']
    cur = getCursor()
    print('Given password' + password)
    query = 'select * from student_info where email = %s'
    emailValue = (email, )
    cur.execute(query, emailValue)
    row = cur.fetchone()
    print("adding this line for Git Test")
    if ( row != None):   
        if row[4] == password:
             return redirect('/debug/' + str(row[0]))
        else:
            return render_template('login.html',error="incorrect password")
    else:
        return render_template('login.html', error="it's wrong email")


@app.route('/do-register',methods=['post'])
def doregister():
    firstname = request.form['fname']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']
    connection.reconnect()
    cur = getCursor()

    query = 'select * from student_info where email = %s'
    emailValue = (email, )
    cur.execute(query, emailValue)
    row = cur.fetchone()
 
    if (row == None):
        insertQuery = 'insert into student_info (first_name, last_name, email, password) value ( %s, %s, %s, %s )'
        value = (firstname, lastname, email, password)
        cur.execute(insertQuery, value)
        connection.commit()
        return redirect('/login')
    else:
        return render_template('register.html', error="User Already Exists. Please try with another email")
   



app.register_blueprint(studentprofilePage)
app.register_blueprint(educationPage)
app.register_blueprint(feesPage)


app.run(host='0.0.0.0', port=5373, debug=True)

