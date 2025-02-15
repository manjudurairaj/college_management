from flask import render_template, request, redirect, Blueprint
from dbconnect import connection, getCursor

educationPage = Blueprint('education_information', __name__, template_folder='templates')

@educationPage.route('/education_information')
def education_informationn():
    return render_template('education_information.html')


@educationPage.route('/ei_edit/<id>')
def ei_edit(id):
    cur = getCursor()
    query = 'select * from branches '
    cur.execute(query)
    branches = cur.fetchall()

    curEdu = getCursor(True)
    educationinformationquery = 'select * from education_information where id = %s'
    idValue = (id, )
    curEdu.execute(educationinformationquery,idValue)
    educationData = curEdu.fetchone()
    if (educationData == None):
        return render_template('ei_edit.html',id=id, branches=branches)
    else:
        return render_template('ei_edit.html',id=id,branchid=educationData['branchid'],  startingYear=educationData['starting_year'], EndingYear=educationData['ending_year'],currentsemester=educationData['current_semester'],registernumber=educationData['register_number'], branches=branches)

# {'primaryid': 3, 'id': 8, 'branchid': 1, 'starting_year': 2023, 'ending_year': 2027, 'current_semester': 3, 'register_number': '12'}

@educationPage.route('/education_information/<id>', methods=['get'])
def debug(id):
    cur = getCursor()
    query = 'select * from education_information inner join branches on education_information.branchid = branches.branchid where id=%s'
    idValue = (id, )
    cur.execute(query, idValue)
    row = cur.fetchone()

    if(row == None):
        return render_template('/education_information.html',id=id)
    else:
        return render_template('/education_information.html',id=row[1],starting_year=row[3],ending_year=row[4],current_semester=row[5],register_number=row[6],branchname=row[8])
        

@educationPage.route('/do-ei_edit/<id>', methods=['post'])
def doeiedit(id):
    branchid = request.form['branchid']
    starting_year = request.form['starting_year']
    ending_year = request.form['ending_year']
    current_semester = request.form['current_semester']
    register_number = request.form['register_number']
    cur = getCursor()
    query = 'select * from education_information where id = %s'
    idValue = (id, )
    cur.execute(query, idValue)
    row = cur.fetchone()
    if(row == None):

        insertQuery = 'insert into education_information ( id, branchid, starting_year, ending_year, current_semester, register_number) value ( %s, %s, %s, %s, %s, %s )'
        value = ( id, branchid, starting_year, ending_year, current_semester, register_number)
        cur.execute(insertQuery, value)
        connection.commit()
        return redirect('/education_information/' + id)   
    else:

        update_query= "UPDATE education_information SET id = %s, branchid = %s, starting_year = %s, ending_year = %s, current_semester = %s, register_number= %s WHERE id = %s"
        values = (id, branchid, starting_year, ending_year,current_semester,register_number,id)
        cur.execute(update_query, values)
        connection.commit()
    return redirect('/education_information/' + id)
  


