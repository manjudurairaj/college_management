from flask import render_template, request, redirect, Blueprint
from dbconnect import connection, getCursor

studentprofilePage = Blueprint('student_info', __name__, template_folder='templates')

@studentprofilePage.route('/My_profile')
def My_profile():
    return render_template('My_profile.html')





@studentprofilePage.route('/edit/<id>')
def edit(id):
    curprofile = getCursor(True)
    profilequery = 'select * from student_info where id = %s'
    idValue = (id, )
    curprofile.execute(profilequery,idValue)
    profiledata = curprofile.fetchone()
    return render_template('edit.html',id=id, gender=profiledata['gender'], fathername=profiledata['fathername'], mothername=profiledata['mothername'],date_of_birth=profiledata['date_of_birth'])


@studentprofilePage.route('/do-edit/<id>', methods=['post'])
def doedit(id):
    father_name = request.form['fathername']
    mothername = request.form['mothername']
    date_of_birth = request.form['date_of_birth']
    gender = request.form['gender']
    
  #  cur = getCursor()

    #query = 'select * from student_info where FatherName = %s ,mothername = %s ,date_ofbirth = %s ,gender = %s'
   # Value = (FatherName,mothername,date_of_birth,gender )
    #cur.execute(query, Value)
    #row = cur.fetchone()

    cur = getCursor()
    update_query = "UPDATE student_info SET fathername = %s, mothername = %s, date_of_birth = %s, gender = %s WHERE id = %s"
    values = (father_name, mothername, date_of_birth, gender, id)
    print(gender)
    cur.execute(update_query, values)
    connection.commit()  # Commit the changes to the database
    cur.close()
    return redirect('/my-profile/' + id)




  

@studentprofilePage.route('/my-profile/<id>', methods=['get'])
def dodebug(id):
    cur = getCursor()
    query = 'select * from student_info where id = %s'
    idValue = (id, )
    cur.execute(query, idValue)
    row = cur.fetchone()
    if (row[8] == 'F'):
        gender = 'Female'
    else:
        gender = 'Male'

    return render_template('/My_profile.html', id=row[0],firstName=row[1],lastname=row[2],fathername=row[5],mothername=row[6],date_of_birth=row[7],gender=gender)



