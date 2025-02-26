from flask import render_template, request, redirect, Blueprint
from dbconnect import connection, getCursor

adminprofilePage = Blueprint('admin', __name__, template_folder='templates')
temp_data=[]
@adminprofilePage.route('/admin')
def admin():
    return render_template('admin.html')

@adminprofilePage.route('/menus')
def menus():
    return render_template('menus.html')

@adminprofilePage.route('/branches')
def branches():
    cur = getCursor()
    query = 'select * from branches '
    cur.execute(query)
    branches = cur.fetchall()
    print(branches)
    print(branches)
    return render_template('branches.html',branches=branches)

@adminprofilePage.route('/menucreate')
def menucreate():
    return render_template('menucreate.html')

@adminprofilePage.route('/menu_update/<id>')
def menu_update(id):
    cur = getCursor()
    query = 'select * from branches where branchid = %s'
    idvalue =(id,)
    cur.execute(query,idvalue)
    branchupdate = cur.fetchone()
    return render_template('menu_update.html',id=id,branchname=branchupdate[1])
    


@adminprofilePage.post('/do-menu_update/<id>')
def domenu_update(id):
    branchname = request.form.get('branchname')
    cur=getCursor()
    updatequery = "update branches set branchname = %s where branchid=%s"
    value =(branchname,id)
    cur.execute(updatequery,value)
    connection.commit()
    return redirect('/branches')

@adminprofilePage.route('/do-menudelete/<id>')
def domenudelete(id):
    #branchname = request.form.get('branchname')
    cur=getCursor()
    deletequery ="DELETE FROM branches WHERE branchid=%s"
    value=(id,)
    cur.execute(deletequery,value)
    connection.commit()
    return redirect("/branches")
   






@adminprofilePage.route('/do-menucreate',methods=['post'])
def domenucreate():
    branchname = request.form.get('branchname')
    cur=getCursor()
    insertquery ='insert into branches(branchname) values(%s)'
    idValue = (branchname, )
    cur.execute(insertquery, idValue)
    branch = connection.commit()
    print(branch)
    return redirect('/branches')
   
       
       
@adminprofilePage.route('/do-admin',methods=['post'])
def doadmin():
    email = request.form['email']
    password = request.form['password']
    
    cur = getCursor()
    query = 'select * from admin where email = %s and password = %s'
    Value = (email,password )
    cur.execute(query, Value)
    row = cur.fetchone()
    if(row==None):
        return render_template('admin.html',error="it is  wrong")

    return redirect('/menus')   
