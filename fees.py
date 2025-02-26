from flask import render_template, request, redirect, Blueprint
from dbconnect import connection, getCursor
import datetime




temp_data = []
feesPage = Blueprint('fees_list', __name__, template_folder='templates')

@feesPage.route('/fees_list/<student_id>')
def fees_list(student_id):
    cur = getCursor(True)
    query ='select * from feeslist where studentid= %s'
    idvalue=(student_id,)
    cur.execute(query,idvalue)
    feeslist = cur.fetchall()
    print(feeslist)
    return render_template('fees_list.html', id=student_id,  feeslist=feeslist)


@feesPage.route('/view/<feesid>')
def view(feesid):
    cur = getCursor(True)
    query ='select * from feesdetails inner join feescategory on feesdetails.feescategoryid = feescategory.id where feesid= %s'
    idvalue=(feesid,)
    cur.execute(query,idvalue)
    feesdetails = cur.fetchall()
    return render_template('view.html', id=feesid, feesdetails=feesdetails)


@feesPage.route('/create/<student_id>', methods=['GET', 'POST'])
def create(student_id):
    cur = getCursor(True)
    categoryquery ='select * from feescategory'
    cur.execute(categoryquery)
    category = cur.fetchall()
    # print(category)

    global temp_data
    if request.method == 'POST':

        if "save_temp" in request.form:
            feesname = request.form.get('feescategory')
            feesamount = request.form.get('amount')
            reason  = request.form.get('reason')
            
            

            feesInfo = {
              "feesname": feesname,
              "feesamount": feesamount,
              "reason": reason
            }
            temp_data.append(feesInfo)
        
       
        if "final_submit" in request.form:
            sum=0
            curent_date = datetime.datetime.now()
            for entry in temp_data:
                sum=sum+int(entry["feesamount"])
            
            cur= getCursor()
            insertQuery = 'insert into feeslist ( studentid, date, total_amount) value ( %s, %s, %s )'
            value = (student_id, curent_date, sum)
            cur.execute(insertQuery, value)
            feesId = cur._last_insert_id
            print(feesId)
            for entry in temp_data: 
                feesQuery = 'insert into feesdetails ( feesid, feescategoryid, feesamount, reason) value ( %s, %s, %s, %s )'
                value = (feesId,entry["feesname"],int(entry["feesamount"]),entry["reason"])
                cur.execute(feesQuery, value)
            connection.commit()
            return redirect('/fees_list/' + str(student_id))

    dict={}
    for item in category: 
        dict[str(item['id'])] = item['feesname']
    
    return render_template('create.html', table_data=temp_data,category=dict)

    











# @feesPage.route('/create/<id>')
# def create(id):
#     cur = getCursor()
#     query = 'select * from feesdetails '
#     cur.execute(query)
#     feesdetails = cur.fetchall()

#     curfees = getCursor(True)
#     feesdwtailsquery = 'select * from fees_details where id = %s'
#     idValue = (id, )
#     curfees.execute(feesdetailsquery,idValue)
#     feesData = curfees.fetchone()
#     if (feesData == None):        
#           return render_template('create.html',id=id, feesdetails=feesdetails)
#     else:
#           return render_template('create.html',id=id,feesid=feesData['feesid'],  amount=feesData['amount'], extra_fees_reason=feesData['reason'], feesdetils=feesdetails)


# @feesPage.route('/fees_information/<id>', methods=['get'])
# def debug(id):
#     cur = getCursor()
#     query = 'select * from fees_information inner join feesdetails on fees_information.feesid = feesdetails.feesid where id=%s'
#     idValue = (id, )
#     cur.execute(query, idValue)
#     row = cur.fetchone()

#     if(row == None):                   
#        return render_template('/fees_information.html',id=id)
#     else:
#        return render_template('/fees_information.html',id=row[1],fees_amount=row[3],extra_fees_reason=row[4],feesname=row[6])
        

# @feesPage.route('/do-create/<id>', methods=['post'])
# def docreate(id):
#     feesid = request.form['feesid']
#     fees_amount = request.form['fees_amount']
#     extra_fees_reason = request.form['extra_fees_reason']
#     cur = getCursor()
#     query = 'select * from fees_information where id = %s'
#     idValue = (id, )
#     cur.execute(query, idValue)
#     row = cur.fetchone()
#     if(row == None):

#         insertQuery = 'insert into fees_information ( id, feesid, fees_amount, extra_fees_reason) value ( %s, %s, %s, %s )'
#         value = ( id, feesid, fees_amount, extra_fees_reason)
#         cur.execute(insertQuery, value)
#         connection.commit()
#         return redirect('/fees_information/' + id)   
#     else:

#        update_query= "UPDATE fees_information SET id = %s, feesid = %s, fees_amount = %s, extra_fees_reason = %s WHERE id = %s"
#        values = (id, feesid, fees_amount, extra_fees_reason,id)
#        cur.execute(update_query, values)
#        connection.commit()
#        return redirect('/fees_information/' + id)
  