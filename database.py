import mysql.connector

def connect_to_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="powertrainer",
        port=3306
    )
    return connection

def get_group_messages(group_id):
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM mensagens WHERE grupo_id = %s"
    cursor.execute(query, (group_id,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result