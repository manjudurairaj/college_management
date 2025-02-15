import mysql.connector

config = {
    'host':"127.0.0.1",
    'port': 3306,
    'user': "root",
    'password': "2006",
    'database': 'student'
}
connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="2006",
    database='student')

def getCursor(dict=False):
    connection.reconnect()
    if(dict == True):
        return connection.cursor(dictionary=True)
    else:
        return connection.cursor()  

# Database host address:Manjudurairaj.mysql.pythonanywhere-services.com
# Username:Manjudurairaj