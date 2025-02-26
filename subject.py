from flask import render_template, request, redirect, Blueprint
from dbconnect import connection, getCursor

temp_data = []
subjectPage = Blueprint('subject_list', __name__, template_folder='templates')

@subjectPage.route('/subject_list/<student_id>')
def subject_list(student_id):
    cur = getCursor(True)
    #query = 'select * from student_semester_list where studentid = %s'
    query ='select student_semester_list.*, semester_list.semester_name  from student_semester_list inner join semester_list on student_semester_list.semesterid = semester_list.id  where studentid= %s'
    idvalue=(student_id,)
    cur.execute(query,idvalue)
    subjectlist = cur.fetchall()
    print(subjectlist)
    return render_template('subject_list.html', id=student_id,  subjectlist=subjectlist)

@subjectPage.route('/subjectcreate/<student_id>', methods=['GET', 'POST'])
def create(student_id):
    cur = getCursor(True)
    subjectquery ='select * from semester_subject'
    cur.execute(subjectquery)
    subject = cur.fetchall()
    



    cur = getCursor(True)
    semesterquery ='select * from semester_list'
    cur.execute(semesterquery)
    semester = cur.fetchall()



    # cur = getCursor(True)
    # query ='select * from student_semester_list inner join semester_list on student_semester_list.semesterid = semester_list.id'
    # cur.execute(query)
    # innerjoin = cur.fetchall()

    global temp_data
    if request.method == 'POST':

        if "save_temp" in request.form:
            subjectname = request.form.get('subject')
            # semestername = request.form.get('semester')
            Mark  = request.form.get('Mark')
            

            subjectInfo = {
              "subjectname": subjectname,
            #   "semestername": semestername,
              "Mark": Mark
            }
            temp_data.append(subjectInfo)
        

       
        if "final_submit" in request.form:
            semesterid = request.form.get('semester')
            sum=0
            for entry in temp_data:
                sum= sum + int(entry['Mark'])
            grade=""
            print(temp_data)
            total_marks = sum
            num_subjects = len(temp_data)  

            if num_subjects > 0:
                average = total_marks / num_subjects
                if(average>=91 and average<=100):
                    grade = 'O'
                elif(average>=81 and average<=90):
                    grade = 'A+'
                elif(average>=71 and average<=80):
                    grade = 'A'
                elif(average>=61 and average<=70):
                    grade = 'B+'
                elif(average>=51 and average<=60):
                    grade = 'B'
                elif(average>=45 and average<=50):
                    grade = 'C'
                else:
                    grade = 'U'
                print(grade)

            cur= getCursor()
            insertQuery = 'insert into student_semester_list ( studentid, semesterid, semester_grade) value ( %s, %s, %s )'
            value = (student_id,semesterid,grade)
            cur.execute(insertQuery, value)
            semesterlistid = cur._last_insert_id
          
            for entry in temp_data: 
                print(entry)
                subjectQuery = 'insert into student_semester_mark_list ( semesterlistid, semestersubjectid, semester_mark) value (%s, %s, %s )'
                value = (semesterlistid,entry["subjectname"],entry["Mark"])
                cur.execute(subjectQuery, value)
            connection.commit()
            return redirect('/subject_list/' + str(student_id))

    dict={}
    for item in subject: 
        dict[str(item['id'])] = item['subject_name']

    output={}
    for x in semester:
        output[str(x['id'])]=x['semester_name']
    print(temp_data)
    print(dict)
    return render_template('subjectcreate.html', table_data=temp_data,subject=dict,semester=output)



@subjectPage.route('/subjectview/<semesterlistid>')
def view(semesterlistid):
    cur = getCursor(True)
    query =' select * from student_semester_mark_list inner join semester_subject on student_semester_mark_list.semestersubjectid = semester_subject.id where semesterlistid = %s'
    idvalue=(semesterlistid,)
    cur.execute(query,idvalue)
    marklist = cur.fetchall()
    print(marklist)
    return render_template('subjectview.html', id=semesterlistid, marklist=marklist)


    

